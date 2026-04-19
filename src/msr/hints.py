from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, NamedTuple, cast

from BaseClasses import Item, Location, LocationProgressType

from .data.internal_names import AreaId
from .items import major_items

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


def create_hints(world: SamusReturnsWorld):
    hints: dict[HintData, list[Location | Item]] = {}
    forbidden_locations = set(world.prefilled_locations)

    _hints = list(hint_data)
    world.random.shuffle(_hints)
    location_hints = _hints[: len(_hints) // 2]
    item_hints = _hints[len(_hints) // 2 :]

    locations = [
        loc
        for loc in world.get_locations()
        if loc.address is not None
        and loc.item is not None
        and loc not in forbidden_locations
        and loc.progress_type != LocationProgressType.EXCLUDED
        and loc.name not in world.options.start_location_hints.value
        and loc.item.name not in world.options.start_hints.value
    ]
    world.random.shuffle(locations)
    for hint, location in zip(location_hints, locations, strict=False):
        hints[hint] = [location]
        forbidden_locations.add(location)

    item_locations = [
        loc
        for loc in world.multiworld.find_items_in_locations(major_items.keys(), world.player)
        if loc not in forbidden_locations
        and loc.name not in world.options.start_location_hints.value
        and cast(Item, loc.item).name not in world.options.start_hints.value
    ]
    world.random.shuffle(item_locations)
    for hint, location in zip(item_hints, item_locations, strict=False):
        hints[hint] = [cast(Item, location.item)]
        forbidden_locations.add(location)

    return hints
