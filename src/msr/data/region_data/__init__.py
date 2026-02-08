from __future__ import annotations

from collections.abc import Sequence
from enum import Enum
from typing import NamedTuple

from rule_builder.rules import Rule, True_

from ..internal_names import AreaId
from ..room_names import RoomName


class Door(Enum):
    Open = "Exit"
    Normal = "Door"
    Charge = "Charge door"
    Missile = "Red door"
    Super = "Green door"
    PowerBomb = "Yellow door"
    MorphTunnel = "Morph tunnel"
    Gigadora = "Gigadora door"
    Gryncore = "Gryncore door"
    Taramarga = "Taramarga door"
    Elevator = "Elevator"


class AreaData(NamedTuple):
    name: str
    id: AreaId
    rooms: Sequence[RoomData]


class RoomData(NamedTuple):
    name: RoomName
    id: str
    regions: Sequence[RegionData]


class RegionData(NamedTuple):
    name: str | None = None
    exits: Sequence[ExitData] = ()
    pickups: Sequence[PickupData] = ()
    events: Sequence[EventData] = ()
    require_exit_access: bool = False  # Require access to one of this room's exits for pickups/events to be reachable


class ExitData(NamedTuple):
    door: Door
    destination: str
    access_rule: Rule = True_()


class PickupData(NamedTuple):
    name: str | None = None
    access_rule: Rule = True_()


class EventData(NamedTuple):
    name: str
    item_name: str | None = None
    access_rule: Rule = True_()
    show_in_spoiler: bool = False
