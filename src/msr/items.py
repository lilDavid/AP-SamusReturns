from enum import StrEnum
from typing import NamedTuple

from BaseClasses import ItemClassification

from .data.internal_names import ItemId, ItemModel, PickupSound


class ItemName(StrEnum):
    MissileLauncher = "Missile Launcher"
    SuperMissile = "Super Missile"
    PowerBomb = "Power Bomb"

    WaveBeam = "Wave Beam"
    SpazerBeam = "Spazer Beam"
    PlasmaBeam = "Plasma Beam"
    ChargeBeam = "Charge Beam"
    IceBeam = "Ice Beam"

    MorphBall = "Morph Ball"
    SpiderBall = "Spider Ball"
    Bomb = "Bomb"
    SpringBall = "Spring Ball"

    VariaSuit = "Varia Suit"
    GravitySuit = "Gravity Suit"

    GrappleBeam = "Grapple Beam"
    HighJumpBoots = "High Jump Boots"
    SpaceJump = "Space Jump"
    ScrewAttack = "Screw Attack"

    ScanPulse = "Scan Pulse"
    LightningArmor = "Lightning Armor"
    BeamBurst = "Beam Burst"
    PhaseDrift = "Phase Drift"

    EnergyTank = "Energy Tank"
    AeionTank = "Aeion Tank"
    MissileTank = "Missile Tank"
    SuperMissileTank = "Super Missile Tank"
    PowerBombTank = "Power Bomb Tank"

    EnergyReserve = "Energy Reserve Tank"
    AeionReserve = "Aeion Reserve Tank"
    MissileReserve = "Missile Reserve Tank"

    MetroidDna = "Metroid DNA"
    Hatchling = "Metroid Hatchling"

    Nothing = "Nothing"


class TankData(NamedTuple):
    ap_id: int
    item_id: ItemId
    model: ItemModel
    sound: PickupSound | None = None

    def classification(self):
        return ItemClassification.progression_deprioritized_skip_balancing


class LauncherData(NamedTuple):
    ap_id: int
    item_id: ItemId
    ammo_id: ItemId
    model: ItemModel
    sound: PickupSound | None = None

    def classification(self):
        return ItemClassification.progression | ItemClassification.useful


class UniqueItemData(NamedTuple):
    ap_id: int
    item_id: ItemId
    model: ItemModel
    is_progression: bool = True
    sound: PickupSound | None = None

    def classification(self):
        if self.is_progression:
            return ItemClassification.progression | ItemClassification.useful
        return ItemClassification.useful


class OtherItemData(NamedTuple):
    ap_id: int
    item_id: ItemId
    model: ItemModel
    item_type: ItemClassification
    sound: PickupSound | None = None

    def classification(self):
        return self.item_type


ItemData = TankData | LauncherData | UniqueItemData | OtherItemData


tanks = {
    ItemName.MissileTank: TankData(1, ItemId.MISSILE_TANKS, ItemModel.MissileTank),
    ItemName.SuperMissileTank: TankData(2, ItemId.SUPER_MISSILE_TANKS, ItemModel.SuperMissileTank),
    ItemName.PowerBombTank: TankData(3, ItemId.POWER_BOMB_TANKS, ItemModel.PowerBombTank),
    ItemName.EnergyTank: TankData(4, ItemId.ENERGY_TANKS, ItemModel.EnergyTank),
    ItemName.AeionTank: TankData(5, ItemId.MAX_AEION, ItemModel.AeionTank),
}

launchers = {
    ItemName.MissileLauncher: LauncherData(
        11, ItemId.MISSILE_LAUNCHER, ItemId.MISSILE_TANKS, ItemModel.MissileLauncher
    ),
    ItemName.SuperMissile: LauncherData(12, ItemId.SUPER_MISSILE, ItemId.SUPER_MISSILE_TANKS, ItemModel.SuperMissile),
    ItemName.PowerBomb: LauncherData(13, ItemId.POWER_BOMB, ItemId.POWER_BOMB_TANKS, ItemModel.PowerBomb),
}

major_items = {
    ItemName.ChargeBeam: UniqueItemData(21, ItemId.CHARGE_BEAM, ItemModel.ChargeBeam),
    ItemName.IceBeam: UniqueItemData(22, ItemId.ICE_BEAM, ItemModel.IceBeam),
    ItemName.WaveBeam: UniqueItemData(23, ItemId.WAVE_BEAM, ItemModel.WaveBeam),
    ItemName.SpazerBeam: UniqueItemData(24, ItemId.SPAZER_BEAM, ItemModel.SpazerBeam),
    ItemName.PlasmaBeam: UniqueItemData(25, ItemId.PLASMA_BEAM, ItemModel.PlasmaBeam),
    ItemName.MorphBall: UniqueItemData(31, ItemId.MORPH_BALL, ItemModel.MorphBall),
    ItemName.SpiderBall: UniqueItemData(32, ItemId.SPIDER_BALL, ItemModel.SpiderBall),
    ItemName.SpringBall: UniqueItemData(33, ItemId.SPRING_BALL, ItemModel.SpringBall),
    ItemName.Bomb: UniqueItemData(34, ItemId.BOMB, ItemModel.Bomb),
    ItemName.VariaSuit: UniqueItemData(41, ItemId.VARIA_SUIT, ItemModel.VariaSuit),
    ItemName.GravitySuit: UniqueItemData(42, ItemId.GRAVITY_SUIT, ItemModel.GravitySuit),
    ItemName.GrappleBeam: UniqueItemData(51, ItemId.GRAPPLE_BEAM, ItemModel.GrappleBeam),
    ItemName.HighJumpBoots: UniqueItemData(52, ItemId.HIGH_JUMP_BOOTS, ItemModel.HighJumpBoots),
    ItemName.SpaceJump: UniqueItemData(53, ItemId.SPACE_JUMP, ItemModel.SpaceJump),
    ItemName.ScrewAttack: UniqueItemData(54, ItemId.SCREW_ATTACK, ItemModel.ScrewAttack),
    ItemName.ScanPulse: UniqueItemData(61, ItemId.SCAN_PULSE, ItemModel.ScanPulse, is_progression=False),
    ItemName.LightningArmor: UniqueItemData(62, ItemId.LIGHTNING_ARMOR, ItemModel.LightningArmor),
    ItemName.BeamBurst: UniqueItemData(63, ItemId.BEAM_BURST, ItemModel.BeamBurst),
    ItemName.PhaseDrift: UniqueItemData(64, ItemId.PHASE_DRIFT, ItemModel.PhaseDrift),
    ItemName.Hatchling: UniqueItemData(65, ItemId.METROID_HATCHLING, ItemModel.Hatchling),
}

reserve_tanks = {
    ItemName.EnergyReserve: UniqueItemData(71, ItemId.ENERGY_RESERVE_TANK, ItemModel.EnergyReserve),
    ItemName.MissileReserve: UniqueItemData(72, ItemId.MISSILE_RESERVE_TANK, ItemModel.MissileReserve),
    ItemName.AeionReserve: UniqueItemData(73, ItemId.ENERGY_RESERVE_TANK, ItemModel.AeionReserve),
}

other_items: dict[ItemName, OtherItemData] = {
    ItemName.MetroidDna: OtherItemData(91, ItemId.DNA, ItemModel.Dna, ItemClassification.progression_skip_balancing),
    ItemName.Nothing: OtherItemData(
        100, ItemId.NOTHING, ItemModel.ItemSphere, ItemClassification.filler, sound=PickupSound.TANK
    ),
}

unique_items: dict[str, ItemData] = {
    **launchers,
    **major_items,
    **reserve_tanks,
}

item_data_table: dict[str, ItemData] = {
    **tanks,
    **launchers,
    **major_items,
    **reserve_tanks,
    **other_items,
}
