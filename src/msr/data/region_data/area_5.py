from ..internal_names import AreaId
from ..room_names import Area5Exterior, Area5Interior, Area5Lobby
from . import AreaData, RoomData

area_5_lobby_data = AreaData(
    name="Area 5 Tower Lobby",
    id=AreaId.AREA_5_LOBBY,
    rooms=[
        RoomData(
            Area5Lobby.LobbySaveStation,
            id="collision_camera_001",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Lobby.TransportTowerIntE,
            id="collision_camera_002",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Lobby.TransportAreas4And6,
            id="collision_camera_004",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Lobby.LobbyTeleporterW,
            id="collision_camera_006",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Lobby.JShapeTunnel,
            id="collision_camera_007",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Lobby.TransportTowerIntW,
            id="collision_camera_010",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Lobby.LobbyTeleporterE,
            id="collision_camera_011",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Lobby.Alpha2,
            id="collision_camera_012",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Lobby.Gamma2Access,
            id="collision_camera_013",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Lobby.PhaseDrift,
            id="collision_camera_014",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Lobby.MeboidMillpond,
            id="collision_camera_015",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Lobby.Gamma2,
            id="collision_camera_016",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Lobby.LobbyPassageway,
            id="collision_camera_017",
            regions=[],  # TODO
        ),
    ],
)

area_5_exterior_data = AreaData(
    name="Area 5 Tower Exterior",
    id=AreaId.AREA_5_EXTERIOR,
    rooms=[
        RoomData(
            Area5Exterior.TowerExt,
            id="collision_camera_002",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Exterior.OvergrownMaze,
            id="collision_camera_004",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Exterior.ScrewAttack,
            id="collision_camera_005",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Exterior.ZetaAccess,
            id="collision_camera_006",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Exterior.RedPlantMaze,
            id="collision_camera_008",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Exterior.TransportTowerIntW,
            id="collision_camera_011",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Exterior.Zeta,
            id="collision_camera_012",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Exterior.ParabyParlor,
            id="collision_camera_013",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Exterior.Gamma2,
            id="collision_camera_014",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Exterior.Gamma,
            id="collision_camera_015",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Exterior.ScrewAttackAccess,
            id="collision_camera_016",
            regions=[],  # TODO
        ),
    ],
)

area_5_interior_data = AreaData(
    name="Area 5 Dam Interior",
    id=AreaId.AREA_5_INTERIOR,
    rooms=[
        RoomData(
            Area5Interior.TransportTowerLobbyE,
            id="collision_camera_002",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Interior.InteriorSaveStation,
            id="collision_camera_003",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Interior.TransportTowerExtE,
            id="collision_camera_005",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Interior.PlasmaBeam,
            id="collision_camera_006",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Interior.GrappleShuffler,
            id="collision_camera_007",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Interior.AutrackAcropolis,
            id="collision_camera_008",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Interior.GravitySuit,
            id="collision_camera_009",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Interior.PhaseDriftTrialReward,
            id="collision_camera_010",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Interior.PhaseDriftTrialW,
            id="collision_camera_011",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Interior.PhaseDriftTrialE,
            id="collision_camera_012",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Interior.TransportTowerLobbyW,
            id="collision_camera_015",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Interior.MetroidMarina,
            id="collision_camera_016",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Interior.Zeta2Access,
            id="collision_camera_017",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Interior.TransportTowerExtW,
            id="collision_camera_018",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Interior.GravitySuitAccess,
            id="collision_camera_020",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Interior.PhaseDriftTrialEntrance,
            id="collision_camera_021",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Interior.Gamma2,
            id="collision_camera_022",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Interior.InteriorTeleporter,
            id="collision_camera_023",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Interior.Zeta2,
            id="collision_camera_025",
            regions=[],  # TODO
        ),
        RoomData(
            Area5Interior.Gamma2Access,
            id="collision_camera_026",
            regions=[],  # TODO
        ),
    ],
)
