from collections import Counter
from pathlib import Path
from typing import ClassVar

import Utils
from BaseClasses import Item
from worlds import LauncherComponents as Launcher
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule

from .data.constants import GAME_NAME
from .data.room_names import SurfaceWest
from .items import VICTORY, ItemName, SamusReturnsItem, item_data_table, launchers, major_items
from .locations import location_table
from .options import SamusReturnsOptions, msr_option_groups
from .patch import SamusReturnsPatch
from .regions import connect_entrances, create_regions, set_starting_room
from .settings import SamusReturnsSettings

LOCATION_COUNT = 211


class SamusReturnsWebWorld(WebWorld):
    theme = "ice"
    option_groups = msr_option_groups


class SamusReturnsWorld(World):
    """TODO"""

    game = GAME_NAME
    settings: ClassVar[SamusReturnsSettings]  # pyright: ignore[reportIncompatibleVariableOverride]
    options_dataclass = SamusReturnsOptions
    options: SamusReturnsOptions  # pyright: ignore[reportIncompatibleVariableOverride]

    web = SamusReturnsWebWorld()

    item_name_to_id: ClassVar[dict[str, int]] = {str(name): data.ap_id for name, data in item_data_table.items()}
    location_name_to_id: ClassVar[dict[str, int]] = {str(name): data.ap_id for name, data in location_table.items()}
    topology_present = not Utils.is_frozen()

    starting_items: Counter[ItemName]
    ammo_amounts: dict[str, int]

    def generate_early(self):
        self.starting_items = Counter(
            {
                ItemName.MissileLauncher: 1,
            }
        )

        if self.options.dna_available.value < self.options.dna_required.value:
            self.options.dna_available.value = self.options.dna_required.value
        self.ammo_amounts = {
            ItemName.EnergyTank: 100,
            ItemName.MissileLauncher: 24,
            ItemName.MissileTank: 3,
            ItemName.SuperMissile: 5,
            ItemName.SuperMissileTank: 1,
            ItemName.PowerBomb: 5,
            ItemName.PowerBombTank: 1,
            ItemName.AeionTank: 50,
            ItemName.ScanPulse: 0,
            ItemName.LightningArmor: 150,
            ItemName.BeamBurst: 150,
            ItemName.PhaseDrift: 150,
        }

        for item in self.starting_items.elements():
            self.push_precollected(self.create_item(item))

    def create_regions(self):
        set_starting_room(self)
        create_regions(self)
        connect_entrances(self)

        # TODO: Temporary fix so the locations can all be present
        from BaseClasses import Region

        region = Region("Extra region", self.player, self.multiworld)
        locations = {location.name for location in self.get_locations()}
        region.add_locations({name: data.ap_id for name, data in location_table.items() if name not in locations})
        self.multiworld.regions.append(region)
        self.get_region("Area 1: Transport to Surface and Area 2 (Area 2)").connect(region)

    def set_rules(self):
        add_rule(
            self.get_location(SurfaceWest.LandingSite.location("Proteus Ridley")),
            lambda state: state.has(ItemName.MetroidDna, self.player, self.options.dna_required.value),
        )
        self.multiworld.completion_condition[self.player] = lambda state: state.has(VICTORY, self.player)

    def create_items(self):
        item_pool: list[Item] = []

        # Major items
        item_pool += [self.create_item(name) for name in launchers if self.starting_items[name] <= 0]
        item_pool += [self.create_item(name) for name in major_items if self.starting_items[name] <= 0]

        # DNA
        item_pool += [self.create_item(ItemName.MetroidDna) for _ in range(self.options.dna_available.value)]

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

    def fill_slot_data(self):
        return {
            "ammo_amounts": self.ammo_amounts,
            **self.options.as_dict(
                "dna_required",
                "wall_jump",
                "infinite_bomb_jump",
                toggles_as_bools=True,
            ),
        }

    def get_filler_item_name(self):
        return ItemName.Nothing

    def create_item(self, name: str):
        item_name = ItemName(name)
        data = item_data_table[item_name]
        return SamusReturnsItem(item_name, data.classification(), data.ap_id, self.player)


def launch_client(*args):
    from . import client

    client.launch(*args)


Launcher.components.append(
    Launcher.Component(
        "Metroid: Samus Returns Client",
        func=lambda *args: Launcher.launch_subprocess(launch_client, name="MetroidSamusReturnsClient", args=args),
        component_type=Launcher.Type.CLIENT,
        file_identifier=Launcher.SuffixIdentifier(SamusReturnsPatch.patch_file_ending),
    )
)
