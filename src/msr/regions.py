from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.rules import False_

from .data.region_data import ExitData, RegionData
from .data.region_data.area_1 import area_1_data
from .data.region_data.area_2 import area_2_entryway_data, area_2_exterior_data, area_2_interior_data
from .data.region_data.area_3 import area_3_caverns_data, area_3_exterior_data, area_3_interior_data
from .data.region_data.area_4 import area_4_caves_data, area_4_mines_data
from .data.region_data.area_5 import area_5_exterior_data, area_5_interior_data, area_5_lobby_data
from .data.region_data.area_6 import area_6_data
from .data.region_data.area_7 import area_7_data
from .data.region_data.area_8 import area_8_data
from .data.region_data.surface import surface_east_data, surface_west_data
from .data.room_names import RoomName
from .items import SamusReturnsItem
from .locations import SamusReturnsLocation, location_table
from .logic import door_rules

if TYPE_CHECKING:
    from . import SamusReturnsWorld

all_areas_data = (
    surface_east_data,
    area_1_data,
    area_2_entryway_data,
    area_2_exterior_data,
    area_2_interior_data,
    area_3_caverns_data,
    area_3_exterior_data,
    area_3_interior_data,
    area_4_caves_data,
    area_4_mines_data,
    area_5_exterior_data,
    area_5_interior_data,
    area_5_lobby_data,
    area_6_data,
    area_7_data,
    area_8_data,
    surface_west_data,
)


def walk_region_graph():
    for area in all_areas_data:
        for room in area.rooms:
            for subregion in room.regions:
                yield room, subregion


def can_take_exit(exit: ExitData):
    return door_rules[exit.door] & exit.access_rule


def can_leave_area(subregion: RegionData):
    rule = False_()
    for exit in subregion.exits:
        rule |= can_take_exit(exit)
    return rule


def create_regions(world: SamusReturnsWorld):
    regions: list[Region] = []
    for room, subregion in walk_region_graph():
        name = room.name.subregion(subregion.name)
        region = Region(name, world.player, multiworld=world.multiworld)  # TODO: Hint text

        for pickup in subregion.pickups:
            pickup_name = room.name.location(pickup.name)
            location = SamusReturnsLocation(world.player, pickup_name, location_table[pickup_name].ap_id, region)
            region.locations.append(location)

        for event in subregion.events:
            region.add_event(
                room.name.location(event.name),
                event.item_name,
                show_in_spoiler=event.show_in_spoiler,
                location_type=SamusReturnsLocation,
                item_type=SamusReturnsItem,
            )
        regions.append(region)
    world.multiworld.regions += regions


def set_location_rules(world: SamusReturnsWorld):
    for room, subregion in walk_region_graph():
        for action in itertools.chain(subregion.pickups, subregion.events):
            location = world.get_location(room.name.location(action.name))
            access_rule = action.access_rule
            if subregion.require_exit_access:
                access_rule &= can_leave_area(subregion)
            world.set_rule(location, access_rule)


def connect_entrances(world: SamusReturnsWorld):
    for room, subregion in walk_region_graph():
        region_name = room.name.subregion(subregion.name) if subregion.name else room.name.with_area()
        region = world.get_region(region_name)
        for exit in subregion.exits:
            world.create_entrance(
                region,
                world.get_region(
                    exit.destination.with_area() if isinstance(exit.destination, RoomName) else exit.destination
                ),
                can_take_exit(exit),
                f"{region_name} - {exit.door.value} to {exit.destination}",
            )
