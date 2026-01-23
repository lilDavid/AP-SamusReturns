from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, OptionGroup, PerGameCommonOptions, Range, StartInventoryPool


class LogicTrick(Choice):
    option_disable = 0
    default = option_disable


# Game options
class MetroidDnaAvailable(Range):
    display_name = "Metroid DNA Available"
    range_start = 0
    range_end = 39
    default = 10


class MetroidDnaRequired(Range):
    display_name = "Metroid DNA Required"
    range_start = 0
    range_end = 39
    default = 10


class WallJump(LogicTrick):
    display_name = "Wall Jump"
    option_enable = 1


class IBJ(LogicTrick):
    display_name = "Infinite Bomb Jump"
    option_double = 1
    option_vertical = 2


# Cosmetics
class RoomNames(DefaultOnToggle):
    display_name = "Display Room Names"


msr_option_groups = [
    OptionGroup(
        "Logic",
        [
            WallJump,
            IBJ,
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

    # Cosmetic
    display_room_names: RoomNames

    # Item & location options
    start_inventory_from_pool: StartInventoryPool
