from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, OptionGroup, PerGameCommonOptions, Range, StartInventoryPool, Toggle


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


# Item pool
class ReserveTankShuffle(Toggle):
    """
    Include the Energy, Missile, and Aeion Reserve Tanks in the item pool.
    """

    display_name = "Shuffle Reserve Tanks"


class ScanPulseStart(DefaultOnToggle):
    """Start with Scan Pulse."""

    display_name = "Starting Scan Pulse"


class WallJump(LogicTrick):
    """
    Jump off of walls in midair.

    Disable: Wall jumping will not be required by logic
    Simple: Logic can expect wall jumping to high ledges and up shafts
    Advanced: Logic can expect wall jumping into tight spaces
    """

    display_name = "Wall Jump"
    option_simple = 1
    option_advanced = 2


class IBJ(LogicTrick):
    """
    Fly by bomb jumping in midair.

    Disable: Bomb jumping in midair will not be required by logic
    Double: Bomb jump in midair once, usually unmorphing in midair to grab ledges
    Vertical: Infinite bomb jump straight up to gain great height
    Diagonal: IBJ off the sides of bombs to fly at angles
    """

    display_name = "Infinite Bomb Jump"
    option_double = 1
    option_vertical = 2
    option_diagonal = 3


class DamageBoost(LogicTrick):
    """
    Taking damage and knockback to gain distance, or otherwise deliberately as part of navigation.
    """

    display_name = "Damage Boost"
    option_enable = 1


class Knowledge(LogicTrick):
    """
    Tricks that require knowledge of how the game works.
    """

    display_name = "Knowledge"
    option_enable = 1


class Movement(LogicTrick):
    """
    Miscellaneous movement tricks not encompassed by other logic options.
    """

    display_name = "Movement"
    option_enable = 1


# Game Patches
class TanksRefillAmmo(Toggle):
    """
    Makes collecting a tank refill its ammo to full capacity. In vanilla, only Energy and Aeion get
    refilled to maximum capacity.
    """

    display_name = "Tanks Refill Ammo"


# Cosmetics
class RoomNames(DefaultOnToggle):
    """
    Display the names of rooms at the bottom of the touch screen map
    """

    display_name = "Display Room Names"


class PickupModels(Choice):
    """
    How to display pickups.

    Full: Pickups for other Metroid games appear as the matching item
    Native: Pickups for other Metroid: Samus Returns players appear as themselves
    Local: Pickups for other players appear as AP items; pickups for yourself appear as usual
    Hidden: All pickups (including your own!) look the same
    """

    display_name = "Pickup Models"
    option_full = 0
    option_native = 1
    option_local = 2
    option_hidden = 3
    default = option_full


class ApItemModels(Choice):
    """
    How to display external "AP Items."

    Progression: Progression items are RDV logos, and non-progression items look like Nothing items
    Generic: All AP items are RDV logos
    """

    display_name = "AP Item Models"
    option_progression = 1
    option_generic = 2
    default = option_progression


msr_option_groups = [
    OptionGroup(
        "Item Pool",
        [
            ReserveTankShuffle,
            ScanPulseStart,
        ],
    ),
    OptionGroup(
        "Logic",
        [
            WallJump,
            IBJ,
            DamageBoost,
            Knowledge,
            Movement,
        ],
    ),
    OptionGroup(
        "Game Patches",
        [
            TanksRefillAmmo,
        ],
    ),
    OptionGroup(
        "Cosmetic",
        [
            RoomNames,
            PickupModels,
            ApItemModels,
        ],
    ),
]


@dataclass
class SamusReturnsOptions(PerGameCommonOptions):
    # Game options
    dna_available: MetroidDnaAvailable
    dna_required: MetroidDnaRequired

    # Item pool
    shuffle_reserve_tanks: ReserveTankShuffle
    starting_scan_pulse: ScanPulseStart

    # Logic
    wall_jump: WallJump
    infinite_bomb_jump: IBJ
    damage_boost: DamageBoost
    knowledge: Knowledge
    movement: Movement

    # Game Patches
    tanks_refill_ammo: TanksRefillAmmo

    # Cosmetic
    display_room_names: RoomNames
    pickup_models: PickupModels
    ap_item_models: ApItemModels

    # Item & location options
    start_inventory_from_pool: StartInventoryPool
