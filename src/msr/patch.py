from __future__ import annotations

import json
from collections import Counter
from typing import TYPE_CHECKING
from zipfile import ZipFile

from worlds.Files import APAutoPatchInterface

from .data.internal_names import AreaId, ItemId, ItemModel
from .items import ItemName, LauncherData, OtherItemData, TankData, UniqueItemData, item_data_table
from .locations import location_table

if TYPE_CHECKING:
    from . import SamusReturnsWorld


PATCH_SCHEMA = "https://raw.githubusercontent.com/randovania/open-samus-returns-rando/refs/heads/main/src/open_samus_returns_rando/files/schema.json"


class SamusReturnsPatch(APAutoPatchInterface):
    patch_file_ending = ".apmsr"
    result_file_ending = ""

    config: dict

    def patch(self, target: str):
        raise NotImplementedError

    def read_contents(self, opened_zipfile: ZipFile):
        self.config = json.loads(opened_zipfile.read("config.json"))
        return super().read_contents(opened_zipfile)

    def write_contents(self, opened_zipfile: ZipFile):
        super().write_contents(opened_zipfile)
        opened_zipfile.writestr("config.json", json.dumps(self.config, indent=4))

    def create_config(self, world: SamusReturnsWorld):
        self.config = {
            "$schema": PATCH_SCHEMA,
            "configuration_identifier": world.multiworld.seed_name,
            "starting_location": {
                "scenario": AreaId.AREA_1,
                "actor": "ST_SaveStation001",
            },
            "starting_items": self.create_starting_items(world),
            "pickups": self.create_pickups(world),
            "hints": [],
            "enable_remote_lua": True,
            "layout_uuid": "00000000-0000-1111-0000-000000000000",
            # Not required by schema, but patching raises if not included
            "game_patches": {},
            "cosmetic_patches": {"camera_names_dict": {area: {} for area in AreaId}},
        }

    def create_starting_items(self, world: SamusReturnsWorld):
        starting_items = Counter(
            {
                ItemId.MAX_ENERGY: 99,
                ItemId.MAX_AEION: 1000,
            }
        )
        for item in world.multiworld.precollected_items[world.player]:
            item_data = item_data_table[item.name]
            match item_data:
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

            pickup = location_table[location.name].to_pickup()
            if location.item.player == world.player:
                pickup["resources"] = self.create_resources(world, ItemName(location.item.name))
                pickup["caption"] = f"{location.item.name} acquired."
            else:
                pickup["resources"] = [[self.create_resource(ItemId.NOTHING, 1)]]
                pickup["caption"] = (
                    f"{world.multiworld.player_name[location.item.player]}'s {location.item.name} acquired."
                )
            if location.native_item:
                pickup["model"] = [item_data_table[location.item.name].model]
            else:
                pickup["model"] = [ItemModel.OffworldGeneric]
            pickups.append(pickup)
        return pickups

    def create_resources(self, world: SamusReturnsWorld, item: ItemName):
        data = item_data_table[item]
        match data:
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
