from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import And, CanReachLocation, Has, HasAll, HasAny, Or, Rule, True_
from typing_extensions import override

from .data.constants import GAME_NAME
from .data.region_data import Door
from .items import ItemName
from .options import IBJ, DamageBoost, Knowledge, LogicTrick, Movement, WallJump

if TYPE_CHECKING:
    from . import SamusReturnsWorld

# TODO: Ammo logic


@dataclass
class HasDna(Rule["SamusReturnsWorld"], game=GAME_NAME):
    @override
    def _instantiate(self, world: SamusReturnsWorld) -> Rule.Resolved:
        return Has(ItemName.MetroidDna, world.options.dna_required.value).resolve(world)


def can_trick(trick: type[LogicTrick], difficulty: int):
    return True_(options=[OptionFilter(trick, difficulty, "ge")])


def can_damage_boost(damage_boost: int):
    return can_trick(DamageBoost, damage_boost)


def has_knowledge(knowledge: int):
    return can_trick(Knowledge, knowledge)


def can_movement(movement: int):
    return can_trick(Movement, movement)


def can_wall_jump(wall_jump: int):
    return can_trick(WallJump, wall_jump)


can_bomb = HasAll(ItemName.MorphBall, ItemName.Bomb)
can_power_bomb = HasAll(ItemName.MorphBall, ItemName.PowerBomb)
can_bomb_block = can_bomb | can_power_bomb


def can_ibj(ibj: int):
    return can_trick(IBJ, ibj) & can_bomb


can_beam_block_through_tunnel = Or(Has(ItemName.WaveBeam), can_bomb_block, can_movement(Movement.option_enable))
can_beam_block_through_fan_tunnel = Or(Has(ItemName.WaveBeam), can_power_bomb, can_movement(Movement.option_enable))

can_spider = HasAll(ItemName.MorphBall, ItemName.SpiderBall)
can_spider_boost = HasAll(ItemName.MorphBall, ItemName.SpiderBall, ItemName.PowerBomb)
can_spider_boost_underwater = And(can_spider_boost, has_knowledge(Knowledge.option_enable), Has(ItemName.GravitySuit))
can_fly_vertical = Or(Has(ItemName.SpaceJump), can_spider_boost, can_ibj(IBJ.option_vertical))
can_fly = Or(Has(ItemName.SpaceJump), can_ibj(IBJ.option_diagonal))
can_climb_wall = can_spider | can_fly_vertical

can_high_jump = Or(Has(ItemName.HighJumpBoots), can_ibj(IBJ.option_double), can_fly_vertical)
can_high_ledge = can_climb_wall | can_high_jump
can_underwater_high_jump = Or(Has(ItemName.GravitySuit) & can_high_jump, can_spider_boost_underwater)

# Needs ~hi-jump height to break but not to access the tunnel
can_medium_bomb_block = Or(can_high_ledge & can_bomb, can_power_bomb)

can_short_shaft = can_high_ledge | can_wall_jump(WallJump.option_simple)
can_climb_shaft = can_wall_jump(WallJump.option_simple) | can_climb_wall

can_any_missile = HasAny(ItemName.MissileLauncher, ItemName.SuperMissile)
can_damage_tough_enemy = Or(
    HasAny(ItemName.MissileLauncher, ItemName.SuperMissile, ItemName.BeamBurst, ItemName.ScrewAttack),
    can_power_bomb,
)
can_damage_metroid = HasAny(ItemName.MissileLauncher, ItemName.SuperMissile, ItemName.BeamBurst, ItemName.IceBeam)


def can_gamma_metroid(*arenas: str):
    return And(
        *(CanReachLocation(arena) for arena in arenas),
        can_damage_metroid,
    )


can_blobthrower = Has(ItemName.BeamBurst) | can_power_bomb
can_tunnel_steel_orb = Or(
    Has(ItemName.BeamBurst) & can_beam_block_through_tunnel,
    can_power_bomb,
)

door_rules = {
    Door.Open: True_(),
    Door.Normal: True_(),  # Player always has a weapon to open this with (power beam can't be randomized)
    Door.Charge: Has(ItemName.ChargeBeam),
    Door.Missile: can_any_missile,
    Door.Super: Has(ItemName.SuperMissile),
    Door.PowerBomb: can_power_bomb,
    Door.MorphTunnel: Has(ItemName.MorphBall),
    Door.Gigadora: Has(ItemName.SpazerBeam),
    Door.Gryncore: Has(ItemName.PlasmaBeam),
    Door.Taramarga: Has(ItemName.WaveBeam),
    Door.Elevator: True_(),
}
