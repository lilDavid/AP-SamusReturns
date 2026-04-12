from collections import Counter
from pathlib import Path
from typing import ClassVar

import Utils
from BaseClasses import ItemClassification, MultiWorld, Tutorial
from Options import DeathLink, Option
from rule_builder.rules import Has
from worlds import LauncherComponents as Launcher
from worlds.AutoWorld import WebWorld, World

from . import lib as lib  # Set up module importer for open-samus-returns-rando
from .data import GAME_NAME
from .items import VICTORY, ItemName, SamusReturnsItem, item_data_table, item_groups, major_items, reserve_tanks
from .locations import location_groups, location_table
from .options import LocalDna, MetroidDnaRequired, SamusReturnsOptions, msr_option_groups
from .patch import SamusReturnsPatch
from .regions import connect_entrances, create_regions, set_location_rules
from .settings import SamusReturnsSettings
from .starting_room import place_starting_loadout, set_starting_room

LOCATION_COUNT = 211


class SamusReturnsWebWorld(WebWorld):
    theme = "ice"
    option_groups = msr_option_groups
    tutorials = [  # noqa: RUF012
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Samus Returns randomizer connected to an Archipelago Multiworld.",
            "English",
            "setup_en.md",
            "setup/en",
            ["lil David"],
        )
    ]


class SamusReturnsWorld(World):
    """
    Metroid: Samus Returns is a complete reimagining of the Game Boy title Metroid II: Return of
    Samus. In the randomizer, you must locate power-ups and collect Metroid DNA scattered across
    SR388. Additionally, the hazardous liquid throughout the planet is drained from the start so
    you can explore the areas freely, and the Chozo seals provide hints instead.
    """

    game = GAME_NAME
    settings: ClassVar[SamusReturnsSettings]  # pyright: ignore[reportIncompatibleVariableOverride]
    options_dataclass = SamusReturnsOptions
    options: SamusReturnsOptions  # pyright: ignore[reportIncompatibleVariableOverride]

    web = SamusReturnsWebWorld()

    item_name_to_id: ClassVar[dict[str, int]] = {str(name): data.ap_id for name, data in item_data_table.items()}
    location_name_to_id: ClassVar[dict[str, int]] = {str(name): data.ap_id for name, data in location_table.items()}
    item_name_groups = item_groups
    location_name_groups = location_groups

    ammo_amounts: dict[str, int]
    skipped_items: Counter[ItemName]

    displaced_filler: list[ItemName]

    @classmethod
    def is_debug(cls):
        return cls.zip_path is None

    def generate_early(self):
        self.topology_present = self.is_debug()

        if self.is_universal_tracker():
            self.set_options_from_slot_data()
        else:
            if self.options.dna_available.value < self.options.dna_required.value:
                self.options.dna_available.value = self.options.dna_required.value

            self.options.local_items.value.add(ItemName.MetroidDnaLocal)

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

        starting_items = Counter([ItemName.MissileLauncher])
        if self.options.starting_scan_pulse.value:
            starting_items[ItemName.ScanPulse] = 1

        for item in starting_items.elements():
            self.push_precollected(self.create_item(item))

        self.skipped_items = starting_items
        self.displaced_filler = []

    def create_regions(self):
        create_regions(self)
        set_location_rules(self)
        connect_entrances(self)
        set_starting_room(self)

        self.set_completion_rule(Has(VICTORY))

    def create_items(self):
        prefilled_locations = place_starting_loadout(self)

        major_item_pool: Counter[ItemName] = Counter()
        minor_item_pool: Counter[ItemName] = Counter()

        # Major items
        major_item_pool.update(major_items.keys())
        if self.options.shuffle_reserve_tanks:
            major_item_pool.update(reserve_tanks.keys())

        local_dna_count = get_local_dna_count(self)
        major_item_pool[ItemName.MetroidDna] = self.options.dna_available.value - local_dna_count
        major_item_pool[ItemName.MetroidDnaLocal] = local_dna_count

        # Tanks
        major_item_pool[ItemName.EnergyTank] = 10  # E-tanks should be immune to tank displacement
        minor_item_pool[ItemName.MissileTank] = 80
        minor_item_pool[ItemName.SuperMissileTank] = 30
        minor_item_pool[ItemName.PowerBombTank] = 15
        minor_item_pool[ItemName.AeionTank] = 15

        # Adjustments
        major_item_pool.subtract(self.skipped_items)
        assert all(count >= 0 for count in major_item_pool.values()), major_item_pool

        item_count = major_item_pool.total() + minor_item_pool.total()
        location_count = LOCATION_COUNT - prefilled_locations
        if item_count < location_count:
            minor_item_pool[self.get_filler_item_name()] = location_count - item_count
        elif item_count > location_count:
            # Store items removed from the pool to make space so they can be returned if a vacancy opens up
            # Items to remove are randomly selected from the tanks (for a tiny bit of silly random fun)
            self.displaced_filler = self.random.sample(
                list(minor_item_pool.keys()), item_count - location_count, counts=minor_item_pool.values()
            )
            minor_item_pool -= Counter(self.displaced_filler)

        self.multiworld.itempool += [self.create_item(name) for name in major_item_pool.elements()]
        self.multiworld.itempool += [self.create_item(name) for name in minor_item_pool.elements()]

    @classmethod
    def stage_finalize_multiworld(cls, multiworld: MultiWorld):
        # Hide the use of item names to implement forced-local Metroid DNA amounts
        for location in multiworld.get_locations():
            assert location.item
            if location.item.game == cls.game and location.item.name == ItemName.MetroidDnaLocal:
                location.item.name = ItemName.MetroidDna
        for world in multiworld.worlds.values():
            if world.game == cls.game:
                world.options.local_items.value.discard(ItemName.MetroidDnaLocal)

    def generate_output(self, output_directory: str):
        patch = SamusReturnsPatch(player=self.player, player_name=self.player_name)
        patch.create_config(self)

        output_filename = f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"
        output_path = Path(output_directory) / output_filename
        patch.write(str(output_path))

    def fill_slot_data(self):
        def get_name(option: type[Option]):
            for name, ty in type(self.options).type_hints.items():
                if ty is option:
                    return name
            raise KeyError(option)

        def resolve_group(name: str):
            for group in self.web.option_groups:
                if group.name == name:
                    return (get_name(opt) for opt in group.options)
            raise KeyError(name)

        def get_options(*types_or_groups: type[Option] | str):
            options: list[str] = []
            for type_or_group in types_or_groups:
                if isinstance(type_or_group, type):
                    options.append(get_name(type_or_group))
                else:
                    options.extend(resolve_group(type_or_group))
            return self.options.as_dict(*options)

        return {
            "ammo_amounts": self.ammo_amounts,
            "options": get_options(
                MetroidDnaRequired,
                DeathLink,
                "Logic",
            ),
        }

    def get_filler_item_name(self):
        if self.displaced_filler:
            return self.displaced_filler.pop()
        return ItemName.Nothing

    def create_item(self, name: str):
        if self.is_universal_tracker() and name == self.glitches_item_name:
            return SamusReturnsItem(name, ItemClassification.progression, None, self.player)

        data = item_data_table[ItemName.MetroidDna if name == ItemName.MetroidDnaLocal else ItemName(name)]
        return SamusReturnsItem(name, data.classification(), data.ap_id, self.player)

    def visualize_regions(self):
        Utils.visualize_regions(self.get_region(self.origin_region_name), Utils.output_path("msr.puml"))

    # UT integration

    ut_can_gen_without_yaml = True
    glitches_item_name = "SEQUENCE BREAKS"

    def is_universal_tracker(self):
        return hasattr(self.multiworld, "generation_is_fake")

    @staticmethod
    def interpret_slot_data(slot_data):
        # Trigger a re-gen instead
        return slot_data

    def set_options_from_slot_data(self):
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if not re_gen_passthrough or self.game not in re_gen_passthrough:
            return
        slot_data = re_gen_passthrough[self.game]

        for key, value in slot_data["options"].items():
            option: Option | None = getattr(self.options, key, None)
            if option is not None:
                setattr(self.options, key, option.from_any(value))

        self.ammo_amounts = slot_data["ammo_amounts"]


def get_local_dna_count(world: SamusReturnsWorld):
    dna_available = world.options.dna_available.value
    local_dna = world.options.local_dna.value
    if world.multiworld.players == 1 or dna_available == 0 or local_dna == 0:
        return 0
    if local_dna == 100:
        return dna_available

    local_dna_amount = dna_available * local_dna / LocalDna.range_end
    local_dna_count = int(local_dna_amount)
    if world.random.random() < (local_dna_amount - local_dna_count):
        local_dna_count += 1
    assert local_dna_count <= dna_available
    return local_dna_count


def launch_client(*args):
    from . import client

    Launcher.launch_subprocess(client.launch, name="MetroidSamusReturnsClient", args=args)


Launcher.components.append(
    Launcher.Component(
        "Metroid: Samus Returns Client",
        func=launch_client,
        component_type=Launcher.Type.CLIENT,
        file_identifier=Launcher.SuffixIdentifier(SamusReturnsPatch.patch_file_ending),
    )
)
