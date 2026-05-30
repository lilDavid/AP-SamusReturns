from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from rule_builder.rules import And, Has, HasAll, HasAny, Or, Rule
from typing_extensions import override

from ..data import GAME_NAME
from ..items import ItemName, launcher_to_ammo
from . import can_any_missile, can_beam_burst, can_power_bomb

if TYPE_CHECKING:
    from .. import SamusReturnsWorld


class EnemyType(Enum):
    NORMAL = "normal enemy", 100, 1000
    WEAK_METROID = "weak Metroid", 100, 300  # Alpha, Gamma
    # ZETA_METROID = "Zeta Metroid", 70, 300
    # OMEGA_METROID = "Omega Metroid", (30 + 60) / 2, (70 + 135) / 2
    # OMEGA_METROID_ARMOR = "Omega Metroid armor", 850, 2100
    DIGGERNAUT = "Diggernaut", 140, 300
    QUEEN = "Queen Metroid", 120, 420

    def __init__(self, description: str, missile_damage: int, super_damage: int):
        self.description = description
        self.missile_damage = missile_damage
        self.super_damage = super_damage


@dataclass
class CanDamageWithMissiles(Rule["SamusReturnsWorld"], game=GAME_NAME):
    damage: int
    enemy_type: EnemyType

    @override
    def _instantiate(self, world: SamusReturnsWorld) -> Rule.Resolved:
        return self.Resolved(
            self.damage,
            self.enemy_type,
            self.AmmoInfo.from_launcher(world, ItemName.MissileLauncher),
            self.AmmoInfo.from_launcher(world, ItemName.SuperMissile),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class AmmoInfo(NamedTuple):
        launcher_name: ItemName
        tank_name: ItemName
        launcher_ammo: int
        tank_ammo: int

        @classmethod
        def from_launcher(cls, world: SamusReturnsWorld, launcher: ItemName):
            tank = launcher_to_ammo[launcher]
            return cls(launcher, tank, world.ammo_amounts[launcher], world.ammo_amounts[tank])

    class Resolved(Rule.Resolved):
        damage: int
        enemy_type: EnemyType
        missiles: CanDamageWithMissiles.AmmoInfo
        supers: CanDamageWithMissiles.AmmoInfo

        def get_ammo(self, ammo_info: CanDamageWithMissiles.AmmoInfo, state: CollectionState):
            if not state.has(ammo_info.launcher_name, self.player):
                return 0
            return ammo_info.launcher_ammo + state.count(ammo_info.tank_name, self.player) * ammo_info.tank_ammo

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            missile_damage = self.enemy_type.missile_damage * self.get_ammo(self.missiles, state)
            super_damage = self.enemy_type.super_damage * self.get_ammo(self.supers, state)
            return missile_damage + super_damage >= self.damage

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                ItemName.MissileLauncher: {id(self)},
                ItemName.MissileTank: {id(self)},
                ItemName.SuperMissile: {id(self)},
                ItemName.SuperMissileTank: {id(self)},
            }

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            return [
                {"type": "text", "text": "Deal "},
                {"type": "color", "color": "green" if state and self(state) else "salmon", "text": str(self.damage)},
                {"type": "text", "text": f"to {self.enemy_type.description} with Missiles and Super Missiles"},
            ]


can_damage_metroid_no_ammo = Has(ItemName.IceBeam) | can_beam_burst
# For when Beam Burst alone is too tight on aeion, but you can supplement with Ice Beam damage
can_beam_burst_and_ice_beam = Has(ItemName.IceBeam) & can_beam_burst


def can_damage_weak_metroid(health: int):
    return can_damage_metroid_no_ammo | CanDamageWithMissiles(health, EnemyType.WEAK_METROID)


can_combat_alpha = can_damage_metroid_no_ammo | can_any_missile  # Farm the projectiles
can_combat_evolved_alpha = can_damage_weak_metroid(2000)
can_combat_gamma = can_damage_metroid_no_ammo | can_any_missile
can_combat_evolved_gamma = can_damage_weak_metroid(2500)

# Honestly fine as long as you can farm missiles with grapple
can_combat_zeta = Or(can_damage_metroid_no_ammo, Has(ItemName.GrappleBeam) & can_any_missile)
can_combat_evolved_zeta = can_combat_zeta

can_dodge_omega = HasAll(ItemName.SpaceJump, ItemName.MorphBall)
can_damage_omega_with_missiles = can_any_missile & HasAny(ItemName.IceBeam, ItemName.PlasmaBeam)  # Farm the rocks
can_combat_omega = And(
    can_dodge_omega,
    # Ice can break the armor and damage the omega, but it's a lot of HP to chew through
    can_beam_burst | can_damage_omega_with_missiles,
    # No counter sequence until you break the armor, but can supplement with ice beam
    Or(can_beam_burst_and_ice_beam, can_power_bomb, can_damage_omega_with_missiles, Has(ItemName.PlasmaBeam)),
)
can_combat_evolved_omega = can_combat_omega
