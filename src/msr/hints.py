from __future__ import annotations

import itertools
import math
from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING, NamedTuple, cast

from BaseClasses import Item, Location, LocationProgressType

from .data.internal_names import AreaId
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


DNA_HINTS_PER_STATUE = 5


def create_hints(world: SamusReturnsWorld):
    hints: dict[HintData, list[Location | Item]] = {}
    forbidden_locations = set(world.prefilled_locations)

    def filter_forbidden(locations: Iterable[Location]):
        return filter(lambda location: location not in forbidden_locations, locations)

    locations = [
        loc
        for loc in world.get_locations()
        if loc.address is not None
        and loc.item is not None
        and loc.progress_type != LocationProgressType.EXCLUDED
        and loc.name not in world.options.start_location_hints.value
        and loc.item.name not in world.options.start_hints.value
    ]
    world.random.shuffle(locations)

    item_locations = [
        loc
        for loc in world.multiworld.find_items_in_locations(major_items.keys(), world.player)
        if loc.name not in world.options.start_location_hints.value
        and cast(Item, loc.item).name not in world.options.start_hints.value
    ]
    world.random.shuffle(item_locations)

    if ItemName.MetroidDna in world.options.start_hints.value:
        dna_statue_count = 0
        dna_groups = []
    else:
        dna_locations = [
            loc
            for loc in world.multiworld.find_item_locations(ItemName.MetroidDna, world.player)
            if loc not in forbidden_locations
            and loc.name not in world.options.start_location_hints.value
            and cast(Item, loc.item).name not in world.options.start_hints.value
        ]
        dna_locations = dna_locations[: world.options.dna_required]
        world.random.shuffle(dna_locations)
        dna_statue_count = math.ceil(world.options.dna_required / DNA_HINTS_PER_STATUE)
        dna_groups: list[list[Location]] = [[] for _ in range(dna_statue_count)]
        # Round robin so the hints are evenly distributed
        for group, location in zip(itertools.cycle(dna_groups), dna_locations, strict=False):
            group.append(location)

    _hints = list(hint_data)
    world.random.shuffle(_hints)

    dna_hints = _hints[:dna_statue_count]
    _hints = _hints[dna_statue_count:]
    location_hints = _hints[: len(_hints) // 2]
    item_hints = _hints[len(_hints) // 2 :]

    for hint, dna_group in zip(dna_hints, dna_groups, strict=False):
        hints[hint] = sorted((cast(Item, location.item) for location in dna_group), key=lambda location: location.name)
        forbidden_locations.update(dna_group)
    for hint, location in zip(location_hints, filter_forbidden(locations), strict=False):
        hints[hint] = [location]
        forbidden_locations.add(location)
    for hint, location in zip(item_hints, filter_forbidden(item_locations), strict=False):
        hints[hint] = [cast(Item, location.item)]
        forbidden_locations.add(location)

    return hints
