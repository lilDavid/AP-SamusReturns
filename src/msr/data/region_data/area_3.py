from ..internal_names import AreaId
from ..room_names import Area3Caverns, Area3Exterior, Area3Interior
from . import AreaData, RoomData

area_3_exterior_data = AreaData(
    name="Area 3 Factory Exterior",
    id=AreaId.AREA_3_EXTERIOR,
    rooms={
        Area3Exterior.TransportArea2: RoomData(id="collision_camera_002"),
        Area3Exterior.ExteriorMaze: RoomData(id="collision_camera_016"),
        Area3Exterior.GrappleBeam: RoomData(id="collision_camera_022"),
        Area3Exterior.FactoryExtTeleporter: RoomData(id="collision_camera_023"),
        Area3Exterior.FactoryExt: RoomData(id="collision_camera_030"),
        Area3Exterior.TransportCavernsW: RoomData(id="collision_camera_031"),
        Area3Exterior.TransportArea4: RoomData(id="collision_camera_032"),
        Area3Exterior.EntranceMaze: RoomData(id="collision_camera_033"),
        Area3Exterior.TransportCavernsN: RoomData(id="collision_camera_035"),
        Area3Exterior.BeamBurst: RoomData(id="collision_camera_036"),
        Area3Exterior.HalzynHangout: RoomData(id="collision_camera_037"),
        Area3Exterior.Gamma: RoomData(id="collision_camera_038"),
        Area3Exterior.NooksCranny: RoomData(id="collision_camera_039"),
        Area3Exterior.FactoryExtAccess: RoomData(id="collision_camera_040"),
    },
)

area_3_caverns_data = AreaData(
    name="Area 3 Metroid Caverns",
    id=AreaId.AREA_3_CAVERNS,
    rooms={
        Area3Caverns.TransportFactoryExtN: RoomData(id="collision_camera_006"),
        Area3Caverns.Alpha2W: RoomData(id="collision_camera_007"),
        Area3Caverns.GammaC: RoomData(id="collision_camera_008"),
        Area3Caverns.GammaS: RoomData(id="collision_camera_009"),
        Area3Caverns.SaveStationN: RoomData(id="collision_camera_010"),
        Area3Caverns.GravittGarden: RoomData(id="collision_camera_012"),
        Area3Caverns.AscendingAlleyway: RoomData(id="collision_camera_024"),
        Area3Caverns.RamulkenRollway: RoomData(id="collision_camera_025"),
        Area3Caverns.CavernsTeleporterE: RoomData(id="collision_camera_026"),
        Area3Caverns.QuarryShaft: RoomData(id="collision_camera_027"),
        Area3Caverns.LonelyLoop: RoomData(id="collision_camera_028"),
        Area3Caverns.QuarryTunnel: RoomData(id="collision_camera_031"),
        Area3Caverns.TransportFactoryIntS: RoomData(id="collision_camera_032"),
        Area3Caverns.Gamma2S: RoomData(id="collision_camera_033"),
        Area3Caverns.Gamma2SAccess: RoomData(id="collision_camera_034"),
        Area3Caverns.WaterfallCavern: RoomData(id="collision_camera_035"),
        Area3Caverns.Gamma2N: RoomData(id="collision_camera_036"),
        Area3Caverns.TransportFactoryExtW: RoomData(id="collision_camera_037"),
        Area3Caverns.Alpha2W: RoomData(id="collision_camera_038"),
        Area3Caverns.LetumShrine: RoomData(id="collision_camera_039"),
        Area3Caverns.CavernsTeleporterW: RoomData(id="collision_camera_040"),
    },
)

area_3_interior_data = AreaData(
    name="Area 3 Factory Interior",
    id=AreaId.AREA_3_INTERIOR,
    rooms={
        Area3Interior.SecuritySite: RoomData(id="collision_camera_011"),
        Area3Interior.GammaSAccess: RoomData(id="collision_camera_013"),
        Area3Interior.ParabyPeriphery: RoomData(id="collision_camera_014"),
        Area3Interior.FanControl: RoomData(id="collision_camera_015"),
        Area3Interior.GrappleCircuit: RoomData(id="collision_camera_017"),
        Area3Interior.FactoryIntersection: RoomData(id="collision_camera_018"),
        Area3Interior.FactoryIntTeleporter: RoomData(id="collision_camera_019"),
        Area3Interior.TransportFactoryExtE: RoomData(id="collision_camera_021"),
        Area3Interior.AlphaAccess: RoomData(id="collision_camera_022"),
        Area3Interior.GammaTransportCavernsE: RoomData(id="collision_camera_023"),
        Area3Interior.RamulkenResidence: RoomData(id="collision_camera_024"),
        Area3Interior.WallfireWatch: RoomData(id="collision_camera_025"),
        Area3Interior.Alpha: RoomData(id="collision_camera_026"),
        Area3Interior.GammaS: RoomData(id="collision_camera_027"),
        Area3Interior.DedicatedCallisoRoost: RoomData(id="collision_camera_028"),
        Area3Interior.FactoryTeleporterAccess: RoomData(id="collision_camera_029"),
        Area3Interior.GammaCAccess: RoomData(id="collision_camera_030"),
    },
)
