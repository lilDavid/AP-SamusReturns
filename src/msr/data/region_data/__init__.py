from __future__ import annotations

from collections.abc import Mapping
from typing import NamedTuple

from ..internal_names import AreaId
from ..room_names import RoomName


def subregion_name(room: RoomName, subregion: str):
    return f"{room.with_area()} - {subregion}"


class AreaData(NamedTuple):
    name: str
    id: AreaId
    rooms: Mapping[RoomName, RoomData]


class RoomData(NamedTuple):
    id: str
    # region_data: RegionData | Mapping[str, RegionData]


class RegionData(NamedTuple):
    id: str
