from __future__ import annotations

import itertools
import math
from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING, NamedTuple, TypeVar, cast

from BaseClasses import Item, Location, LocationProgressType

from .data.internal_names import AreaId
from .data.room_names import Area6, Area8
from .items import ItemName, major_items

if TYPE_CHECKING:
    from . import SamusReturnsWorld


class HintData(NamedTuple):
    scenario: AreaId
    actor: str

    def get_config(self, lines: Sequence[str]):
        text = "".join(line + "\n" for line in lines)
        return {
            "accesspoint_actor": {
                "scenario": self.scenario,
                "actor": self.actor,
            },
            "text": text,
        }


hint_data = [
    # Vanilla
    HintData(AreaId.SURFACE_EAST, "LE_ChozoUnlockAreaDNA"),
    HintData(AreaId.AREA_1, "LE_ChozoUnlockAreaDNA"),
    HintData(AreaId.AREA_2_ENTRYWAY, "LE_ChozoUnlockAreaDNA"),
    HintData(AreaId.AREA_3_EXTERIOR, "LE_ChozoUnlockAreaDNA"),
    HintData(AreaId.AREA_4_CAVES, "LE_ChozoUnlockAreaDNA_001"),
    HintData(AreaId.AREA_4_CAVES, "LE_ChozoUnlockAreaDNA_002"),
    HintData(AreaId.AREA_5_LOBBY, "LE_ChozoUnlockAreaDNA"),
    HintData(AreaId.AREA_6, "LE_ChozoUnlockAreaDNA_001"),
    HintData(AreaId.AREA_6, "LE_ChozoUnlockAreaDNA_002"),
    HintData(AreaId.AREA_7, "LE_ChozoUnlockAreaDNA"),
    # Rando
    HintData(AreaId.AREA_1, "LE_RandoDNA"),
    HintData(AreaId.AREA_2_EXTERIOR, "LE_RandoDNA"),
    HintData(AreaId.AREA_3_CAVERNS, "LE_RandoDNA"),
    HintData(AreaId.AREA_4_MINES, "LE_RandoDNA"),
    HintData(AreaId.AREA_5_EXTERIOR, "LE_RandoDNA"),
    HintData(AreaId.AREA_6, "LE_RandoDNA_001"),
    HintData(AreaId.AREA_6, "LE_RandoDNA_002"),
    HintData(AreaId.AREA_7, "LE_RandoDNA"),
    HintData(AreaId.AREA_8, "LE_RandoDNA"),
    HintData(AreaId.SURFACE_WEST, "LE_RandoDNA"),
]

T = TypeVar("T")

DNA_HINTS_PER_STATUE = 5

# Always hint these locations
# May change based on settings in future
ALWAYS_HINTS = [
    Area6.Diggernaut.location(),
    Area6.ElectricEscalade.location(),
    Area8.Hatchling.location(),
]


def split_list(list: list[T], index: int) -> tuple[list[T], list[T]]:
    return list[:index], list[index:]


def create_hints(world: SamusReturnsWorld):
    forbidden_locations = set(world.prefilled_locations)

    def get_hintable_locations(locations: Iterable[Location]):
        valid_locations = [
            loc
            for loc in locations
            if loc.address is not None
            and loc.item is not None
            and loc.progress_type != LocationProgressType.EXCLUDED
            and loc.name not in world.options.start_location_hints.value
            and loc.item.name not in world.options.start_hints.value
        ]
        world.random.shuffle(valid_locations)
        return valid_locations

    def filter_forbidden(locations: Iterable[Location]):
        return filter(lambda location: location not in forbidden_locations, locations)

    locations = get_hintable_locations(world.get_locations())
    always_hint_locations = get_hintable_locations(world.get_location(loc) for loc in ALWAYS_HINTS)
    item_locations = get_hintable_locations(world.multiworld.find_items_in_locations(major_items.keys(), world.player))
    if ItemName.MetroidDna in world.options.start_hints.value:
        dna_statue_count = 0
        dna_groups = []
    else:
        dna_locations = get_hintable_locations(world.multiworld.find_item_locations(ItemName.MetroidDna, world.player))
        dna_locations = dna_locations[: world.options.dna_required]
        dna_statue_count = math.ceil(world.options.dna_required / DNA_HINTS_PER_STATUE)
        dna_groups: list[list[Location]] = [[] for _ in range(dna_statue_count)]
        # Round robin so the hints are evenly distributed
        for group, location in zip(itertools.cycle(dna_groups), dna_locations, strict=False):
            group.append(location)

    hints: dict[HintData, list[Location | Item]] = {}
    _hints = list(hint_data)
    world.random.shuffle(_hints)

    # Allocate DNA and always hints first
    # Then at least 2 location hints for every item hint because the item hints are powerful
    dna_hints, _hints = split_list(_hints, dna_statue_count)
    always_hints, _hints = split_list(_hints, len(ALWAYS_HINTS))
    item_hints, location_hints = map(iter, split_list(_hints, len(_hints) // 3))

    for hint, dna_group in zip(dna_hints, dna_groups, strict=False):
        hints[hint] = sorted(dna_group, key=lambda location: location.name)
        forbidden_locations.update(dna_group)
    for hint, location in zip(always_hints, filter_forbidden(always_hint_locations), strict=False):
        hints[hint] = [location]
        forbidden_locations.add(location)
    for hint, location in itertools.chain(
        zip(location_hints, filter_forbidden(locations), strict=False),
        zip(item_hints, filter_forbidden(item_locations), strict=False),
    ):
        hints[hint] = [world.random.choice([location, cast(Item, location.item)])]
        forbidden_locations.add(location)

    # If we run out of either location or item hints, spill the other type into the remaining hint slots
    for hint, location in itertools.chain(
        zip(location_hints, filter_forbidden(item_locations), strict=False),
        zip(item_hints, filter_forbidden(locations), strict=False),
    ):
        hints[hint] = [world.random.choice([location, cast(Item, location.item)])]
        forbidden_locations.add(location)

    return hints
