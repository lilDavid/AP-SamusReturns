from __future__ import annotations

import functools
import hashlib
import importlib.metadata
import json
import shutil
from collections import Counter, defaultdict
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import TYPE_CHECKING
from zipfile import ZipFile

import Utils
from BaseClasses import Item, Location, MultiWorld
from worlds.Files import APAutoPatchInterface

from . import lib  # Set up module importer for open-samus-returns-rando  # noqa: F401
from .data import GAME_NAME
from .data.internal_names import RANDO_DNA_TEMPLATE, AreaId, ItemId, ItemModel, PickupSound
from .data.remote_items import REMOTE_ITEM_MAPPING
from .items import (
    BASE_AEION,
    BASE_ENERGY,
    ItemName,
    OtherItemData,
    TankData,
    UniqueItemData,
    get_ammo_id,
    item_data_table,
    launcher_to_ammo,
    reserve_tanks,
)
from .locations import location_table
from .options import ApItemModels, PickupModels
from .regions import all_areas_data
from .starting_room import landing_site_data

if TYPE_CHECKING:
    from . import SamusReturnsWorld


TITLE_ID_US = "00040000001BB200"
TITLE_ID_EU = "00040000001BFB00"
TITLE_ID_JP = "00040000001BFC00"

MOD_FILES = {"romfs", "code.bin", "code.bps", "exheader.bin", "archipelago.json", "patcher.json"}


@functools.cache
def get_osrr_version():
    return importlib.metadata.version("open-samus-returns-rando")


def patch_schema():
    return f"https://raw.githubusercontent.com/randovania/open-samus-returns-rando/refs/tags/v{get_osrr_version()}/src/open_samus_returns_rando/files/schema.json"


def get_title_id(rom_path: str | Path):
    from open_samus_returns_rando.romfs import rom3ds

    if not isinstance(rom_path, Path):
        rom_path = Path(rom_path)

    with open(rom_path, "rb") as stream:
        try:
            parsed_rom = rom3ds.Rom3DS(rom3ds.parse_rom_file(rom_path, stream), stream)
        except ValueError as e:
            raise e from None  # Clear cause
        return parsed_rom.get_title_id()


def create_resource(resources: Sequence[tuple[str, int]]):
    return [{"item_id": item_id, "quantity": quantity} for item_id, quantity in resources]


def sentence_case(string: str):
    if string == "":
        return ""
    return string[0].upper() + string[1:]


def make_safe_name(string: str):
    return string.replace('"', '\\"').replace("\n", " ")


def format_remote_pickup(multiworld: MultiWorld, pickup: Item | Location):
    player_name = make_safe_name(multiworld.player_name[pickup.player])
    pickup_name = make_safe_name(pickup.name)
    return f"{player_name}'s {pickup_name}"


class SamusReturnsPatch(APAutoPatchInterface):
    game = GAME_NAME
    patch_file_ending = ".apmsr"
    result_file_ending = ""

    config: dict
    config_md5: str
    required_dna: int
    placed_dna: int

    def __init__(self, path: str | None = None, player: int | None = None, player_name: str = "", server: str = ""):
        super().__init__(path, player, player_name, server)

    def _patch(self, target: str | Path, status_update: Callable[[float, str], None] | None):
        import open_samus_returns_rando

        from . import SamusReturnsWorld

        self.read()

        rom_path = self.get_path(SamusReturnsWorld.settings.rom_file)
        output_path = target if isinstance(target, Path) else Path(target)
        output_path.mkdir(exist_ok=True)
        output_path /= get_title_id(rom_path)
        self.verify_file_structure(output_path)
        output_path.mkdir(exist_ok=True)

        # Skip patching if it's already been done before for this seed
        # as determined by the patching world version and patch file contents
        config_cache = output_path / "archipelago.json"
        world_version = SamusReturnsWorld.world_version.as_simple_string()
        try:
            with open(config_cache, "r") as stream:
                patch_info = json.load(stream)
                if patch_info["world_version"] == world_version and patch_info["config_md5"] == self.config_md5:
                    return
        except (FileNotFoundError, Exception):
            pass

        for file in output_path.iterdir():
            shutil.rmtree(file, ignore_errors=True)

        config = {
            **self.config,
            "text_patches": {
                **self.config.get("text_patches", {}),
                "GUI_SAMUS_DATA_TITLE": f"OSSR v{get_osrr_version()}",
            },
        }
        if status_update is None:
            open_samus_returns_rando.patch(rom_path, output_path, config)
        else:
            open_samus_returns_rando.patch_with_status_update(rom_path, output_path, config, status_update)

        with open(config_cache, "w") as stream:
            json.dump({"world_version": world_version, "config_md5": self.config_md5}, stream)

    def patch(self, target: str | Path):
        self._patch(target, None)

    def patch_with_status_update(self, target: str | Path, status_update: Callable[[float, str], None] | None = None):
        self._patch(target, status_update)

    @staticmethod
    def get_path(path: str):
        _path = Path(path)
        if _path.exists():
            return _path
        return Path(Utils.user_path(path))

    @staticmethod
    def verify_file_structure(target: Path):
        try:
            if not MOD_FILES.issuperset({file.name for file in target.iterdir()}):
                raise ValueError(
                    "Unexpected files were found in the output path. "
                    f'Verify you have the correct path and delete "{target}" if it is correct.'
                )
        except FileNotFoundError:
            pass

    def read_contents(self, opened_zipfile: ZipFile):
        config_bytes = opened_zipfile.read("config.json")
        self.config = json.loads(config_bytes)

        hasher = hashlib.md5()
        hasher.update(config_bytes)
        self.config_md5 = hasher.hexdigest()

        return super().read_contents(opened_zipfile)

    def write_contents(self, opened_zipfile: ZipFile):
        super().write_contents(opened_zipfile)
        opened_zipfile.writestr("config.json", json.dumps(self.config, indent=4))

    def create_config(self, world: SamusReturnsWorld):
        generator_info = "\n".join(
            [
                f"AP {Utils.version_tuple.as_simple_string()} - MSR AP {world.world_version.as_simple_string()}",
                f"{world.multiworld.seed_name}",
                f"P{world.player} - {world.player_name}",
            ]
        )

        self.config = {
            "$schema": patch_schema(),
            "configuration_identifier": self.get_config_identifier(world),
            "starting_location": landing_site_data.to_config(),
            "starting_items": self.create_starting_items(world),
            "pickups": self.create_pickups(world),
            "hints": self.create_hints(world),
            "spoiler_log": self.create_spoiler(world),
            "objective": {
                "final_boss": "Ridley",
                "total_dna": world.options.dna_available.value,
                "required_dna": self.required_dna,
                "placed_dna": world.options.dna_available.value,
            },
            "game_patches": {
                "reverse_area8": bool(world.options.reverse_area_8.value),
                "tanks_refill_ammo": bool(world.options.tanks_refill_ammo.value),
                "skip_opening": True,
            },
            "constant_environment_damage": {
                "heat": 20,
                "lava": 20,
            },
            "cosmetic_patches": {
                "enable_room_name_display": "ALWAYS" if world.options.display_room_names.value else "NEVER",
                "camera_names_dict": self.get_room_names(),
                "use_fusion_models": bool(world.options.fusion_suit.value),
            },
            "text_patches": {
                "GUI_MSG_NEW_FILE_CREATION": generator_info,
                "GUI_MSG_NEW_GAME": generator_info,
            },
            "enable_remote_lua": True,
            "layout_uuid": "00000000-0000-1111-0000-000000000000",
        }

    @staticmethod
    def get_config_identifier(world: SamusReturnsWorld):
        # AP player names can't contain leading or trailing whitespace, so we
        # can parse the name by padding it and taking the last 16 characters.
        return f"{world.multiworld.seed_name}{world.player_name:<16}"

    @staticmethod
    def parse_config_identifier(config: str):
        seed_name = config[:-16]
        player_name = config[-16:].strip()
        return seed_name, player_name

    def create_starting_items(self, world: SamusReturnsWorld):
        starting_items = Counter(
            {
                ItemId.MAX_ENERGY: BASE_ENERGY,
                ItemId.MAX_AEION: BASE_AEION,
            }
        )
        self.required_dna = world.options.dna_required.value
        for item in world.multiworld.precollected_items[world.player]:
            # Because of how the patcher works, we need to adjust the
            # requirement down instead of starting with some
            if item.name == ItemName.MetroidDna:
                self.required_dna -= 1
                continue
            item_data = item_data_table[item.name]
            match item_data:
                case TankData(_, item_id):
                    if item_id == ItemId.ENERGY_TANKS:
                        starting_items[ItemId.ENERGY_TANKS] += 1
                    else:
                        starting_items[item_id] += world.ammo_amounts[item.name]
                case UniqueItemData(_, item_id) | OtherItemData(_, item_id):
                    starting_items[item_id] += 1
                    ammo_id = get_ammo_id(item.name)
                    if ammo_id is not None:
                        starting_items[ammo_id] += world.ammo_amounts[item.name]
        return starting_items

    def create_pickups(self, world: SamusReturnsWorld):
        self.placed_dna = 0
        pickups = []
        for location in world.get_locations():
            if location.address is None:
                continue
            assert location.item is not None
            item = location.item

            pickup = location_table[location.name].to_pickup()
            pickup["model"] = [self.get_pickup_model(world, item)]
            pickup["resources"] = [create_resource([(ItemId.NOTHING, 1)])]
            if item.player == world.player:
                item_data = item_data_table[item.name]
                pickup["caption"] = f"{item.name} acquired."
                pickup["sound"] = item_data.pickup_sound()
            else:
                pickup["caption"] = f"{format_remote_pickup(world.multiworld, item)} acquired."
                pickup["sound"] = PickupSound.TANK
            pickups.append(pickup)
        return pickups

    def create_hints(self, world: SamusReturnsWorld):
        hints = []
        for hint, placements in world.hints.items():
            lines = []
            for placement in placements:
                if isinstance(placement, Location):
                    assert placement.item
                    item_name = self.get_item_name(world, placement.item)
                    location_name = self.get_location_name(world, placement)
                    lines.append(sentence_case(f"{location_name} contains {item_name}."))
                elif isinstance(placement, Item):
                    assert placement.location
                    item_name = self.get_item_name(world, placement)
                    location_name = self.get_location_name(world, placement.location)
                    lines.append(sentence_case(f"{item_name} can be found at {location_name}."))
            if lines:
                hints.append(hint.get_config(lines))
        return hints

    def create_spoiler(self, world: SamusReturnsWorld):
        spoiler: defaultdict[str, list[str]] = defaultdict(list)

        spoiler_items = set(world.spoiler.keys())
        if not world.options.shuffle_reserve_tanks.value:
            spoiler_items.difference_update(reserve_tanks)
        spoiler_items.discard(ItemName.MissileLauncher)

        for item in sorted(
            (item.name for item in world.multiworld.precollected_items[world.player] if item in spoiler_items),
            key=lambda item: item_data_table[item].ap_id,
        ):
            spoiler[item].append("Starting equipment")
            # Assumes majors are unique, need to change when progressive items added
            spoiler_items.discard(item)

        for item, locations in world.spoiler.items():
            if item not in spoiler_items:
                continue
            # For individual items, prioritize grouping by player over logcal order
            # Other games may not have a semantic meaning to location IDs like this one does
            # So maintain the logical order within that player's group since that always means *something*
            locations.sort(key=lambda loc: (loc.player, loc.address if loc.game == world.game else 0))
            for location in locations:
                spoiler[item].append(sentence_case(self.get_location_name(world, location)))

        # Always write Metroid DNA at the end
        entries = sorted(spoiler.items(), key=lambda kvp: kvp[0] == ItemName.MetroidDna)
        return {item: "\n".join(locations) for item, locations in entries}

    @staticmethod
    def get_item_name(world: SamusReturnsWorld, item: Item):
        if world.multiworld.players > 1:
            if item.player == world.player:
                return f"your {item.name}"
            return format_remote_pickup(world.multiworld, item)

        item_data = item_data_table[ItemName(item.name)]
        if item.name in (ItemName.EnergyTank, ItemName.AeionTank):
            return f"an {item.name}"
        if type(item_data) is TankData:
            return f"a {item.name}"
        if type(item_data) is UniqueItemData:
            return f"the {item.name}"
        if type(item_data) is OtherItemData:
            return item.name
        raise TypeError(type(item_data))

    @staticmethod
    def get_location_name(world: SamusReturnsWorld, location: Location):
        if world.multiworld.players == 1:
            return location.name
        if location.player == world.player:
            return f"your {location.name}"
        return format_remote_pickup(world.multiworld, location)

    @staticmethod
    def get_pickup_model(world: SamusReturnsWorld, item: Item):
        # Try to display a Metroid item
        match world.options.pickup_models.value:
            case PickupModels.option_hidden:
                return ItemModel.ItemSphere

            case PickupModels.option_local if item.player == world.player:
                return item_data_table[item.name].model

            case PickupModels.option_native | PickupModels.option_full if item.game == GAME_NAME:
                return item_data_table[item.name].model

            case PickupModels.option_full:
                game_lookup = REMOTE_ITEM_MAPPING.get(item.game)
                if game_lookup is not None:
                    model = game_lookup.get(item.name)
                    if model is not None:
                        return model

        # Display an AP item
        match world.options.ap_item_models.value:
            case ApItemModels.option_generic:
                return ItemModel.OffworldGeneric

            case ApItemModels.option_progression:
                if item.advancement or item.trap:
                    return ItemModel.OffworldGeneric
                return ItemModel.ItemSphere

    # Currently unused since items are completely remote
    def create_resources(self, world: SamusReturnsWorld, item: ItemName):
        data = item_data_table[item]
        match data:
            case OtherItemData(_, ItemId.DNA):
                self.placed_dna += 1
                item_id = ItemId(RANDO_DNA_TEMPLATE + str(self.placed_dna))
                return [create_resource([(item_id, 1)])]
            case TankData(_, item_id):
                return [create_resource([(item_id, world.ammo_amounts[item])])]
            case UniqueItemData(_, item_id) | OtherItemData(_, item_id):
                ammo_id = launcher_to_ammo.get(item)
                if ammo_id is None:
                    return [create_resource([(item_id, 1)])]
                else:  # noqa: RET505
                    return [create_resource([(item_id, 1), (ammo_id, world.ammo_amounts[item])])]

    @staticmethod
    @functools.cache
    def get_room_names():
        mapping: dict[AreaId, dict[str, str]] = {}
        for area_data in all_areas_data:
            mapping[area_data.area.id] = {room.id: room.name for room in area_data.rooms}
        return mapping
