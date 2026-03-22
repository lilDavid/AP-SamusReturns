from rule_builder.rules import And, Has, HasAll, HasAny, Or

from ...items import ItemName
from ...logic import (
    can_any_missile,
    can_bomb_block,
    can_bomb_block_near_ceiling,
    can_climb_shaft,
    can_climb_wall,
    can_combat_omega,
    can_damage_boost,
    can_damage_metroid,
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
    can_thorns,
    can_wall_jump,
)
from ...options import IBJ, DamageBoost, Movement, WallJump
from ..internal_names import AreaId
from ..room_names import Area5Lobby as Area5
from ..room_names import Area6
from . import AreaData, Door, ExitData, PickupData, RegionData, RoomData, Subregion

can_cross_crumbling_bridge = Has(ItemName.PhaseDrift) | can_spider_boost
can_navigate_hideout_sprawl_tunnels = And(
    HasAll(ItemName.ScrewAttack, ItemName.SuperMissile, ItemName.GrappleBeam),
    can_bomb_block,
    Or(
        HasAny(ItemName.HighJumpBoots, ItemName.ScrewAttack),
        can_wall_jump(WallJump.option_simple),
    ),
)
can_combat_diggernaut = And(
    can_spider,
    HasAny(ItemName.MissileLauncher, ItemName.SuperMissile, ItemName.BeamBurst),
    HasAll(ItemName.MorphBall, ItemName.Bomb, ItemName.SpiderBall, ItemName.SpaceJump),
)
can_cross_swarm_square = Or(
    Has(ItemName.SpaceJump),
    can_spider,
    can_power_bomb,
    can_ibj(IBJ.option_vertical) & can_thorns,
)

can_escape_chozo_seal_w_bottom = can_high_ledge
can_escape_chozo_seal_e = Or(
    can_climb_wall,
    # Can also midair morph-unmorph LMAO
    Has(ItemName.HighJumpBoots) & can_wall_jump(WallJump.option_simple),
)
can_escape_crumbling_bridge_pit = can_bomb_block_near_ceiling
can_escape_diggernaut = can_combat_diggernaut & can_power_bomb
can_escape_swarm_square_to_transport = Has(ItemName.GrappleBeam)
can_escape_diggernaut_loop = And(
    can_escape_diggernaut,
    can_fly_vertical,
    can_cross_swarm_square,
    can_escape_swarm_square_to_transport,
)

area_6_data = AreaData(
    name="Area 6",
    id=AreaId.AREA_6,
    rooms=[
        RoomData(
            Area6.TransportArea7,
            id="collision_camera_034",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area6.CrumblingStairwell,
                            access_rule=Has(ItemName.MorphBall),
                        ),
                        ExitData(
                            Door.Charge,
                            Area6.Diggernaut,
                            access_rule=can_escape_diggernaut_loop,
                        ),
                        # ExitData(
                        #     Door.Normal,
                        #     Area7.TransportArea6,  # TODO: Area 7
                        #     access_rule=can_bomb_block,
                        # ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=And(
                                can_thorns,
                                can_high_bomb_block,
                                Has(ItemName.GrappleBeam),
                                can_any_missile | can_power_bomb,
                                can_spider,
                            )
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Area6.TeleporterS,
            id="collision_camera_035",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area6.CrumblingStairwell,
                        )
                    ]
                )
            ],
        ),
        RoomData(
            Area6.Omega,
            id="collision_camera_037",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area6.PoisonousTunnel.subregion("Upper"),
                        ),
                        ExitData(
                            Door.Normal,
                            Area6.ZetaAccess,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=can_combat_omega,
                        )
                    ],
                )
            ],
        ),
        RoomData(
            Area6.HideoutSprawl,
            id="collision_camera_038",
            regions=[
                RegionData(
                    "Bottom",
                    exits=[
                        ExitData(
                            Door.Missile,
                            Area6.HideoutEntrance,
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Main"),
                            access_rule=can_climb_wall,
                        ),
                    ],
                ),
                RegionData(
                    "Main",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Bottom"),
                        ),
                        ExitData(
                            Door.Normal,
                            Area6.OmegaAccess,
                            access_rule=Has(ItemName.ScrewAttack) & can_high_ledge,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Left",
                            access_rule=And(
                                HasAll(ItemName.ScrewAttack, ItemName.GrappleBeam),
                                can_spider_boost,
                            ),
                        ),
                    ],
                ),
                RegionData(
                    "Tunnels",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area6.OmegaAccess,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Main"),
                            access_rule=can_navigate_hideout_sprawl_tunnels,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Right",
                            access_rule=can_navigate_hideout_sprawl_tunnels,
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Area6.TeleporterNAccess,
            id="collision_camera_039",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Charge,
                            Area6.PoisonousTunnel.subregion("Upper"),
                            access_rule=can_climb_shaft,
                        ),
                        ExitData(
                            Door.Normal,
                            Area6.TeleporterN.subregion("Upper"),
                        ),
                    ]
                )
            ],
        ),
        RoomData(
            Area6.CrumblingBridge,
            id="collision_camera_040",
            regions=[
                RegionData(
                    "Right",
                    exits=[
                        ExitData(
                            Door.Charge,
                            Area6.ChozoSealE.subregion("Upper"),
                            access_rule=can_escape_chozo_seal_e,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Left"),
                            access_rule=can_cross_crumbling_bridge,
                        ),
                    ],
                ),
                RegionData(
                    "Left",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area6.Zeta,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Right"),
                            access_rule=can_cross_crumbling_bridge,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Tunnel",
                            access_rule=can_power_bomb | can_escape_crumbling_bridge_pit,
                        ),
                        PickupData(
                            "Pit",
                            access_rule=can_any_missile & can_escape_crumbling_bridge_pit,
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Area6.HideoutEntrance,
            id="collision_camera_041",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Charge,
                            Area6.TeleporterN.subregion("Upper"),
                            access_rule=Or(
                                HasAll(ItemName.SpaceJump, ItemName.ScrewAttack),
                                can_bomb_block_near_ceiling,
                            ),
                        ),
                        ExitData(
                            Door.Missile,
                            Area6.HideoutSprawl.subregion("Bottom"),
                            access_rule=Or(
                                HasAll(ItemName.SpaceJump, ItemName.ScrewAttack),
                                can_bomb_block_near_ceiling,
                            ),
                        ),
                    ]
                )
            ],
        ),
        RoomData(
            Area6.CrumblingStairwell,
            id="collision_camera_042",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area6.ChozoSealW.subregion("Main"),
                            access_rule=can_escape_chozo_seal_w_bottom,
                        ),
                        ExitData(
                            Door.Normal,
                            Area6.TransportArea7,
                            access_rule=Or(
                                Has(ItemName.SpaceJump),
                                And(
                                    # This is actually a DBJ but diagonal DBJs aren't fully considered yet
                                    Has(ItemName.HighJumpBoots) | can_ibj(IBJ.option_diagonal),
                                    can_spider,
                                ),
                            ),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=And(
                                can_bomb_block,
                                Has(ItemName.PhaseDrift) | can_spider,
                            )
                        )
                    ],
                )
            ],
        ),
        RoomData(
            Area6.Diggernaut,
            id="collision_camera_043",
            regions=[
                RegionData(
                    exits=[
                        # ExitData(
                        #     Door.Locked,
                        #     Area6.TransportArea7,
                        #     access_rule=can_bomb_block,
                        # ),
                        ExitData(
                            Door.Normal,
                            Area6.ElectricEscalade,
                            access_rule=can_escape_diggernaut,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=can_combat_diggernaut,
                        )
                    ],
                )
            ],
        ),
        RoomData(
            Area6.SwarmSquare,
            id="collision_camera_044",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.PowerBomb,
                            Area6.ElectricEscalade,
                            access_rule=can_cross_swarm_square,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area6.TransportArea7,
                            access_rule=can_cross_swarm_square & can_escape_swarm_square_to_transport,
                        ),
                    ]
                )
            ],
        ),
        RoomData(
            Area6.ElectricEscalade,
            id="collision_camera_045",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area6.Diggernaut,
                            access_rule=can_escape_diggernaut,
                        ),
                        ExitData(
                            Door.PowerBomb,
                            Area6.SwarmSquare,
                            access_rule=can_climb_wall,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=can_spider_boost | can_ibj(IBJ.option_vertical),
                        )
                    ],
                )
            ],
        ),
        RoomData(
            Area6.PoisonousTunnel,
            id="collision_camera_046",
            regions=[
                RegionData(
                    "Upper",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area6.Omega,
                        ),
                        ExitData(
                            Door.Charge,
                            Area6.TeleporterNAccess,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Pickup"),
                            access_rule=And(
                                can_bomb_block,
                                Has(ItemName.LightningArmor) | can_spider,
                            ),
                        ),
                    ],
                ),
                RegionData(
                    "Pickup",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Upper"),
                            access_rule=And(
                                can_bomb_block,
                                Has(ItemName.LightningArmor) | can_spider,
                            ),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area6.TeleporterNAccess,
                            access_rule=Has(ItemName.GrappleBeam),
                        ),
                    ],
                    pickups=[
                        PickupData(),
                    ],
                ),
            ],
        ),
        RoomData(
            Area6.ZetaAccess,
            id="collision_camera_047",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area6.Omega,
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.Normal,
                            Area6.Zeta,
                            access_rule=can_bomb_block,
                        ),
                    ]
                )
            ],
        ),
        RoomData(
            Area6.Zeta,
            id="collision_camera_048",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area6.ZetaAccess,
                        ),
                        ExitData(
                            Door.Normal,
                            Area6.CrumblingBridge.subregion("Left"),
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
            Area6.TransportArea5,
            id="collision_camera_051",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Elevator,
                            Area5.TransportAreas4And6.subregion("Bottom"),
                            access_rule=Or(
                                HasAny(ItemName.HighJumpBoots, ItemName.SpaceJump),
                                can_spider,
                                can_damage_boost(DamageBoost.option_static),
                            ),
                        ),
                        ExitData(
                            Door.Normal,
                            Area6.ChozoSealW.subregion("Main"),
                            access_rule=Or(
                                HasAny(ItemName.HighJumpBoots, ItemName.SpaceJump),
                                can_spider,
                                can_high_ledge & can_damage_boost(DamageBoost.option_static),
                            ),
                        ),
                    ]
                )
            ],
        ),
        RoomData(
            Area6.ChozoSealE,
            id="collision_camera_060",
            regions=[
                RegionData(
                    "Lower",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Area6.ChozoSealW.subregion("Top"),
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Upper"),
                            access_rule=And(
                                can_bomb_block,
                                can_any_missile,
                                Has(ItemName.GrappleBeam),
                                can_high_ledge,
                                Or(
                                    HasAny(ItemName.SpaceJump, ItemName.SpiderBall, ItemName.LightningArmor),
                                    can_damage_boost(DamageBoost.option_static),
                                ),
                            ),
                        ),
                    ],
                ),
                RegionData(
                    "Upper",
                    exits=[
                        ExitData(
                            Door.Charge,
                            Area6.CrumblingBridge.subregion("Right"),
                            access_rule=can_escape_chozo_seal_e,
                        )
                    ],
                    pickups=[
                        PickupData(
                            access_rule=And(
                                can_bomb_block,
                                Has(ItemName.GrappleBeam),
                                Or(
                                    Has(ItemName.Hatchling),
                                    And(
                                        # Pitfall block in tunnel
                                        Or(
                                            can_spider,
                                            Has(ItemName.PhaseDrift),
                                            can_movement(Movement.option_enable),
                                        ),
                                    ),
                                ),
                            )
                        )
                    ],
                ),
            ],
        ),
        RoomData(
            Area6.OmegaAccess,
            id="collision_camera_061",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area6.HideoutSprawl.subregion("Main"),
                            access_rule=can_high_jump,
                        ),
                        ExitData(Door.PowerBomb, Area6.HideoutSprawl.subregion("Tunnels")),
                        ExitData(
                            Door.Open,
                            Area6.Omega,
                            access_rule=can_high_jump,
                        ),
                    ]
                )
            ],
        ),
        RoomData(
            Area6.ChozoSealW,
            id="collision_camera_Hazard_End_A",
            regions=[
                RegionData(
                    "Main",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area6.TransportArea5,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Passageway"),
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.Normal,
                            Area6.TeleporterS,
                            access_rule=can_high_ledge,
                        ),
                        # ExitData(
                        #     Door.Locked,
                        #     Area6.CrumblingStairwell,
                        # ),
                    ],
                    pickups=[
                        PickupData(
                            "Tunnel",
                            access_rule=And(
                                can_bomb_block,
                                can_spider | can_movement(Movement.option_enable),
                            ),
                        ),
                        PickupData(
                            "Ceiling",
                            access_rule=can_bomb_block_near_ceiling | can_ibj(IBJ.option_vertical),
                        ),
                        PickupData(
                            "Bottom",
                            access_rule=And(
                                can_power_bomb,
                                HasAll(ItemName.GrappleBeam, ItemName.ScrewAttack),
                                can_any_missile,
                                Or(
                                    Has(ItemName.SpaceJump),
                                    And(
                                        can_fly_vertical,
                                        Has(ItemName.HighJumpBoots) | can_wall_jump(WallJump.option_simple),
                                    ),
                                ),
                            ),
                        ),
                    ],
                ),
                RegionData(
                    "Passageway",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Subregion("Main"),
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.Normal,
                            Area6.TransportArea5,
                            access_rule=HasAll(ItemName.MorphBall, ItemName.GrappleBeam),
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Top"),
                            access_rule=can_climb_wall,
                        ),
                    ],
                ),
                RegionData(
                    "Top",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Passageway"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area6.ChozoSealE.subregion("Lower"),
                        ),
                        ExitData(
                            Door.Normal,
                            Area6.TeleporterN.subregion("Lower"),
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Area6.TeleporterN,
            id="collision_camera_Hazard_End_B",
            regions=[
                RegionData(
                    "Lower",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area6.ChozoSealW.subregion("Top"),
                        ),
                        ExitData(
                            Door.Open,
                            Subregion("Upper"),
                            access_rule=can_short_shaft,
                        ),
                    ],
                ),
                RegionData(
                    "Upper",
                    exits=[
                        ExitData(
                            Door.Open,
                            Subregion("Lower"),
                        ),
                        ExitData(
                            Door.Charge,
                            Area6.HideoutEntrance,
                        ),
                        # ExitData(
                        #     Door.Locked,
                        #     Area6.TeleporterNAccess,
                        # ),
                    ],
                ),
            ],
        ),
    ],
)
