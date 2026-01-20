from ..internal_names import AreaId
from ..room_names import Area4Caves, Area4Mines
from . import AreaData, RoomData

area_4_caves_data = AreaData(
    name="Area 4 Central Caves",
    id=AreaId.AREA_4_CAVES,
    rooms={
        Area4Caves.CavesIntersectionTerminal: RoomData(id="collision_camera_001"),
        Area4Caves.SpazerBeam: RoomData(id="collision_camera_003"),
        Area4Caves.LavaPond: RoomData(id="collision_camera_005"),
        Area4Caves.TransportArea3Mines: RoomData(id="collision_camera_006"),
        Area4Caves.Alpha2: RoomData(id="collision_camera_007"),
        Area4Caves.TransitTunnel: RoomData(id="collision_camera_010"),
        Area4Caves.FleechSwarmCave: RoomData(id="collision_camera_011"),
        Area4Caves.HostileHangout: RoomData(id="collision_camera_012"),
        Area4Caves.Gamma: RoomData(id="collision_camera_013"),
        Area4Caves.GammaAccessS: RoomData(id="collision_camera_014"),
        Area4Caves.OutwardClimb: RoomData(id="collision_camera_015"),
        Area4Caves.AmethystAltars: RoomData(id="collision_camera_016"),
        Area4Caves.GammaAccessN: RoomData(id="collision_camera_018"),
        Area4Caves.Alpha2Access: RoomData(id="collision_camera_019"),
        Area4Caves.VenomousPond: RoomData(id="collision_camera_022"),
        Area4Caves.TransportArea5: RoomData(id="collision_camera_023"),
    },
)

area_4_mines_data = AreaData(
    name="Area 4 Crystal Mines",
    id=AreaId.AREA_4_MINES,
    rooms={
        Area4Mines.MinesIntersectionTunnel: RoomData(id="collision_camera_001"),
        Area4Mines.SuperMissile: RoomData(id="collision_camera_002"),
        Area4Mines.PinkCrystalPreserve: RoomData(id="collision_camera_003"),
        Area4Mines.TransportCentralCaves: RoomData(id="collision_camera_005"),
        Area4Mines.LavaReservoir: RoomData(id="collision_camera_006"),
        Area4Mines.DualPondAlcove: RoomData(id="collision_camera_007"),
        Area4Mines.Zeta: RoomData(id="collision_camera_008"),
        Area4Mines.GawronGroove: RoomData(id="collision_camera_009"),
        Area4Mines.MinesEntrance: RoomData(id="collision_camera_010"),
        Area4Mines.TsumuriTunnel: RoomData(id="collision_camera_011"),
        Area4Mines.MinesTeleporter: RoomData(id="collision_camera_012"),
        Area4Mines.GreenCrystalDugout: RoomData(id="collision_camera_013"),
        Area4Mines.GemstoneGorge: RoomData(id="collision_camera_014"),
        Area4Mines.Gamma2: RoomData(id="collision_camera_015"),
        Area4Mines.BasaltBasin: RoomData(id="collision_camera_017"),
        Area4Mines.SpaceJump: RoomData(id="collision_camera_AfterChase"),
        Area4Mines.DiggernautExcavationTunnels: RoomData(id="collision_camera_AfterChase_001"),
    },
)
