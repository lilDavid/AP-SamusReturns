from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from enum import Enum
from typing import NamedTuple

from BaseClasses import CollectionState

from ..internal_names import AreaId
from ..room_names import RoomName

AccessRule = Callable[[CollectionState, int], bool] | None


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
    rooms: Mapping[RoomName, RoomData]


class RoomData(NamedTuple):
    id: str
    region_data: RegionData | Mapping[str, RegionData]


class RegionData(NamedTuple):
    exits: Sequence[ExitData]
    pickups: Sequence[PickupData] = []
    pickups_require_exit: bool = False  # Require access to one of this room's exits for pickups to be reachable


class ExitData(NamedTuple):
    door: Door
    destination: str
    access_rule: AccessRule = None


class PickupData(NamedTuple):
    name: str | None = None
    access_rule: AccessRule = None
