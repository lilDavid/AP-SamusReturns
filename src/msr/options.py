from dataclasses import dataclass

from Options import PerGameCommonOptions, Range


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


@dataclass
class SamusReturnsOptions(PerGameCommonOptions):
    dna_available: MetroidDnaAvailable
    dna_required: MetroidDnaRequired
