from __future__ import annotations

import asyncio
import logging
import traceback
from collections import Counter

import Patch
import Utils
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from kvui import GameManager
from NetUtils import NetworkItem

from .data.constants import GAME_NAME
from .game_interface import LuaError, SamusReturnsInterface
from .items import ItemName, LauncherData, item_data_table, tanks, unique_items

ALL_ITEMS = 0b111


BACKOFF_LONG = 3.0
BACKOFF_SHORT = 1.0
POLL_COOLDOWN = 0.5


class SamusReturnsManager(GameManager):
    base_title = "Archipelago Metroid: Samus Returns Client"


class SamusReturnsFilter(logging.Filter):
    last_message: str | None

    def __init__(self):
        self.last_message = None

    def clear(self):
        self.last_message = None

    def filter(self, record: logging.LogRecord):
        matches = record.getMessage() == self.last_message
        if matches:
            return False
        self.last_message = record.getMessage()
        return True


class SamusReturnsCommandProcessor(ClientCommandProcessor):
    ctx: SamusReturnsContext

    def _cmd_test_hud(self, *text: str):
        """Write a message to the HUD."""
        Utils.async_start(self.ctx.game_interface.display_hud_message(" ".join(text)))

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
        Utils.async_start(self.ctx.test_lua(joined_code))


class SamusReturnsContext(CommonContext):
    game = GAME_NAME
    command_processor = SamusReturnsCommandProcessor if Utils.is_frozen() else SamusReturnsDebugCommandProcessor
    items_handling = ALL_ITEMS
    want_slot_data = True

    log_filter: SamusReturnsFilter

    # Game info
    game_sync_task: asyncio.Task
    game_interface: SamusReturnsInterface
    ip_address: str
    force_client_dc: bool

    # Slot data
    ammo_amounts: dict[str, int]

    local_locations: set[int]

    def __init__(self, server_address: str | None, password: str | None):
        super().__init__(server_address, password)

        self.log_filter = SamusReturnsFilter()
        logger.addFilter(self.log_filter)
        self.game_interface = SamusReturnsInterface()
        self.ip_address = self.get_default_ip_address()
        self.force_client_dc = False

        self.local_locations = set()
        self.ammo_amounts = {}

    @staticmethod
    def get_default_ip_address():
        from . import SamusReturnsWorld
        from .settings import SamusReturnsSettings, TargetSystem

        settings: SamusReturnsSettings = SamusReturnsWorld.settings
        if settings.target_system == TargetSystem.EMULATOR:
            return "localhost"
        return settings.console_settings.ip_address or ""

    def run_gui(self):
        ui = SamusReturnsManager(self)
        self.ui = ui
        self.ui_task = asyncio.create_task(ui.async_run(), name="UI")

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            slot_data = args["slot_data"]
            try:
                self.ammo_amounts = slot_data["ammo_amounts"]
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
                    self.game_interface.disconnect()
                    self.force_client_dc = False

                if not self.game_interface.is_connected():
                    if not self.ip_address:
                        logger.error("Client IP address is unset. Use /console_ip to connect to the game.")
                        await asyncio.sleep(BACKOFF_LONG)
                        continue

                    if await self.game_interface.connect(self.ip_address):
                        logger.debug("Connected")
                    else:
                        await asyncio.sleep(BACKOFF_LONG)
                        continue

                if not self.server:
                    logger.info("Waiting for player to connect to server")
                    await asyncio.sleep(BACKOFF_SHORT)
                    continue
                if not self.slot:
                    logger.debug("Waiting for slot")
                    await asyncio.sleep(BACKOFF_SHORT)
                    continue

                if await self.game_interface.is_in_game():
                    await self.handle_game_ready()
                    await asyncio.sleep(POLL_COOLDOWN)
                else:
                    await asyncio.sleep(BACKOFF_SHORT)
            except OSError as e:
                logger.error(str(e))
                await asyncio.sleep(BACKOFF_LONG)
            except Exception:
                logger.error(traceback.format_exc())
                await asyncio.sleep(BACKOFF_LONG)

    async def handle_game_ready(self):
        await self.handle_locations()
        await self.handle_received_items()

    async def handle_locations(self):
        locations = await self.game_interface.get_locations()
        if locations is None:
            return
        locations.difference_update(self.local_locations)
        if not Utils.is_frozen():
            self.local_locations.update(locations)
            for location in locations:
                logger.info(f"New location: {self.location_names.lookup_in_slot(location)}")
        await self.check_locations(locations)

    async def handle_received_items(self):
        # Uniques
        current_inventory = await self.game_interface.get_inventory()
        if current_inventory is None:
            return
        for network_item in self.items_received:
            item = self.item_names.lookup_in_slot(network_item.item)
            if item in unique_items:
                await self.give_item_if_not_owned(current_inventory, network_item)

        # Consumables
        # FIXME: Modify capacities on the fly to avoid the double read
        current_inventory = await self.game_interface.get_inventory()
        if current_inventory is None:
            return
        await self.handle_weapon_capacity(current_inventory, ItemName.MissileTank, ItemName.MissileLauncher)
        await self.handle_weapon_capacity(current_inventory, ItemName.SuperMissileTank, ItemName.SuperMissile)
        await self.handle_weapon_capacity(current_inventory, ItemName.PowerBombTank, ItemName.PowerBomb)
        await self.handle_energy_capacity(current_inventory)
        await self.handle_aeion_capacity(current_inventory)

    async def give_item_if_not_owned(self, current_inventory: Counter[str], network_item: NetworkItem):
        item_name = self.item_names.lookup_in_slot(network_item.item)
        if current_inventory[item_name] >= 0:
            return

        item_data = item_data_table[item_name]
        if type(item_data) is LauncherData:
            await self.game_interface.set_items(
                [(item_data.item_id, 1), (item_data.ammo_id, self.ammo_amounts[item_name])]
            )
        else:
            await self.game_interface.set_items([(item_data.item_id, 1)])
        current_inventory[item_name] = 1
        message = f"{item_name} online"
        if network_item.player != self.slot:
            message += f" ({self.player_names[network_item.player]})"
        await self.game_interface.display_hud_message(message)

    async def handle_weapon_capacity(self, current_inventory: Counter[str], item: ItemName, launcher: ItemName):
        item_data = tanks[item]
        current_capacity = current_inventory[item]
        new_capacity = 0
        sender = None
        new_capacity, sender = self.get_count_and_sender(item, self.ammo_amounts[item])
        if current_inventory[launcher]:
            new_capacity += self.ammo_amounts[launcher]

        diff = new_capacity - current_capacity
        if diff > 0:
            message = f"{item[: -len(' Tank')]} capacity increased by {diff}"
            if diff == self.ammo_amounts[item] and sender is not None:
                message += f" ({sender})"
            await self.game_interface.set_items([(item_data.item_id, diff)])
            await self.game_interface.display_hud_message(message)

    async def handle_energy_capacity(self, current_inventory: Counter[str]):
        current_capacity = current_inventory[ItemName.EnergyTank]
        new_capacity, sender = self.get_count_and_sender(ItemName.EnergyTank, self.ammo_amounts[ItemName.EnergyTank])
        new_capacity = min(99 + new_capacity, 1099)
        diff = new_capacity - current_capacity
        if diff > 0:
            message = f"Energy capacity increased by {diff}"
            if diff == self.ammo_amounts[ItemName.EnergyTank] and sender is not None:
                message += f" ({sender})"
            await self.game_interface.set_items(
                [(tanks[ItemName.EnergyTank].item_id, (diff - 99) // self.ammo_amounts[ItemName.EnergyTank])]
            )
            await self.game_interface.display_hud_message(message)

    async def handle_aeion_capacity(self, current_inventory: Counter[str]):
        current_capacity = 1000 + current_inventory[ItemName.AeionTank]
        new_capacity, sender = self.get_count_and_sender(ItemName.AeionTank, self.ammo_amounts[ItemName.AeionTank])
        diff = new_capacity - current_capacity
        if diff > 0:
            message = f"Aeion capacity increased by {diff}"
            if diff == self.ammo_amounts[ItemName.AeionTank] and sender is not None:
                message += f" ({sender})"
            await self.game_interface.set_items([(tanks[ItemName.AeionTank].item_id, diff)])
            await self.game_interface.display_hud_message(message)

    async def handle_metroid_dna(self, current_inventory: Counter[str]):
        current_amount = current_inventory[ItemName.MetroidDna]
        new_amount, sender = self.get_count_and_sender(ItemName.MetroidDna)
        diff = new_amount - current_amount
        if diff > 0:
            message = "Metroid DNA received"
            if diff > 1:
                message += f" x{diff}"
            elif sender is not None:
                message += f" ({sender})"
            await self.game_interface.set_items([(tanks[ItemName.MetroidDna].item_id, diff)])
            await self.game_interface.display_hud_message(message)

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

    async def test_lua(self, code: str):
        try:
            result = await self.game_interface.connector.run_lua(code)
            logger.info(result)
        except (OSError, LuaError) as e:
            logger.exception(str(e))


def launch_game(rom_file: str):
    import subprocess
    import webbrowser

    from . import SamusReturnsWorld
    from .settings import SamusReturnsSettings

    # In 3DS modding, we supply a patch to the loader, so we actually need to launch the original rom
    settings: SamusReturnsSettings = SamusReturnsWorld.settings
    auto_start = settings.emulator_settings.rom_start
    rom_file = settings.rom_file

    if isinstance(auto_start, str):
        subprocess.Popen([auto_start, rom_file], close_fds=True)
    elif auto_start:
        webbrowser.open(rom_file)


def launch(*launch_args: str):
    async def main():
        parser = get_base_parser()
        parser.add_argument("patch_file", default="", type=str, nargs="?", help="Path to an apmsr patch")
        args = parser.parse_args(launch_args)

        if args.patch_file:
            metadata, result_file = Patch.create_rom_file(args.patch_file)
            logger.info(f"Patch with meta-data {metadata} was written to {result_file}")
            if "server" in metadata:
                args.connect = metadata["server"]
            launch_game(result_file)

        ctx = SamusReturnsContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

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
