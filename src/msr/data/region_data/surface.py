from ..internal_names import AreaId
from ..room_names import SurfaceEast, SurfaceWest
from . import AreaData, RoomData

surface_east_data = AreaData(
    name="Surface East",
    id=AreaId.SURFACE_EAST,
    rooms={
        SurfaceEast.LandingSite: RoomData(id="collision_camera_000"),
        SurfaceEast.TwistyTunnel: RoomData(id="collision_camera_002"),
        SurfaceEast.MorphBall: RoomData(id="collision_camera_003"),
        SurfaceEast.ChozoSeal: RoomData(id="collision_camera_004"),
        SurfaceEast.TransportArea1: RoomData(id="collision_camera_006"),
        SurfaceEast.ChozoCacheE: RoomData(id="collision_camera_007"),
        SurfaceEast.ChargeBeam: RoomData(id="collision_camera_008"),
        SurfaceEast.Alpha: RoomData(id="collision_camera_010"),
        SurfaceEast.ScanPulse: RoomData(id="collision_camera_011"),
        SurfaceEast.ChozoCacheW: RoomData(id="collision_camera_012"),
        SurfaceEast.MoheekMarket: RoomData(id="collision_camera_013"),
        SurfaceEast.CavernCavity: RoomData(id="collision_camera_014"),
        SurfaceEast.ChargeBeamAccess: RoomData(id="collision_camera_015"),
        SurfaceEast.HornoadHallway: RoomData(id="collision_camera_016"),
        SurfaceEast.SurfaceStash: RoomData(id="collision_camera_018"),
        SurfaceEast.SurfaceCrumbleChallenge: RoomData(id="collision_camera_019"),
        SurfaceEast.TransportCache: RoomData(id="collision_camera_020"),
        SurfaceEast.CavernAlcove: RoomData(id="collision_camera_021"),
        SurfaceEast.EnergyRechargeShaft: RoomData(id="collision_camera_023"),
        SurfaceEast.AmmoRecharge: RoomData(id="collision_camera_024"),
    },
)

surface_west_data = AreaData(
    name="Surface West",
    id=AreaId.SURFACE_WEST,
    rooms={
        SurfaceWest.TransportArea8: RoomData(id="collision_camera_017"),
    },
)
