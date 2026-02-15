from __future__ import annotations

import logging
from collections import Counter
from typing import TYPE_CHECKING

from BaseClasses import CollectionState, Item
from Fill import fill_restrictive

from .data.constants import GAME_NAME
from .data.room_names import SurfaceWest
from .items import ItemName

if TYPE_CHECKING:
    from . import SamusReturnsWorld


def set_starting_room(world: SamusReturnsWorld):
    starting_region = SurfaceWest.LandingSite.subregion("East")
    loadout = [ItemName.MissileLauncher, ItemName.MorphBall]

    logging.debug("Starting region for %s: %s", world.player_name, starting_region)
    world.origin_region_name = starting_region
    place_starting_loadout(world, Counter(loadout))


def place_starting_loadout(world: SamusReturnsWorld, equipment: Counter[ItemName]):
    precollected = Counter(ItemName(item.name) for item in world.multiworld.precollected_items[world.player])
    loadout = equipment - precollected
    if loadout.total() == 0:
        return

    # Determine the maximal set of locations we could put these items in
    # The result will contain locations that go unused because they're only reachable with all and that's ok
    items: list[Item] = [world.create_item(name) for name in loadout.elements()]
    state = CollectionState(world.multiworld)
    for item in items:
        state.collect(item, prevent_sweep=True)
    state.sweep_for_advancements()
    locations = [loc for loc in world.get_locations() if loc.item is None and loc.can_reach(state)]
    initial_location_count = len(locations)

    state = CollectionState(world.multiworld)
    state.sweep_for_advancements()
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
    world.prefilled_locations += initial_location_count - len(locations)
