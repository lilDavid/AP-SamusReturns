from ..internal_names import AreaId
from ..room_names import Area6
from . import AreaData, RoomData

area_6_data = AreaData(
    name="Area 6",
    id=AreaId.AREA_6,
    rooms={
        Area6.TransportArea7: RoomData(id="collision_camera_034"),
        Area6.TeleporterS: RoomData(id="collision_camera_035"),
        Area6.Omega: RoomData(id="collision_camera_037"),
        Area6.HideoutSprawl: RoomData(id="collision_camera_038"),
        Area6.TeleporterNAccess: RoomData(id="collision_camera_039"),
        Area6.CrumblingBridge: RoomData(id="collision_camera_040"),
        Area6.HideoutEntrance: RoomData(id="collision_camera_041"),
        Area6.CrumblingStairwell: RoomData(id="collision_camera_042"),
        Area6.Diggernaut: RoomData(id="collision_camera_043"),
        Area6.SwarmSquare: RoomData(id="collision_camera_044"),
        Area6.ElectricEscalade: RoomData(id="collision_camera_045"),
        Area6.PoisonousTunnel: RoomData(id="collision_camera_046"),
        Area6.ZetaAccess: RoomData(id="collision_camera_047"),
        Area6.Zeta: RoomData(id="collision_camera_048"),
        Area6.TransportArea5: RoomData(id="collision_camera_051"),
        Area6.ChozoSealE: RoomData(id="collision_camera_060"),
        Area6.OmegaAccess: RoomData(id="collision_camera_061"),
        Area6.ChozoSealW: RoomData(id="collision_camera_Hazard_End_A"),
        Area6.TeleporterN: RoomData(id="collision_camera_Hazard_End_B"),
    },
)
