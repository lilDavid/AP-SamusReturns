from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState, ItemClassification, Region
from worlds.generic.Rules import CollectionRule, add_rule

from .data.region_data import AccessRule, ExitData, RegionData
from .data.region_data.area_1 import area_1_data
from .data.region_data.area_2 import area_2_entryway_data, area_2_exterior_data, area_2_interior_data
from .data.region_data.area_3 import area_3_caverns_data, area_3_exterior_data, area_3_interior_data
from .data.region_data.area_4 import area_4_caves_data, area_4_mines_data
from .data.region_data.area_5 import area_5_exterior_data, area_5_interior_data, area_5_lobby_data
from .data.region_data.area_6 import area_6_data
from .data.region_data.area_7 import area_7_data
from .data.region_data.area_8 import area_8_data
from .data.region_data.surface import surface_east_data, surface_west_data
from .data.room_names import RoomName, SurfaceWest
from .items import SamusReturnsItem
from .locations import SamusReturnsLocation, location_table, make_name
from .logic import can_open_door

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


def create_rule(logic_rule: AccessRule, player: int) -> CollectionRule:
    if logic_rule is None:
        return None
    return lambda state: logic_rule(state, player)


def exit_rule(state: CollectionState, player: int, exit: ExitData):
    if not can_open_door(state, player, exit.door):
        return False
    if exit.access_rule and not exit.access_rule(state, player):
        return False
    return True


def can_take_exit(player: int, exit: ExitData):
    def rule(state: CollectionState):
        return exit_rule(state, player, exit)

    return rule


def can_leave_area(subregion: RegionData, player: int):
    def rule(state: CollectionState):
        for exit in subregion.exits:
            if exit_rule(state, player, exit):
                return True
        return False

    return rule


def set_starting_room(world: SamusReturnsWorld):
    world.origin_region_name = SurfaceWest.LandingSite.subregion("East")


def create_regions(world: SamusReturnsWorld):
    regions: list[Region] = []
    for area in all_areas_data:
        for room in area.rooms:
            for subregion in room.regions:
                name = room.name.subregion(subregion.name) if subregion.name else room.name.with_area()
                region = Region(name, world.player, multiworld=world.multiworld)  # TODO: Hint text

                for pickup in subregion.pickups:
                    pickup_name = make_name(room.name, pickup.name)
                    location = SamusReturnsLocation(
                        world.player, pickup_name, location_table[pickup_name].ap_id, region
                    )
                    if pickup.access_rule:
                        add_rule(location, create_rule(pickup.access_rule, world.player))
                    if subregion.require_exit_access:
                        add_rule(location, can_leave_area(subregion, world.player))
                    region.locations.append(location)

                for event in subregion.events:
                    event_name = make_name(room.name, event.name)
                    location = SamusReturnsLocation(world.player, event_name, None, region)
                    if event.access_rule:
                        add_rule(location, create_rule(event.access_rule, world.player))
                    if subregion.require_exit_access:
                        add_rule(location, can_leave_area(subregion, world.player))
                    location.place_locked_item(
                        SamusReturnsItem(
                            event_name if event.item_name is None else event.item_name,
                            ItemClassification.progression,
                            None,
                            world.player,
                        )
                    )
                    location.show_in_spoiler = event.show_in_spoiler
                    region.locations.append(location)
                regions.append(region)
    world.multiworld.regions += regions


def connect_entrances(world: SamusReturnsWorld):
    for area in all_areas_data:
        for room in area.rooms:
            for subregion in room.regions:
                region_name = room.name.subregion(subregion.name) if subregion.name else room.name.with_area()
                region = world.get_region(region_name)
                for exit in subregion.exits:
                    region.connect(
                        world.get_region(
                            exit.destination.with_area() if isinstance(exit.destination, RoomName) else exit.destination
                        ),
                        f"{region_name} - {exit.door.value} to {exit.destination}",
                        can_take_exit(world.player, exit),
                    )
