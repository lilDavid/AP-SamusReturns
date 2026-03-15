from __future__ import annotations

import asyncio
import logging
import pkgutil
import shutil
import struct
import traceback
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

import Patch
import Utils
from CommonClient import ClientCommandProcessor, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import NetworkItem
from worlds._bizhawk.context import AuthStatus

from .connector import (
    UUID_LENGTH,
    PacketType,
    SamusReturnsConnector,
    SRConnectorError,
    Subscription,
)
from .data import GAME_NAME
from .data.internal_names import AreaId, ItemId
from .items import ItemName, item_data_table, launcher_to_ammo, tanks, unique_items
from .locations import location_table
from .patch import GAME_ID_US, SamusReturnsPatch, create_resource
from .settings import SamusReturnsSettings, TargetSystem

if TYPE_CHECKING:
    from CommonClient import CommonContext as BaseContext

    tracker_loaded = False
else:
    try:
        from worlds.tracker.TrackerClient import TrackerGameContext as BaseContext

        tracker_loaded = True
    except ModuleNotFoundError:
        from CommonClient import CommonContext as BaseContext

        tracker_loaded = False


ALL_ITEMS = 0b111


BACKOFF_LONG = 3.0
BACKOFF_SHORT = 1.0
POLL_COOLDOWN = 0.5


class SamusReturnsFilter(logging.Filter):
    last_message: str | None

    def __init__(self):
        self.last_message = None

    def clear(self):
        self.last_message = None

    def filter(self, record: logging.LogRecord):
        if record.levelno < logging.INFO:
            return True
        matches = record.getMessage() == self.last_message
        if matches:
            return False
        self.last_message = record.getMessage()
        return True


class SamusReturnsCommandProcessor(ClientCommandProcessor):
    ctx: SamusReturnsContext

    def _cmd_test_hud(self, *text: str):
        """Write a message to the HUD."""
        Utils.async_start(self.ctx.display_hud_message(" ".join(text)))

    def _cmd_console_ip(self, ip_address: str | None = None):
        """Get or set the IP address to connect to the game. Use "localhost" to connect to emulator."""
        if ip_address is None:
            logger.info(self.ctx.ip_address or "<unset>")
        else:
            self.ctx.ip_address = ip_address
            self.ctx.force_client_dc = True


class SamusReturnsDebugCommandProcessor(SamusReturnsCommandProcessor):
    def _cmd_test_lua(self, *code: str):
        """Run some Lua code in the game."""
        joined_code = " ".join(code)
        Utils.async_start(self.ctx.run_lua(joined_code))

    def _cmd_reload_ap_code(self):
        """Reload the multiworld handling code"""
        Utils.async_start(self.ctx.load_rando_code())

    def _cmd_dump_state(self):
        """Dump the current game state in the client"""
        logger.info(self.ctx.game_state)

    # Logic testing
    def _cmd_set_item(self, *item: str):
        """
        Enable an item without affecting the AP server. You must return to your last save or
        checkpoint to reset the item.
        """
        item_name = " ".join(item)
        if item_name not in unique_items:
            logger.warning("No effect!")
            return
        current_inventory = self.ctx.game_state.inventory
        if current_inventory is None:
            current_inventory = Counter()
        item_data = unique_items[item_name]
        Utils.async_start(
            self.ctx.give_item_if_not_owned(
                current_inventory,
                NetworkItem(item_data.ap_id, self.ctx.slot or 0, 0),
            )
        )


def get_lua_file(file):
    lua = pkgutil.get_data(__name__, f"data/lua/{file}")
    assert lua is not None
    return lua


@dataclass
class SamusReturnsState:
    config_id: str | None = None
    scenario: AreaId | None = None
    locations: frozenset[int] = frozenset()
    inventory: Counter[str] | None = None
    received_item_index: int | None = None

    def is_in_game(self):
        return self.scenario is not None


INVENTORY_ITEM_MAPPING: dict[str, str] = {data.item_id: name for name, data in item_data_table.items()}

INVENTORY_ITEMS = [
    *INVENTORY_ITEM_MAPPING.keys(),
    ItemId.MISSILE_CAPACITY,
    ItemId.SUPER_MISSILE_CAPACITY,
    ItemId.POWER_BOMB_CAPACITY,
    ItemId.MAX_ENERGY,
]


class SamusReturnsContext(BaseContext):
    game = GAME_NAME
    items_handling = ALL_ITEMS
    want_slot_data = True

    # AP server
    auth_status: AuthStatus
    password_requested: bool

    log_filter: SamusReturnsFilter

    current_area: AreaId | None

    # Game info
    game_sync_task: asyncio.Task
    game_reader_task: asyncio.Task | None
    ip_address: str
    connector: SamusReturnsConnector
    game_state: SamusReturnsState
    force_client_dc: bool

    # Slot data
    ammo_amounts: dict[str, int]
    dna_required: int

    def __init__(self, server_address: str | None, password: str | None):
        from . import SamusReturnsWorld

        super().__init__(server_address, password)
        self.tags = {"AP"}
        if SamusReturnsWorld.is_debug():
            self.command_processor = SamusReturnsDebugCommandProcessor
        else:
            self.command_processor = SamusReturnsCommandProcessor

        self.log_filter = SamusReturnsFilter()
        logger.addFilter(self.log_filter)

        self.auth_status = AuthStatus.NOT_AUTHENTICATED
        self.password_requested = False

        self.current_area = None

        self.ip_address = self.get_default_ip_address()
        self.connector = SamusReturnsConnector()
        self.game_state = SamusReturnsState()
        self.force_client_dc = False

        self.ammo_amounts = {}

    @staticmethod
    def get_default_ip_address():
        from . import SamusReturnsWorld

        settings: SamusReturnsSettings = SamusReturnsWorld.settings
        if settings.target_system == TargetSystem.EMULATOR:
            return "localhost"
        return settings.console_settings.ip_address or ""

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Metroid: Samus Returns Client"
        return ui

    async def server_auth(self, password_requested: bool = False):
        self.password_requested = password_requested
        if not self.auth:
            logger.info("Awaiting connection to game before authenticating")
            return
        await super().server_auth(password_requested)
        await self.send_connect()
        self.auth_status = AuthStatus.PENDING

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == "Connected":
            slot_data = args["slot_data"]
            try:
                self.ammo_amounts = slot_data["ammo_amounts"]
                self.dna_required = slot_data["options"]["dna_required"]
            except KeyError as e:
                message = f'Missing slot data key: "{e}"'
                logger.exception(message)
                self._messagebox_connection_loss = self.gui_error("Could not connect", message)
                Utils.async_start(self.disconnect(False))

    async def game_sync_loop(self):
        logger.debug("Starting Samus Returns connector, attempting to connect to game")
        while not self.exit_event.is_set():
            try:
                if self.force_client_dc:
                    self.connector.disconnect()
                    self.force_client_dc = False

                if not self.connector.is_connected():
                    if not self.ip_address:
                        logger.error("Client IP address is unset. Use /console_ip to connect to the game.")
                        await asyncio.sleep(BACKOFF_LONG)
                        continue

                    if not await self.connector.connect(self.ip_address):
                        self.connector.disconnect()
                        await asyncio.sleep(BACKOFF_LONG)
                        continue

                    await self.connector.send_msg(
                        PacketType.HANDSHAKE,
                        struct.pack("<B", Subscription.LOGGING | Subscription.MULTIWORLD),
                    )
                    await self._read_msg()

                    await self.load_rando_code()

                    await self.connector.run_lua('Game.AddSF(0.5, RL.SendRandoIdentifier, "")')
                    await self._read_msg()
                    await self.connector.run_lua('Game.AddSF(1.0, RL.UpdateRDVClient, "")')
                    await self._read_msg()

                    self.game_reader_task = asyncio.create_task(self.handle_messages(), name="Samus Returns Messages")

                if self.auth is None:
                    config_id = self.game_state.config_id
                    if config_id is None:
                        await asyncio.sleep(BACKOFF_SHORT)
                        continue
                    self.seed_name, self.auth = SamusReturnsPatch.parse_config_identifier(config_id)
                    logger.debug(f"Connected to {self.seed_name} as {self.auth}")

                if self.server is None:
                    logger.info("Waiting for player to connect to server")

                if self.server is not None and not self.server.socket.closed:
                    if self.auth_status == AuthStatus.NOT_AUTHENTICATED:
                        Utils.async_start(self.server_auth(self.password_requested))
                else:
                    self.auth_status = AuthStatus.NOT_AUTHENTICATED
                    await asyncio.sleep(BACKOFF_SHORT)
                    continue

                await self.handle_game_ready()

                await asyncio.sleep(POLL_COOLDOWN)

            except (SRConnectorError, ConnectionResetError) as e:
                self.connector.disconnect()
                logger.debug(e, exc_info=True)
                logger.info("Unable to connect to game")
                await asyncio.sleep(BACKOFF_LONG)
            except:
                logger.error(traceback.format_exc())
                self.connector.disconnect()
                await asyncio.sleep(BACKOFF_LONG)
                raise

        self.connector.disconnect()
        if self.game_reader_task:
            await self.game_reader_task

    async def handle_game_ready(self):
        await self.check_locations(self.game_state.locations)
        await self.handle_received_items()
        if self.game_state.scenario != self.current_area:
            await self.send_msg(
                cmd="Set",
                key=f"msr_area_{self.team}_{self.slot}",
                default=None,
                want_reply=False,
                operations=[{"operation": "replace", "value": self.game_state.scenario}],
            )
            self.current_area = self.game_state.scenario

    async def send_msg(self, **kwargs):
        await self.send_msgs([kwargs])

    async def _read_msg(self):
        while self.connector.is_connected():
            try:
                return await asyncio.wait_for(self.connector.read_msg(), 1)
            except TimeoutError:
                continue
        raise SRConnectorError("Disconnected from game")

    async def load_rando_code(self):
        await self.connector.run_lua(get_lua_file("bootstrap.lua"))
        logger.debug(await self._read_msg())

        location_data = [
            (location.ap_id, location.scenario, location.internal_name()) for location in location_table.values()
        ]
        batches = [
            location_data[: len(location_data) // 2],
            location_data[len(location_data) // 2 :],
        ]
        template = "for k, v in pairs{} do RL.LocationMapping[k] = RandomizerPowerup.PropertyForLocation(v) end"
        for batch in batches:
            table = "{"
            for id, scenario, name in batch:
                table += f'[{id}]="{scenario}_{name}",'
            table += "}"
            code = template.format(table)
            await self.connector.run_lua(code)
            logger.debug(await self._read_msg())

        name_list = ",".join(f'"{item}"' for item in INVENTORY_ITEMS)
        code = f"RL.Items = {{{name_list}}}"
        await self.connector.run_lua(code)
        logger.debug(await self._read_msg())

    async def handle_messages(self):
        from . import SamusReturnsWorld

        try:
            while self.connector.is_connected():
                packet, data = await self._read_msg()
                logger.debug("%s", data)
                match packet:
                    case PacketType.GAME_STATE:
                        key, value = data.split(":")
                        match key:
                            case "rando_id":
                                self.game_state.config_id = value[:-UUID_LENGTH]
                            case "scenario":
                                try:
                                    self.game_state.scenario = AreaId(value)
                                except ValueError:
                                    self.game_state.scenario = None
                            case _:
                                logger.debug("Unrecognized game state key: %s", key)
                    case PacketType.COLLECTED_INDICES:
                        if not data:
                            continue
                        locations = frozenset(map(int, data.split(",")))
                        new_locations = locations.difference(self.game_state.locations)
                        self.game_state.locations = locations
                        if SamusReturnsWorld.is_debug():
                            for location in new_locations:
                                logger.info(f"New location: {self.location_names.lookup_in_game(location, GAME_NAME)}")
                    case PacketType.NEW_INVENTORY:
                        pairs = [pair.split("=") for pair in data.split(",")]
                        internal_inventory = {k: int(v) for k, v in pairs}
                        inventory = Counter(
                            {
                                INVENTORY_ITEM_MAPPING[k]: v
                                for k, v in internal_inventory.items()
                                if k in INVENTORY_ITEM_MAPPING
                            }
                        )
                        if inventory[ItemName.MissileLauncher]:
                            inventory[ItemName.MissileTank] = internal_inventory[ItemId.MISSILE_CAPACITY]
                        if inventory[ItemName.SuperMissile]:
                            inventory[ItemName.SuperMissileTank] = internal_inventory[ItemId.SUPER_MISSILE_CAPACITY]
                        if inventory[ItemName.PowerBomb]:
                            inventory[ItemName.PowerBombTank] = internal_inventory[ItemId.POWER_BOMB_CAPACITY]
                        inventory[ItemName.EnergyTank] = internal_inventory[ItemId.MAX_ENERGY]
                        self.game_state.inventory = inventory
                    case PacketType.RECEIVED_ITEMS:
                        self.game_state.received_item_index = int(data)
                    case PacketType.LOG_MESSAGE:
                        logger.info(data)
        except SRConnectorError as e:
            self.connector.disconnect()
            logger.debug(e, exc_info=True)
            logger.info("Disconnected from game")
            await asyncio.sleep(BACKOFF_LONG)
        except Exception:
            self.connector.disconnect()
            logger.error(traceback.format_exc())
            await asyncio.sleep(BACKOFF_LONG)

    async def handle_received_items(self):
        current_inventory = self.game_state.inventory
        if current_inventory is None:
            return

        # Uniques and E-tanks
        # (E-tanks can't be received in bulk, so may as well have fun and mix them into the majors)
        energy_capacity = 99
        for network_item in self.items_received:
            item = self.item_names.lookup_in_slot(network_item.item)
            if item in unique_items:
                if await self.give_item_if_not_owned(current_inventory, network_item):
                    return
            if item == ItemName.EnergyTank:
                energy_capacity += self.ammo_amounts[ItemName.EnergyTank]
                if energy_capacity > 1099:
                    energy_capacity = 1099
                if energy_capacity > current_inventory[ItemName.EnergyTank]:
                    await self.give_e_tank(network_item)
                    return

        if await self.handle_metroid_dna(current_inventory):
            return
        if await self.handle_weapon_capacity(current_inventory, ItemName.MissileTank, ItemName.MissileLauncher):
            return
        if await self.handle_weapon_capacity(current_inventory, ItemName.SuperMissileTank, ItemName.SuperMissile):
            return
        if await self.handle_weapon_capacity(current_inventory, ItemName.PowerBombTank, ItemName.PowerBomb):
            return
        if await self.handle_aeion_capacity(current_inventory):
            return

    async def give_items(self, msg: str, items: Sequence[tuple[str, int]], index: int):
        from open_samus_returns_rando.pickups.multiworld_integration import get_lua_for_item

        scenario = '""'
        await self.connector.run_lua(
            f"RL.ReceivePickup('{msg}', '{get_lua_for_item([create_resource(items)], scenario)}', {index})"
        )

    async def give_item_if_not_owned(self, current_inventory: Counter[str], network_item: NetworkItem):
        received_item_index = self.game_state.received_item_index
        if received_item_index is None:
            return False

        item_name = self.item_names.lookup_in_game(network_item.item, GAME_NAME)
        if current_inventory[item_name] > 0:
            return False

        item_data = item_data_table[item_name]
        resources = [(item_data.item_id, 1)]
        current_inventory[item_name] = 1
        ammo_id = launcher_to_ammo.get(item_name)
        if ammo_id is not None:
            ammo_amount = self.ammo_amounts[item_name]
            resources.append((ammo_id, ammo_amount))
            current_inventory[ammo_id] += ammo_amount

        message = f"{item_name} "
        message += "acquired" if item_name == ItemName.Hatchling else "online"
        if network_item.player != self.slot:
            message += f" ({self.player_names[network_item.player]})"

        await self.give_items(message, resources, received_item_index)
        self.game_state.received_item_index = None
        return True

    async def handle_weapon_capacity(self, current_inventory: Counter[str], item: ItemName, launcher: ItemName):
        received_item_index = self.game_state.received_item_index
        if received_item_index is None:
            return False

        item_data = tanks[item]
        current_capacity = current_inventory[item]
        new_capacity = 0
        sender = None
        new_capacity, sender = self.get_count_and_sender(item, self.ammo_amounts[item])
        new_capacity += self.ammo_amounts[launcher] * current_inventory[launcher]

        diff = new_capacity - current_capacity
        if diff > 0:
            message = f"{item[: -len(' Tank')]} capacity increased by {diff}"
            if diff == self.ammo_amounts[item] and sender is not None:
                message += f" ({sender})"
            await self.give_items(message, [(item_data.item_id, diff)], received_item_index)
            return True
        return False

    async def give_e_tank(self, network_item: NetworkItem):
        received_item_index = self.game_state.received_item_index
        if received_item_index is None:
            return False

        message = f"{ItemName.EnergyTank} acquired"
        if network_item.player != self.slot:
            message += f" ({self.player_names[network_item.player]})"

        await self.give_items(message, [(tanks[ItemName.EnergyTank].item_id, 1)], received_item_index)
        self.game_state.received_item_index = None
        return True

    async def handle_aeion_capacity(self, current_inventory: Counter[str]):
        received_item_index = self.game_state.received_item_index
        if received_item_index is None:
            return False

        current_capacity = 1000 + current_inventory[ItemName.AeionTank]
        new_capacity, sender = self.get_count_and_sender(ItemName.AeionTank, self.ammo_amounts[ItemName.AeionTank])
        for upgrade in (ItemName.ScanPulse, ItemName.LightningArmor, ItemName.BeamBurst, ItemName.PhaseDrift):
            new_capacity += self.ammo_amounts[upgrade] * current_inventory[upgrade]
        diff = new_capacity - current_capacity
        if diff > 0:
            message = f"Aeion capacity increased by {diff}"
            if diff == self.ammo_amounts[ItemName.AeionTank] and sender is not None:
                message += f" ({sender})"
            await self.give_items(message, [(tanks[ItemName.AeionTank].item_id, diff)], received_item_index)
            return True
        return False

    async def handle_metroid_dna(self, current_inventory: Counter[str]):
        received_item_index = self.game_state.received_item_index
        if received_item_index is None:
            return False

        current_amount = self.dna_required - current_inventory[ItemName.MetroidDna]
        new_amount, sender = self.get_count_and_sender(ItemName.MetroidDna)
        diff = min(new_amount, self.dna_required) - current_amount
        if diff > 0:
            message = "Metroid DNA received"
            if diff > 1:
                message += f" x{diff}"
            elif sender is not None:
                message += f" ({sender})"
            # TODO: Work out a way to increment area counts when receiving local DNAs
            await self.give_items(message, [("ITEM_RANDO_DNA", diff)], received_item_index)
            return True
        return False

    def get_count_and_sender(self, item: ItemName, amount_per_item: int = 1):
        amount = 0
        sender = None
        for network_item in self.items_received:
            if network_item.item != item_data_table[item].ap_id:
                continue
            amount += 1
            sender = network_item.player
        if amount > 1 or sender == self.slot:
            sender_name = None
        else:
            sender_name = None if sender is None else self.player_names[sender]
        return amount * amount_per_item, sender_name

    async def run_lua(self, code: str):
        try:
            await self.connector.run_lua(code)
        except SRConnectorError as e:
            logger.error(str(e))
        except Exception as e:
            logger.exception(str(e))

    async def display_hud_message(self, text: str):
        await self.run_lua(f"Scenario.QueueAsyncPopup({text!r})")


def launch_game(rom_file: str):
    import subprocess
    import webbrowser

    from . import SamusReturnsWorld

    # In 3DS modding, we supply a patch to the loader, so we actually need to launch the original rom
    settings: SamusReturnsSettings = SamusReturnsWorld.settings
    auto_start = settings.emulator_settings.rom_start
    rom_file = settings.rom_file

    if isinstance(auto_start, str):
        subprocess.Popen([auto_start, rom_file], close_fds=True)
    elif auto_start:
        webbrowser.open(rom_file)


def install_rando_patch(patch_dir: str):
    from . import SamusReturnsWorld

    settings: SamusReturnsSettings = SamusReturnsWorld.settings
    if settings.target_system == TargetSystem.CONSOLE:
        path = settings.console_settings.sd_path
        if path is None:
            return
        output_path = SamusReturnsPatch.get_path(path) / "luma"
        output_path.mkdir(exist_ok=True)
        output_path /= "titles"
    else:
        path = settings.emulator_settings.user_path
        if path is None:
            return
        output_path = SamusReturnsPatch.get_path(path) / "load"
        output_path.mkdir(exist_ok=True)
        output_path /= "mods"
    output_path.mkdir(exist_ok=True)
    SamusReturnsPatch.verify_file_structure(output_path / GAME_ID_US)

    shutil.copytree(patch_dir, output_path, dirs_exist_ok=True)
    logger.info(f"Wrote randomizer patch to {output_path}")


def launch(*launch_args: str):
    async def main():
        parser = get_base_parser()
        parser.add_argument("patch_file", default="", type=str, nargs="?", help="Path to an apmsr patch")
        args = parser.parse_args(launch_args)

        if args.patch_file:
            metadata, result_file = Patch.create_rom_file(args.patch_file)
            install_rando_patch(result_file)
            if "server" in metadata:
                args.connect = metadata["server"]
            launch_game(result_file)

        ctx = SamusReturnsContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        if tracker_loaded:
            ctx.run_generator()  # pyright: ignore[reportAttributeAccessIssue]
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        ctx.game_sync_task = asyncio.create_task(ctx.game_sync_loop(), name="Samus Returns Sync")

        await ctx.exit_event.wait()
        await ctx.shutdown()
        await ctx.game_sync_task

    import logging

    import colorama

    Utils.init_logging("Metroid: Samus Returns Client", exception_logger="Client", loglevel=logging.DEBUG)
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()
