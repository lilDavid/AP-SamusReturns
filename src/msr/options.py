from dataclasses import dataclass

from Options import DefaultOnToggle, OptionGroup, PerGameCommonOptions, Range


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


# Cosmetics
class RoomNames(DefaultOnToggle):
    display_name = "Display Room Names"


msr_option_groups = [
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

    # Cosmetic
    display_room_names: RoomNames
