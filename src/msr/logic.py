from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import And, False_, Has, HasAll, HasAny, Or, Rule, True_
from typing_extensions import override

from .data import GAME_NAME
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


@dataclass
class Trick(Rule["SamusReturnsWorld"], game=GAME_NAME):
    trick: type[LogicTrick]
    difficulty: int

    @override
    def _instantiate(self, world: SamusReturnsWorld) -> Rule.Resolved:
        normal_rule = True_(options=[OptionFilter(self.trick, self.difficulty, "ge")])
        if not world.is_universal_tracker():
            return normal_rule.resolve(world)

        from .settings import TrackerTrickLogic

        sequence_break_rule = Has(world.glitches_item_name)
        if world.settings.universal_tracker_settings.show_tricks == TrackerTrickLogic.NEXT_LEVEL:
            sequence_break_rule.options = [OptionFilter(self.trick, self.difficulty - 1, "ge")]
        return (normal_rule | sequence_break_rule).resolve(world)


def can_damage_boost(damage_boost: int):
    return Trick(DamageBoost, damage_boost)


def has_knowledge(knowledge: int):
    return Trick(Knowledge, knowledge)


def can_movement(movement: int):
    return Trick(Movement, movement)


def can_wall_jump(wall_jump: int):
    return Trick(WallJump, wall_jump)


can_bomb = HasAll(ItemName.MorphBall, ItemName.Bomb)
can_power_bomb = HasAll(ItemName.MorphBall, ItemName.PowerBomb)
can_bomb_block = can_bomb | can_power_bomb


def can_ibj(ibj: int):
    return Trick(IBJ, ibj) & can_bomb


can_beam_block_through_tunnel = Or(Has(ItemName.WaveBeam), can_bomb_block, can_movement(Movement.option_enable))
can_beam_block_through_fan_tunnel = Or(Has(ItemName.WaveBeam), can_power_bomb, can_movement(Movement.option_enable))

can_spider = HasAll(ItemName.MorphBall, ItemName.SpiderBall)
can_spider_boost = HasAll(ItemName.MorphBall, ItemName.SpiderBall, ItemName.PowerBomb)
can_spider_boost_underwater = And(can_spider_boost, has_knowledge(Knowledge.option_enable) | Has(ItemName.GravitySuit))
can_cross_pitfall_bridge = Or(Has(ItemName.PhaseDrift), has_knowledge(Knowledge.option_enable) & can_spider_boost)

can_fly_vertical = Or(Has(ItemName.SpaceJump), can_spider_boost, can_ibj(IBJ.option_vertical))
can_fly_vertical_underwater = Or(Has(ItemName.GravitySuit) & can_fly_vertical, can_spider_boost_underwater)
can_fly = Or(Has(ItemName.SpaceJump), can_ibj(IBJ.option_diagonal))
can_climb_wall = can_spider | can_fly_vertical
can_climb_wall_underwater = Or(can_spider, Has(ItemName.GravitySuit) & can_fly_vertical)

can_high_jump = Or(Has(ItemName.HighJumpBoots), can_ibj(IBJ.option_double), can_fly_vertical)
can_high_ledge = can_spider | can_high_jump
can_high_underwater_ledge = Or(can_spider, Has(ItemName.GravitySuit) & can_high_jump)
can_underwater_high_jump = Or(Has(ItemName.GravitySuit) & can_high_jump, can_spider_boost_underwater)

# Needs ~hi-jump height to break but not to access the tunnel
can_high_bomb_block = Or(can_high_ledge & can_bomb, can_power_bomb)
can_bomb_block_near_ceiling = Or(
    can_spider & can_bomb_block,
    Has(ItemName.SpaceJump) & can_power_bomb,
    # IBJ alone is possible but super tricky
)

can_short_shaft = can_high_ledge | can_wall_jump(WallJump.option_simple)
can_climb_shaft = can_wall_jump(WallJump.option_simple) | can_climb_wall

can_any_missile = HasAny(ItemName.MissileLauncher, ItemName.SuperMissile)
can_damage_tough_enemy = Or(
    HasAny(ItemName.MissileLauncher, ItemName.SuperMissile, ItemName.BeamBurst, ItemName.ScrewAttack),
    can_power_bomb,
)
can_damage_metroid = HasAny(ItemName.MissileLauncher, ItemName.SuperMissile, ItemName.BeamBurst, ItemName.IceBeam)
can_blobthrower = Has(ItemName.BeamBurst) | can_power_bomb
can_tunnel_steel_orb = Or(
    Has(ItemName.BeamBurst) & can_beam_block_through_tunnel,
    can_power_bomb,
)

# Brief contact at least
can_thorns = Has(ItemName.LightningArmor) | can_damage_boost(DamageBoost.option_static)

# TODO: Proper combat logic. SJ seems required for no damage
can_combat_omega = And(
    can_damage_metroid,
    Has(ItemName.SpaceJump),
)

door_rules = {
    Door.Open: True_(),
    Door.Normal: True_(),  # Player always has a weapon to open this with (power beam can't be randomized)
    Door.Charge: Or(Has(ItemName.ChargeBeam), has_knowledge(Knowledge.option_enable) & Has(ItemName.BeamBurst)),
    Door.Missile: can_any_missile,
    Door.Super: Has(ItemName.SuperMissile),
    Door.PowerBomb: can_power_bomb,
    Door.MorphTunnel: Has(ItemName.MorphBall),
    Door.Gigadora: Has(ItemName.SpazerBeam),
    Door.Gryncore: Has(ItemName.PlasmaBeam),
    Door.Taramarga: Has(ItemName.WaveBeam),
    Door.Elevator: True_(),
    Door.Locked: False_(),
}
