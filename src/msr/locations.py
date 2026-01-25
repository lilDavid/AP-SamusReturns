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
    SurfaceEast,
    SurfaceWest,
)


class SamusReturnsLocation(Location):
    game = GAME_NAME


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
    SurfaceEast.TwistyTunnel.location(): ActorLocationData(1, AreaId.SURFACE_EAST, "LE_Item_006"),
    SurfaceEast.MorphBall.location(): ActorLocationData(2, AreaId.SURFACE_EAST, "LE_PowerUP_Morphball"),
    SurfaceEast.ChozoSeal.location(): ActorLocationData(3, AreaId.SURFACE_EAST, "LE_Item_005"),
    SurfaceEast.TransportArea1.location(): ActorLocationData(4, AreaId.SURFACE_EAST, "LE_Item_004"),
    SurfaceEast.ChozoCacheE.location(): ActorLocationData(5, AreaId.SURFACE_EAST, "LE_Item_007"),
    SurfaceEast.ChargeBeam.location(): ActorLocationData(6, AreaId.SURFACE_EAST, "LE_PowerUP_ChargeBeam"),
    SurfaceEast.Alpha.location("Missile"): ActorLocationData(7, AreaId.SURFACE_EAST, "LE_Item_001"),
    SurfaceEast.Alpha.location("Alpha Metroid"): MetroidLocationData(8, AreaId.SURFACE_EAST, "SG_Alpha_001"),
    SurfaceEast.ScanPulse.location(): ActorLocationData(9, AreaId.SURFACE_EAST, "LE_SpecialAbility_ScanningPulse"),
    SurfaceEast.ChozoCacheW.location(): ActorLocationData(10, AreaId.SURFACE_EAST, "LE_Item_008"),
    SurfaceEast.ChargeBeamAccess.location(): ActorLocationData(11, AreaId.SURFACE_EAST, "LE_Item_010"),
    SurfaceEast.SurfaceStash.location(): ActorLocationData(12, AreaId.SURFACE_EAST, "LE_Item_002"),
    SurfaceEast.SurfaceCrumbleChallenge.location(): ActorLocationData(13, AreaId.SURFACE_EAST, "LE_Item_003"),
    SurfaceEast.TransportCache.location(): ActorLocationData(14, AreaId.SURFACE_EAST, "LE_Item_012"),
    SurfaceEast.CavernAlcove.location(): ActorLocationData(15, AreaId.SURFACE_EAST, "LE_Item_011"),
    SurfaceEast.EnergyRechargeShaft.location(): ActorLocationData(16, AreaId.SURFACE_EAST, "HiddenPowerup001"),
    # Surface - west
    SurfaceWest.TransportArea8.location("Left"): ActorLocationData(17, AreaId.SURFACE_WEST, "LE_Item_013"),
    SurfaceWest.TransportArea8.location("Right"): ActorLocationData(18, AreaId.SURFACE_WEST, "HiddenPowerup002"),
    # Area 1
    Area1.Bomb.location("Missile"): ActorLocationData(101, AreaId.AREA_1, "LE_Item_005"),
    Area1.Bomb.location("Statue"): ActorLocationData(102, AreaId.AREA_1, "LE_PowerUp_Bomb"),
    Area1.DestroyedArmory.location(): ActorLocationData(103, AreaId.AREA_1, "LE_Item_011"),
    Area1.SpiderBall.location("Tunnel"): ActorLocationData(104, AreaId.AREA_1, "LE_Item_013"),
    Area1.SpiderBall.location("Buried Item"): ActorLocationData(105, AreaId.AREA_1, "LE_PowerUp_SpiderBall"),
    Area1.ExteriorAlpha.location("Above Arena"): ActorLocationData(106, AreaId.AREA_1, "LE_Item_008"),
    Area1.ExteriorAlpha.location("Alpha Metroid"): MetroidLocationData(107, AreaId.AREA_1, "SG_Alpha_004"),
    Area1.TempleExterior.location("Crevice"): ActorLocationData(108, AreaId.AREA_1, "LE_Item_014"),
    Area1.TempleExterior.location("Ceiling"): ActorLocationData(109, AreaId.AREA_1, "LE_Item_017"),
    Area1.TempleExterior.location("Hidden"): ActorLocationData(110, AreaId.AREA_1, "HiddenPowerup001"),
    Area1.CavernsAlphaSe.location(): MetroidLocationData(111, AreaId.AREA_1, "SG_Alpha_002"),
    Area1.CavernsAlphaNe.location(): MetroidLocationData(112, AreaId.AREA_1, "SG_Alpha_003"),
    Area1.WaterMaze.location(): ActorLocationData(113, AreaId.AREA_1, "LE_Item_004"),
    Area1.IceBeam.location("Statue"): ActorLocationData(114, AreaId.AREA_1, "LE_PowerUp_IceBeam"),
    Area1.IceBeam.location("Crystals"): ActorLocationData(115, AreaId.AREA_1, "HiddenPowerup003"),
    Area1.MagmaPool.location("Alcove"): ActorLocationData(116, AreaId.AREA_1, "LE_Item_001"),
    Area1.MagmaPool.location("Magma"): ActorLocationData(117, AreaId.AREA_1, "HiddenPowerup002"),
    Area1.CavernsSaveStation.location(): ActorLocationData(118, AreaId.AREA_1, "LE_Item_006"),
    Area1.InnerTempleVentShaft.location(): ActorLocationData(119, AreaId.AREA_1, "LE_Item_016"),
    Area1.TransportCache.location(): ActorLocationData(120, AreaId.AREA_1, "LE_Item_003"),
    Area1.CavernsAlphaSw.location(): MetroidLocationData(121, AreaId.AREA_1, "SG_Alpha_001"),
    # Area 2 - dam exterior
    Area2Exterior.DamExterior.location(): ActorLocationData(201, AreaId.AREA_2_EXTERIOR, "LE_Item_004"),
    Area2Exterior.Arachnus.location(): ActorLocationData(202, AreaId.AREA_2_EXTERIOR, "LE_PowerUp_Springball"),
    Area2Exterior.CritterPlayground.location(): ActorLocationData(203, AreaId.AREA_2_EXTERIOR, "LE_Item_005"),
    Area2Exterior.CavernsEntrance.location(): ActorLocationData(204, AreaId.AREA_2_EXTERIOR, "HiddenPowerup002"),
    Area2Exterior.SpikeRavine.location(): ActorLocationData(205, AreaId.AREA_2_EXTERIOR, "LE_Item_001"),
    Area2Exterior.CavernsMaze.location(): ActorLocationData(206, AreaId.AREA_2_EXTERIOR, "LE_Item_006"),
    Area2Exterior.CavernsAlphaNw.location(): MetroidLocationData(207, AreaId.AREA_2_EXTERIOR, "SG_Alpha_003"),
    Area2Exterior.CavernsAlphaSw.location(): MetroidLocationData(208, AreaId.AREA_2_EXTERIOR, "SG_Alpha_004"),
    Area2Exterior.CavernsTeleporter.location(): ActorLocationData(209, AreaId.AREA_2_EXTERIOR, "HiddenPowerup001"),
    Area2Exterior.ExteriorAlpha2.location(): MetroidLocationData(210, AreaId.AREA_2_EXTERIOR, "SG_Alpha_001"),
    Area2Exterior.SereneShelter.location(): ActorLocationData(211, AreaId.AREA_2_EXTERIOR, "LE_Item_003"),
    Area2Exterior.CavernsAlpha2.location(): MetroidLocationData(212, AreaId.AREA_2_EXTERIOR, "SG_Alpha_005"),
    Area2Exterior.InnerAlpha.location(): MetroidLocationData(213, AreaId.AREA_2_EXTERIOR, "SG_Alpha_006"),
    Area2Exterior.CavernsAlphaE.location(): MetroidLocationData(214, AreaId.AREA_2_EXTERIOR, "SG_Alpha_007"),
    # Area 2 - dam interior
    Area2Interior.WaveBeam.location(): ActorLocationData(215, AreaId.AREA_2_INTERIOR, "LE_PowerUp_WaveBeam"),
    Area2Interior.LavaGenerator.location(): ActorLocationData(216, AreaId.AREA_2_INTERIOR, "HP_Item_001"),
    Area2Interior.CrumbleCavern.location(): ActorLocationData(217, AreaId.AREA_2_INTERIOR, "LE_Item_006"),
    Area2Interior.DamBasement.location("Lower"): ActorLocationData(218, AreaId.AREA_2_INTERIOR, "LE_Item_001"),
    Area2Interior.DamBasement.location("Upper"): ActorLocationData(219, AreaId.AREA_2_INTERIOR, "LE_Item_002"),
    Area2Interior.HighJumpBoots.location(): ActorLocationData(220, AreaId.AREA_2_INTERIOR, "LE_PowerUp_HighJumpBoots"),
    Area2Interior.TeleporterStorage.location(): ActorLocationData(221, AreaId.AREA_2_INTERIOR, "LE_Item_005"),
    Area2Interior.Gamma.location(): MetroidLocationData(222, AreaId.AREA_2_INTERIOR, "SG_Gamma_001"),
    Area2Interior.VariaSuit.location("Statue"): ActorLocationData(223, AreaId.AREA_2_INTERIOR, "LE_PowerUp_VariaSuite"),
    Area2Interior.VariaSuit.location("Tunnel"): ActorLocationData(224, AreaId.AREA_2_INTERIOR, "HP_Item_002"),
    # Area 2 - dam entryway
    Area2Entryway.TransportAreas1And3.location("Plants"): ActorLocationData(225, AreaId.AREA_2_ENTRYWAY, "LE_Item_005"),
    Area2Entryway.TransportAreas1And3.location("Tunnel"): ActorLocationData(
        226, AreaId.AREA_2_ENTRYWAY, "HiddenPowerup001"
    ),
    Area2Entryway.EntrywayTeleporter.location(): ActorLocationData(227, AreaId.AREA_2_ENTRYWAY, "LE_Item_003"),
    Area2Entryway.LightningArmor.location("Tutorial"): ActorLocationData(228, AreaId.AREA_2_ENTRYWAY, "LE_Item_002"),
    Area2Entryway.LightningArmor.location("Artifact"): ActorLocationData(
        229, AreaId.AREA_2_ENTRYWAY, "LE_SpecialAbility_EnergyShield"
    ),
    Area2Entryway.FleechSwarmFloodway.location(): ActorLocationData(230, AreaId.AREA_2_ENTRYWAY, "LE_Item_001"),
    Area2Entryway.Alpha2.location(): MetroidLocationData(231, AreaId.AREA_2_ENTRYWAY, "SG_Alpha_002"),
    # Area 3 - factory exterior
    Area3Exterior.ExteriorMaze.location(): ActorLocationData(301, AreaId.AREA_3_EXTERIOR, "LE_Item_004"),
    Area3Exterior.GrappleBeam.location(): ActorLocationData(302, AreaId.AREA_3_EXTERIOR, "LE_PowerUp_GrappleBeam"),
    Area3Exterior.FactoryExt.location("Ceiling"): ActorLocationData(303, AreaId.AREA_3_EXTERIOR, "LE_Item_003"),
    Area3Exterior.FactoryExt.location("Shaft"): ActorLocationData(304, AreaId.AREA_3_EXTERIOR, "LE_Item_005"),
    Area3Exterior.TransportCavernsW.location(): ActorLocationData(305, AreaId.AREA_3_EXTERIOR, "HP_ChozoHologram_002"),
    Area3Exterior.TransportArea4.location(): ActorLocationData(306, AreaId.AREA_3_EXTERIOR, "LE_Item_002"),
    Area3Exterior.EntranceMaze.location(): ActorLocationData(307, AreaId.AREA_3_EXTERIOR, "LE_Item_001"),
    Area3Exterior.BeamBurst.location(): ActorLocationData(308, AreaId.AREA_3_EXTERIOR, "LE_SpecialAbility_EnergyWave"),
    Area3Exterior.HalzynHangout.location("Top"): ActorLocationData(309, AreaId.AREA_3_EXTERIOR, "HiddenPowerup001"),
    Area3Exterior.HalzynHangout.location("Bottom"): ActorLocationData(310, AreaId.AREA_3_EXTERIOR, "HiddenPowerup002"),
    Area3Exterior.Gamma.location("Bottom"): MetroidLocationData(311, AreaId.AREA_3_EXTERIOR, "SG_Gamma_005_C"),
    # Area 3 - Metroid caverns
    Area3Caverns.TransportFactoryExtN.location(): ActorLocationData(312, AreaId.AREA_3_CAVERNS, "HiddenPowerup001"),
    Area3Caverns.Alpha2W.location(): MetroidLocationData(313, AreaId.AREA_3_CAVERNS, "SG_Alpha_002"),
    Area3Caverns.GammaC.location(): MetroidLocationData(314, AreaId.AREA_3_CAVERNS, "SG_Gamma_001"),
    Area3Caverns.GammaS.location("Tunnels"): ActorLocationData(315, AreaId.AREA_3_CAVERNS, "LE_Item_001"),
    Area3Caverns.GammaS.location("Gamma Metroid"): MetroidLocationData(316, AreaId.AREA_3_CAVERNS, "SG_Gamma_001"),
    Area3Caverns.GravittGarden.location(): ActorLocationData(317, AreaId.AREA_3_CAVERNS, "HiddenPowerup002"),
    Area3Caverns.AscendingAlleyway.location(): ActorLocationData(318, AreaId.AREA_3_CAVERNS, "LE_Item_007"),
    Area3Caverns.RamulkenRollway.location(): ActorLocationData(319, AreaId.AREA_3_CAVERNS, "LE_Item_002"),
    Area3Caverns.CavernsTeleporterE.location(): ActorLocationData(320, AreaId.AREA_3_CAVERNS, "LE_Item_003"),
    Area3Caverns.QuarryShaft.location(): ActorLocationData(321, AreaId.AREA_3_CAVERNS, "LE_Item_004"),
    Area3Caverns.TransportFactoryIntS.location(): ActorLocationData(322, AreaId.AREA_3_CAVERNS, "HiddenPowerup003"),
    Area3Caverns.Gamma2S.location(): MetroidLocationData(323, AreaId.AREA_3_CAVERNS, "SG_Gamma_004_B"),
    Area3Caverns.Gamma2N.location(): MetroidLocationData(324, AreaId.AREA_3_CAVERNS, "SG_Gamma_003"),
    Area3Caverns.Alpha2N.location(): MetroidLocationData(325, AreaId.AREA_3_CAVERNS, "SG_Alpha_003"),
    # Area 3 - factory interior
    Area3Interior.SecuritySite.location(): ActorLocationData(326, AreaId.AREA_3_INTERIOR, "LE_Item_006"),
    Area3Interior.ParabyPeriphery.location(): ActorLocationData(327, AreaId.AREA_3_INTERIOR, "LE_Item_004"),
    Area3Interior.FanControl.location(): ActorLocationData(328, AreaId.AREA_3_INTERIOR, "LE_Item_002"),
    Area3Interior.FactoryIntersection.location(): ActorLocationData(329, AreaId.AREA_3_INTERIOR, "LE_Item_001"),
    Area3Interior.GammaTransportCavernsE.location(): MetroidLocationData(330, AreaId.AREA_3_INTERIOR, "SG_Gamma_006"),
    Area3Interior.Alpha.location("Lava"): ActorLocationData(331, AreaId.AREA_3_INTERIOR, "HiddenPowerup001"),
    Area3Interior.Alpha.location("Alpha Metroid"): MetroidLocationData(332, AreaId.AREA_3_INTERIOR, "SG_Alpha_001"),
    Area3Interior.GammaS.location(): MetroidLocationData(333, AreaId.AREA_3_INTERIOR, "SG_Gamma_007_A"),
    # Area 4 - caves
    Area4Caves.CavesIntersectionTerminal.location(): ActorLocationData(401, AreaId.AREA_4_CAVES, "LE_Item_007"),
    Area4Caves.SpazerBeam.location(): ActorLocationData(402, AreaId.AREA_4_CAVES, "LE_PowerUp_SpazerBeam"),
    Area4Caves.CrumbleCatwalk.location(): ActorLocationData(403, AreaId.AREA_4_CAVES, "LE_Item_006"),
    Area4Caves.TransportArea3Mines.location(): ActorLocationData(404, AreaId.AREA_4_CAVES, "LE_Item_002"),
    Area4Caves.Alpha2.location("Missile"): ActorLocationData(405, AreaId.AREA_4_CAVES, "LE_Item_003"),
    Area4Caves.Alpha2.location("Evolved Alpha Metroid"): MetroidLocationData(406, AreaId.AREA_4_CAVES, "SG_Alpha_001"),
    Area4Caves.TransitTunnel.location(): ActorLocationData(407, AreaId.AREA_4_CAVES, "HiddenPowerup004"),
    Area4Caves.FleechSwarmCave.location(): ActorLocationData(408, AreaId.AREA_4_CAVES, "LE_Item_005"),
    Area4Caves.Gamma.location("Tunnel"): ActorLocationData(409, AreaId.AREA_4_CAVES, "HP_ChozoHologram_002"),
    Area4Caves.Gamma.location("Gamma Metroid"): MetroidLocationData(410, AreaId.AREA_4_CAVES, "SG_Gamma_001_A"),
    Area4Caves.GammaAccessS.location(): ActorLocationData(411, AreaId.AREA_4_CAVES, "LE_Item_008"),
    Area4Caves.AmethystAltars.location(): ActorLocationData(412, AreaId.AREA_4_CAVES, "HiddenPowerup001"),
    Area4Caves.TransportArea5.location(): ActorLocationData(413, AreaId.AREA_4_CAVES, "HiddenPowerup003"),
    # Area 4 - crystal mines
    Area4Mines.MinesIntersectionTunnel.location("Top"): ActorLocationData(414, AreaId.AREA_4_MINES, "LE_Item_009"),
    Area4Mines.MinesIntersectionTunnel.location("Bottom"): ActorLocationData(
        415, AreaId.AREA_4_MINES, "HiddenPowerup002"
    ),
    Area4Mines.SuperMissile.location(): ActorLocationData(416, AreaId.AREA_4_MINES, "LE_PoweUp_SuperMissile"),
    Area4Mines.PinkCrystalPreserve.location(): ActorLocationData(417, AreaId.AREA_4_MINES, "LE_Item_012"),
    Area4Mines.LavaReservoir.location(): ActorLocationData(418, AreaId.AREA_4_MINES, "LE_Item_013"),
    Area4Mines.DualPondAlcove.location(): ActorLocationData(419, AreaId.AREA_4_MINES, "LE_Item_005"),
    Area4Mines.Zeta.location(): MetroidLocationData(420, AreaId.AREA_4_MINES, "SG_Zeta_001"),
    Area4Mines.GawronGroove.location(): ActorLocationData(421, AreaId.AREA_4_MINES, "HiddenPowerup001"),
    Area4Mines.GemstoneGorge.location(): ActorLocationData(422, AreaId.AREA_4_MINES, "LE_Item_006"),
    Area4Mines.Gamma2.location(): MetroidLocationData(423, AreaId.AREA_4_MINES, "SG_Gamma_002_A"),
    Area4Mines.SpaceJump.location(): ActorLocationData(424, AreaId.AREA_4_MINES, "LE_PowerUp_SpaceJump"),
    Area4Mines.DiggernautExcavationTunnels.location("Crystals"): ActorLocationData(
        425, AreaId.AREA_4_MINES, "LE_Item_002"
    ),
    Area4Mines.DiggernautExcavationTunnels.location("Plants"): ActorLocationData(
        426, AreaId.AREA_4_MINES, "LE_Item_003"
    ),
    Area4Mines.DiggernautExcavationTunnels.location("Puzzle"): ActorLocationData(
        427, AreaId.AREA_4_MINES, "LE_Item_004"
    ),
    Area4Mines.DiggernautExcavationTunnels.location("Floor"): ActorLocationData(
        428, AreaId.AREA_4_MINES, "LE_Item_010"
    ),
    # Area 5 - tower lobby
    Area5Lobby.TransportAreas4And6.location("Left"): ActorLocationData(501, AreaId.AREA_5_LOBBY, "LE_Item_002"),
    Area5Lobby.TransportAreas4And6.location("Right"): ActorLocationData(502, AreaId.AREA_5_LOBBY, "HiddenPowerup002"),
    Area5Lobby.LobbyTeleporterW.location("Lower"): ActorLocationData(503, AreaId.AREA_5_LOBBY, "LE_Item_006"),
    Area5Lobby.LobbyTeleporterW.location("Upper"): ActorLocationData(504, AreaId.AREA_5_LOBBY, "LE_Item_007"),
    Area5Lobby.LobbyTeleporterE.location(): ActorLocationData(505, AreaId.AREA_5_LOBBY, "LE_Item_003"),
    Area5Lobby.Alpha2.location(): MetroidLocationData(506, AreaId.AREA_5_LOBBY, "SG_Alpha_001"),
    Area5Lobby.PhaseDrift.location("Artifact"): ActorLocationData(
        507, AreaId.AREA_5_LOBBY, "LE_SpecialAbility_PhaseDisplacement"
    ),
    Area5Lobby.PhaseDrift.location("Pitfall Blocks"): ActorLocationData(508, AreaId.AREA_5_LOBBY, "HiddenPowerup001"),
    Area5Lobby.MeboidMillpond.location(): ActorLocationData(509, AreaId.AREA_5_LOBBY, "LE_Item_004"),
    Area5Lobby.Gamma2.location(): MetroidLocationData(510, AreaId.AREA_5_LOBBY, "SG_Gamma_004"),
    # Area 5 - tower exterior
    Area5Exterior.TowerExt.location("Alcove"): ActorLocationData(511, AreaId.AREA_5_EXTERIOR, "LE_Item_006"),
    Area5Exterior.TowerExt.location("Crevice"): ActorLocationData(512, AreaId.AREA_5_EXTERIOR, "HiddenPowerup001"),
    Area5Exterior.TowerExt.location("Puzzle"): ActorLocationData(513, AreaId.AREA_5_EXTERIOR, "LE_Item_005"),
    Area5Exterior.TowerExt.location("Ceiling"): ActorLocationData(514, AreaId.AREA_5_EXTERIOR, "LE_Item_002"),
    Area5Exterior.OvergrownMaze.location("Right"): ActorLocationData(515, AreaId.AREA_5_EXTERIOR, "LE_Item_001"),
    Area5Exterior.OvergrownMaze.location("Left"): ActorLocationData(516, AreaId.AREA_5_EXTERIOR, "LE_Item_007"),
    Area5Exterior.ScrewAttack.location(): ActorLocationData(517, AreaId.AREA_5_EXTERIOR, "LE_PowerUp_ScrewAttack"),
    Area5Exterior.RedPlantMaze.location(): ActorLocationData(518, AreaId.AREA_5_EXTERIOR, "LE_Item_003"),
    Area5Exterior.Zeta.location(): MetroidLocationData(519, AreaId.AREA_5_EXTERIOR, "SG_Zeta_001"),
    Area5Exterior.Gamma2.location(): MetroidLocationData(520, AreaId.AREA_5_EXTERIOR, "SG_Gamma_002"),
    Area5Exterior.Gamma.location("Gamma Metroid"): MetroidLocationData(521, AreaId.AREA_5_EXTERIOR, "SG_Gamma_003"),
    Area5Exterior.Gamma.location("Maze"): ActorLocationData(522, AreaId.AREA_5_EXTERIOR, "LE_Item_004"),
    # Area 5 - tower interior
    Area5Interior.InteriorSaveStation.location(): ActorLocationData(523, AreaId.AREA_5_INTERIOR, "LE_Item_004"),
    Area5Interior.PlasmaBeam.location(): ActorLocationData(524, AreaId.AREA_5_INTERIOR, "LE_PowerUp_PlasmaBeam"),
    Area5Interior.GrappleShuffler.location(): ActorLocationData(525, AreaId.AREA_5_INTERIOR, "HiddenPowerup002"),
    Area5Interior.GravitySuit.location(): ActorLocationData(526, AreaId.AREA_5_INTERIOR, "LE_PowerUp_GravitySuite"),
    Area5Interior.PhaseDriftTrialReward.location(): ActorLocationData(527, AreaId.AREA_5_INTERIOR, "LE_Item_001"),
    Area5Interior.PhaseDriftTrialW.location("Lower"): ActorLocationData(
        528, AreaId.AREA_5_INTERIOR, "HiddenPowerup003"
    ),
    Area5Interior.PhaseDriftTrialW.location("Upper"): ActorLocationData(529, AreaId.AREA_5_INTERIOR, "LE_Item_002"),
    Area5Interior.Zeta2Access.location(): ActorLocationData(530, AreaId.AREA_5_INTERIOR, "LE_Item_005"),
    Area5Interior.GravitySuitAccess.location(): ActorLocationData(531, AreaId.AREA_5_INTERIOR, "HP_ChozoHologram_001"),
    Area5Interior.Gamma2.location(): MetroidLocationData(532, AreaId.AREA_5_INTERIOR, "SG_Gamma_001"),
    Area5Interior.InteriorTeleporter.location(): ActorLocationData(533, AreaId.AREA_5_INTERIOR, "LE_Item_003"),
    Area5Interior.Zeta2.location(): MetroidLocationData(534, AreaId.AREA_5_INTERIOR, "SG_Zeta_002"),
    # Area 6
    Area6.TransportArea7.location(): ActorLocationData(601, AreaId.AREA_6, "LE_Item_014"),
    Area6.Omega.location(): MetroidLocationData(602, AreaId.AREA_6, "SG_Omega_001"),
    Area6.HideoutSprawl.location("Right"): ActorLocationData(603, AreaId.AREA_6, "LE_Item_008"),
    Area6.HideoutSprawl.location("Left"): ActorLocationData(604, AreaId.AREA_6, "LE_Item_012"),
    Area6.CrumblingBridge.location("Pit"): ActorLocationData(605, AreaId.AREA_6, "LE_Item_011"),
    Area6.CrumblingBridge.location("Tunnel"): ActorLocationData(606, AreaId.AREA_6, "LE_Item_009"),
    Area6.CrumblingStairwell.location(): ActorLocationData(607, AreaId.AREA_6, "LE_Item_015"),
    Area6.Diggernaut.location(): ActorLocationData(608, AreaId.AREA_6, "LE_PowerUp_Powerbomb"),
    Area6.ElectricEscalade.location(): ActorLocationData(609, AreaId.AREA_6, "LE_Item_004"),
    Area6.PoisonousTunnel.location(): ActorLocationData(610, AreaId.AREA_6, "LE_Item_001"),
    Area6.Zeta.location(): MetroidLocationData(611, AreaId.AREA_6, "SG_Zeta_001"),
    Area6.ChozoSealE.location(): ActorLocationData(612, AreaId.AREA_6, "LE_Item_010"),
    Area6.ChozoSealW.location("Ceiling"): ActorLocationData(613, AreaId.AREA_6, "LE_Item_002"),
    Area6.ChozoSealW.location("Tunnel"): ActorLocationData(614, AreaId.AREA_6, "LE_Item_007"),
    Area6.ChozoSealW.location("Bottom"): ActorLocationData(615, AreaId.AREA_6, "LE_Item_013"),
    # Area 7
    Area7.LabTeleporterW.location(): ActorLocationData(701, AreaId.AREA_7, "LE_Item_008"),
    Area7.SpiderBoostTunnelS.location(): ActorLocationData(702, AreaId.AREA_7, "LE_Item_003"),
    Area7.Omega2.location(): MetroidLocationData(703, AreaId.AREA_7, "SG_Omega_002"),
    Area7.RobotRegime.location("Lower"): ActorLocationData(704, AreaId.AREA_7, "LE_Item_013"),
    Area7.RobotRegime.location("Upper"): ActorLocationData(705, AreaId.AREA_7, "LE_Item_001"),
    Area7.TransportArea6.location("Crystals"): ActorLocationData(706, AreaId.AREA_7, "LE_Item_010"),
    Area7.TransportArea6.location("Alcove"): ActorLocationData(707, AreaId.AREA_7, "HiddenPowerup003"),
    Area7.TransportArea6.location("Pitfall Blocks"): ActorLocationData(708, AreaId.AREA_7, "LE_Item_002"),
    Area7.TransportArea6.location("Tunnel"): ActorLocationData(709, AreaId.AREA_7, "HiddenPowerup001"),
    Area7.OmegaSAccess.location(): ActorLocationData(710, AreaId.AREA_7, "LE_Item_009"),
    Area7.OmegaS.location(): MetroidLocationData(711, AreaId.AREA_7, "SG_Omega_003"),
    Area7.OmegaN.location(): MetroidLocationData(712, AreaId.AREA_7, "SG_Omega_001"),
    Area7.OmegaNAccess.location(): ActorLocationData(713, AreaId.AREA_7, "LE_Item_004"),
    Area7.WallfireWorkstation.location(): ActorLocationData(714, AreaId.AREA_7, "HiddenPowerup002"),
    Area7.GrapplePuzzleFoyer.location(): ActorLocationData(715, AreaId.AREA_7, "LE_Item_011"),
    Area7.SpiderBoostTunnelN.location(): ActorLocationData(716, AreaId.AREA_7, "LE_Item_012"),
    # Area 8
    Area8.TransportSurface.location("Left"): ActorLocationData(801, AreaId.AREA_8, "LE_Item_013"),
    Area8.TransportSurface.location("Right"): ActorLocationData(802, AreaId.AREA_8, "LE_Item_014"),
    Area8.Amphitheater.location("Spikes"): ActorLocationData(803, AreaId.AREA_8, "HiddenPowerup001"),
    Area8.Amphitheater.location("Upper Left"): ActorLocationData(804, AreaId.AREA_8, "LE_Item_004"),
    Area8.Amphitheater.location("Grapple Block"): ActorLocationData(805, AreaId.AREA_8, "LE_Item_003"),
    Area8.Amphitheater.location("Upper Right"): ActorLocationData(806, AreaId.AREA_8, "LE_Item_012"),
    Area8.Amphitheater.location("Maze"): ActorLocationData(807, AreaId.AREA_8, "LE_Item_005"),
    Area8.NestNetwork.location("Crystals"): ActorLocationData(808, AreaId.AREA_8, "LE_Item_011"),
    Area8.NestNetwork.location("Hallway"): ActorLocationData(809, AreaId.AREA_8, "LE_Item_008"),
    Area8.EntranceTeleporter.location(): ActorLocationData(810, AreaId.AREA_8, "LE_Item_009"),
    Area8.NestNodule.location("Tunnel"): ActorLocationData(811, AreaId.AREA_8, "LE_Item_010"),
    Area8.NestNodule.location("Crystals"): ActorLocationData(812, AreaId.AREA_8, "LE_Item_001"),
    Area8.NestShaftW.location(): ActorLocationData(813, AreaId.AREA_8, "HiddenPowerup002"),
    Area8.Hatchling.location(): ActorLocationData(814, AreaId.AREA_8, "LE_Baby_Hatchling"),
    Area8.NestVestibule.location(): ActorLocationData(815, AreaId.AREA_8, "LE_Item_007"),
}
