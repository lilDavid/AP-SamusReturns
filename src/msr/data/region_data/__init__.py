from __future__ import annotations

from collections.abc import Sequence
from enum import Enum
from typing import TYPE_CHECKING, NamedTuple

from rule_builder.rules import Rule, True_

from ..internal_names import AreaId
from ..room_names import RoomName

if TYPE_CHECKING:
    from ... import SamusReturnsWorld


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
    Locked = "Locked door"


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


class ExitData(NamedTuple):
    door: Door
    destination: str
    access_rule: Rule[SamusReturnsWorld] = True_()


class PickupData(NamedTuple):
    name: str | None = None
    access_rule: Rule[SamusReturnsWorld] = True_()


class EventData(NamedTuple):
    name: str
    item_name: str | None = None
    access_rule: Rule[SamusReturnsWorld] = True_()
    show_in_spoiler: bool = False


# Contextually links to a subregion in the same room
class Subregion(str):
    pass
