from ..internal_names import AreaId
from ..room_names import Area8, AreaName
from . import AreaData, RoomData

area_8_data = AreaData(
    name=AreaName.Area8,
    id=AreaId.AREA_8,
    rooms={
        Area8.TransportSurface: RoomData(id="collision_camera_007"),
        Area8.NestHallwayS: RoomData(id="collision_camera_008"),
        Area8.Amphitheater: RoomData(id="collision_camera_009"),
        Area8.NestNetwork: RoomData(id="collision_camera_010"),
        Area8.EntranceTeleporter: RoomData(id="collision_camera_011"),
        Area8.NestNodule: RoomData(id="collision_camera_012"),
        Area8.NestSmallShaft: RoomData(id="collision_camera_013"),
        Area8.NestShaftE: RoomData(id="collision_camera_014"),
        Area8.NestHallwayNe: RoomData(id="collision_camera_015"),
        Area8.NestHallwayNw: RoomData(id="collision_camera_016"),
        Area8.NestRechargeStations: RoomData(id="collision_camera_017"),
        Area8.NestShaftW: RoomData(id="collision_camera_018"),
        Area8.QueenAccess: RoomData(id="collision_camera_019"),
        Area8.Queen: RoomData(id="collision_camera_020"),
        Area8.TransportArea7: RoomData(id="collision_camera_021"),
        Area8.Hatchling: RoomData(id="collision_camera_022"),
        Area8.NestVestibule: RoomData(id="collision_camera_023"),
        Area8.NestTeleporter: RoomData(id="collision_camera_024"),
    },
)
