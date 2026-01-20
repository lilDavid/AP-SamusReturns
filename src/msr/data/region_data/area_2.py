from ..internal_names import AreaId
from ..room_names import Area2Entryway, Area2Exterior, Area2Interior
from . import AreaData, RoomData

area_2_exterior_data = AreaData(
    name="Area 2 Dam Exterior",
    id=AreaId.AREA_2_EXTERIOR,
    rooms={
        Area2Exterior.DamExterior: RoomData(id="collision_camera_005"),
        Area2Exterior.Arachnus: RoomData(id="collision_camera_006"),
        Area2Exterior.FanFunnel: RoomData(id="collision_camera_007"),
        Area2Exterior.CritterPlayground: RoomData(id="collision_camera_008"),
        Area2Exterior.CavernsEntrance: RoomData(id="collision_camera_023"),
        Area2Exterior.SpikeRavine: RoomData(id="collision_camera_024"),
        Area2Exterior.AmmoRechargeAccess: RoomData(id="collision_camera_025"),
        Area2Exterior.CavernsMaze: RoomData(id="collision_camera_026"),
        Area2Exterior.CavernsSaveStation: RoomData(id="collision_camera_027"),
        Area2Exterior.CavernsAlphaNw: RoomData(id="collision_camera_028"),
        Area2Exterior.CavernsLobby: RoomData(id="collision_camera_029"),
        Area2Exterior.CavernsAlphaSw: RoomData(id="collision_camera_030"),
        Area2Exterior.CavernsAlphaEAccess: RoomData(id="collision_camera_031"),
        Area2Exterior.CavernsTeleporter: RoomData(id="collision_camera_032"),
        Area2Exterior.ExteriorAlpha2: RoomData(id="collision_camera_033"),
        Area2Exterior.SereneShelter: RoomData(id="collision_camera_034"),
        Area2Exterior.CavernsAlpha2: RoomData(id="collision_camera_035"),
        Area2Exterior.InnerAlpha: RoomData(id="collision_camera_036"),
        Area2Exterior.RockIcicleCorridor: RoomData(id="collision_camera_037"),
        Area2Exterior.MaintenanceTunnel: RoomData(id="collision_camera_038"),
        Area2Exterior.CavernsAmmoRecharge: RoomData(id="collision_camera_039"),
        Area2Exterior.CavernsAlphaE: RoomData(id="collision_camera_040"),
    },
)

area_2_interior_data = AreaData(
    name="Area 2 Dam Interior",
    id=AreaId.AREA_2_INTERIOR,
    rooms={
        Area2Interior.WaveBeam: RoomData(id="collision_camera_009"),
        Area2Interior.InteriorIntersection: RoomData(id="collision_camera_011"),
        Area2Interior.LavaGenerator: RoomData(id="collision_camera_012"),
        Area2Interior.CrumbleCavern: RoomData(id="collision_camera_013"),
        Area2Interior.WhimsicalWaterwhieels: RoomData(id="collision_camera_015"),
        Area2Interior.InteriorTeleporter: RoomData(id="collision_camera_016"),
        Area2Interior.FleechFireContainment: RoomData(id="collision_camera_017"),
        Area2Interior.DamBasement: RoomData(id="collision_camera_018"),
        Area2Interior.GulluggHideout: RoomData(id="collision_camera_019"),
        Area2Interior.HighJumpBoots: RoomData(id="collision_camera_021"),
        Area2Interior.HighJumpBootsAccess: RoomData(id="collision_camera_022"),
        Area2Interior.WallfireCorridor: RoomData(id="collision_camera_035"),
        Area2Interior.TeleporterStorage: RoomData(id="collision_camera_036"),
        Area2Interior.Gamma: RoomData(id="collision_camera_037"),
        Area2Interior.VariaSuit: RoomData(id="collision_camera_040"),
        Area2Interior.GeneratorAccess: RoomData(id="collision_camera_041"),
    },
)

area_2_entryway_data = AreaData(
    name="Area 2 Dam Entryway",
    id=AreaId.AREA_2_ENTRYWAY,
    rooms={
        Area2Entryway.TransportAreas1And3: RoomData(id="collision_camera"),
        Area2Entryway.EntrywayTeleporter: RoomData(id="collision_camera_003"),
        Area2Entryway.LightningArmor: RoomData(id="collision_camera_004"),
        Area2Entryway.TransportAccess: RoomData(id="collision_camera_005"),
        Area2Entryway.FleechSwarmFloodway: RoomData(id="collision_camera_006"),
        Area2Entryway.Alpha2: RoomData(id="collision_camera_007"),
    },
)
