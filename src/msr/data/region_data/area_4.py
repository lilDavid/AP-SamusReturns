from ..internal_names import AreaId
from ..room_names import Area4Caves, Area4Mines
from . import AreaData, RoomData

area_4_caves_data = AreaData(
    name="Area 4 Central Caves",
    id=AreaId.AREA_4_CAVES,
    rooms=[
        RoomData(
            Area4Caves.CavesIntersectionTerminal,
            id="collision_camera_001",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Caves.SpazerBeam,
            id="collision_camera_003",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Caves.LavaPond,
            id="collision_camera_005",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Caves.TransportArea3Mines,
            id="collision_camera_006",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Caves.Alpha2,
            id="collision_camera_007",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Caves.TransitTunnel,
            id="collision_camera_010",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Caves.FleechSwarmCave,
            id="collision_camera_011",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Caves.HostileHangout,
            id="collision_camera_012",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Caves.Gamma,
            id="collision_camera_013",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Caves.GammaAccessS,
            id="collision_camera_014",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Caves.OutwardClimb,
            id="collision_camera_015",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Caves.AmethystAltars,
            id="collision_camera_016",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Caves.GammaAccessN,
            id="collision_camera_018",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Caves.Alpha2Access,
            id="collision_camera_019",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Caves.VenomousPond,
            id="collision_camera_022",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Caves.TransportArea5,
            id="collision_camera_023",
            regions=[],  # TODO
        ),
    ],
)

area_4_mines_data = AreaData(
    name="Area 4 Crystal Mines",
    id=AreaId.AREA_4_MINES,
    rooms=[
        RoomData(
            Area4Mines.MinesIntersectionTunnel,
            id="collision_camera_001",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Mines.SuperMissile,
            id="collision_camera_002",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Mines.PinkCrystalPreserve,
            id="collision_camera_003",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Mines.TransportCentralCaves,
            id="collision_camera_005",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Mines.LavaReservoir,
            id="collision_camera_006",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Mines.DualPondAlcove,
            id="collision_camera_007",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Mines.Zeta,
            id="collision_camera_008",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Mines.GawronGroove,
            id="collision_camera_009",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Mines.MinesEntrance,
            id="collision_camera_010",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Mines.TsumuriTunnel,
            id="collision_camera_011",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Mines.MinesTeleporter,
            id="collision_camera_012",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Mines.GreenCrystalDugout,
            id="collision_camera_013",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Mines.GemstoneGorge,
            id="collision_camera_014",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Mines.Gamma2,
            id="collision_camera_015",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Mines.BasaltBasin,
            id="collision_camera_017",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Mines.SpaceJump,
            id="collision_camera_AfterChase",
            regions=[],  # TODO
        ),
        RoomData(
            Area4Mines.DiggernautExcavationTunnels,
            id="collision_camera_AfterChase_001",
            regions=[],  # TODO
        ),
    ],
)
