from rule_builder.rules import And, Has, HasAll, HasAny, Or

from ...items import ItemName
from ...logic import (
    can_any_missile,
    can_bomb,
    can_bomb_block,
    can_climb_shaft,
    can_climb_wall,
    can_damage_boost,
    can_damage_metroid,
    can_fly,
    can_fly_vertical,
    can_high_bomb_block,
    can_high_jump,
    can_high_ledge,
    can_ibj,
    can_movement,
    can_power_bomb,
    can_short_shaft,
    can_spider,
    can_spider_boost,
    can_spider_boost_underwater,
    can_thorns,
    door_rules,
    has_knowledge,
)
from ...options import IBJ, DamageBoost, Knowledge, Movement
from ..internal_names import AreaId
from ..room_names import Area3Exterior as Area3
from ..room_names import Area4Caves as Caves
from ..room_names import Area4Mines as Mines
from ..room_names import Area5Lobby as Area5
from . import AreaData, Door, EventData, ExitData, PickupData, RegionData, RoomData, Subregion

can_cross_purple_puddle = Or(
    Has(ItemName.SpaceJump),
    can_spider,
    # FIXME: Longest requires exactly one e-tank, and repeated dips are rather painful
    can_damage_boost(DamageBoost.option_static),
)
can_traverse_transit_tunnel = can_spider | can_thorns
can_escape_evolved_alpha = can_high_jump | Has(ItemName.GravitySuit)
can_cross_caves_gamma_hazards = Or(
    Has(ItemName.GrappleBeam),
    can_spider_boost,
    can_thorns,
)

can_escape_spazer_chamber = door_rules[Door.Gigadora] & can_high_ledge
can_escape_pink_crystals = Or(
    Has(ItemName.SpaceJump),
    can_ibj(IBJ.option_vertical),
    # There are spikes at the top of the room but there's a gap so
    # you can either do the damage boost or squeeze in
    And(
        can_spider_boost,
        Or(
            can_damage_boost(DamageBoost.option_static),
            has_knowledge(Knowledge.option_enable),
        ),
    ),
)
can_escape_evolved_gamma = can_high_ledge

area_4_caves_data = AreaData(
    name="Area 4 Central Caves",
    id=AreaId.AREA_4_CAVES,
    rooms=[
        RoomData(
            Caves.CavesIntersectionTerminal,
            id="collision_camera_001",
            regions=[
                RegionData(
                    "Center",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Bottom"),
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Alcove"),
                            access_rule=HasAny(ItemName.MorphBall, ItemName.Hatchling),
                        ),
                        ExitData(
                            Door.Normal,
                            Caves.TransportArea3Mines.subregion("Top Left"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Caves.FleechSwarmCave,
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.Gryncore,
                            Caves.CrumbleCatwalk,
                            access_rule=HasAll(ItemName.MorphBall, ItemName.GrappleBeam),
                        ),
                    ],
                ),
                RegionData(
                    "Bottom",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Center"),
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.Open,
                            Caves.AmethystAltars,
                        ),
                        ExitData(
                            Door.Charge,
                            Caves.TransitTunnel.subregion("Top"),
                        ),
                    ],
                ),
                RegionData(
                    "Alcove",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Center"),
                            access_rule=HasAny(ItemName.MorphBall, ItemName.Hatchling),
                        ),
                        ExitData(
                            Door.Gigadora,
                            Caves.LavaPond.subregion("Arena"),
                        ),
                    ],
                ),
                RegionData(
                    "Pickup",
                    exits=[
                        ExitData(
                            Door.Gigadora,
                            Caves.TransportArea3Mines.subregion("Top Left"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Center"),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=Has(ItemName.MorphBall),
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Caves.SpazerBeam,
            id="collision_camera_003",
            regions=[
                RegionData(
                    exits=[
                        # ExitData(
                        #     Door.Locked,
                        #     Caves.AmethystAltars,
                        # ),
                        ExitData(
                            Door.Gigadora,
                            Caves.AmethystAltars,
                            access_rule=can_high_ledge,
                        ),
                    ],
                    pickups=[
                        PickupData(),
                    ],
                )
            ],
        ),
        RoomData(
            Caves.CrumbleCatwalk,
            id="collision_camera_004",
            regions=[
                RegionData(
                    exits=[
                        # ExitData(
                        #     Door.Locked,
                        #     Caves.CavesIntersectionTerminal.subregion("Center"),
                        # ),
                        ExitData(
                            Door.MorphTunnel,
                            Caves.CavesIntersectionTerminal.subregion("Center"),
                            access_rule=Has(ItemName.GrappleBeam),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=And(
                                Has(ItemName.MorphBall),
                                Or(
                                    And(
                                        Has(ItemName.SpaceJump) | can_spider,
                                        Has(ItemName.GrappleBeam),
                                    ),
                                    And(
                                        Has(ItemName.PhaseDrift),
                                        Or(
                                            Has(ItemName.GrappleBeam),
                                            can_spider_boost,
                                            can_ibj(IBJ.option_vertical),
                                        ),
                                    ),
                                ),
                            )
                        )
                    ],
                )
            ],
        ),
        RoomData(
            Caves.LavaPond,
            id="collision_camera_005",
            regions=[
                RegionData(
                    "Arena",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Caves.CavesIntersectionTerminal.subregion("Alcove"),
                            access_rule=Has(ItemName.VariaSuit),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Exit"),
                            access_rule=HasAll(ItemName.VariaSuit, ItemName.GrappleBeam),
                        ),
                    ],
                ),
                RegionData(
                    "Exit",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Arena"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Caves.GammaAccessS.subregion("Right"),
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Caves.TransportArea3Mines,
            id="collision_camera_006",
            regions=[
                RegionData(
                    "Top",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Left Seal"),
                            access_rule=can_cross_purple_puddle,
                        ),
                        ExitData(
                            Door.Elevator,
                            Area3.TransportArea4.subregion("Transport"),
                            access_rule=can_cross_purple_puddle,
                        ),
                    ],
                    events=[
                        EventData(
                            "Pickup Grapple Block",
                            access_rule=HasAll(ItemName.MorphBall, ItemName.GrappleBeam),
                        )
                    ],
                ),
                RegionData(
                    "Left Seal",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Top"),
                            access_rule=can_cross_purple_puddle,
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Right Seal"),
                            access_rule=can_cross_purple_puddle,
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Top Left"),
                            access_rule=Or(
                                can_fly_vertical,
                                Has(ItemName.GrappleBeam) & can_spider,
                            ),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Caves.TransitTunnel.subregion("Middle"),
                            access_rule=Has(Caves.TransportArea3Mines.location("Left Grapple Block")),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=And(
                                HasAll(
                                    Caves.TransportArea3Mines.location("Pickup Grapple Block"),
                                    ItemName.MorphBall,
                                ),
                                can_cross_purple_puddle,
                            ),
                        )
                    ],
                    events=[
                        EventData(
                            "Left Grapple Block",
                            access_rule=HasAll(ItemName.SuperMissile, ItemName.GrappleBeam),
                        )
                    ],
                ),
                RegionData(
                    "Top Left",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Left Seal"),
                        ),
                        ExitData(
                            Door.Normal,
                            Caves.CavesIntersectionTerminal.subregion("Center"),
                        ),
                        ExitData(
                            Door.Gigadora,
                            Caves.CavesIntersectionTerminal.subregion("Pickup"),
                            access_rule=can_fly_vertical,
                        ),
                    ],
                ),
                RegionData(
                    "Right Seal",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Left Seal"),
                            access_rule=Has(ItemName.SpaceJump) | can_spider,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Top"),
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Bottom"),
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Mines Transport"),
                            # Grapple block is already moved for us
                        ),
                        # ExitData(
                        #     Door.Charge,
                        #     Caves.TransportArea5,
                        #     # Blocked by grapple block
                        # ),
                    ],
                ),
                RegionData(
                    "Mines Transport",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Right Seal"),
                        ),
                        ExitData(
                            Door.Elevator,
                            Mines.TransportCentralCaves,
                        ),
                    ],
                ),
                RegionData(
                    "Bottom",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Right Seal"),
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Bottom Left"),
                            access_rule=can_spider,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Caves.VenomousPond.subregion("Right"),
                            access_rule=can_bomb_block,
                        ),
                    ],
                ),
                RegionData(
                    "Bottom Left",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Bottom"),
                            access_rule=can_spider,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Caves.TransportArea5.subregion("Upper"),
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Caves.Alpha2,
            id="collision_camera_007",
            regions=[
                # The anti-softlock logic for the missile pickup is weird because of this room's
                # layout, but we can just gate everything under the pitfall blocks behind the
                # door's access rule instead of the usual subregion connection
                RegionData(
                    exits=[
                        ExitData(
                            Door.Normal,
                            Caves.Alpha2Access.subregion("Upper"),
                            access_rule=can_escape_evolved_alpha,
                        )
                    ],
                    pickups=[
                        PickupData(
                            "Missile",
                            access_rule=can_short_shaft | can_escape_evolved_alpha,
                        ),
                        PickupData(
                            "Evolved Alpha Metroid",
                            access_rule=can_damage_metroid & can_escape_evolved_alpha,
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Caves.TransitTunnel,
            id="collision_camera_010",
            regions=[
                RegionData(
                    "Top",
                    exits=[
                        ExitData(
                            Door.Charge,
                            Caves.CavesIntersectionTerminal.subregion("Bottom"),
                        ),
                        # ExitData(
                        #     Door.Locked,
                        #     Caves.Alpha2Access.subregion("Upper"),
                        # ),
                        ExitData(
                            Door.Charge,
                            Subregion("Middle"),
                            access_rule=can_traverse_transit_tunnel,
                        ),
                    ],
                ),
                RegionData(
                    "Middle",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Top"),
                            access_rule=can_traverse_transit_tunnel,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Bottom"),
                            access_rule=Or(
                                can_power_bomb,
                                And(
                                    HasAll(
                                        Caves.TransportArea3Mines.location("Left Grapple Block"),
                                        ItemName.GrappleBeam,
                                    ),
                                    can_bomb,
                                ),
                            ),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=can_traverse_transit_tunnel,
                        )
                    ],
                ),
                RegionData(
                    "Bottom",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Middle"),
                            access_rule=can_bomb,
                        ),
                        ExitData(
                            Door.Gigadora,
                            Caves.Alpha2Access.subregion("Lower"),
                            access_rule=can_bomb,
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Caves.FleechSwarmCave,
            id="collision_camera_011",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Caves.CavesIntersectionTerminal.subregion("Center"),
                            access_rule=can_bomb,
                        )
                    ],
                    pickups=[
                        PickupData(
                            access_rule=HasAll(ItemName.MorphBall, ItemName.LightningArmor),
                        )
                    ],
                )
            ],
        ),
        RoomData(
            Caves.HostileHangout,
            id="collision_camera_012",
            regions=[],  # Gamma doesn't escape
        ),
        RoomData(
            Caves.Gamma,
            id="collision_camera_013",
            regions=[
                RegionData(
                    "Arena",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Caves.GammaAccessN.subregion("Right"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Lower"),
                            access_rule=can_bomb_block,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Gamma Metroid",
                            access_rule=can_damage_metroid,
                        ),
                    ],
                ),
                RegionData(
                    "Lower",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Arena"),
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.Open,
                            Caves.GammaAccessS.subregion("Top"),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Tunnel",
                            access_rule=HasAll(ItemName.MorphBall, ItemName.MissileLauncher) & can_fly_vertical,
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Caves.GammaAccessS,
            id="collision_camera_014",
            regions=[
                RegionData(
                    "Right",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Caves.LavaPond.subregion("Exit"),
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Left"),
                            access_rule=can_cross_caves_gamma_hazards,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=Or(
                                can_power_bomb,
                                can_bomb & Has(ItemName.LightningArmor),
                                HasAll(ItemName.Hatchling, ItemName.MorphBall),
                            )
                        )
                    ],
                ),
                RegionData(
                    "Left",
                    exits=[
                        ExitData(
                            Door.Open,
                            Caves.OutwardClimb,
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Right"),
                            access_rule=can_cross_caves_gamma_hazards,
                        ),
                    ],
                ),
                RegionData(
                    "Top",
                    exits=[
                        ExitData(
                            Door.Open,
                            Caves.Gamma.subregion("Lower"),
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Right"),
                            access_rule=HasAll(ItemName.GrappleBeam, ItemName.MorphBall),
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Caves.OutwardClimb,
            id="collision_camera_015",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Open,
                            Caves.GammaAccessS.subregion("Right"),
                        ),
                        ExitData(
                            Door.Open,
                            Caves.GammaAccessN.subregion("Right"),
                        ),
                    ]
                )
            ],
        ),
        RoomData(
            Caves.AmethystAltars,
            id="collision_camera_016",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Open,
                            Caves.CavesIntersectionTerminal.subregion("Bottom"),
                        ),
                        ExitData(
                            Door.Missile,
                            Caves.SpazerBeam,
                            access_rule=can_escape_spazer_chamber,
                        ),
                        # ExitData(
                        #     Door.Locked,
                        #     Caves.SpazerBeam,
                        # ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=And(
                                can_any_missile,
                                Or(
                                    Has(ItemName.IceBeam),
                                    # Drop down and shoot the block in midair
                                    can_fly_vertical & can_movement(Movement.option_enable),
                                ),
                            ),
                        )
                    ],
                )
            ],
        ),
        RoomData(
            Caves.GammaAccessN,
            id="collision_camera_018",
            regions=[
                RegionData(
                    "Left",
                    exits=[
                        ExitData(
                            Door.Open,
                            Caves.OutwardClimb,
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Right"),
                            access_rule=can_cross_caves_gamma_hazards,
                        ),
                    ],
                ),
                RegionData(
                    "Right",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Caves.Gamma.subregion("Arena"),
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Left"),
                            access_rule=can_cross_caves_gamma_hazards,
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Caves.Alpha2Access,
            id="collision_camera_019",
            regions=[
                RegionData(
                    "Lower",
                    exits=[
                        # ExitData(
                        #     Door.Locked,
                        #     Caves.TransitTunnel.subregion("Bottom"),
                        # ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Upper"),
                        ),
                    ],
                ),
                RegionData(
                    "Upper",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Lower"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Caves.Alpha2,
                        ),
                        ExitData(
                            Door.Normal,
                            Caves.TransitTunnel.subregion("Top"),
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Caves.VenomousPond,
            id="collision_camera_022",
            regions=[
                RegionData(
                    "Right",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Caves.TransportArea3Mines.subregion("Bottom"),
                            access_rule=can_fly_vertical,
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Left"),
                            access_rule=Has(ItemName.SpaceJump) | can_spider_boost,
                        ),
                    ],
                ),
                RegionData(
                    "Left",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Caves.TransportArea5.subregion("Lower"),
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Right"),
                            access_rule=Has(ItemName.SpaceJump) | can_spider_boost,
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Caves.TransportArea5,
            id="collision_camera_023",
            regions=[
                RegionData(
                    "Upper",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Caves.TransportArea3Mines.subregion("Bottom Left"),
                        ),
                        ExitData(
                            Door.Charge,
                            Caves.TransportArea3Mines.subregion("Right Seal"),
                            access_rule=HasAll(ItemName.MorphBall, ItemName.GrappleBeam),
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Lower"),
                            access_rule=Has(ItemName.ScrewAttack),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=HasAll(ItemName.MorphBall, ItemName.GrappleBeam, ItemName.SuperMissile),
                        )
                    ],
                ),
                RegionData(
                    "Lower",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Caves.VenomousPond.subregion("Left"),
                        ),
                        ExitData(
                            Door.Elevator,
                            Area5.TransportAreas4And6.subregion("Upper"),
                            access_rule=HasAll(ItemName.MorphBall, ItemName.GrappleBeam),
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Upper"),
                            access_rule=Has(ItemName.ScrewAttack),
                        ),
                    ],
                ),
            ],
        ),
    ],
)

area_4_mines_data = AreaData(
    name="Area 4 Crystal Mines",
    id=AreaId.AREA_4_MINES,
    rooms=[
        RoomData(
            Mines.MinesIntersectionTerminal,
            id="collision_camera_001",
            regions=[
                RegionData(
                    "Exit",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Bottom"),
                            access_rule=Has(ItemName.MorphBall) | can_short_shaft,
                        ),
                        ExitData(
                            Door.Open,
                            Mines.TsumuriTunnel,
                        ),
                    ],
                ),
                RegionData(
                    "Bottom",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Exit"),
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Save Station"),
                            access_rule=can_high_ledge,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Bottom",
                            access_rule=And(
                                can_bomb_block,
                                Has(ItemName.WaveBeam) | can_power_bomb,
                                HasAny(ItemName.PhaseDrift, ItemName.Hatchling),
                            ),
                        )
                    ],
                ),
                RegionData(
                    "Save Station",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Bottom"),
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Middle"),
                            access_rule=Has(ItemName.HighJumpBoots) | can_climb_wall,
                        ),
                        ExitData(
                            Door.Super,
                            Mines.GemstoneGorge.subregion("Bottom"),
                        ),
                    ],
                ),
                RegionData(
                    "Middle",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Save Station"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Mines.DualPondAlcove,
                            access_rule=can_power_bomb,
                        ),
                        ExitData(
                            Door.Gigadora,
                            Mines.LavaReservoir.subregion("Right"),
                        ),
                        ExitData(
                            Door.Missile,
                            Mines.SuperMissile,
                        ),
                    ],
                ),
                RegionData(
                    "Accessway",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Middle"),
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Top"),
                            access_rule=can_short_shaft,
                        ),
                        ExitData(
                            Door.Super,
                            Mines.SuperMissile,
                        ),
                    ],
                ),
                RegionData(
                    "Top",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Accessway"),
                        ),
                        ExitData(
                            Door.Open,
                            Mines.GreenCrystalDugout,
                            access_rule=can_high_ledge,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Top",
                            access_rule=And(
                                HasAll(ItemName.SuperMissile, ItemName.MorphBall),
                                Or(
                                    Has(ItemName.GrappleBeam),
                                    Has(ItemName.GravitySuit) & can_ibj(IBJ.option_vertical),
                                    can_spider_boost_underwater,
                                    # There's a weird underwater IBJ you can do without gravity but
                                    # I need more logic options for that
                                ),
                            ),
                        )
                    ],
                ),
            ],
        ),
        RoomData(
            Mines.SuperMissile,
            id="collision_camera_002",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Missile,
                            Mines.MinesIntersectionTerminal.subregion("Accessway"),
                        ),
                        ExitData(
                            Door.Super,
                            Mines.MinesIntersectionTerminal.subregion("Middle"),
                            access_rule=Or(
                                can_climb_wall,
                                can_high_jump & can_climb_shaft,
                            ),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=can_climb_wall,
                        )
                    ],
                )
            ],
        ),
        RoomData(
            Mines.PinkCrystalPreserve,
            id="collision_camera_003",
            regions=[
                RegionData(
                    "Top",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Bottom"),
                            access_rule=can_escape_pink_crystals,
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Pickup"),
                            access_rule=Has(ItemName.SpaceJump) | can_spider_boost,
                        ),
                    ],
                ),
                RegionData(
                    "Bottom",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Top"),
                            access_rule=can_escape_pink_crystals,
                        ),
                        ExitData(
                            Door.Normal,
                            Mines.Zeta,
                            access_rule=Or(
                                can_high_jump,
                                And(
                                    can_spider,
                                    # Spider around the opposite wall with either a ball jump or midair morph
                                    HasAny(ItemName.Bomb, ItemName.SpringBall) | can_movement(Movement.option_enable),
                                ),
                            ),
                        ),
                    ],
                ),
                RegionData(
                    "Pickup",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Bottom"),
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Top"),
                            access_rule=Has(ItemName.SpaceJump) | can_spider_boost,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=Has(ItemName.MorphBall) & can_fly_vertical,
                        )
                    ],
                ),
            ],
        ),
        RoomData(
            Mines.TransportCentralCaves,
            id="collision_camera_005",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Elevator,
                            Caves.TransportArea3Mines.subregion("Mines Transport"),
                        ),
                        ExitData(
                            Door.Charge,
                            Mines.MinesEntrance,
                        ),
                    ]
                )
            ],
        ),
        RoomData(
            Mines.LavaReservoir,
            id="collision_camera_006",
            regions=[
                RegionData(
                    "Right",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Mines.MinesIntersectionTerminal.subregion("Middle"),
                            access_rule=Has(ItemName.VariaSuit),
                        ),
                        ExitData(
                            Door.Normal,
                            Subregion("Left"),
                            access_rule=HasAll(ItemName.VariaSuit, ItemName.GravitySuit) & can_fly_vertical,
                        ),
                    ],
                ),
                RegionData(
                    "Left",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Subregion("Right"),
                            access_rule=HasAll(ItemName.VariaSuit, ItemName.GravitySuit),
                        ),
                        ExitData(
                            Door.Normal,
                            Mines.GemstoneGorge.subregion("Top"),
                            access_rule=Has(ItemName.VariaSuit),
                        ),
                    ],
                    pickups=[
                        PickupData(),
                    ],
                ),
            ],
        ),
        RoomData(
            Mines.DualPondAlcove,
            id="collision_camera_007",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Mines.MinesIntersectionTerminal.subregion("Middle"),
                            access_rule=can_power_bomb,
                        )
                    ],
                    pickups=[
                        PickupData(
                            access_rule=And(
                                can_spider_boost,
                                Or(
                                    # Spider boost out of the water
                                    And(
                                        has_knowledge(Knowledge.option_enable),
                                        Has(ItemName.GravitySuit),
                                    ),
                                    # Jump up the shaft after getting out of the water
                                    And(
                                        Or(
                                            HasAny(ItemName.GravitySuit, ItemName.HighJumpBoots),
                                            # Spider up and unmorph to grab ledge
                                            can_spider & can_movement(Movement.option_enable),
                                        ),
                                        HasAny(ItemName.SpaceJump, ItemName.HighJumpBoots),
                                    ),
                                    # Can grapple or spider boost to get out
                                ),
                            ),
                        )
                    ],
                )
            ],
        ),
        RoomData(
            Mines.Zeta,
            id="collision_camera_008",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Normal,
                            Mines.PinkCrystalPreserve.subregion("Bottom"),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=can_damage_metroid,
                        )
                    ],
                )
            ],
        ),
        RoomData(
            Mines.GawronGroove,
            id="collision_camera_009",
            regions=[
                RegionData(
                    "Left",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Top"),
                            access_rule=Has(ItemName.VariaSuit) & can_high_ledge,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Arena Left"),
                            access_rule=HasAll(ItemName.SuperMissile, ItemName.VariaSuit) & can_bomb_block,
                        ),
                    ],
                ),
                RegionData(
                    "Top",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Left"),
                            access_rule=Has(ItemName.VariaSuit),
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Right"),
                            access_rule=Has(ItemName.VariaSuit),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Mines.BasaltBasin.subregion("Top"),
                            access_rule=Has(ItemName.VariaSuit) & can_bomb_block,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=HasAll(ItemName.MorphBall, ItemName.SuperMissile, ItemName.VariaSuit),
                        )
                    ],
                ),
                RegionData(
                    "Right",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Top"),
                            access_rule=And(
                                Has(ItemName.VariaSuit),
                                Or(
                                    can_high_ledge,
                                    can_movement(Movement.option_enable),  # Slightly tricky jump around the ledge
                                ),
                            ),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Mines.BasaltBasin.subregion("Top"),
                            access_rule=HasAll(ItemName.SuperMissile, ItemName.VariaSuit) & can_bomb_block,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Mines.Gamma2,
                            access_rule=Has(ItemName.VariaSuit) & can_escape_evolved_gamma,
                        ),
                    ],
                ),
                RegionData(
                    "Arena Left",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Left"),
                            access_rule=And(
                                can_fly_vertical,
                                can_bomb_block,
                                HasAll(ItemName.SuperMissile, ItemName.VariaSuit),
                            ),
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Arena Right"),
                            access_rule=And(
                                Has(ItemName.VariaSuit),
                                Or(
                                    can_fly,
                                    can_spider_boost,
                                    can_damage_boost(DamageBoost.option_static),
                                ),
                            ),
                        ),
                    ],
                ),
                RegionData(
                    "Arena Right",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Mines.BasaltBasin.subregion("Seal"),
                            access_rule=And(
                                Has(ItemName.VariaSuit),
                                can_climb_wall,
                                can_bomb_block,
                            ),
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Arena Left"),
                            access_rule=And(
                                Has(ItemName.VariaSuit),
                                Or(
                                    can_fly,
                                    can_spider_boost,
                                    can_damage_boost(DamageBoost.option_static),
                                ),
                            ),
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Mines.MinesEntrance,
            id="collision_camera_010",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Charge,
                            Mines.TransportCentralCaves,
                        ),
                        ExitData(
                            Door.Charge,
                            Mines.DiggernautExcavationTunnels.subregion("Entrance"),
                        ),
                        # ExitData(
                        #     Door.Locked,
                        #     Mines.TsumuriTunnel,
                        #     access_rule=can_fly_vertical,
                        # ),
                    ]
                )
            ],
        ),
        RoomData(
            Mines.TsumuriTunnel,
            id="collision_camera_011",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Super,
                            Mines.MinesIntersectionTerminal.subregion("Exit"),
                        ),
                        ExitData(
                            Door.Normal,
                            Mines.MinesEntrance,
                        ),
                    ]
                )
            ],
        ),
        RoomData(
            Mines.MinesTeleporter,
            id="collision_camera_012",
            regions=[],  # Not relevant
        ),
        RoomData(
            Mines.GreenCrystalDugout,
            id="collision_camera_013",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Open,
                            Mines.MinesIntersectionTerminal.subregion("Top"),
                        ),
                        ExitData(
                            Door.Normal,
                            Mines.GawronGroove.subregion("Left"),
                        ),
                    ]
                )
            ],
        ),
        RoomData(
            Mines.GemstoneGorge,
            id="collision_camera_014",
            regions=[
                RegionData(
                    "Bottom",
                    exits=[
                        ExitData(
                            Door.Super,
                            Mines.MinesIntersectionTerminal.subregion("Save Station"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Top"),
                            access_rule=can_fly_vertical,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=HasAll(ItemName.SpaceJump, ItemName.ScrewAttack) & can_bomb_block,
                        )
                    ],
                ),
                RegionData(
                    "Top",
                    exits=[
                        ExitData(
                            Door.Open,
                            Mines.PinkCrystalPreserve.subregion("Bottom"),
                        ),
                        # ExitData(
                        #     Door.Locked,
                        #     Mines.LavaReservoir.subregion("Left"),
                        # ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Bottom"),
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Mines.Gamma2,
            id="collision_camera_015",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Mines.GawronGroove.subregion("Right"),
                            access_rule=Has(ItemName.VariaSuit) & can_escape_evolved_gamma,
                        )
                    ],
                    pickups=[
                        PickupData(
                            access_rule=Has(ItemName.VariaSuit) & can_damage_metroid,
                        )
                    ],
                )
            ],
        ),
        RoomData(
            Mines.BasaltBasin,
            id="collision_camera_017",
            regions=[
                RegionData(
                    "Top",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Seal"),
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Mines.GawronGroove.subregion("Left"),
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Mines.GawronGroove.subregion("Right"),
                            access_rule=And(
                                Has(ItemName.SuperMissile),
                                can_bomb_block,
                                can_high_ledge,
                            ),
                        ),
                    ],
                ),
                RegionData(
                    "Seal",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Mines.GawronGroove.subregion("Arena Right"),
                            access_rule=can_high_bomb_block,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Top"),
                            access_rule=can_fly_vertical & can_bomb_block,
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Mines.SpaceJump,
            id="collision_camera_AfterChase",
            regions=[
                # All the parts of this room have the same access rule and we only need to consider
                # the pickup at the bottom
                RegionData(
                    exits=[
                        ExitData(
                            Door.Normal,
                            Mines.MinesIntersectionTerminal.subregion("Bottom"),
                            access_rule=can_fly_vertical,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Mines.DiggernautExcavationTunnels.subregion("Sublevel 1"),
                            access_rule=can_fly_vertical & Has(ItemName.SuperMissile),
                        ),
                        # Excavation tunnels Sublevel 2 - reverse grapple block
                        ExitData(
                            Door.MorphTunnel,
                            Mines.DiggernautExcavationTunnels.subregion("Sublevel 3"),
                            access_rule=And(
                                # Has you fall through a pitfall block and navigate some obstacles in DET
                                Has(ItemName.SuperMissile),
                                can_bomb,
                                can_spider,
                            ),
                        ),
                    ],
                    pickups=[
                        PickupData(),
                    ],
                )
            ],
        ),
        RoomData(
            Mines.DiggernautExcavationTunnels,
            id="collision_camera_AfterChase_001",
            regions=[
                RegionData(
                    "Entrance",
                    exits=[
                        ExitData(
                            Door.Missile,
                            Mines.MinesEntrance,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Sublevel 1"),
                        ),
                    ],
                ),
                RegionData(
                    "Sublevel 1",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Entrance"),
                            access_rule=Has(ItemName.SpaceJump) | can_ibj(IBJ.option_vertical),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Sublevel 2"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Mines.SpaceJump,
                            access_rule=Has(ItemName.SuperMissile),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Crystals",
                            access_rule=And(
                                Has(ItemName.MorphBall),
                                Or(
                                    Has(ItemName.Hatchling),
                                    Has(ItemName.PhaseDrift) & can_bomb_block,
                                ),
                            ),
                        )
                    ],
                ),
                RegionData(
                    "Sublevel 2",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Sublevel 1"),
                            access_rule=can_climb_shaft,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Sublevel 3"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Mines.SpaceJump,
                            access_rule=Has(ItemName.GrappleBeam),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Plants",
                            access_rule=can_bomb_block & Has(ItemName.LightningArmor),
                        ),
                        PickupData(
                            "Puzzle",
                            # The escape logic here is a little weird because unless you regrab you'll fall to SL3
                            access_rule=can_bomb_block,
                        ),
                    ],
                ),
                RegionData(
                    "Sublevel 3",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Sublevel 2"),
                            access_rule=can_climb_shaft,
                        ),
                        # There's an entrance from SJ chamber that goes through this little backdoor area
                    ],
                    pickups=[
                        PickupData(
                            "Floor",
                            access_rule=can_bomb_block,
                        ),
                    ],
                ),
            ],
        ),
    ],
)
