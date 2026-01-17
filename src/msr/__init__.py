from collections import Counter
from pathlib import Path
from typing import ClassVar

from BaseClasses import Item, Location, Region
from worlds.AutoWorld import World

from .data.constants import GAME_NAME
from .data.room_names import SurfaceWest
from .items import ItemName, item_data_table, launchers, major_items
from .locations import location_table, make_name
from .patch import SamusReturnsPatch

LOCATION_COUNT = 211
VICTORY = "Mission Accomplished!"


class SamusReturnsItem(Item):
    game = GAME_NAME


class SamusReturnsLocation(Location):
    game = GAME_NAME


class SamusReturnsWorld(World):
    """TODO"""

    game = GAME_NAME

    item_name_to_id: ClassVar[dict[str, int]] = {str(name): data.ap_id for name, data in item_data_table.items()}
    location_name_to_id: ClassVar[dict[str, int]] = {str(name): data.ap_id for name, data in location_table.items()}

    starting_items: Counter[ItemName]
    ammo_amounts: dict[str, int]

    def generate_early(self):
        self.starting_items = Counter(
            {
                ItemName.MissileLauncher: 1,
            }
        )
        self.ammo_amounts = {
            ItemName.EnergyTank: 100,
            ItemName.MissileLauncher: 24,
            ItemName.MissileTank: 3,
            ItemName.SuperMissile: 5,
            ItemName.SuperMissileTank: 1,
            ItemName.PowerBomb: 5,
            ItemName.PowerBombTank: 1,
            ItemName.AeionTank: 50,
        }

        for item in self.starting_items.elements():
            self.push_precollected(self.create_item(item))

    def create_regions(self):
        menu = Region(self.origin_region_name, self.player, self.multiworld)
        menu.add_locations(
            {name: data.ap_id for name, data in location_table.items()}, location_type=SamusReturnsLocation
        )
        menu.add_event(make_name(SurfaceWest.LandingSite, "Proteus Ridley"), VICTORY)
        self.multiworld.regions.append(menu)

        self.multiworld.completion_condition[self.player] = lambda state: state.has(VICTORY, self.player)

    def create_items(self):
        item_pool: list[Item] = []

        # Major items
        item_pool += [self.create_item(name) for name in launchers if self.starting_items[name] <= 0]
        item_pool += [self.create_item(name) for name in major_items if self.starting_items[name] <= 0]

        # DNA
        item_pool += [self.create_item(ItemName.MetroidDna) for _ in range(39)]

        # Tanks
        item_pool += [self.create_item(ItemName.EnergyTank) for _ in range(10)]
        item_pool += [self.create_item(ItemName.MissileTank) for _ in range(80)]
        item_pool += [self.create_item(ItemName.SuperMissileTank) for _ in range(30)]
        item_pool += [self.create_item(ItemName.PowerBombTank) for _ in range(15)]
        item_pool += [self.create_item(ItemName.AeionTank) for _ in range(15)]

        # Filler
        item_pool += [self.create_filler() for _ in range(LOCATION_COUNT - len(item_pool))]

        self.multiworld.itempool += item_pool

    def generate_output(self, output_directory: str):
        patch = SamusReturnsPatch(player=self.player, player_name=self.player_name)
        patch.create_config(self)

        output_filename = f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"
        output_path = Path(output_directory) / output_filename
        patch.write(str(output_path))

    def get_filler_item_name(self):
        return ItemName.Nothing

    def create_item(self, name: str):
        item_name = ItemName(name)
        data = item_data_table[item_name]
        return SamusReturnsItem(item_name, data.classification(), data.ap_id, self.player)
