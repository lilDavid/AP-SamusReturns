from typing import NamedTuple

from BaseClasses import Location

from .data.constants import GAME_NAME
from .data.internal_names import AreaId
from .data.room_names import (
    Area1,
    Area2Entryway,
    Area2Exterior,
    Area2Interior,
    Area3Caverns,
    Area3Exterior,
    Area3Interior,
    Area4Caves,
    Area4Mines,
    Area5Exterior,
    Area5Interior,
    Area5Lobby,
    Area6,
    Area7,
    Area8,
    RoomName,
    SurfaceEast,
    SurfaceWest,
)


class SamusReturnsLocation(Location):
    game = GAME_NAME


def make_name(room: RoomName, location: str | None = None):
    if location is None:
        return room.with_area()
    return f"{room.with_area()} - {location}"


class ActorLocationData(NamedTuple):
    ap_id: int
    scenario: AreaId
    actor: str

    def internal_name(self):
        return self.actor

    def to_pickup(self):
        return {
            "pickup_type": "actor",
            "pickup_actor": {
                "scenario": self.scenario,
                "actor": self.actor,
            },
        }


class MetroidLocationData(NamedTuple):
    ap_id: int
    scenario: AreaId
    spawngroup: str

    def internal_name(self):
        return self.spawngroup

    def to_pickup(self):
        return {
            "pickup_type": "metroid",
            "metroid_callback": {
                "scenario": self.scenario,
                "spawngroup": self.spawngroup,
            },
        }


LocationData = ActorLocationData | MetroidLocationData


location_table: dict[str, LocationData] = {
    # Surface - east
    make_name(SurfaceEast.TwistyTunnel): ActorLocationData(1, AreaId.SURFACE_EAST, "LE_Item_006"),
    make_name(SurfaceEast.MorphBall): ActorLocationData(2, AreaId.SURFACE_EAST, "LE_PowerUP_Morphball"),
    make_name(SurfaceEast.ChozoSeal): ActorLocationData(3, AreaId.SURFACE_EAST, "LE_Item_005"),
    make_name(SurfaceEast.TransportArea1): ActorLocationData(4, AreaId.SURFACE_EAST, "LE_Item_004"),
    make_name(SurfaceEast.ChozoCacheE): ActorLocationData(5, AreaId.SURFACE_EAST, "LE_Item_007"),
    make_name(SurfaceEast.ChargeBeam): ActorLocationData(6, AreaId.SURFACE_EAST, "LE_PowerUP_ChargeBeam"),
    make_name(SurfaceEast.Alpha, "Missile"): ActorLocationData(7, AreaId.SURFACE_EAST, "LE_Item_001"),
    make_name(SurfaceEast.Alpha, "Alpha Metroid"): MetroidLocationData(8, AreaId.SURFACE_EAST, "SG_Alpha_001"),
    make_name(SurfaceEast.ScanPulse): ActorLocationData(9, AreaId.SURFACE_EAST, "LE_SpecialAbility_ScanningPulse"),
    make_name(SurfaceEast.ChozoCacheW): ActorLocationData(10, AreaId.SURFACE_EAST, "LE_Item_008"),
    make_name(SurfaceEast.ChargeBeamAccess): ActorLocationData(11, AreaId.SURFACE_EAST, "LE_Item_010"),
    make_name(SurfaceEast.SurfaceStash): ActorLocationData(12, AreaId.SURFACE_EAST, "LE_Item_002"),
    make_name(SurfaceEast.SurfaceCrumbleChallenge): ActorLocationData(13, AreaId.SURFACE_EAST, "LE_Item_003"),
    make_name(SurfaceEast.TransportCache): ActorLocationData(14, AreaId.SURFACE_EAST, "LE_Item_012"),
    make_name(SurfaceEast.CavernAlcove): ActorLocationData(15, AreaId.SURFACE_EAST, "LE_Item_011"),
    make_name(SurfaceEast.EnergyRechargeShaft): ActorLocationData(16, AreaId.SURFACE_EAST, "HiddenPowerup001"),
    # Surface - west
    make_name(SurfaceWest.TransportArea8, "Left"): ActorLocationData(17, AreaId.SURFACE_WEST, "LE_Item_013"),
    make_name(SurfaceWest.TransportArea8, "Right"): ActorLocationData(18, AreaId.SURFACE_WEST, "HiddenPowerup002"),
    # Area 1
    make_name(Area1.Bomb, "Missile"): ActorLocationData(101, AreaId.AREA_1, "LE_Item_005"),
    make_name(Area1.Bomb, "Statue"): ActorLocationData(102, AreaId.AREA_1, "LE_PowerUp_Bomb"),
    make_name(Area1.DestroyedArmory): ActorLocationData(103, AreaId.AREA_1, "LE_Item_011"),
    make_name(Area1.SpiderBall, "Tunnel"): ActorLocationData(104, AreaId.AREA_1, "LE_Item_013"),
    make_name(Area1.SpiderBall, "Buried Item"): ActorLocationData(105, AreaId.AREA_1, "LE_PowerUp_SpiderBall"),
    make_name(Area1.ExteriorAlpha, "Above Arena"): ActorLocationData(106, AreaId.AREA_1, "LE_Item_008"),
    make_name(Area1.ExteriorAlpha, "Alpha Metroid"): MetroidLocationData(107, AreaId.AREA_1, "SG_Alpha_004"),
    make_name(Area1.TempleExterior, "Crevice"): ActorLocationData(108, AreaId.AREA_1, "LE_Item_014"),
    make_name(Area1.TempleExterior, "Ceiling"): ActorLocationData(109, AreaId.AREA_1, "LE_Item_017"),
    make_name(Area1.TempleExterior, "Hidden"): ActorLocationData(110, AreaId.AREA_1, "HiddenPowerup001"),
    make_name(Area1.CavernsAlphaSe): MetroidLocationData(111, AreaId.AREA_1, "SG_Alpha_002"),
    make_name(Area1.CavernsAlphaNe): MetroidLocationData(112, AreaId.AREA_1, "SG_Alpha_003"),
    make_name(Area1.WaterMaze): ActorLocationData(113, AreaId.AREA_1, "LE_Item_004"),
    make_name(Area1.IceBeam, "Statue"): ActorLocationData(114, AreaId.AREA_1, "LE_PowerUp_IceBeam"),
    make_name(Area1.IceBeam, "Crystals"): ActorLocationData(115, AreaId.AREA_1, "HiddenPowerup003"),
    make_name(Area1.MagmaPool, "Alcove"): ActorLocationData(116, AreaId.AREA_1, "LE_Item_001"),
    make_name(Area1.MagmaPool, "Magma"): ActorLocationData(117, AreaId.AREA_1, "HiddenPowerup002"),
    make_name(Area1.CavernsSaveStation): ActorLocationData(118, AreaId.AREA_1, "LE_Item_006"),
    make_name(Area1.InnerTempleVentShaft): ActorLocationData(119, AreaId.AREA_1, "LE_Item_016"),
    make_name(Area1.TransportCache): ActorLocationData(120, AreaId.AREA_1, "LE_Item_003"),
    make_name(Area1.CavernsAlphaSw): MetroidLocationData(121, AreaId.AREA_1, "SG_Alpha_001"),
    # Area 2 - dam exterior
    make_name(Area2Exterior.DamExterior): ActorLocationData(201, AreaId.AREA_2_EXTERIOR, "LE_Item_004"),
    make_name(Area2Exterior.Arachnus): ActorLocationData(202, AreaId.AREA_2_EXTERIOR, "LE_PowerUp_Springball"),
    make_name(Area2Exterior.CritterPlayground): ActorLocationData(203, AreaId.AREA_2_EXTERIOR, "LE_Item_005"),
    make_name(Area2Exterior.CavernsEntrance): ActorLocationData(204, AreaId.AREA_2_EXTERIOR, "HiddenPowerup002"),
    make_name(Area2Exterior.SpikeRavine): ActorLocationData(205, AreaId.AREA_2_EXTERIOR, "LE_Item_001"),
    make_name(Area2Exterior.CavernsMaze): ActorLocationData(206, AreaId.AREA_2_EXTERIOR, "LE_Item_006"),
    make_name(Area2Exterior.CavernsAlphaNw): MetroidLocationData(207, AreaId.AREA_2_EXTERIOR, "SG_Alpha_003"),
    make_name(Area2Exterior.CavernsAlphaSw): MetroidLocationData(208, AreaId.AREA_2_EXTERIOR, "SG_Alpha_004"),
    make_name(Area2Exterior.CavernsTeleporter): ActorLocationData(209, AreaId.AREA_2_EXTERIOR, "HiddenPowerup001"),
    make_name(Area2Exterior.ExteriorAlpha2): MetroidLocationData(210, AreaId.AREA_2_EXTERIOR, "SG_Alpha_001"),
    make_name(Area2Exterior.SereneShelter): ActorLocationData(211, AreaId.AREA_2_EXTERIOR, "LE_Item_003"),
    make_name(Area2Exterior.CavernsAlpha2): MetroidLocationData(212, AreaId.AREA_2_EXTERIOR, "SG_Alpha_005"),
    make_name(Area2Exterior.InnerAlpha): MetroidLocationData(213, AreaId.AREA_2_EXTERIOR, "SG_Alpha_006"),
    make_name(Area2Exterior.CavernsAlphaE): MetroidLocationData(214, AreaId.AREA_2_EXTERIOR, "SG_Alpha_007"),
    # Area 2 - dam interior
    make_name(Area2Interior.WaveBeam): ActorLocationData(215, AreaId.AREA_2_INTERIOR, "LE_PowerUp_WaveBeam"),
    make_name(Area2Interior.LavaGenerator): ActorLocationData(216, AreaId.AREA_2_INTERIOR, "HP_Item_001"),
    make_name(Area2Interior.CrumbleCavern): ActorLocationData(217, AreaId.AREA_2_INTERIOR, "LE_Item_006"),
    make_name(Area2Interior.DamBasement, "Lower"): ActorLocationData(218, AreaId.AREA_2_INTERIOR, "LE_Item_001"),
    make_name(Area2Interior.DamBasement, "Upper"): ActorLocationData(219, AreaId.AREA_2_INTERIOR, "LE_Item_002"),
    make_name(Area2Interior.HighJumpBoots): ActorLocationData(220, AreaId.AREA_2_INTERIOR, "LE_PowerUp_HighJumpBoots"),
    make_name(Area2Interior.TeleporterStorage): ActorLocationData(221, AreaId.AREA_2_INTERIOR, "LE_Item_005"),
    make_name(Area2Interior.Gamma): MetroidLocationData(222, AreaId.AREA_2_INTERIOR, "SG_Gamma_001"),
    make_name(Area2Interior.VariaSuit, "Statue"): ActorLocationData(
        223, AreaId.AREA_2_INTERIOR, "LE_PowerUp_VariaSuite"
    ),
    make_name(Area2Interior.VariaSuit, "Tunnel"): ActorLocationData(224, AreaId.AREA_2_INTERIOR, "HP_Item_002"),
    # Area 2 - dam entryway
    make_name(Area2Entryway.TransportAreas1And3, "Plants"): ActorLocationData(
        225, AreaId.AREA_2_ENTRYWAY, "LE_Item_005"
    ),
    make_name(Area2Entryway.TransportAreas1And3, "Tunnel"): ActorLocationData(
        226, AreaId.AREA_2_ENTRYWAY, "HiddenPowerup001"
    ),
    make_name(Area2Entryway.EntrywayTeleporter): ActorLocationData(227, AreaId.AREA_2_ENTRYWAY, "LE_Item_003"),
    make_name(Area2Entryway.LightningArmor, "Tutorial"): ActorLocationData(228, AreaId.AREA_2_ENTRYWAY, "LE_Item_002"),
    make_name(Area2Entryway.LightningArmor, "Artifact"): ActorLocationData(
        229, AreaId.AREA_2_ENTRYWAY, "LE_SpecialAbility_EnergyShield"
    ),
    make_name(Area2Entryway.FleechSwarmFloodway): ActorLocationData(230, AreaId.AREA_2_ENTRYWAY, "LE_Item_001"),
    make_name(Area2Entryway.Alpha2): MetroidLocationData(231, AreaId.AREA_2_ENTRYWAY, "SG_Alpha_002"),
    # Area 3 - factory exterior
    make_name(Area3Exterior.ExteriorMaze): ActorLocationData(301, AreaId.AREA_3_EXTERIOR, "LE_Item_004"),
    make_name(Area3Exterior.GrappleBeam): ActorLocationData(302, AreaId.AREA_3_EXTERIOR, "LE_PowerUp_GrappleBeam"),
    make_name(Area3Exterior.FactoryExt, "Ceiling"): ActorLocationData(303, AreaId.AREA_3_EXTERIOR, "LE_Item_003"),
    make_name(Area3Exterior.FactoryExt, "Shaft"): ActorLocationData(304, AreaId.AREA_3_EXTERIOR, "LE_Item_005"),
    make_name(Area3Exterior.TransportCavernsW): ActorLocationData(305, AreaId.AREA_3_EXTERIOR, "HP_ChozoHologram_002"),
    make_name(Area3Exterior.TransportArea4): ActorLocationData(306, AreaId.AREA_3_EXTERIOR, "LE_Item_002"),
    make_name(Area3Exterior.EntranceMaze): ActorLocationData(307, AreaId.AREA_3_EXTERIOR, "LE_Item_001"),
    make_name(Area3Exterior.BeamBurst): ActorLocationData(308, AreaId.AREA_3_EXTERIOR, "LE_SpecialAbility_EnergyWave"),
    make_name(Area3Exterior.HalzynHangout, "Top"): ActorLocationData(309, AreaId.AREA_3_EXTERIOR, "HiddenPowerup001"),
    make_name(Area3Exterior.HalzynHangout, "Bottom"): ActorLocationData(
        310, AreaId.AREA_3_EXTERIOR, "HiddenPowerup002"
    ),
    make_name(Area3Exterior.Gamma, "Bottom"): MetroidLocationData(311, AreaId.AREA_3_EXTERIOR, "SG_Gamma_005_C"),
    # Area 3 - Metroid caverns
    make_name(Area3Caverns.TransportFactoryExtN): ActorLocationData(312, AreaId.AREA_3_CAVERNS, "HiddenPowerup001"),
    make_name(Area3Caverns.Alpha2W): MetroidLocationData(313, AreaId.AREA_3_CAVERNS, "SG_Alpha_002"),
    make_name(Area3Caverns.GammaC): MetroidLocationData(314, AreaId.AREA_3_CAVERNS, "SG_Gamma_001"),
    make_name(Area3Caverns.GammaS, "Tunnels"): ActorLocationData(315, AreaId.AREA_3_CAVERNS, "LE_Item_001"),
    make_name(Area3Caverns.GammaS, "Gamma Metroid"): MetroidLocationData(316, AreaId.AREA_3_CAVERNS, "SG_Gamma_001"),
    make_name(Area3Caverns.GravittGarden): ActorLocationData(317, AreaId.AREA_3_CAVERNS, "HiddenPowerup002"),
    make_name(Area3Caverns.AscendingAlleyway): ActorLocationData(318, AreaId.AREA_3_CAVERNS, "LE_Item_007"),
    make_name(Area3Caverns.RamulkenRollway): ActorLocationData(319, AreaId.AREA_3_CAVERNS, "LE_Item_002"),
    make_name(Area3Caverns.CavernsTeleporterE): ActorLocationData(320, AreaId.AREA_3_CAVERNS, "LE_Item_003"),
    make_name(Area3Caverns.QuarryShaft): ActorLocationData(321, AreaId.AREA_3_CAVERNS, "LE_Item_004"),
    make_name(Area3Caverns.TransportFactoryIntS): ActorLocationData(322, AreaId.AREA_3_CAVERNS, "HiddenPowerup003"),
    make_name(Area3Caverns.Gamma2S): MetroidLocationData(323, AreaId.AREA_3_CAVERNS, "SG_Gamma_004_B"),
    make_name(Area3Caverns.Gamma2N): MetroidLocationData(324, AreaId.AREA_3_CAVERNS, "SG_Gamma_003"),
    make_name(Area3Caverns.Alpha2N): MetroidLocationData(325, AreaId.AREA_3_CAVERNS, "SG_Alpha_003"),
    # Area 3 - factory interior
    make_name(Area3Interior.SecuritySite): ActorLocationData(326, AreaId.AREA_3_INTERIOR, "LE_Item_006"),
    make_name(Area3Interior.ParabyPeriphery): ActorLocationData(327, AreaId.AREA_3_INTERIOR, "LE_Item_004"),
    make_name(Area3Interior.FanControl): ActorLocationData(328, AreaId.AREA_3_INTERIOR, "LE_Item_002"),
    make_name(Area3Interior.FactoryIntersection): ActorLocationData(329, AreaId.AREA_3_INTERIOR, "LE_Item_001"),
    make_name(Area3Interior.GammaTransportCavernsE): MetroidLocationData(330, AreaId.AREA_3_INTERIOR, "SG_Gamma_006"),
    make_name(Area3Interior.Alpha, "Lava"): ActorLocationData(331, AreaId.AREA_3_INTERIOR, "HiddenPowerup001"),
    make_name(Area3Interior.Alpha, "Alpha Metroid"): MetroidLocationData(332, AreaId.AREA_3_INTERIOR, "SG_Alpha_001"),
    make_name(Area3Interior.GammaS): MetroidLocationData(333, AreaId.AREA_3_INTERIOR, "SG_Gamma_007_A"),
    # Area 4 - caves
    make_name(Area4Caves.CavesIntersectionTerminal): ActorLocationData(401, AreaId.AREA_4_CAVES, "LE_Item_007"),
    make_name(Area4Caves.SpazerBeam): ActorLocationData(402, AreaId.AREA_4_CAVES, "LE_PowerUp_SpazerBeam"),
    make_name(Area4Caves.CrumbleCatwalk): ActorLocationData(403, AreaId.AREA_4_CAVES, "LE_Item_006"),
    make_name(Area4Caves.TransportArea3Mines): ActorLocationData(404, AreaId.AREA_4_CAVES, "LE_Item_002"),
    make_name(Area4Caves.Alpha2, "Missile"): ActorLocationData(405, AreaId.AREA_4_CAVES, "LE_Item_003"),
    make_name(Area4Caves.Alpha2, "Evolved Alpha Metroid"): MetroidLocationData(
        406, AreaId.AREA_4_CAVES, "SG_Alpha_001"
    ),
    make_name(Area4Caves.TransitTunnel): ActorLocationData(407, AreaId.AREA_4_CAVES, "HiddenPowerup004"),
    make_name(Area4Caves.FleechSwarmCave): ActorLocationData(408, AreaId.AREA_4_CAVES, "LE_Item_005"),
    make_name(Area4Caves.Gamma, "Tunnel"): ActorLocationData(409, AreaId.AREA_4_CAVES, "HP_ChozoHologram_002"),
    make_name(Area4Caves.Gamma, "Gamma Metroid"): MetroidLocationData(410, AreaId.AREA_4_CAVES, "SG_Gamma_001_A"),
    make_name(Area4Caves.GammaAccessS): ActorLocationData(411, AreaId.AREA_4_CAVES, "LE_Item_008"),
    make_name(Area4Caves.AmethystAltars): ActorLocationData(412, AreaId.AREA_4_CAVES, "HiddenPowerup001"),
    make_name(Area4Caves.TransportArea5): ActorLocationData(413, AreaId.AREA_4_CAVES, "HiddenPowerup003"),
    # Area 4 - crystal mines
    make_name(Area4Mines.MinesIntersectionTunnel, "Top"): ActorLocationData(414, AreaId.AREA_4_MINES, "LE_Item_009"),
    make_name(Area4Mines.MinesIntersectionTunnel, "Bottom"): ActorLocationData(
        415, AreaId.AREA_4_MINES, "HiddenPowerup002"
    ),
    make_name(Area4Mines.SuperMissile): ActorLocationData(416, AreaId.AREA_4_MINES, "LE_PoweUp_SuperMissile"),
    make_name(Area4Mines.PinkCrystalPreserve): ActorLocationData(417, AreaId.AREA_4_MINES, "LE_Item_012"),
    make_name(Area4Mines.LavaReservoir): ActorLocationData(418, AreaId.AREA_4_MINES, "LE_Item_013"),
    make_name(Area4Mines.DualPondAlcove): ActorLocationData(419, AreaId.AREA_4_MINES, "LE_Item_005"),
    make_name(Area4Mines.Zeta): MetroidLocationData(420, AreaId.AREA_4_MINES, "SG_Zeta_001"),
    make_name(Area4Mines.GawronGroove): ActorLocationData(421, AreaId.AREA_4_MINES, "HiddenPowerup001"),
    make_name(Area4Mines.GemstoneGorge): ActorLocationData(422, AreaId.AREA_4_MINES, "LE_Item_006"),
    make_name(Area4Mines.Gamma2): MetroidLocationData(423, AreaId.AREA_4_MINES, "SG_Gamma_002_A"),
    make_name(Area4Mines.SpaceJump): ActorLocationData(424, AreaId.AREA_4_MINES, "LE_PowerUp_SpaceJump"),
    make_name(Area4Mines.DiggernautExcavationTunnels, "Crystals"): ActorLocationData(
        425, AreaId.AREA_4_MINES, "LE_Item_002"
    ),
    make_name(Area4Mines.DiggernautExcavationTunnels, "Plants"): ActorLocationData(
        426, AreaId.AREA_4_MINES, "LE_Item_003"
    ),
    make_name(Area4Mines.DiggernautExcavationTunnels, "Puzzle"): ActorLocationData(
        427, AreaId.AREA_4_MINES, "LE_Item_004"
    ),
    make_name(Area4Mines.DiggernautExcavationTunnels, "Floor"): ActorLocationData(
        428, AreaId.AREA_4_MINES, "LE_Item_010"
    ),
    # Area 5 - tower lobby
    make_name(Area5Lobby.TransportAreas4And6, "Left"): ActorLocationData(501, AreaId.AREA_5_LOBBY, "LE_Item_002"),
    make_name(Area5Lobby.TransportAreas4And6, "Right"): ActorLocationData(502, AreaId.AREA_5_LOBBY, "HiddenPowerup002"),
    make_name(Area5Lobby.LobbyTeleporterW, "Lower"): ActorLocationData(503, AreaId.AREA_5_LOBBY, "LE_Item_006"),
    make_name(Area5Lobby.LobbyTeleporterW, "Upper"): ActorLocationData(504, AreaId.AREA_5_LOBBY, "LE_Item_007"),
    make_name(Area5Lobby.LobbyTeleporterE): ActorLocationData(505, AreaId.AREA_5_LOBBY, "LE_Item_003"),
    make_name(Area5Lobby.Alpha2): MetroidLocationData(506, AreaId.AREA_5_LOBBY, "SG_Alpha_001"),
    make_name(Area5Lobby.PhaseDrift, "Artifact"): ActorLocationData(
        507, AreaId.AREA_5_LOBBY, "LE_SpecialAbility_PhaseDisplacement"
    ),
    make_name(Area5Lobby.PhaseDrift, "Pitfall Blocks"): ActorLocationData(508, AreaId.AREA_5_LOBBY, "HiddenPowerup001"),
    make_name(Area5Lobby.MeboidMillpond): ActorLocationData(509, AreaId.AREA_5_LOBBY, "LE_Item_004"),
    make_name(Area5Lobby.Gamma2): MetroidLocationData(510, AreaId.AREA_5_LOBBY, "SG_Gamma_004"),
    # Area 5 - tower exterior
    make_name(Area5Exterior.TowerExt, "Alcove"): ActorLocationData(511, AreaId.AREA_5_EXTERIOR, "LE_Item_006"),
    make_name(Area5Exterior.TowerExt, "Crevice"): ActorLocationData(512, AreaId.AREA_5_EXTERIOR, "HiddenPowerup001"),
    make_name(Area5Exterior.TowerExt, "Puzzle"): ActorLocationData(513, AreaId.AREA_5_EXTERIOR, "LE_Item_005"),
    make_name(Area5Exterior.TowerExt, "Ceiling"): ActorLocationData(514, AreaId.AREA_5_EXTERIOR, "LE_Item_002"),
    make_name(Area5Exterior.OvergrownMaze, "Right"): ActorLocationData(515, AreaId.AREA_5_EXTERIOR, "LE_Item_001"),
    make_name(Area5Exterior.OvergrownMaze, "Left"): ActorLocationData(516, AreaId.AREA_5_EXTERIOR, "LE_Item_007"),
    make_name(Area5Exterior.ScrewAttack): ActorLocationData(517, AreaId.AREA_5_EXTERIOR, "LE_PowerUp_ScrewAttack"),
    make_name(Area5Exterior.RedPlantMaze): ActorLocationData(518, AreaId.AREA_5_EXTERIOR, "LE_Item_003"),
    make_name(Area5Exterior.Zeta): MetroidLocationData(519, AreaId.AREA_5_EXTERIOR, "SG_Zeta_001"),
    make_name(Area5Exterior.Gamma2): MetroidLocationData(520, AreaId.AREA_5_EXTERIOR, "SG_Gamma_002"),
    make_name(Area5Exterior.Gamma, "Gamma Metroid"): MetroidLocationData(521, AreaId.AREA_5_EXTERIOR, "SG_Gamma_003"),
    make_name(Area5Exterior.Gamma, "Maze"): ActorLocationData(522, AreaId.AREA_5_EXTERIOR, "LE_Item_004"),
    # Area 5 - tower interior
    make_name(Area5Interior.InteriorSaveStation): ActorLocationData(523, AreaId.AREA_5_INTERIOR, "LE_Item_004"),
    make_name(Area5Interior.PlasmaBeam): ActorLocationData(524, AreaId.AREA_5_INTERIOR, "LE_PowerUp_PlasmaBeam"),
    make_name(Area5Interior.GrappleShuffler): ActorLocationData(525, AreaId.AREA_5_INTERIOR, "HiddenPowerup002"),
    make_name(Area5Interior.GravitySuit): ActorLocationData(526, AreaId.AREA_5_INTERIOR, "LE_PowerUp_GravitySuite"),
    make_name(Area5Interior.PhaseDriftTrialReward): ActorLocationData(527, AreaId.AREA_5_INTERIOR, "LE_Item_001"),
    make_name(Area5Interior.PhaseDriftTrialW, "Lower"): ActorLocationData(
        528, AreaId.AREA_5_INTERIOR, "HiddenPowerup003"
    ),
    make_name(Area5Interior.PhaseDriftTrialW, "Upper"): ActorLocationData(529, AreaId.AREA_5_INTERIOR, "LE_Item_002"),
    make_name(Area5Interior.Zeta2Access): ActorLocationData(530, AreaId.AREA_5_INTERIOR, "LE_Item_005"),
    make_name(Area5Interior.GravitySuitAccess): ActorLocationData(531, AreaId.AREA_5_INTERIOR, "HP_ChozoHologram_001"),
    make_name(Area5Interior.Gamma2): MetroidLocationData(532, AreaId.AREA_5_INTERIOR, "SG_Gamma_001"),
    make_name(Area5Interior.InteriorTeleporter): ActorLocationData(533, AreaId.AREA_5_INTERIOR, "LE_Item_003"),
    make_name(Area5Interior.Zeta2): MetroidLocationData(534, AreaId.AREA_5_INTERIOR, "SG_Zeta_002"),
    # Area 6
    make_name(Area6.TransportArea7): ActorLocationData(601, AreaId.AREA_6, "LE_Item_014"),
    make_name(Area6.Omega): MetroidLocationData(602, AreaId.AREA_6, "SG_Omega_001"),
    make_name(Area6.HideoutSprawl, "Right"): ActorLocationData(603, AreaId.AREA_6, "LE_Item_008"),
    make_name(Area6.HideoutSprawl, "Left"): ActorLocationData(604, AreaId.AREA_6, "LE_Item_012"),
    make_name(Area6.CrumblingBridge, "Pit"): ActorLocationData(605, AreaId.AREA_6, "LE_Item_011"),
    make_name(Area6.CrumblingBridge, "Tunnel"): ActorLocationData(606, AreaId.AREA_6, "LE_Item_009"),
    make_name(Area6.CrumblingStairwell): ActorLocationData(607, AreaId.AREA_6, "LE_Item_015"),
    make_name(Area6.Diggernaut): ActorLocationData(608, AreaId.AREA_6, "LE_PowerUp_Powerbomb"),
    make_name(Area6.ElectricEscalade): ActorLocationData(609, AreaId.AREA_6, "LE_Item_004"),
    make_name(Area6.PoisonousTunnel): ActorLocationData(610, AreaId.AREA_6, "LE_Item_001"),
    make_name(Area6.Zeta): MetroidLocationData(611, AreaId.AREA_6, "SG_Zeta_001"),
    make_name(Area6.ChozoSealE): ActorLocationData(612, AreaId.AREA_6, "LE_Item_010"),
    make_name(Area6.ChozoSealW, "Ceiling"): ActorLocationData(613, AreaId.AREA_6, "LE_Item_002"),
    make_name(Area6.ChozoSealW, "Tunnel"): ActorLocationData(614, AreaId.AREA_6, "LE_Item_007"),
    make_name(Area6.ChozoSealW, "Bottom"): ActorLocationData(615, AreaId.AREA_6, "LE_Item_013"),
    # Area 7
    make_name(Area7.LabTeleporterW): ActorLocationData(701, AreaId.AREA_7, "LE_Item_008"),
    make_name(Area7.SpiderBoostTunnelS): ActorLocationData(702, AreaId.AREA_7, "LE_Item_003"),
    make_name(Area7.Omega2): MetroidLocationData(703, AreaId.AREA_7, "SG_Omega_002"),
    make_name(Area7.RobotRegime, "Lower"): ActorLocationData(704, AreaId.AREA_7, "LE_Item_013"),
    make_name(Area7.RobotRegime, "Upper"): ActorLocationData(705, AreaId.AREA_7, "LE_Item_001"),
    make_name(Area7.TransportArea6, "Crystals"): ActorLocationData(706, AreaId.AREA_7, "LE_Item_010"),
    make_name(Area7.TransportArea6, "Alcove"): ActorLocationData(707, AreaId.AREA_7, "HiddenPowerup003"),
    make_name(Area7.TransportArea6, "Pitfall Blocks"): ActorLocationData(708, AreaId.AREA_7, "LE_Item_002"),
    make_name(Area7.TransportArea6, "Tunnel"): ActorLocationData(709, AreaId.AREA_7, "HiddenPowerup001"),
    make_name(Area7.OmegaSAccess): ActorLocationData(710, AreaId.AREA_7, "LE_Item_009"),
    make_name(Area7.OmegaS): MetroidLocationData(711, AreaId.AREA_7, "SG_Omega_003"),
    make_name(Area7.OmegaN): MetroidLocationData(712, AreaId.AREA_7, "SG_Omega_001"),
    make_name(Area7.OmegaNAccess): ActorLocationData(713, AreaId.AREA_7, "LE_Item_004"),
    make_name(Area7.WallfireWorkstation): ActorLocationData(714, AreaId.AREA_7, "HiddenPowerup002"),
    make_name(Area7.GrapplePuzzleFoyer): ActorLocationData(715, AreaId.AREA_7, "LE_Item_011"),
    make_name(Area7.SpiderBoostTunnelN): ActorLocationData(716, AreaId.AREA_7, "LE_Item_012"),
    # Area 8
    make_name(Area8.TransportSurface, "Left"): ActorLocationData(801, AreaId.AREA_8, "LE_Item_013"),
    make_name(Area8.TransportSurface, "Right"): ActorLocationData(802, AreaId.AREA_8, "LE_Item_014"),
    make_name(Area8.Amphitheater, "Spikes"): ActorLocationData(803, AreaId.AREA_8, "HiddenPowerup001"),
    make_name(Area8.Amphitheater, "Upper Left"): ActorLocationData(804, AreaId.AREA_8, "LE_Item_004"),
    make_name(Area8.Amphitheater, "Grapple Block"): ActorLocationData(805, AreaId.AREA_8, "LE_Item_003"),
    make_name(Area8.Amphitheater, "Upper Right"): ActorLocationData(806, AreaId.AREA_8, "LE_Item_012"),
    make_name(Area8.Amphitheater, "Maze"): ActorLocationData(807, AreaId.AREA_8, "LE_Item_005"),
    make_name(Area8.NestNetwork, "Crystals"): ActorLocationData(808, AreaId.AREA_8, "LE_Item_011"),
    make_name(Area8.NestNetwork, "Hallway"): ActorLocationData(809, AreaId.AREA_8, "LE_Item_008"),
    make_name(Area8.EntranceTeleporter): ActorLocationData(810, AreaId.AREA_8, "LE_Item_009"),
    make_name(Area8.NestNodule, "Tunnel"): ActorLocationData(811, AreaId.AREA_8, "LE_Item_010"),
    make_name(Area8.NestNodule, "Crystals"): ActorLocationData(812, AreaId.AREA_8, "LE_Item_001"),
    make_name(Area8.NestShaftW): ActorLocationData(813, AreaId.AREA_8, "HiddenPowerup002"),
    make_name(Area8.Hatchling): ActorLocationData(814, AreaId.AREA_8, "LE_Baby_Hatchling"),
    make_name(Area8.NestVestibule): ActorLocationData(815, AreaId.AREA_8, "LE_Item_007"),
}
