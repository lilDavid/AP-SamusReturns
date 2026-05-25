from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import And, False_, Has, HasAll, HasAny, Or, Rule, True_
from typing_extensions import override

from .data import GAME_NAME
from .data.region_data import Door
from .items import ItemName
from .options import IBJ, DamageBoost, Knowledge, LogicTrick, MorphExtend, Movement, SuperJump, WallJump

if TYPE_CHECKING:
    from . import SamusReturnsWorld

# TODO: Ammo logic
# TODO: Separate out midair morph tricks
# TODO: Separate vertical and diagonal IBJ tricks (so complex verticals and double diags are different)


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


def can_super_jump(super_jump: int):
    return Trick(SuperJump, super_jump)


def can_morph_extend(morph_extend: int):
    return Trick(MorphExtend, morph_extend)


can_super_jump_morph_extend = can_super_jump(SuperJump.option_medium) & can_morph_extend(MorphExtend.option_medium)

can_bomb = HasAll(ItemName.MorphBall, ItemName.Bomb)
can_power_bomb = HasAll(ItemName.MorphBall, ItemName.PowerBomb)
can_bomb_block = can_bomb | can_power_bomb


def can_ibj(ibj: int):
    return Trick(IBJ, ibj) & can_bomb


can_beam_burst = Has(ItemName.BeamBurst) & HasAny(ItemName.WaveBeam, ItemName.SpazerBeam, ItemName.PlasmaBeam)

can_beam_block_through_tunnel = Or(Has(ItemName.WaveBeam), can_bomb_block, can_movement(Movement.option_simple))
can_beam_block_through_fan_tunnel = Or(Has(ItemName.WaveBeam), can_power_bomb, can_movement(Movement.option_simple))

can_spider = HasAll(ItemName.MorphBall, ItemName.SpiderBall)
can_spider_boost = HasAll(ItemName.MorphBall, ItemName.SpiderBall, ItemName.PowerBomb)
can_spider_boost_underwater = And(can_spider_boost, has_knowledge(Knowledge.option_simple) | Has(ItemName.GravitySuit))
can_spider_boost_through_pitfalls = has_knowledge(Knowledge.option_simple) & can_spider_boost
can_cross_pitfall_bridge = Or(Has(ItemName.PhaseDrift), can_spider_boost_through_pitfalls)

can_fly_vertical = Or(Has(ItemName.SpaceJump), can_spider_boost, can_ibj(IBJ.option_vertical))
can_fly_vertical_underwater = Or(Has(ItemName.GravitySuit) & can_fly_vertical, can_spider_boost_underwater)
can_fly = Or(Has(ItemName.SpaceJump), can_ibj(IBJ.option_diagonal))
can_climb_wall = can_spider | can_fly_vertical
can_climb_wall_underwater = Or(can_spider, Has(ItemName.GravitySuit) & can_fly_vertical)

# High Jump Boots-ish height
can_high_jump_no_grip = Or(Has(ItemName.HighJumpBoots), can_ibj(IBJ.option_double), can_fly_vertical)
can_high_jump = can_high_jump_no_grip | can_super_jump_morph_extend
can_high_ledge = can_spider | can_high_jump
can_high_underwater_ledge = Or(Has(ItemName.GravitySuit) & can_high_jump, can_spider)

# Super jumps alone fall just short of other methods
can_almost_high_jump = can_high_jump | can_super_jump(SuperJump.option_beginner)
can_almost_high_ledge = can_almost_high_jump | can_spider
can_almost_high_jump_gap = can_high_jump | can_super_jump(SuperJump.option_easy)
can_underwater_almost_high_jump = Or(Has(ItemName.GravitySuit) & can_almost_high_jump, can_spider_boost_underwater)
can_underwater_almost_high_ledge = Or(Has(ItemName.GravitySuit) & can_almost_high_jump, can_spider)

# Basically almost-high-jump but with water added
can_jump_underwater = HasAny(ItemName.HighJumpBoots, ItemName.GravitySuit) | can_super_jump(SuperJump.option_easy)


def can_high_super_jump(super_jump: int = SuperJump.option_beginner):
    return Has(ItemName.HighJumpBoots) & can_super_jump(super_jump)


def can_high_super_jump_or_climb(super_jump: int = SuperJump.option_beginner):
    return can_high_super_jump(super_jump) | can_spider


can_almost_higher_jump = Or(
    can_high_super_jump(),
    Has(ItemName.HighJumpBoots) & can_ibj(IBJ.option_double),
    can_fly_vertical,
)
can_almost_higher_ledge = can_almost_higher_jump | can_spider

can_higher_jump = Or(
    can_high_super_jump(SuperJump.option_easy),
    Has(ItemName.HighJumpBoots) & can_ibj(IBJ.option_double),
    can_fly_vertical,
)
can_higher_ledge = can_higher_jump | can_spider

# Needs ~hi-jump height to break but not to access the tunnel
can_high_bomb_block = Or(can_high_ledge & can_bomb, can_power_bomb)
can_bomb_block_near_ceiling = Or(
    can_spider & can_bomb_block,
    Has(ItemName.SpaceJump) & can_power_bomb,
    # IBJ alone is possible but super tricky
)

can_shorter_shaft = can_wall_jump(WallJump.option_simple) | can_almost_high_ledge
can_short_shaft = can_wall_jump(WallJump.option_simple) | can_high_ledge
can_climb_shaft = can_wall_jump(WallJump.option_simple) | can_climb_wall
can_climb_elevated_shaft = Or(
    can_spider,
    can_climb_shaft & can_high_jump_no_grip,
    can_climb_shaft & can_super_jump(SuperJump.option_easy),
)

can_any_missile = HasAny(ItemName.MissileLauncher, ItemName.SuperMissile)
can_damage_tough_enemy_ranged = Or(can_any_missile, can_beam_burst, can_power_bomb)
can_damage_tough_enemy = Or(can_damage_tough_enemy_ranged, Has(ItemName.ScrewAttack))
can_damage_metroid = Or(HasAny(ItemName.MissileLauncher, ItemName.SuperMissile, ItemName.IceBeam), can_beam_burst)
can_blobthrower = can_beam_burst | can_power_bomb
can_tunnel_steel_orb = Or(can_beam_burst & can_beam_block_through_tunnel, can_power_bomb)

# Brief contact at least
can_thorns = Has(ItemName.LightningArmor) | can_damage_boost(DamageBoost.option_static)
# Fleech swarms deactivate if you have Gravity Suit
can_fleech_swarm = HasAny(ItemName.LightningArmor, ItemName.GravitySuit)

# TODO: Proper combat logic. SJ and morph both seem required for no damage
can_combat_omega = can_damage_metroid & HasAll(ItemName.SpaceJump, ItemName.MorphBall)

door_rules = {
    Door.Open: True_(),
    Door.Normal: True_(),  # Player always has a weapon to open this with (power beam can't be randomized)
    Door.Charge: Or(Has(ItemName.ChargeBeam), has_knowledge(Knowledge.option_simple) & can_beam_burst),
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
