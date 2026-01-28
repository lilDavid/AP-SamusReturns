from ...items import ItemName
from ...logic import (
    can_any_missile,
    can_beam_block_through_fan_tunnel,
    can_beam_block_through_tunnel,
    can_blobthrower,
    can_bomb,
    can_bomb_block,
    can_climb_shaft,
    can_climb_wall,
    can_damage_boost,
    can_damage_metroid,
    can_damage_tough_enemy,
    can_fly_straight_up,
    can_high_jump,
    can_high_ledge,
    can_ibj,
    can_movement,
    can_power_bomb,
    can_short_shaft,
    can_spider,
    can_spider_boost,
    can_wall_jump,
)
from ...options import IBJ, DamageBoost, Movement, WallJump
from ..internal_names import AreaId
from ..room_names import Area1
from ..room_names import Area2Entryway as Entryway
from ..room_names import Area2Exterior as Exterior
from ..room_names import Area2Interior as Interior
from . import AreaData, Door, EventData, ExitData, PickupData, RegionData, RoomData

area_2_exterior_data = AreaData(
    name="Area 2 Dam Exterior",
    id=AreaId.AREA_2_EXTERIOR,
    rooms=[
        RoomData(
            Exterior.DamExterior,
            id="collision_camera_005",
            regions=[
                RegionData(
                    "East",
                    exits=[
                        ExitData(
                            Door.Elevator,
                            Entryway.LightningArmor.subregion("Upper"),
                        ),
                        ExitData(
                            Door.Normal,
                            Exterior.CritterPlayground.subregion("Bottom"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.CritterPlayground.subregion("Tunnel"),
                        ),
                        ExitData(
                            Door.Open,
                            Exterior.DamExterior.subregion("Top"),
                            access_rule=can_fly_straight_up,
                        ),
                    ],
                    pickups=[
                        # Spider boost as a solution is a little obscure but not too bad?
                        PickupData(access_rule=can_fly_straight_up),
                    ],
                ),
                RegionData(
                    "Top",
                    exits=[
                        ExitData(
                            Door.Open,
                            Exterior.DamExterior.subregion("East"),
                        ),
                        ExitData(
                            Door.Open,
                            Exterior.DamExterior.subregion("West"),
                        ),
                        # FIXME: Dangerous action
                        ExitData(
                            Door.Open,
                            Exterior.DamExterior.subregion("Inner"),
                        ),
                        ExitData(
                            Door.Open,
                            Exterior.DamExterior.subregion("Alpha Ledge"),
                            access_rule=lambda state, player: state.has(ItemName.SpaceJump, player)
                            or can_spider_boost(state, player)
                            or can_ibj(state, player, IBJ.option_diagonal),
                        ),
                    ],
                ),
                RegionData(
                    "Inner",
                    exits=[
                        ExitData(
                            Door.Open,
                            Exterior.DamExterior.subregion("Top"),
                            access_rule=can_climb_wall,
                        ),
                        # FIXME: Dangrous action
                        ExitData(
                            Door.Missile,
                            Exterior.Arachnus,
                        ),
                        # ExitData(
                        #     Door.Locked,
                        #     Exterior.MaintenanceTunnel,
                        # ),
                    ],
                ),
                RegionData(
                    "West",
                    exits=[
                        ExitData(
                            Door.Open,
                            Exterior.DamExterior.subregion("Top"),
                            access_rule=can_climb_wall,
                        ),
                        ExitData(
                            Door.Open,
                            Exterior.DamExterior.subregion("Alpha Ledge"),
                            access_rule=lambda state, player: can_fly_straight_up(state, player)
                            or (state.has(ItemName.LightningArmor, player) and can_spider(state, player)),
                        ),
                        ExitData(
                            Door.Open,
                            Exterior.DamExterior.subregion("Bottom"),
                            access_rule=lambda state, player: state.has(ItemName.Hatchling, player)
                            or can_bomb_block(state, player),
                        ),
                        ExitData(
                            Door.Normal,
                            Exterior.RockIcicleCorridor,
                        ),
                        ExitData(
                            Door.Normal,
                            Exterior.CavernsEntrance,
                        ),
                        ExitData(
                            Door.Elevator,
                            Interior.WaveBeam.subregion("Northwest"),
                        ),
                    ],
                ),
                RegionData(
                    "Bottom",
                    exits=[
                        ExitData(
                            Door.Open,
                            Exterior.DamExterior.subregion("West"),
                            access_rule=lambda state, player: can_bomb_block(state, player)
                            or (
                                state.has(ItemName.Hatchling, player)
                                and (
                                    can_climb_wall(state, player)
                                    or can_wall_jump(state, player, WallJump.option_enable)
                                )
                            ),
                        ),
                        # ExitData(
                        #     Door.Locked,
                        #     Exterior.CavernsEntrance,
                        # ),
                        ExitData(
                            Door.Open,
                            Exterior.DamExterior.subregion("Top"),
                            access_rule=lambda state, player: state.has(ItemName.SpaceJump, player)
                            or can_spider_boost(state, player)
                            or can_ibj(state, player, IBJ.option_diagonal)
                            or (
                                can_spider(state, player) and can_damage_boost(state, player, DamageBoost.option_enable)
                            ),
                        ),
                    ],
                ),
                RegionData(
                    "Alpha Ledge",
                    exits=[
                        ExitData(
                            Door.Open,
                            Exterior.DamExterior.subregion("West"),
                        ),
                        ExitData(
                            Door.Open,
                            Exterior.DamExterior.subregion("Top"),
                            access_rule=lambda state, player: state.has(ItemName.SpaceJump, player)
                            or can_spider_boost(state, player)
                            or can_ibj(state, player, IBJ.option_diagonal)
                            or (
                                can_spider(state, player) and can_damage_boost(state, player, DamageBoost.option_enable)
                            ),
                        ),
                        ExitData(
                            Door.Normal,
                            Exterior.ExteriorAlpha2,
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Exterior.Arachnus,
            id="collision_camera_006",
            regions=[
                RegionData(
                    None,
                    exits=[
                        # ExitData(
                        #     Door.Locked,
                        #     Exterior.DamExterior.subregion("Inner"),
                        # ),
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.FanFunnel,
                            access_rule=can_bomb_block,
                        ),
                    ],
                    pickups=[
                        PickupData(),
                    ],
                )
            ],
        ),
        RoomData(
            Exterior.FanFunnel,
            id="collision_camera_007",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.Arachnus,
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.MaintenanceTunnel,
                            access_rule=lambda state, player: state.has_all(
                                (ItemName.SpringBall, ItemName.Bomb), player
                            )
                            or state.has(ItemName.PowerBomb, player),
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Exterior.CritterPlayground,
            id="collision_camera_008",
            regions=[
                RegionData(
                    "Top",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Exterior.RockIcicleCorridor,
                        ),
                        ExitData(
                            Door.Normal,
                            Exterior.InnerAlpha,
                        ),
                        ExitData(
                            Door.Open,
                            Exterior.CritterPlayground.subregion("Middle"),
                        ),
                    ],
                ),
                RegionData(
                    "Middle",
                    exits=[
                        ExitData(
                            Door.Open,
                            Exterior.CritterPlayground.subregion("Top"),
                            access_rule=can_climb_wall,
                        ),
                        ExitData(
                            Door.Open,
                            Exterior.CritterPlayground.subregion("Pickup"),
                            access_rule=lambda state, player: state.has(ItemName.Hatchling, player)
                            and can_climb_wall(state, player),
                        ),
                    ],
                ),
                RegionData(
                    "Bottom",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.CritterPlayground.subregion("Middle"),
                        ),
                        ExitData(
                            Door.Normal,
                            Exterior.DamExterior.subregion("East"),
                        ),
                    ],
                ),
                RegionData(
                    "Tunnel",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.DamExterior.subregion("East"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.CritterPlayground.subregion("Pickup"),
                            access_rule=lambda state, player: can_climb_wall(state, player)
                            and can_bomb_block(state, player),
                        ),
                    ],
                ),
                RegionData(
                    "Pickup",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.CritterPlayground.subregion("Tunnel"),
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.CritterPlayground.subregion("Middle"),
                            access_rule=lambda state, player: state.has(ItemName.Hatchling, player),
                        ),
                    ],
                    pickups=[
                        PickupData(),
                    ],
                ),
            ],
        ),
        RoomData(
            Exterior.CavernsEntrance,
            id="collision_camera_023",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.Normal,
                            Exterior.DamExterior.subregion("West"),
                        ),
                        # No logical effect
                        # ExitData(
                        #     Door.Normal,
                        #     Exterior.AmmoRechargeAccess,
                        # ),
                        ExitData(
                            Door.Normal,
                            Exterior.DamExterior.subregion("Bottom"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.SpikeRavine.subregion("Upper"),
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.SpikeRavine.subregion("Lower"),
                        ),
                        ExitData(
                            Door.Normal,
                            Exterior.CavernsSaveStation,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=lambda state, player: (
                                can_spider(state, player) or state.has(ItemName.SpaceJump, player)
                            )
                            and (
                                state.has(ItemName.Hatchling, player)
                                or (state.has(ItemName.SuperMissile, player) or can_bomb_block(state, player))
                            )
                        )
                    ],
                )
            ],
        ),
        RoomData(
            Exterior.SpikeRavine,
            id="collision_camera_024",
            regions=[
                RegionData(
                    "Upper",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.CavernsEntrance,
                            access_rule=can_bomb,
                        ),
                        ExitData(
                            Door.Open,
                            Exterior.SpikeRavine.subregion("Lower"),
                        ),
                        ExitData(
                            Door.Open,
                            Exterior.SpikeRavine.subregion("Pickup"),
                            access_rule=lambda state, player: (
                                state.has(ItemName.GrappleBeam, player) or can_spider_boost(state, player)
                            ),
                        ),
                    ],
                ),
                RegionData(
                    "Lower",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.CavernsEntrance,
                            access_rule=can_bomb,
                        ),
                        ExitData(
                            Door.Open,
                            Exterior.SpikeRavine.subregion("Upper"),
                            access_rule=can_climb_wall,
                        ),
                        ExitData(
                            Door.Open,
                            Exterior.SpikeRavine.subregion("Pickup"),
                            access_rule=can_spider_boost,
                        ),
                    ],
                ),
                RegionData(
                    "Pickup",
                    exits=[
                        ExitData(
                            Door.Open,
                            Exterior.SpikeRavine.subregion("Upper"),
                            access_rule=can_spider_boost,
                        ),
                        ExitData(
                            Door.Open,
                            Exterior.SpikeRavine.subregion("Lower"),
                        ),
                    ],
                    pickups=[
                        PickupData(access_rule=lambda state, player: state.has(ItemName.MorphBall, player)),
                    ],
                ),
            ],
        ),
        RoomData(
            Exterior.AmmoRechargeAccess,
            id="collision_camera_025",
            regions=[
                # No logical effect
                # RegionData(
                #     None,
                #     exits=[
                #         ExitData(
                #             Door.Normal,
                #             Exterior.CavernsEntrance,
                #         ),
                #         ExitData(
                #             Door.Normal,
                #             Exterior.CavernsAmmoRecharge,
                #         ),
                #     ]
                # )
            ],
        ),
        RoomData(
            Exterior.CavernsMaze,
            id="collision_camera_026",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.CavernsSaveStation,
                            access_rule=can_bomb,
                        ),
                    ],
                    pickups=[
                        PickupData(access_rule=can_bomb_block),
                    ],
                )
            ],
        ),
        RoomData(
            Exterior.CavernsSaveStation,
            id="collision_camera_027",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.Normal,
                            Exterior.CavernsEntrance,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.CavernsMaze,
                            access_rule=can_bomb,
                        ),
                        ExitData(
                            Door.Normal,
                            Exterior.CavernsAlphaNw,
                        ),
                        ExitData(
                            Door.Open,
                            Exterior.CavernsAlphaEAccess.subregion("Left"),
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Exterior.CavernsAlphaNw,
            id="collision_camera_028",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.Normal,
                            Exterior.CavernsSaveStation,
                            access_rule=can_climb_wall,
                        ),
                        ExitData(
                            Door.Charge,
                            Exterior.CavernsLobby,
                            # IBJ is dubious but not difficult
                            access_rule=can_climb_wall,
                        ),
                    ],
                    pickups=[
                        PickupData(access_rule=can_damage_metroid),
                    ],
                )
            ],
        ),
        RoomData(
            Exterior.CavernsLobby,
            id="collision_camera_029",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.Charge,
                            Exterior.CavernsAlphaNw,
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player),
                        ),
                        ExitData(
                            Door.Taramarga,
                            Exterior.CavernsAlphaSw,
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player),
                        ),
                        ExitData(
                            Door.Normal,
                            Exterior.CavernsTeleporter.subregion("Left"),
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player),
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Exterior.CavernsAlphaSw,
            id="collision_camera_030",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.Normal,
                            Exterior.CavernsLobby,
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player)
                            and can_damage_metroid(state, player)
                        )
                    ],
                )
            ],
        ),
        RoomData(
            Exterior.CavernsAlphaEAccess,
            id="collision_camera_031",
            regions=[
                RegionData(
                    "Left",
                    exits=[
                        ExitData(
                            Door.Open,
                            Exterior.CavernsSaveStation,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.CavernsAlphaEAccess.subregion("Right"),
                            access_rule=lambda state, player: can_power_bomb(state, player)
                            or (state.has(ItemName.SpringBall, player) and can_bomb(state, player)),
                        ),
                    ],
                ),
                RegionData(
                    "Right",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.CavernsAlphaEAccess.subregion("Left"),
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.CavernsAlphaE,
                            # FIXME: Dangerous action
                            access_rule=can_bomb_block,
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Exterior.CavernsTeleporter,
            id="collision_camera_032",
            regions=[
                RegionData(
                    "Left",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Exterior.CavernsLobby,
                        ),
                        ExitData(
                            Door.Open,
                            Exterior.CavernsTeleporter.subregion("Right"),
                            # Missile block
                            access_rule=lambda state, player: can_any_missile(state, player)
                            and state.has_any((ItemName.HighJumpBoots, ItemName.SpaceJump), player)
                            # Magma pool
                            and (
                                state.has_any((ItemName.IceBeam, ItemName.SpaceJump), player)
                                or can_spider(state, player)
                            ),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=lambda state, player: can_blobthrower(state, player)
                            and can_bomb_block(state, player)
                        )
                    ],
                ),
                RegionData(
                    "Right",
                    exits=[
                        ExitData(
                            Door.Open,
                            Exterior.CavernsTeleporter.subregion("Left"),
                            # Magma pool
                            access_rule=lambda state, player: (
                                state.has_any((ItemName.IceBeam, ItemName.SpaceJump, ItemName.MorphBall), player)
                            )
                            # Missile block
                            and can_any_missile(state, player),
                        ),
                        ExitData(
                            Door.Normal,
                            Exterior.CavernsAlpha2,
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Exterior.ExteriorAlpha2,
            id="collision_camera_033",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.Normal,
                            Exterior.DamExterior.subregion("Alpha Ledge"),
                        ),
                        ExitData(
                            Door.Super,
                            Exterior.SereneShelter,
                            access_rule=can_high_ledge,
                        ),
                    ],
                    pickups=[
                        PickupData(access_rule=can_damage_metroid),
                    ],
                )
            ],
        ),
        RoomData(
            Exterior.SereneShelter,
            id="collision_camera_034",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.Super,
                            Exterior.ExteriorAlpha2,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=lambda state, player: can_climb_shaft(state, player)
                            and (
                                can_bomb(state, player)
                                or (
                                    # Time an unmorph to grab the ledge
                                    can_movement(state, player, Movement.option_enable)
                                    and can_power_bomb(state, player)
                                )
                            )
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Exterior.CavernsAlpha2,
            id="collision_camera_035",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.Normal,
                            Exterior.CavernsTeleporter.subregion("Right"),
                        )
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
            Exterior.InnerAlpha,
            id="collision_camera_036",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.Normal,
                            Exterior.CritterPlayground.subregion("Top"),
                        )
                    ],
                    pickups=[
                        PickupData(access_rule=can_damage_metroid),
                    ],
                )
            ],
        ),
        RoomData(
            Exterior.RockIcicleCorridor,
            id="collision_camera_037",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.Normal,
                            Exterior.DamExterior.subregion("West"),
                        ),
                        ExitData(
                            Door.Normal,
                            Exterior.CritterPlayground.subregion("Top"),
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Exterior.MaintenanceTunnel,
            id="collision_camera_038",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.FanFunnel,
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.Normal,
                            Exterior.DamExterior.subregion("Inner"),
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Exterior.CavernsAmmoRecharge,
            id="collision_camera_039",
            regions=[
                # No logical effect
                # RegionData(
                #     None,
                #     exits=[
                #         ExitData(
                #             Door.Normal,
                #             Exterior.AmmoRechargeAccess,
                #         ),
                #     ]
                # )
            ],
        ),
        RoomData(
            Exterior.CavernsAlphaE,
            id="collision_camera_040",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Exterior.CavernsAlphaEAccess.subregion("Right"),
                            access_rule=lambda state, player: can_high_ledge(state, player)
                            and can_bomb_block(state, player),
                        )
                    ],
                    pickups=[
                        PickupData(access_rule=can_damage_metroid),
                    ],
                )
            ],
        ),
    ],
)

area_2_interior_data = AreaData(
    name="Area 2 Dam Interior",
    id=AreaId.AREA_2_INTERIOR,
    rooms=[
        RoomData(
            Interior.WaveBeam,
            id="collision_camera009",
            regions=[
                RegionData(
                    "Northwest",
                    exits=[
                        ExitData(
                            Door.Elevator,
                            Exterior.DamExterior.subregion("West"),
                        ),
                        ExitData(
                            Door.Open,
                            Interior.WaveBeam.subregion("South"),
                            # FIXME: Dangerous action
                        ),
                    ],
                ),
                RegionData(
                    "South",
                    exits=[
                        ExitData(
                            Door.Open,
                            Interior.WaveBeam.subregion("Northwest"),
                            access_rule=can_high_jump,
                        ),
                        ExitData(
                            Door.Charge,
                            Interior.LavaGenerator,
                        ),
                        ExitData(
                            Door.Charge,
                            Interior.GeneratorAccess.subregion("Upper"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Interior.WaveBeam.subregion("Northeast"),
                            access_rule=lambda state, player: (
                                state.has(ItemName.LightningArmor, player) or can_damage_tough_enemy(state, player)
                            )
                            and can_climb_wall(state, player),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Interior.WaveBeam.subregion("East"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Interior.WaveBeam.subregion("Southeast"),
                            # TODO: Dangerous action?
                        ),
                    ],
                ),
                RegionData(
                    "Southeast",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Interior.WaveBeam.subregion("South"),
                            access_rule=can_beam_block_through_tunnel,
                        ),
                        ExitData(
                            Door.Normal,
                            Interior.WallfireCorridor,
                        ),
                    ],
                ),
                RegionData(
                    "East",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Interior.WaveBeam.subregion("South"),
                        ),
                        ExitData(
                            Door.Taramarga,
                            Interior.InteriorIntersection.subregion("North chamber"),
                        ),
                    ],
                ),
                RegionData(
                    "Northeast",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Interior.WaveBeam.subregion("South"),
                        ),
                        ExitData(
                            Door.Taramarga,
                            Interior.InteriorIntersection.subregion("Side tunnel"),
                        ),
                    ],
                ),
                RegionData(
                    "Chamber",
                    exits=[
                        ExitData(
                            Door.Missile,
                            Interior.InteriorIntersection.subregion("North chamber"),
                        ),
                    ],
                    pickups=[
                        PickupData(),
                    ],
                ),
            ],
        ),
        RoomData(
            Interior.InteriorIntersection,
            id="collision_camera011",
            regions=[
                RegionData(
                    "Side tunnel",
                    exits=[
                        ExitData(
                            Door.Open,
                            Interior.InteriorIntersection.subregion("Southeast"),
                        ),
                        ExitData(
                            Door.Taramarga,
                            Interior.WaveBeam.subregion("Northeast"),
                        ),
                        ExitData(
                            Door.Open,
                            Interior.InteriorIntersection.subregion("South tunnel"),
                            access_rule=lambda state, player: state.has(ItemName.ScrewAttack, player),
                        ),
                    ],
                ),
                RegionData(
                    "Southeast",
                    exits=[
                        ExitData(
                            Door.Open,
                            Interior.InteriorIntersection.subregion("Side tunnel"),
                            access_rule=can_high_ledge,
                        ),
                        ExitData(
                            Door.Normal,
                            Interior.WhimsicalWaterwheels,
                        ),
                    ],
                ),
                RegionData(
                    "South tunnel",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Interior.InteriorIntersection.subregion("South"),
                        ),
                        ExitData(
                            Door.Open,
                            Interior.InteriorIntersection.subregion("North tunnel"),
                            access_rule=can_climb_wall,
                        ),
                    ],
                ),
                RegionData(
                    "North tunnel",
                    exits=[
                        ExitData(
                            Door.Open,
                            Interior.InteriorIntersection.subregion("South tunnel"),
                        ),
                        ExitData(
                            Door.Open,
                            Interior.InteriorIntersection.subregion("South chamber"),
                            access_rule=lambda state, player: state.has(ItemName.ScrewAttack, player),
                        ),
                        ExitData(
                            Door.Open,
                            Interior.InteriorIntersection.subregion("Side tunnel"),
                            access_rule=lambda state, player: state.has(ItemName.ScrewAttack, player),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Interior.InteriorIntersection.subregion("North chamber"),
                        ),
                    ],
                ),
                RegionData(
                    "South chamber",
                    exits=[
                        ExitData(
                            Door.Open,
                            Interior.InteriorIntersection.subregion("South tunnel"),
                            access_rule=lambda state, player: state.has(ItemName.ScrewAttack, player),
                        ),
                        ExitData(
                            Door.Charge,
                            Interior.GeneratorAccess.subregion("Northeast"),
                        ),
                        ExitData(
                            Door.Missile,
                            Interior.WallfireCorridor,
                        ),
                    ],
                    pickups=[
                        PickupData("Statue"),
                        PickupData(
                            "Tunnel",
                            access_rule=lambda state, player: state.has(ItemName.ScrewAttack, player),
                        ),
                    ],
                ),
                RegionData(
                    "South",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Interior.InteriorIntersection.subregion("South tunnel"),
                            access_rule=lambda state, player: state.has(ItemName.MissileLauncher, player)
                            and can_bomb_block(state, player)
                            and can_spider(state, player),
                        ),
                        ExitData(
                            Door.Normal,
                            Interior.Gamma,
                        ),
                    ],
                ),
                RegionData(
                    "North chamber",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Interior.InteriorIntersection.subregion("North tunnel"),
                            access_rule=can_beam_block_through_fan_tunnel,
                        ),
                        ExitData(
                            Door.Taramarga,
                            Interior.WaveBeam.subregion("East"),
                        ),
                        ExitData(
                            Door.Missile,
                            Interior.WaveBeam.subregion("Chamber"),
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Interior.LavaGenerator,
            id="collision_camera012",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.Charge,
                            Interior.WaveBeam.subregion("South"),
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player),
                        ),
                        ExitData(
                            Door.Normal,
                            Interior.GeneratorAccess.subregion("Lower"),
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player),
                        ),
                        ExitData(
                            Door.PowerBomb,
                            Interior.CrumbleCavern,
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player),
                        ),
                        ExitData(
                            Door.Charge,
                            Interior.Gamma,
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player)
                            and (
                                (can_spider(state, player) and can_bomb_block(state, player))
                                or (
                                    can_damage_tough_enemy(state, player)
                                    and (
                                        can_power_bomb(state, player)
                                        or can_ibj(state, player, IBJ.option_double)
                                        or (
                                            can_movement(state, player, Movement.option_enable)
                                            and (
                                                can_wall_jump(state, player, WallJump.option_enable)
                                                or can_high_jump(state, player)
                                            )
                                        )
                                    )
                                )
                            )
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Interior.CrumbleCavern,
            id="collision_camera013",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.PowerBomb,
                            Interior.LavaGenerator,
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player),
                        )
                    ],
                    pickups=[
                        PickupData(
                            # TODO: You can probably also do this with spider boost shenanigans but I can't be bothered
                            access_rule=lambda state, player: state.has_all(
                                (
                                    ItemName.VariaSuit,
                                    ItemName.GrappleBeam,
                                    ItemName.PhaseDrift,
                                    ItemName.ScrewAttack,
                                    ItemName.MorphBall,
                                ),
                                player,
                            )
                        )
                    ],
                )
            ],
        ),
        RoomData(
            Interior.WhimsicalWaterwheels,
            id="collision_camera015",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.Normal,
                            Interior.InteriorIntersection.subregion("Southeast"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Interior.InteriorTeleporter.subregion("Upper"),
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Interior.InteriorTeleporter,
            id="collision_camera016",
            regions=[
                RegionData(
                    "Upper",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Interior.WhimsicalWaterwheels,
                        ),
                        ExitData(
                            Door.Open,
                            Interior.InteriorTeleporter.subregion("Lower"),
                            # FIXME: Dangerous action?
                        ),
                    ],
                ),
                RegionData(
                    "Lower",
                    exits=[
                        ExitData(
                            Door.Open,
                            Interior.InteriorTeleporter.subregion("Upper"),
                            access_rule=can_short_shaft,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Interior.HighJumpBootsAccess,
                            # FIXME: Dangrous action
                        ),
                        ExitData(
                            Door.Taramarga,
                            Interior.FleechFireContainment.subregion("Upper"),
                        ),
                        ExitData(
                            Door.Gryncore,
                            Interior.TeleporterStorage,
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Interior.FleechFireContainment,
            id="collision_camera017",
            regions=[
                RegionData(
                    "Upper",
                    exits=[
                        ExitData(
                            Door.Taramarga,
                            Interior.InteriorTeleporter.subregion("Lower"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Interior.FleechFireContainment.subregion("Lower"),
                            # FIXME: Dangerous action
                            access_rule=lambda state, player: state.has(ItemName.LightningArmor, player),
                        ),
                    ],
                ),
                RegionData(
                    "Lower",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Interior.FleechFireContainment.subregion("Upper"),
                            access_rule=lambda state, player: state.has(ItemName.LightningArmor, player)
                            and can_climb_shaft(state, player),
                        ),
                        ExitData(
                            Door.Normal,
                            Interior.DamBasement.subregion("Lower"),
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Interior.DamBasement,
            id="collision_camera018",
            regions=[
                RegionData(
                    "Upper",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Interior.GulluggHideout,
                        )
                    ],
                    pickups=[
                        PickupData("Upper"),
                    ],
                ),
                RegionData(
                    "Lower",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Interior.FleechFireContainment.subregion("Lower"),
                        )
                    ],
                    pickups=[
                        PickupData("Lower"),
                    ],
                ),
            ],
        ),
        RoomData(
            Interior.GulluggHideout,
            id="collision_camera019",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Interior.HighJumpBoots.subregion("Lower"),
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Interior.DamBasement.subregion("Upper"),
                            access_rule=can_high_jump,
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Interior.HighJumpBoots,
            id="collision_camera_021",
            regions=[
                RegionData(
                    "Upper",
                    exits=[
                        ExitData(
                            Door.Missile,
                            Interior.HighJumpBootsAccess,
                        ),
                        ExitData(
                            Door.Open,
                            Interior.HighJumpBoots.subregion("Lower"),
                            access_rule=can_bomb_block,
                        ),
                    ],
                    pickups=[
                        PickupData(),
                    ],
                ),
                RegionData(
                    "Lower",
                    exits=[
                        ExitData(
                            Door.Open,
                            Interior.HighJumpBoots.subregion("Upper"),
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Interior.GulluggHideout,
                            access_rule=can_bomb_block,
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Interior.HighJumpBootsAccess,
            id="collision_camera022",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Interior.InteriorTeleporter.subregion("Lower"),
                            access_rule=can_climb_wall,
                        ),
                        ExitData(
                            Door.Missile,
                            Interior.HighJumpBoots.subregion("Upper"),
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Interior.WallfireCorridor,
            id="collision_camera035",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.Normal,
                            Interior.WaveBeam.subregion("Southeast"),
                        ),
                        ExitData(
                            Door.Missile,
                            Interior.InteriorIntersection.subregion("South chamber"),
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Interior.TeleporterStorage,
            id="collision_camera036",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.Gryncore,
                            Interior.InteriorTeleporter.subregion("Lower"),
                        )
                    ],
                    pickups=[
                        PickupData(
                            access_rule=lambda state, player: state.has(ItemName.MissileLauncher, player)
                            and can_bomb_block(state, player)
                        )
                    ],
                )
            ],
        ),
        RoomData(
            Interior.Gamma,
            id="collision_camera037",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.Charge,
                            Interior.LavaGenerator,
                        ),
                        ExitData(
                            Door.Charge,
                            Interior.InteriorIntersection.subregion("South"),
                        ),
                    ],
                    pickups=[
                        PickupData(access_rule=can_damage_metroid),
                    ],
                )
            ],
        ),
        RoomData(
            Interior.VariaSuit,
            id="collision_camera040",
            regions=[],  # Unused?
        ),
        RoomData(
            Interior.GeneratorAccess,
            id="collision_camera041",
            regions=[
                RegionData(
                    "Upper",
                    exits=[
                        ExitData(
                            Door.Charge,
                            Interior.WaveBeam.subregion("South"),
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Interior.GeneratorAccess.subregion("Lower"),
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player),
                        ),
                        ExitData(
                            Door.Open,
                            Interior.GeneratorAccess.subregion("Northeast"),
                            access_rule=lambda state, player: state.has_all(
                                (ItemName.VariaSuit, ItemName.ScrewAttack), player
                            ),
                        ),
                    ],
                ),
                RegionData(
                    "Lower",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Interior.GeneratorAccess.subregion("Upper"),
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player),
                        ),
                        ExitData(
                            Door.Charge,
                            Interior.LavaGenerator,
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player),
                        ),
                    ],
                ),
                RegionData(
                    "Northeast",
                    exits=[
                        ExitData(
                            Door.Open,
                            Interior.GeneratorAccess.subregion("Upper"),
                            access_rule=lambda state, player: state.has_all(
                                (ItemName.VariaSuit, ItemName.ScrewAttack), player
                            ),
                        ),
                        ExitData(
                            Door.Charge,
                            Interior.InteriorIntersection.subregion("South chamber"),
                            access_rule=lambda state, player: state.has_all(
                                (ItemName.VariaSuit, ItemName.ScrewAttack), player
                            ),
                        ),
                    ],
                ),
            ],
        ),
    ],
)

area_2_entryway_data = AreaData(
    name="Area 2 Dam Entryway",
    id=AreaId.AREA_2_ENTRYWAY,
    rooms=[
        RoomData(
            Entryway.TransportAreas1And3,
            id="collision_camera",
            regions=[
                RegionData(
                    "Area 1",
                    exits=[
                        ExitData(
                            Door.Elevator,
                            Area1.TransportSurfaceArea2.subregion("Area 2"),
                        ),
                        # ExitData(
                        #     Door.Locked,
                        #     Entryway.EntrywayTeleporter.subregion("Upper"),
                        # ),
                        ExitData(
                            Door.MorphTunnel,
                            Entryway.TransportAreas1And3.subregion("Seal"),
                        ),
                    ],
                ),
                RegionData(
                    "Seal",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Entryway.TransportAreas1And3.subregion("Area 1"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Entryway.EntrywayTeleporter.subregion("Lower"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Entryway.TransportAreas1And3.subregion("Area 3"),
                            # Shoot out the top and free aim down for the bottom
                            access_rule=can_beam_block_through_tunnel,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Plants",
                            access_rule=lambda state, player: state.has(ItemName.MorphBall, player)
                            and state.has_any((ItemName.Hatchling, ItemName.PowerBomb), player),
                        ),
                        PickupData(
                            "Tunnel",
                            access_rule=lambda state, player: state.has(ItemName.MorphBall, player)
                            and can_bomb_block(state, player),
                        ),
                    ],
                ),
                RegionData(
                    "Area 3",
                    exits=[
                        # Grapple block has no effect
                        ExitData(
                            Door.MorphTunnel,
                            Entryway.TransportAreas1And3.subregion("Seal"),
                        ),
                        # ExitData(
                        #     Door.Elevator,
                        #     # TODO: Area 3
                        # ),
                    ],
                ),
            ],
        ),
        RoomData(
            Entryway.EntrywayTeleporter,
            id="collision_camera_003",
            regions=[
                RegionData(
                    "Lower",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Entryway.TransportAreas1And3.subregion("Seal"),
                        ),
                        ExitData(
                            Door.Open,
                            Entryway.EntrywayTeleporter.subregion("Upper"),
                            access_rule=can_high_ledge,
                        ),
                    ],
                ),
                RegionData(
                    "Upper",
                    exits=[
                        ExitData(
                            Door.Open,
                            Entryway.EntrywayTeleporter.subregion("Lower"),
                        ),
                        # No logical effect
                        # ExitData(
                        #     Door.Normal,
                        #     Entryway.TransportAreas1And3.subregion("Upper"),
                        #     access_rule=lambda state, player: state.has(ItemName.MorphBall, player),
                        # ),
                        ExitData(
                            Door.Normal,
                            Entryway.Alpha2.subregion("Arena"),
                        ),
                    ],
                    pickups=[
                        PickupData(access_rule=lambda state, player: state.has(ItemName.MorphBall, player)),
                    ],
                ),
            ],
        ),
        RoomData(
            Entryway.LightningArmor,
            id="collision_camera_004",
            regions=[
                RegionData(
                    "Lower",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Entryway.TransportAccess.subregion("Lower"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Entryway.LightningArmor.subregion("Tutorial"),
                            access_rule=lambda state, player: state.has(ItemName.LightningArmor, player),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Artifact",
                            access_rule=lambda state, player: state.has(ItemName.MorphBall, player),
                        ),
                    ],
                ),
                RegionData(
                    "Tutorial",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Entryway.LightningArmor.subregion("Lower"),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Tutorial",
                            access_rule=lambda state, player: state.has(ItemName.LightningArmor, player),
                        ),
                    ],
                    events=[
                        EventData("Opened door (from bottom)"),
                    ],
                ),
                RegionData(
                    "Upper",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Entryway.TransportAccess.subregion("Upper"),
                        ),
                        ExitData(
                            Door.Elevator,
                            Exterior.DamExterior.subregion("West"),
                        ),
                    ],
                    events=[
                        EventData("Opened door (from top)"),
                    ],
                ),
            ],
        ),
        RoomData(
            Entryway.TransportAccess,
            id="collision_camera_005",
            regions=[
                RegionData(
                    "Upper",
                    exits=[
                        ExitData(
                            Door.Open,
                            Entryway.Alpha2.subregion("Exit"),
                        ),
                        ExitData(
                            Door.Normal,
                            Entryway.LightningArmor.subregion("Upper"),
                            access_rule=lambda state, player: state.has_any(
                                (
                                    Entryway.LightningArmor.location("Opened door (from top)"),
                                    Entryway.LightningArmor.location("Opened door (from bottom)"),
                                ),
                                player,
                            ),
                        ),
                        ExitData(
                            Door.Open,
                            Entryway.TransportAccess.subregion("Lower"),
                            access_rule=lambda state, player: state.has(ItemName.LightningArmor, player)
                            or can_spider(state, player),  # TODO: SJ across?; FIXME: Dangerous action
                        ),
                    ],
                ),
                RegionData(
                    "Lower",
                    exits=[
                        ExitData(
                            Door.Open,
                            Entryway.TransportAccess.subregion("Upper"),
                            access_rule=lambda state, player: can_high_ledge(state, player)
                            and (state.has(ItemName.LightningArmor, player) or can_spider(state, player)),
                        ),
                        ExitData(
                            Door.Open,
                            Entryway.FleechSwarmFloodway,
                            access_rule=can_high_ledge,
                        ),
                        ExitData(
                            Door.Open,
                            Entryway.LightningArmor.subregion("Lower"),
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Entryway.FleechSwarmFloodway,
            id="collision_camera_006",
            regions=[
                RegionData(
                    None,
                    exits=[
                        ExitData(
                            Door.Open,
                            Entryway.TransportAccess.subregion("Lower"),
                        )
                    ],
                    pickups=[
                        PickupData(access_rule=lambda state, player: state.has(ItemName.LightningArmor, player)),
                    ],
                )
            ],
        ),
        RoomData(
            Entryway.Alpha2,
            id="collision_camera_007",
            regions=[
                RegionData(
                    "Arena",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Entryway.EntrywayTeleporter.subregion("Upper"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Entryway.Alpha2.subregion("Exit"),
                            access_rule=can_any_missile,
                        ),
                    ],
                    pickups=[
                        PickupData(access_rule=can_damage_metroid),
                    ],
                ),
                RegionData(
                    "Exit",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Entryway.Alpha2.subregion("Arena"),
                            access_rule=can_any_missile,
                        ),
                        ExitData(
                            Door.Open,
                            Entryway.TransportAccess.subregion("Upper"),
                        ),
                    ],
                ),
            ],
        ),
    ],
)
