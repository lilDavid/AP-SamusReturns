from __future__ import annotations

import functools
import json
import shutil
from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING
from zipfile import ZipFile

import Utils
from open_samus_returns_rando import samus_returns_patcher
from worlds.Files import APAutoPatchInterface

from .data.constants import GAME_NAME
from .data.internal_names import RANDO_DNA_TEMPLATE, AreaId, ItemId, ItemModel, PickupSound
from .items import ItemName, LauncherData, OtherItemData, TankData, UniqueItemData, item_data_table
from .locations import location_table
from .regions import all_areas_data

if TYPE_CHECKING:
    from . import SamusReturnsWorld


GAME_ID_US = "00040000001BB200"
MD5_US_DECRYPTED = "d5c4ea950c46a5344e07c9108828142a"

MOD_FILES = {"romfs", "code.bin", "exheader.bin"}

PATCH_SCHEMA = "https://raw.githubusercontent.com/randovania/open-samus-returns-rando/refs/heads/main/src/open_samus_returns_rando/files/schema.json"


class SamusReturnsPatch(APAutoPatchInterface):
    game = GAME_NAME
    patch_file_ending = ".apmsr"
    result_file_ending = ""

    config: dict
    required_dna: int
    placed_dna: int

    def __init__(self, path: str | None = None, player: int | None = None, player_name: str = "", server: str = ""):
        super().__init__(path, player, player_name, server)

    def patch(self, target: str):
        from . import SamusReturnsWorld
        from .settings import TargetSystem

        self.read()

        rom_path = self.get_path(SamusReturnsWorld.settings.rom_file)
        if SamusReturnsWorld.settings.target_system == TargetSystem.CONSOLE:
            path = SamusReturnsWorld.settings.console_settings.sd_path
            if path is None:
                output_path = Path(target)
            else:
                output_path = self.get_path(path) / "luma"
                output_path.mkdir(exist_ok=True)
                output_path /= "titles"
        else:
            path = SamusReturnsWorld.settings.emulator_settings.user_path
            if path is None:
                output_path = Path(target)
            else:
                output_path = self.get_path(path) / "load"
                output_path.mkdir(exist_ok=True)
                output_path /= "mods"
        output_path.mkdir(exist_ok=True)

        output_path /= GAME_ID_US
        try:
            if not MOD_FILES.issuperset({file.name for file in output_path.iterdir()}):
                raise ValueError(
                    "Unexpected files were found in the output path. "
                    f'Verify you have the correct path and delete "{output_path}" if it is correct.'
                )
            shutil.rmtree(output_path)
        except FileNotFoundError:
            pass
        output_path.mkdir(exist_ok=True)

        samus_returns_patcher.patch_extracted(rom_path, output_path, self.config)
        if path is not None:
            import logging

            logger = logging.getLogger(type(self).__name__)
            logger.setLevel(logging.INFO)
            logger.info(f"Wrote randomizer files to {output_path}")

    @staticmethod
    def get_path(path: str):
        _path = Path(path)
        if _path.exists():
            return _path
        return Path(Utils.user_path(path))

    def read_contents(self, opened_zipfile: ZipFile):
        self.config = json.loads(opened_zipfile.read("config.json"))
        return super().read_contents(opened_zipfile)

    def write_contents(self, opened_zipfile: ZipFile):
        super().write_contents(opened_zipfile)
        opened_zipfile.writestr("config.json", json.dumps(self.config, indent=4))

    def create_config(self, world: SamusReturnsWorld):
        self.config = {
            "$schema": PATCH_SCHEMA,
            "configuration_identifier": self.get_config_identifier(world),
            "starting_location": {
                "scenario": AreaId.SURFACE_EAST,
                "actor": "StartPoint0",
            },
            "starting_items": self.create_starting_items(world),
            "pickups": self.create_pickups(world),
            "hints": [],
            "objective": {
                "final_boss": "Ridley",
                "total_dna": world.options.dna_available.value,
                "required_dna": self.required_dna,
                "placed_dna": world.options.dna_available.value,
            },
            "cosmetic_patches": {
                "enable_room_name_display": "ALWAYS" if world.options.display_room_names.value else "NEVER",
                "camera_names_dict": self.get_room_names(),
            },
            "enable_remote_lua": True,
            "layout_uuid": "00000000-0000-1111-0000-000000000000",
            # Not required by schema, but patching raises if not included
            "game_patches": {},
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
                ItemId.MAX_ENERGY: 99,
                ItemId.MAX_AEION: 1000,
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
                case TankData(_, ItemId.ENERGY_TANKS):
                    starting_items[ItemId.ENERGY_TANKS] += 1
                case TankData(_, item_id):
                    starting_items[item_id] += world.ammo_amounts[item.name]
                case LauncherData(_, item_id, ammo_id):
                    starting_items[item_id] += 1
                    starting_items[ammo_id] += world.ammo_amounts[item.name]
                case UniqueItemData(_, item_id) | OtherItemData(_, item_id):
                    starting_items[item_id] += 1
        return starting_items

    def create_pickups(self, world: SamusReturnsWorld):
        pickups = []
        for location in world.get_locations():
            assert location.item is not None
            if location.address is None:
                continue

            self.placed_dna = 0
            pickup = location_table[location.name].to_pickup()
            if location.item.player == world.player:
                item_data = item_data_table[location.item.name]
                pickup["resources"] = self.create_resources(world, ItemName(location.item.name))
                pickup["caption"] = f"{location.item.name} acquired."
                if item_data.sound:
                    pickup["sound"] = item_data.sound
            else:
                pickup["resources"] = [[self.create_resource(ItemId.NOTHING, 1)]]
                pickup["caption"] = (
                    f"{world.multiworld.player_name[location.item.player]}'s {location.item.name} acquired."
                )
                pickup["sound"] = PickupSound.TANK
            if location.native_item:
                pickup["model"] = [item_data_table[location.item.name].model]
            else:
                pickup["model"] = [ItemModel.OffworldGeneric]
            pickups.append(pickup)
        return pickups

    def create_resources(self, world: SamusReturnsWorld, item: ItemName):
        data = item_data_table[item]
        match data:
            case OtherItemData(_, ItemId.DNA):
                self.placed_dna += 1
                item_id = ItemId(RANDO_DNA_TEMPLATE + str(self.placed_dna))
                return [[self.create_resource(item_id, 1)]]
            case TankData(_, item_id):
                return [[self.create_resource(item_id, world.ammo_amounts[item])]]
            case LauncherData(_, item_id, ammo_id):
                return [[self.create_resource(item_id, 1), self.create_resource(ammo_id, world.ammo_amounts[item])]]
            case UniqueItemData(_, item_id) | OtherItemData(_, item_id):
                return [[self.create_resource(item_id, 1)]]

    @staticmethod
    def create_resource(item_id: ItemId, quantity: int):
        return {
            "item_id": item_id,
            "quantity": quantity,
        }

    @staticmethod
    @functools.cache
    def get_room_names():
        mapping: dict[AreaId, dict[str, str]] = {}
        for area_data in all_areas_data:
            mapping[area_data.id] = {room.id: room.name for room in area_data.rooms}
        return mapping
