from collections import Counter
from pathlib import Path
from typing import ClassVar

import Utils
from rule_builder.rules import Has
from worlds import LauncherComponents as Launcher
from worlds.AutoWorld import WebWorld, World

from . import lib as lib  # Set up module importer for open-samus-returns-rando
from .data.constants import GAME_NAME
from .items import VICTORY, ItemName, SamusReturnsItem, item_data_table, major_items, reserve_tanks
from .locations import SamusReturnsLocation, location_table
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

    ammo_amounts: dict[str, int]
    starting_items: Counter[ItemName]

    displaced_filler: list[ItemName]

    def generate_early(self):
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

        self.starting_items = Counter(
            {
                ItemName.MissileLauncher: 1,
            }
        )
        if self.options.starting_scan_pulse.value:
            self.starting_items[ItemName.ScanPulse] = 1

        for item in self.starting_items.elements():
            self.push_precollected(self.create_item(item))

        self.displaced_filler = []

    def create_regions(self):
        set_starting_room(self)
        create_regions(self)
        connect_entrances(self)

        # TODO: Temporary fix so the locations can all be present
        from BaseClasses import Region

        region = Region("Placeholder", self.player, self.multiworld)
        locations = {location.name for location in self.get_locations()}
        region.add_locations(
            {name: data.ap_id for name, data in location_table.items() if name not in locations}, SamusReturnsLocation
        )
        self.multiworld.regions.append(region)
        self.create_entrance(
            self.get_region(self.origin_region_name),
            region,
            Has(ItemName.MetroidDna, self.options.dna_required.value),
        )

    def set_rules(self):
        self.set_completion_rule(Has(VICTORY))

    def create_items(self):
        major_item_pool: Counter[ItemName] = Counter()
        minor_item_pool: Counter[ItemName] = Counter()

        # Major items
        major_item_pool.update({name: 1 for name in major_items if self.starting_items[name] <= 0})
        major_item_pool[ItemName.MetroidDna] = self.options.dna_available.value
        if self.options.shuffle_reserve_tanks:
            major_item_pool.update({name: 1 for name in reserve_tanks if self.starting_items[name] <= 0})

        # Tanks
        major_item_pool[ItemName.EnergyTank] = 10  # E-tanks should be immune to tank displacement
        minor_item_pool[ItemName.MissileTank] = 80
        minor_item_pool[ItemName.SuperMissileTank] = 30
        minor_item_pool[ItemName.PowerBombTank] = 15
        minor_item_pool[ItemName.AeionTank] = 15

        # Filler
        item_count = sum(major_item_pool.values()) + sum(minor_item_pool.values())
        if item_count < LOCATION_COUNT:
            minor_item_pool[self.get_filler_item_name()] = LOCATION_COUNT - item_count
        elif item_count > LOCATION_COUNT:
            # This is so overengineered lol
            # We actually store items removed from the pool to make space so they can be returned if a vacancy opens up
            # And these are randomly selected from the tank items (instead of like, just missiles)
            self.displaced_filler = self.random.sample(
                list(minor_item_pool.keys()), item_count - LOCATION_COUNT, counts=minor_item_pool.values()
            )
            minor_item_pool -= Counter(self.displaced_filler)

        self.multiworld.itempool += [self.create_item(name) for name in major_item_pool.elements()]
        self.multiworld.itempool += [self.create_item(name) for name in minor_item_pool.elements()]

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
        if self.displaced_filler:
            return self.displaced_filler.pop()
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
