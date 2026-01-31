from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, OptionGroup, PerGameCommonOptions, Range, StartInventoryPool


class LogicTrick(Choice):
    option_disable = 0
    default = option_disable


# Game options
class MetroidDnaAvailable(Range):
    """Amount of Metroid DNA in the item pool"""

    display_name = "Metroid DNA Available"
    range_start = 0
    range_end = 39
    default = 10


class MetroidDnaRequired(Range):
    """Amount of Metroid DNA required to fight the final boss"""

    display_name = "Metroid DNA Required"
    range_start = 0
    range_end = 39
    default = 10


class WallJump(LogicTrick):
    """
    Jump off of walls in midair.

    Disable: Wall jumping will not be required by logic
    Enable: Wall jumping may be required by logic
    """

    display_name = "Wall Jump"
    option_enable = 1


class IBJ(LogicTrick):
    """
    Fly by bomb jumping in midair.

    Disable: Bomb jumping in midair will not be required by logic
    Double: Logic may expect you to bomb jump in midair at most once
    Vertical: Logic may expect you to infinite bomb jump directly up
    """

    display_name = "Infinite Bomb Jump"
    option_double = 1
    option_vertical = 2
    option_diagonal = 3


class DamageBoost(LogicTrick):
    display_name = "Damage Boost"
    option_enable = 1


class Movement(LogicTrick):
    """
    Miscellaneous movement tricks not encompassed by other logic options.
    """

    display_name = "Movement"
    option_enable = 1


# Cosmetics
class RoomNames(DefaultOnToggle):
    display_name = "Display Room Names"


msr_option_groups = [
    OptionGroup(
        "Logic",
        [
            WallJump,
            IBJ,
            Movement,
        ],
    ),
    OptionGroup(
        "Cosmetic",
        [
            RoomNames,
        ],
    ),
]


@dataclass
class SamusReturnsOptions(PerGameCommonOptions):
    # Game options
    dna_available: MetroidDnaAvailable
    dna_required: MetroidDnaRequired

    # Logic
    wall_jump: WallJump
    infinite_bomb_jump: IBJ
    damabe_boost: DamageBoost
    movement: Movement

    # Cosmetic
    display_room_names: RoomNames

    # Item & location options
    start_inventory_from_pool: StartInventoryPool
