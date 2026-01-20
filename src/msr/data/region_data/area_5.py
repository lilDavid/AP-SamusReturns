from ..internal_names import AreaId
from ..room_names import Area5Exterior, Area5Interior, Area5Lobby
from . import AreaData, RoomData

area_5_lobby_data = AreaData(
    name="Area 5 Tower Lobby",
    id=AreaId.AREA_5_LOBBY,
    rooms={
        Area5Lobby.LobbySaveStation: RoomData(id="collision_camera_001"),
        Area5Lobby.TransportTowerIntE: RoomData(id="collision_camera_002"),
        Area5Lobby.TransportAreas4And6: RoomData(id="collision_camera_004"),
        Area5Lobby.LobbyTeleporterW: RoomData(id="collision_camera_006"),
        Area5Lobby.JShapeTunnel: RoomData(id="collision_camera_007"),
        Area5Lobby.TransportTowerIntW: RoomData(id="collision_camera_010"),
        Area5Lobby.LobbyTeleporterE: RoomData(id="collision_camera_011"),
        Area5Lobby.Alpha2: RoomData(id="collision_camera_012"),
        Area5Lobby.Gamma2Access: RoomData(id="collision_camera_013"),
        Area5Lobby.PhaseDrift: RoomData(id="collision_camera_014"),
        Area5Lobby.MeboidMillpond: RoomData(id="collision_camera_015"),
        Area5Lobby.Gamma2: RoomData(id="collision_camera_016"),
        Area5Lobby.LobbyPassageway: RoomData(id="collision_camera_017"),
    },
)

area_5_exterior_data = AreaData(
    name="Area 5 Tower Exterior",
    id=AreaId.AREA_5_EXTERIOR,
    rooms={
        Area5Exterior.TowerExt: RoomData(id="collision_camera_002"),
        Area5Exterior.OvergrownMaze: RoomData(id="collision_camera_004"),
        Area5Exterior.ScrewAttack: RoomData(id="collision_camera_005"),
        Area5Exterior.ZetaAccess: RoomData(id="collision_camera_006"),
        Area5Exterior.RedPlantMaze: RoomData(id="collision_camera_008"),
        Area5Exterior.TransportTowerIntW: RoomData(id="collision_camera_011"),
        Area5Exterior.Zeta: RoomData(id="collision_camera_012"),
        Area5Exterior.ParabyParlor: RoomData(id="collision_camera_013"),
        Area5Exterior.Gamma2: RoomData(id="collision_camera_014"),
        Area5Exterior.Gamma: RoomData(id="collision_camera_015"),
        Area5Exterior.ScrewAttackAccess: RoomData(id="collision_camera_016"),
    },
)

area_5_interior_data = AreaData(
    name="Area 5 Dam Interior",
    id=AreaId.AREA_5_INTERIOR,
    rooms={
        Area5Interior.TransportTowerLobbyE: RoomData(id="collision_camera_002"),
        Area5Interior.InteriorSaveStation: RoomData(id="collision_camera_003"),
        Area5Interior.TransportTowerExtE: RoomData(id="collision_camera_005"),
        Area5Interior.PlasmaBeam: RoomData(id="collision_camera_006"),
        Area5Interior.GrappleShuffler: RoomData(id="collision_camera_007"),
        Area5Interior.AutrackAcropolis: RoomData(id="collision_camera_008"),
        Area5Interior.GravitySuit: RoomData(id="collision_camera_009"),
        Area5Interior.PhaseDriftTrialReward: RoomData(id="collision_camera_010"),
        Area5Interior.PhaseDriftTrialW: RoomData(id="collision_camera_011"),
        Area5Interior.PhaseDriftTrialE: RoomData(id="collision_camera_012"),
        Area5Interior.TransportTowerLobbyW: RoomData(id="collision_camera_015"),
        Area5Interior.MetroidMarina: RoomData(id="collision_camera_016"),
        Area5Interior.Zeta2Access: RoomData(id="collision_camera_017"),
        Area5Interior.TransportTowerExtW: RoomData(id="collision_camera_018"),
        Area5Interior.GravitySuitAccess: RoomData(id="collision_camera_020"),
        Area5Interior.PhaseDriftTrialEntrance: RoomData(id="collision_camera_021"),
        Area5Interior.Gamma2: RoomData(id="collision_camera_022"),
        Area5Interior.InteriorTeleporter: RoomData(id="collision_camera_023"),
        Area5Interior.Zeta2: RoomData(id="collision_camera_025"),
        Area5Interior.Gamma2Access: RoomData(id="collision_camera_026"),
    },
)
