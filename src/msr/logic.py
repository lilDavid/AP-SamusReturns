from enum import StrEnum

from BaseClasses import CollectionState

from .items import ItemName
from .options import IBJ, WallJump

# TODO: Ammo logic


class Trick(StrEnum):
    WallJump = "wall_jump"
    IBJ = "infinite_bomb_jump"


def get_option(state: CollectionState, player: int, option: str):
    world = state.multiworld.worlds[player]
    return getattr(world.options, option)


def can_trick(state: CollectionState, player: int, trick: Trick, difficulty: int) -> bool:
    return get_option(state, player, trick) >= difficulty


def can_bomb(state: CollectionState, player: int):
    return state.has_all((ItemName.MorphBall, ItemName.Bomb), player)


def can_power_bomb(state: CollectionState, player: int):
    return state.has_all((ItemName.MorphBall, ItemName.PowerBomb), player)


def can_bomb_block(state: CollectionState, player: int):
    return can_bomb(state, player) or can_power_bomb(state, player)


def can_spider(state: CollectionState, player: int):
    return state.has_all((ItemName.MorphBall, ItemName.SpiderBall), player)


def can_wall_jump(state: CollectionState, player: int, wall_jump: int):
    return can_trick(state, player, Trick.WallJump, WallJump.option_enable)


def can_ibj(state: CollectionState, player: int, ibj: int):
    return can_trick(state, player, Trick.IBJ, ibj) and can_bomb(state, player)


def can_spider_boost(state: CollectionState, player: int):
    return state.has_all((ItemName.MorphBall, ItemName.SpiderBall, ItemName.PowerBomb), player)


def can_fly_straight_up(state: CollectionState, player: int):
    return (
        state.has(ItemName.SpaceJump, player)
        or can_spider_boost(state, player)
        or can_ibj(state, player, IBJ.option_vertical)
    )


def can_climb_wall(state: CollectionState, player: int):
    return can_spider(state, player) or can_fly_straight_up(state, player)


def can_high_ledge(state: CollectionState, player: int):
    return (
        state.has(ItemName.HighJumpBoots, player)
        or can_ibj(state, player, IBJ.option_double)
        or can_climb_wall(state, player)
    )


def can_climb_shaft(state: CollectionState, player: int):
    return can_wall_jump(state, player, WallJump.option_enable) or can_climb_wall(state, player)


def can_any_missile(state: CollectionState, player: int):
    return state.has_any((ItemName.MissileLauncher, ItemName.SuperMissile), player)


def can_damage_metroid(state: CollectionState, player: int):
    return state.has_any(
        (ItemName.MissileLauncher, ItemName.SuperMissile, ItemName.BeamBurst, ItemName.IceBeam), player
    )
