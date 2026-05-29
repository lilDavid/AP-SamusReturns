from enum import StrEnum
from typing import NamedTuple

from BaseClasses import Item, ItemClassification

from .data import GAME_NAME
from .data.internal_names import ItemId, ItemModel, PickupSound


class SamusReturnsItem(Item):
    game = GAME_NAME


VICTORY = "Mission Accomplished!"


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
    MetroidDnaLocal = "Local Metroid DNA"
    Hatchling = "Metroid Hatchling"

    Nothing = "Nothing"


class TankData(NamedTuple):
    ap_id: int
    item_id: ItemId
    model: ItemModel
    is_useful: bool = False

    def classification(self):
        if self.is_useful:
            return ItemClassification.useful
        # return ItemClassification.progression_deprioritized_skip_balancing
        return ItemClassification.filler

    def pickup_sound(self):
        return PickupSound.TANK


class UniqueItemData(NamedTuple):
    ap_id: int
    item_id: ItemId
    model: ItemModel
    is_progression: bool = True

    def classification(self):
        if self.is_progression:
            return ItemClassification.progression | ItemClassification.useful
        return ItemClassification.useful

    def pickup_sound(self):
        return PickupSound.ITEM


class OtherItemData(NamedTuple):
    ap_id: int
    item_id: ItemId
    model: ItemModel
    item_type: ItemClassification
    sound: PickupSound

    def classification(self):
        return self.item_type

    def pickup_sound(self):
        return self.sound


ItemData = TankData | UniqueItemData | OtherItemData


tanks = {
    ItemName.MissileTank: TankData(1, ItemId.MISSILE_TANKS, ItemModel.MissileTank),
    ItemName.SuperMissileTank: TankData(2, ItemId.SUPER_MISSILE_TANKS, ItemModel.SuperMissileTank),
    ItemName.PowerBombTank: TankData(3, ItemId.POWER_BOMB_TANKS, ItemModel.PowerBombTank),
    ItemName.EnergyTank: TankData(4, ItemId.ENERGY_TANKS, ItemModel.EnergyTank, is_useful=True),
    ItemName.AeionTank: TankData(5, ItemId.MAX_AEION, ItemModel.AeionTank),
}

major_items = {
    ItemName.MissileLauncher: UniqueItemData(11, ItemId.MISSILE_LAUNCHER, ItemModel.MissileLauncher),
    ItemName.SuperMissile: UniqueItemData(12, ItemId.SUPER_MISSILE, ItemModel.SuperMissile),
    ItemName.PowerBomb: UniqueItemData(13, ItemId.POWER_BOMB, ItemModel.PowerBomb),
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
    ItemName.Hatchling: UniqueItemData(55, ItemId.METROID_HATCHLING, ItemModel.Hatchling),
    ItemName.ScanPulse: UniqueItemData(61, ItemId.SCAN_PULSE, ItemModel.ScanPulse, is_progression=False),
    ItemName.LightningArmor: UniqueItemData(62, ItemId.LIGHTNING_ARMOR, ItemModel.LightningArmor),
    ItemName.BeamBurst: UniqueItemData(63, ItemId.BEAM_BURST, ItemModel.BeamBurst),
    ItemName.PhaseDrift: UniqueItemData(64, ItemId.PHASE_DRIFT, ItemModel.PhaseDrift),
}

reserve_tanks = {
    ItemName.EnergyReserve: UniqueItemData(
        71, ItemId.ENERGY_RESERVE_TANK, ItemModel.EnergyReserve, is_progression=False
    ),
    ItemName.MissileReserve: UniqueItemData(
        72, ItemId.MISSILE_RESERVE_TANK, ItemModel.MissileReserve, is_progression=False
    ),
    ItemName.AeionReserve: UniqueItemData(73, ItemId.AEION_RESERVE_TANK, ItemModel.AeionReserve, is_progression=False),
}

other_items: dict[ItemName, OtherItemData] = {
    ItemName.MetroidDna: OtherItemData(
        91, ItemId.DNA, ItemModel.Dna, ItemClassification.progression_skip_balancing, sound=PickupSound.AEION
    ),
    ItemName.Nothing: OtherItemData(
        100, ItemId.NOTHING, ItemModel.ItemSphere, ItemClassification.filler, sound=PickupSound.TANK
    ),
}

unique_items: dict[str, ItemData] = {
    **major_items,
    **reserve_tanks,
}

item_data_table: dict[str, ItemData] = {
    **tanks,
    **major_items,
    **reserve_tanks,
    **other_items,
}


launcher_to_ammo: dict[str, ItemName] = {
    ItemName.MissileLauncher: ItemName.MissileTank,
    ItemName.SuperMissile: ItemName.SuperMissileTank,
    ItemName.PowerBomb: ItemName.PowerBombTank,
    ItemName.ScanPulse: ItemName.AeionTank,
    ItemName.LightningArmor: ItemName.AeionTank,
    ItemName.BeamBurst: ItemName.AeionTank,
    ItemName.PhaseDrift: ItemName.AeionTank,
}


def get_ammo_id(launcher: str):
    ammo_item = launcher_to_ammo.get(launcher)
    if ammo_item is None:
        return None
    return item_data_table[ammo_item].item_id


BASE_ENERGY = 99
BASE_AEION = 1000

default_ammo_amounts: dict[str, int] = {
    ItemName.EnergyTank: 100,
    ItemName.MissileLauncher: 24,
    ItemName.MissileTank: 3,
    ItemName.SuperMissile: 5,
    ItemName.SuperMissileTank: 1,
    ItemName.PowerBomb: 5,
    ItemName.PowerBombTank: 1,
    ItemName.AeionTank: 50,
    ItemName.ScanPulse: 0,
    ItemName.LightningArmor: 150,
    ItemName.BeamBurst: 150,
    ItemName.PhaseDrift: 150,
}


def item_group(*items: ItemName):
    return {item.value for item in items}


item_groups = {
    "Major Items": {item.value for item in major_items.keys()},
    "Reserve Tanks": {item.value for item in reserve_tanks.keys()},
    "Tanks": {item.value for item in tanks.keys()},
    "Missile Launchers": item_group(
        ItemName.MissileLauncher,
        ItemName.SuperMissile,
    ),
    "Beams": item_group(
        ItemName.ChargeBeam,
        ItemName.IceBeam,
        ItemName.WaveBeam,
        ItemName.SpazerBeam,
        ItemName.PlasmaBeam,
    ),
    "Suits": item_group(
        ItemName.VariaSuit,
        ItemName.GravitySuit,
    ),
    "Aeion Abilities": item_group(
        ItemName.ScanPulse,
        ItemName.LightningArmor,
        ItemName.BeamBurst,
        ItemName.PhaseDrift,
    ),
    "Weapons": item_group(
        ItemName.MissileLauncher,
        ItemName.SuperMissile,
        ItemName.ChargeBeam,
        ItemName.IceBeam,
        ItemName.WaveBeam,
        ItemName.SpazerBeam,
        ItemName.PlasmaBeam,
        ItemName.ScrewAttack,
        ItemName.BeamBurst,
    ),
    "Morph Ball Upgrades": item_group(
        ItemName.MorphBall,
        ItemName.SpiderBall,
        ItemName.SpringBall,
        ItemName.Bomb,
        ItemName.PowerBomb,
    ),
    "Movement Systems": item_group(
        ItemName.GrappleBeam,
        ItemName.HighJumpBoots,
        ItemName.SpaceJump,
        ItemName.GravitySuit,
        ItemName.PhaseDrift,
    ),
    "Life Support Upgrades": item_group(
        ItemName.EnergyTank,
        ItemName.VariaSuit,
        ItemName.GravitySuit,
        ItemName.LightningArmor,
    ),
}
