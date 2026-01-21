from ..internal_names import AreaId
from ..room_names import Area4Caves, Area4Mines
from . import AreaData, RoomData

area_4_caves_data = AreaData(
    name="Area 4 Central Caves",
    id=AreaId.AREA_4_CAVES,
    rooms={
        Area4Caves.CavesIntersectionTerminal: RoomData(
            id="collision_camera_001",
            region_data={},  # TODO
        ),
        Area4Caves.SpazerBeam: RoomData(
            id="collision_camera_003",
            region_data={},  # TODO
        ),
        Area4Caves.LavaPond: RoomData(
            id="collision_camera_005",
            region_data={},  # TODO
        ),
        Area4Caves.TransportArea3Mines: RoomData(
            id="collision_camera_006",
            region_data={},  # TODO
        ),
        Area4Caves.Alpha2: RoomData(
            id="collision_camera_007",
            region_data={},  # TODO
        ),
        Area4Caves.TransitTunnel: RoomData(
            id="collision_camera_010",
            region_data={},  # TODO
        ),
        Area4Caves.FleechSwarmCave: RoomData(
            id="collision_camera_011",
            region_data={},  # TODO
        ),
        Area4Caves.HostileHangout: RoomData(
            id="collision_camera_012",
            region_data={},  # TODO
        ),
        Area4Caves.Gamma: RoomData(
            id="collision_camera_013",
            region_data={},  # TODO
        ),
        Area4Caves.GammaAccessS: RoomData(
            id="collision_camera_014",
            region_data={},  # TODO
        ),
        Area4Caves.OutwardClimb: RoomData(
            id="collision_camera_015",
            region_data={},  # TODO
        ),
        Area4Caves.AmethystAltars: RoomData(
            id="collision_camera_016",
            region_data={},  # TODO
        ),
        Area4Caves.GammaAccessN: RoomData(
            id="collision_camera_018",
            region_data={},  # TODO
        ),
        Area4Caves.Alpha2Access: RoomData(
            id="collision_camera_019",
            region_data={},  # TODO
        ),
        Area4Caves.VenomousPond: RoomData(
            id="collision_camera_022",
            region_data={},  # TODO
        ),
        Area4Caves.TransportArea5: RoomData(
            id="collision_camera_023",
            region_data={},  # TODO
        ),
    },
)

area_4_mines_data = AreaData(
    name="Area 4 Crystal Mines",
    id=AreaId.AREA_4_MINES,
    rooms={
        Area4Mines.MinesIntersectionTunnel: RoomData(
            id="collision_camera_001",
            region_data={},  # TODO
        ),
        Area4Mines.SuperMissile: RoomData(
            id="collision_camera_002",
            region_data={},  # TODO
        ),
        Area4Mines.PinkCrystalPreserve: RoomData(
            id="collision_camera_003",
            region_data={},  # TODO
        ),
        Area4Mines.TransportCentralCaves: RoomData(
            id="collision_camera_005",
            region_data={},  # TODO
        ),
        Area4Mines.LavaReservoir: RoomData(
            id="collision_camera_006",
            region_data={},  # TODO
        ),
        Area4Mines.DualPondAlcove: RoomData(
            id="collision_camera_007",
            region_data={},  # TODO
        ),
        Area4Mines.Zeta: RoomData(
            id="collision_camera_008",
            region_data={},  # TODO
        ),
        Area4Mines.GawronGroove: RoomData(
            id="collision_camera_009",
            region_data={},  # TODO
        ),
        Area4Mines.MinesEntrance: RoomData(
            id="collision_camera_010",
            region_data={},  # TODO
        ),
        Area4Mines.TsumuriTunnel: RoomData(
            id="collision_camera_011",
            region_data={},  # TODO
        ),
        Area4Mines.MinesTeleporter: RoomData(
            id="collision_camera_012",
            region_data={},  # TODO
        ),
        Area4Mines.GreenCrystalDugout: RoomData(
            id="collision_camera_013",
            region_data={},  # TODO
        ),
        Area4Mines.GemstoneGorge: RoomData(
            id="collision_camera_014",
            region_data={},  # TODO
        ),
        Area4Mines.Gamma2: RoomData(
            id="collision_camera_015",
            region_data={},  # TODO
        ),
        Area4Mines.BasaltBasin: RoomData(
            id="collision_camera_017",
            region_data={},  # TODO
        ),
        Area4Mines.SpaceJump: RoomData(
            id="collision_camera_AfterChase",
            region_data={},  # TODO
        ),
        Area4Mines.DiggernautExcavationTunnels: RoomData(
            id="collision_camera_AfterChase_001",
            region_data={},  # TODO
        ),
    },
)
