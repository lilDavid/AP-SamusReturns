from __future__ import annotations

from enum import StrEnum
from typing import Protocol


class AreaName(StrEnum):
    SurfaceEast = "Surface"
    Area1 = "Area 1"
    Area2Exterior = "Area 2"
    Area2Interior = "Area 2"
    Area2Entryway = "Area 2"
    Area3Exterior = "Area 3"
    Area3Caverns = "Area 3"
    Area3Interior = "Area 3"
    Area4Caves = "Area 4"
    Area4Mines = "Area 4"
    Area5Lobby = "Area 4"
    Area5Exterior = "Area 5"
    Area5Interior = "Area 5"
    Area6 = "Area 6"
    Area7 = "Area 7"
    Area8 = "Area 8"
    SurfaceWest = "Surface"


def format_room_name(area: AreaName, room: str):
    return f"{area}: {room}"


# This is a bit of a hack, but it beats writing a custom metaclass
class _WithArea(Protocol):
    def with_area(self) -> str: ...


class _RoomNameMixin:
    def subregion(self: _WithArea, name: str | None = None):
        if name is None:
            return self.with_area()
        return f"{self.with_area()} ({name})"

    def location(self: _WithArea, name: str | None = None):
        if name is None:
            return self.with_area()
        return f"{self.with_area()} - {name}"


class SurfaceEast(_RoomNameMixin, StrEnum):
    LandingSite = "Landing Site"
    TwistyTunnel = "Twisty Tunnel"
    MorphBall = "Morph Ball Chamber"
    ChozoSeal = "Chozo Seal"
    TransportArea1 = "Transport to Area 1"
    ChozoCacheE = "Chozo Cache East"
    ChargeBeam = "Charge Beam Chamber"
    Alpha = "Alpha Arena"
    ScanPulse = "Scan Pulse Chamber"
    ChozoCacheW = "Chozo Cache West"
    MoheekMarket = "Moheek Market"
    CavernCavity = "Cavern Cavity"
    ChargeBeamAccess = "Charge Beam Chamber Access"
    HornoadHallway = "Hornoad Hallway"
    TransportArea8 = "Transport to Area 8"
    SurfaceStash = "Surface Stash"
    SurfaceCrumbleChallenge = "Surface Crumble Block Challenge"
    TransportCache = "Transport Cache"
    CavernAlcove = "Cavern Alcove"
    EnergyRechargeShaft = "Energy Recharge Station Shaft"
    AmmoRecharge = "Ammo Recharge Station"

    def with_area(self):
        return format_room_name(AreaName.SurfaceEast, self)


class Area1(_RoomNameMixin, StrEnum):
    TransportSurfaceArea2 = "Transport to Surface and Area 2"
    MoheekMount = "Moheek Mount"
    GulluggGangway = "Gullugg Gangway"
    Bomb = "Bomb Chamber"
    InnerTempleEHall = "Inner Temple East Hall"
    DestroyedArmory = "Destroyed Armory"
    SpiderBall = "Spider Ball Chamber"
    ExteriorAlpha = "Exterior Alpha Arena"
    TempleExterior = "Temple Exterior"
    CavernsLobby = "Metroid Caverns Lobby"
    CavernsAlphaSwAccess = "Metroid Caverns Alpha Arena Southwest Access"
    CavernsAlphaSe = "Metroid Caverns Alpha Arena Southeast"
    CavernsAlphaNe = "Metroid Caverns Alpha Arena Northeast"
    WaterMaze = "Water Maze"
    IceBeam = "Ice Beam Chamber"
    CavernsEnergyRecharge = "Metroid Caverns Energy Recharge Station"
    MagmaPool = "Magma Pool"
    InnerTempleWHall = "Inner Temple West Hall"
    CavernsSaveStation = "Metroid Caverns Save Station"
    InnerTempleTeleporterAccess = "Inner Temple Teleporter Access"
    InnerTempleVentShaft = "Inner Temple Ventilation Shaft"
    CavernsHub = "Metroid Caverns Hub"
    CavernsAlphaNeAccess = "Metroid Caverns Alpha Arena Northeast Access"
    BombAccess = "Bomb Chamber Access"
    InnerTempleSaveStation = "Inner Temple Save Station"
    InnerTempleUpperHallway = "Inner Temple Upper Hallway"
    InnerTempleTeleporter = "Inner Temple Teleporter"
    IceBeamAccess = "Ice Beam Chamber Access"
    TransportCache = "Transport Cache"
    HarmonizedHallway = "Harmonized Hallway"
    CavernsAlphaSw = "Metroid Caverns Alpha Arena Southwest"
    ChuteLeechCabin = "Chute Leech Cabin"

    def with_area(self):
        return format_room_name(AreaName.Area1, self)


class Area2Exterior(_RoomNameMixin, StrEnum):
    DamExterior = "Dam Exterior"
    Arachnus = "Arachnus Arena"
    FanFunnel = "Fan Funnel"
    CritterPlayground = "Critter Playground"
    CavernsEntrance = "Metroid Caverns Entrance"
    SpikeRavine = "Spike Ravine"
    AmmoRechargeAccess = "Metroid Caverns Ammo Recharge Station Access"
    CavernsMaze = "Metroid Caverns Maze"
    CavernsSaveStation = "Metroid Caverns Save Station"
    CavernsAlphaNw = "Metroid Caverns Alpha Arena Northwest"
    CavernsLobby = "Metroid Caverns Lobby"
    CavernsAlphaSw = "Metroid Caverns Alpha Arena Southwest"
    CavernsAlphaEAccess = "Metroid Caverns Alpha Arena East Access"
    CavernsTeleporter = "Metroid Caverns Teleporter"
    ExteriorAlpha2 = "Exterior Alpha+ Arena"
    SereneShelter = "Serene Shelter"
    CavernsAlpha2 = "Metroid Caverns Alpha+ Arena"
    InnerAlpha = "Inner Alpha Arena"
    RockIcicleCorridor = "Rock Icicle Corridor"
    MaintenanceTunnel = "Maintenance Tunnel"
    CavernsAmmoRecharge = "Metroid Caverns Ammo Recharge Station"
    CavernsAlphaE = "Metroid Caverns Alpha Arena East"

    def with_area(self):
        return format_room_name(AreaName.Area2Exterior, self)


class Area2Interior(_RoomNameMixin, StrEnum):
    WaveBeam = "Wave Beam & Transport to Dam Exterior West"
    VariaSuit = "Varia Suit Chamber"
    InteriorIntersection = "Interior Intersection Terminal"
    LavaGenerator = "Lava Generator"
    CrumbleCavern = "Crumble Cavern"
    WhimsicalWaterwhieels = "Whimsical Waterwheels"
    InteriorTeleporter = "Interior Teleporter"
    FleechFireContainment = "Fleech Fire Containment"
    DamBasement = "Dam Basement"
    GulluggHideout = "Gullugg Hideout"
    HighJumpBoots = "High Jump Boots Chamber"
    HighJumpBootsAccess = "High Jump Boots Chamber Access"
    WallfireCorridor = "Wallfire Corridor"
    TeleporterStorage = "Teleporter Storage"
    Gamma = "Gamma Arena"
    GeneratorAccess = "Generator Access"

    def with_area(self):
        return format_room_name(AreaName.Area2Interior, self)


class Area2Entryway(_RoomNameMixin, StrEnum):
    TransportAreas1And3 = "Transport to Areas 1 and 3"
    EntrywayTeleporter = "Entryway Teleporter"
    LightningArmor = "Lightning Armor & Transport to Dam Exterior East"
    TransportAccess = "Transport Access"
    FleechSwarmFloodway = "Fleech Swarm Floodway"
    Alpha2 = "Alpha+ Arena"

    def with_area(self):
        return format_room_name(AreaName.Area2Entryway, self)


class Area3Exterior(_RoomNameMixin, StrEnum):
    TransportArea2 = "Transport to Area 2"
    ExteriorMaze = "Exterior Maze"
    GrappleBeam = "Grapple Beam Chamber"
    FactoryExtTeleporter = "Factory Exterior Teleporter Cave"
    FactoryExt = "Factory Exterior"
    TransportCavernsW = "Transport to Metroid Caverns West"
    TransportArea4 = "Transport to Area 4"
    EntranceMaze = "Entrance Maze"
    TransportCavernsN = "Transport to Metroid Caverns North"
    BeamBurst = "Beam Burst Chamber & Tsumuri Station"
    HalzynHangout = "Halzyn Hangout"
    Gamma = "Exterior Gamma Arena"
    NooksCranny = "Nook's Cranny"
    FactoryExtAccess = "Factory Exterior Access"

    def with_area(self):
        return format_room_name(AreaName.Area3Exterior, self)


class Area3Caverns(_RoomNameMixin, StrEnum):
    TransportFactoryExtN = "Transport to Factory Exterior North"
    Alpha2W = "Alpha+ Arena West"
    GammaC = "Gamma Arena Center"
    GammaS = "Caverns Gamma Arena South"
    SaveStationN = "Save Station North"
    GravittGarden = "Gravitt Garden"
    AscendingAlleyway = "Ascending Alleyway"
    RamulkenRollway = "Ramulken Rollway"
    CavernsTeleporterE = "Caverns Teleporter East"
    QuarryShaft = "Quarry Shaft"
    LonelyLoop = "Lonely Loop"
    QuarryTunnel = "Quarry Tunnel"
    TransportFactoryIntS = "Transport to Factory Interior South"
    Gamma2S = "Gamma+ Arena South"
    Gamma2SAccess = "Gamma+ Arena South Access"
    WaterfallCavern = "Waterfall Cavern"
    Gamma2N = "Gamma+ Arena North"
    TransportFactoryExtW = "Transport to Factory Exterior West"
    Alpha2N = "Alpha+ Arena North"
    LetumShrine = "Letum Shrine"
    CavernsTeleporterW = "Caverns Teleporter West"

    def with_area(self):
        return format_room_name(AreaName.Area3Caverns, self)


class Area3Interior(_RoomNameMixin, StrEnum):
    SecuritySite = "Security Site"
    GammaSAccess = "Factory Gamma Arena South Access"
    ParabyPeriphery = "Paraby Periphery"
    FanControl = "Fan Control"
    GrappleCircuit = "Grapple Circuit"
    FactoryIntersection = "Factory Intersection"
    FactoryIntTeleporter = "Factory Interior Teleporter"
    TransportFactoryExtE = "Transport to Factory Exterior East"
    AlphaAccess = "Alpha Arena Access"
    GammaTransportCavernsE = "Gamma Arena & Transport to Metroid Caverns East"
    RamulkenResidence = "Ramulken Residence"
    WallfireWatch = "Wallfire Watch"
    Alpha = "Alpha Arena"
    GammaS = "Factory Gamma Arena South"
    DedicatedCallisoRoost = "Dedicated Callisto Roost"
    FactoryTeleporterAccess = "Factory Teleporter Access"
    GammaCAccess = "Gamma Arena Center Access"

    def with_area(self):
        return format_room_name(AreaName.Area3Interior, self)


class Area4Caves(_RoomNameMixin, StrEnum):
    CavesIntersectionTerminal = "Caves Intersection Terminal"
    SpazerBeam = "Spazer Beam Chamber"
    CrumbleCatwalk = "Crumble Catwalk"
    LavaPond = "Lava Pond"
    TransportArea3Mines = "Transport to Area 3 and Crystal Mines"
    Alpha2 = "Alpha+ Arena"
    TransitTunnel = "Transit Tunnel"
    FleechSwarmCave = "Fleech Swarm Cave"
    HostileHangout = "Hostile Hangout"
    Gamma = "Gamma Arena"
    GammaAccessS = "Gamma Arena Access South"
    OutwardClimb = "Outward Climb"
    AmethystAltars = "Amethyst Altars"
    GammaAccessN = "Gamma Arena Access North"
    Alpha2Access = "Alpha+ Arena Access"
    VenomousPond = "Venomous Pond"
    TransportArea5 = "Transport to Area 5"

    def with_area(self):
        return format_room_name(AreaName.Area4Caves, self)


class Area4Mines(_RoomNameMixin, StrEnum):
    MinesIntersectionTunnel = "Mines Intersection Terminal"
    SuperMissile = "Super Missile Chamber"
    PinkCrystalPreserve = "Pink Crystal Preserve"
    TransportCentralCaves = "Transport to Central Caves"
    LavaReservoir = "Lava Reservoir"
    DualPondAlcove = "Dual Pond Alcove"
    Zeta = "Zeta Arena"
    Gamma2 = "Gamma+ Arena"
    GawronGroove = "Gawron Groove"
    BasaltBasin = "Basalt Basin"
    MinesEntrance = "Mines Entrance"
    TsumuriTunnel = "Tsumuri Tunnel"
    MinesTeleporter = "Mines Teleporter"
    GreenCrystalDugout = "Green Crystal Dugout"
    GemstoneGorge = "Gemstone Gorge"
    SpaceJump = "Space Jump Chamber"
    DiggernautExcavationTunnels = "Diggernaut Excavation Tunnels"

    def with_area(self):
        return format_room_name(AreaName.Area4Mines, self)


class Area5Lobby(_RoomNameMixin, StrEnum):
    LobbySaveStation = "Lobby Save Station"
    TransportTowerIntE = "Transport to Tower Interior East"
    TransportAreas4And6 = "Transport to Areas 4 and 6"
    LobbyTeleporterW = "Lobby Teleporter West"
    JShapeTunnel = "J-Shape Tunnel"
    TransportTowerIntW = "Transport to Tower Interior West"
    LobbyTeleporterE = "Lobby Teleporter East"
    Alpha2 = "Alpha+ Arena"
    Gamma2Access = "Lobby Gamma+ Arena Access"
    PhaseDrift = "Phase Drift Chamber"
    MeboidMillpond = "Meboid Millpond"
    Gamma2 = "Lobby Gamma+ Arena"
    LobbyPassageway = "Lobby Passageway"

    def with_area(self):
        return format_room_name(AreaName.Area5Lobby, self)


class Area5Exterior(_RoomNameMixin, StrEnum):
    TowerExt = "Tower Exterior"
    OvergrownMaze = "Overgrown Maze"
    ScrewAttack = "Screw Attack Chamber"
    ZetaAccess = "Zeta Arena Access"
    RedPlantMaze = "Red Plant Maze"
    TransportTowerIntW = "Transport to Tower Interior West"
    Zeta = "Zeta Arena"
    ParabyParlor = "Paraby Parlor"
    Gamma = "Gamma Arena"
    ScrewAttackAccess = "Screw Attack Chamber Access"
    Gamma2 = "Gamma+ Arena & Access"

    def with_area(self):
        return format_room_name(AreaName.Area5Exterior, self)


class Area5Interior(_RoomNameMixin, StrEnum):
    TransportTowerLobbyE = "Transport to Tower Lobby East"
    InteriorSaveStation = "Interior Save Station"
    TransportTowerExtE = "Transport to Tower Exterior East"
    PlasmaBeam = "Plasma Beam Chamber"
    GrappleShuffler = "Grapple Shuffler"
    AutrackAcropolis = "Autrack Acropolis"
    GravitySuit = "Gravity Suit Chamber"
    PhaseDriftTrialReward = "Phase Drift Trial Reward Room"
    PhaseDriftTrialW = "Phase Drift Trial West"
    PhaseDriftTrialE = "Phase Drift Trial East"
    TransportTowerLobbyW = "Transport to Tower Lobby West"
    MetroidMarina = "Meboid Marina"
    Zeta2Access = "Zeta+ Arena Access"
    TransportTowerExtW = "Transport to Tower Exterior West"
    GravitySuitAccess = "Gravity Suit Chamber Access"
    PhaseDriftTrialEntrance = "Phase Drift Trial Entrance"
    Gamma2 = "Tower Gamma+ Arena"
    InteriorTeleporter = "Interior Teleporter"
    Zeta2 = "Zeta+ Arena"
    Gamma2Access = "Tower Gamma+ Arena Access"

    def with_area(self):
        return format_room_name(AreaName.Area5Interior, self)


class Area6(_RoomNameMixin, StrEnum):
    TransportArea7 = "Transport to Area 7"
    TeleporterS = "Teleporter South"
    Omega = "Omega Arena"
    HideoutSprawl = "Hideout Sprawl"
    TeleporterNAccess = "Teleporter North Access"
    CrumblingBridge = "Crumbling Bridge"
    HideoutEntrance = "Hideout Entrance"
    CrumblingStairwell = "Crumbling Stairwell"
    Diggernaut = "Diggernaut Arena"
    SwarmSquare = "Swarm Square"
    ElectricEscalade = "Electric Escalade"
    PoisonousTunnel = "Poisonous Tunnel"
    ZetaAccess = "Zeta Arena Access"
    Zeta = "Zeta Arena"
    TransportArea5 = "Transport to Area 5"
    ChozoSealE = "Chozo Seal East"
    OmegaAccess = "Omega Arena Access"
    ChozoSealW = "Chozo Seal West Intersection Terminal"
    TeleporterN = "Teleporter North"

    def with_area(self):
        return format_room_name(AreaName.Area6, self)


class Area7(_RoomNameMixin, StrEnum):
    LabTeleporterW = "Laboratory Teleporter West"
    GrapplePuzzleMadness = "Grapple Puzzle Madness"
    SpiderBoostTunnelS = "Spider Boost Tunnel South"
    LabTeleporterE = "Laboratory Teleporter East"
    Omega2 = "Omega+ Arena"
    RobotRegime = "Robot Regime"
    TransportArea6 = "Transport to Area 6"
    OmegaSAccess = "Omega Arena South Access"
    OmegaS = "Omega Arena South"
    OmegaN = "Omega Arena North"
    OmegaNAccess = "Omega Arena North Access"
    WallfireWorkstation = "Wallfire Workstation"
    GrapplePuzzleFoyer = "Grapple Puzzle Foyer"
    RobotRetreat = "Robot Retreat"
    SpiderBoostTunnelN = "Spider Boost Tunnel North"
    TransportArea8 = "Transport to Area 8"

    def with_area(self):
        return format_room_name(AreaName.Area7, self)


class Area8(_RoomNameMixin, StrEnum):
    TransportSurface = "Transport to Surface"
    NestHallwayS = "Metroid Nest Hallway South"
    Amphitheater = "Amphitheater"
    NestNetwork = "Nest Network"
    EntranceTeleporter = "Entrance Teleporter"
    NestNodule = "Nest Nodule"
    NestSmallShaft = "Metroid Nest Small Shaft"
    NestShaftE = "Metroid Nest Shaft East"
    NestHallwayNe = "Metroid Nest Hallway Northeast"
    NestHallwayNw = "Metroid Nest Hallway Northwest"
    NestRechargeStations = "Metroid Nest Recharge Stations"
    NestShaftW = "Metroid Nest Shaft West"
    QueenAccess = "Queen Arena Access"
    TransportArea7 = "Transport to Area 7"
    Queen = "Queen Arena"
    Hatchling = "Hatchling Room"
    NestVestibule = "Nest Vestibule"
    NestTeleporter = "Metroid Nest Teleporter"

    def with_area(self):
        return format_room_name(AreaName.Area8, self)


class SurfaceWest(_RoomNameMixin, StrEnum):
    LandingSite = "Landing Site"
    TransportArea8 = "Transport to Area 8"
    SurfaceStash = "Surface Stash"
    SurfaceCrumbleChallenge = "Surface Crumble Block Challenge"

    def with_area(self):
        return format_room_name(AreaName.SurfaceWest, self)


RoomName = (
    SurfaceEast
    | Area1
    | Area2Exterior
    | Area2Interior
    | Area2Entryway
    | Area3Exterior
    | Area3Caverns
    | Area3Interior
    | Area4Caves
    | Area4Mines
    | Area5Lobby
    | Area5Exterior
    | Area5Interior
    | Area6
    | Area7
    | Area8
    | SurfaceWest
)
