from __future__ import annotations

import logging
from collections import Counter
from collections.abc import Sequence
from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import CollectionState, Item, ItemClassification
from Fill import fill_restrictive

from .data import GAME_NAME
from .data.room_names import RoomName, SurfaceEast
from .items import VICTORY, ItemName, SamusReturnsItem

if TYPE_CHECKING:
    from . import SamusReturnsWorld


class StartingRoomData(NamedTuple):
    room: RoomName
    actor: str
    loadout: Sequence[ItemName] = ()
    subregion: str | None = None

    def to_config(self):
        return {
            "scenario": self.room.area().id,
            "actor": self.actor,
        }


landing_site_data = StartingRoomData(
    SurfaceEast.LandingSite,
    subregion="East",
    actor="StartPoint0",
    loadout=[ItemName.MissileLauncher, ItemName.MorphBall],
)


def set_starting_room(world: SamusReturnsWorld):
    starting_region = landing_site_data.room.subregion(landing_site_data.subregion)
    logging.debug("Starting region for %s: %s", world.player_name, starting_region)
    world.origin_region_name = starting_region


def place_starting_loadout(world: SamusReturnsWorld):
    precollected = Counter(ItemName(item.name) for item in world.multiworld.precollected_items[world.player])
    loadout = Counter(landing_site_data.loadout) - precollected
    if loadout.total() == 0:
        return 0

    # Determine the maximal set of locations we could put these items in
    # The result will contain locations that go unused because they're only reachable with all and that's ok
    items: list[Item] = [world.create_item(name) for name in loadout.elements()]
    world_locations = list(world.get_locations())
    state = CollectionState(world.multiworld)
    for item in items:
        state.collect(item, prevent_sweep=True)
    state.sweep_for_advancements(locations=world_locations)
    locations = [loc for loc in world_locations if loc.item is None and loc.can_reach(state)]
    initial_location_count = len(locations)

    state = CollectionState(world.multiworld)
    state.sweep_for_advancements(locations=world_locations)
    if state.has(VICTORY, world.player):
        state.remove(SamusReturnsItem(VICTORY, ItemClassification.progression, None, world.player))
    world.random.shuffle(items)
    world.random.shuffle(locations)
    fill_restrictive(
        world.multiworld,
        state,
        locations,
        items,
        single_player_placement=True,
        lock=True,
        allow_partial=True,
        allow_excluded=True,
        name=f"{GAME_NAME} starting loadout P{world.player}",
    )
    for item in items:
        world.push_precollected(item)
        logging.debug("Added %s to starting equipment", world.multiworld.get_name_string_for_object(item))

    world.skipped_items.update(loadout)
    return initial_location_count - len(locations)
