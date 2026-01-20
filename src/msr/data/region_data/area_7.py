from ..internal_names import AreaId
from ..room_names import Area7, AreaName
from . import AreaData, RoomData

area_7_data = AreaData(
    name=AreaName.Area7,
    id=AreaId.AREA_7,
    rooms={
        Area7.LabTeleporterW: RoomData(id="collision_camera_005"),
        Area7.GrapplePuzzleMadness: RoomData(id="collision_camera_006"),
        Area7.SpiderBoostTunnelS: RoomData(id="collision_camera_007"),
        Area7.LabTeleporterE: RoomData(id="collision_camera_008"),
        Area7.Omega2: RoomData(id="collision_camera_009"),
        Area7.RobotRegime: RoomData(id="collision_camera_010"),
        Area7.TransportArea6: RoomData(id="collision_camera_011"),
        Area7.OmegaSAccess: RoomData(id="collision_camera_012"),
        Area7.OmegaS: RoomData(id="collision_camera_013"),
        Area7.OmegaN: RoomData(id="collision_camera_014"),
        Area7.OmegaNAccess: RoomData(id="collision_camera_015"),
        Area7.WallfireWorkstation: RoomData(id="collision_camera_016"),
        Area7.GrapplePuzzleFoyer: RoomData(id="collision_camera_017"),
        Area7.RobotRetreat: RoomData(id="collision_camera_018"),
        Area7.SpiderBoostTunnelN: RoomData(id="collision_camera_019"),
        Area7.TransportArea8: RoomData(id="collision_camera_021"),
    },
)
