from ...items import ItemName
from ...logic import (
    can_any_missile,
    can_bomb_block,
    can_climb_shaft,
    can_climb_wall,
    can_damage_metroid,
    can_fly_straight_up,
    can_high_ledge,
    can_power_bomb,
    can_spider,
    can_wall_jump,
)
from ...options import WallJump
from ..internal_names import AreaId
from ..room_names import Area1
from ..room_names import SurfaceEast as East
from ..room_names import SurfaceWest as West
from . import AreaData, Door, ExitData, PickupData, RegionData, RoomData, subregion

surface_east_data = AreaData(
    name="Surface East",
    id=AreaId.SURFACE_EAST,
    rooms={
        East.LandingSite: RoomData(
            id="collision_camera_000",
            region_data={
                "East": RegionData(
                    exits=[
                        ExitData(
                            Door.Open,
                            subregion(East.LandingSite, "West"),
                            access_rule=can_climb_wall,
                        ),
                        ExitData(
                            Door.Open,
                            subregion(East.HornoadHallway, "West"),
                        ),
                    ]
                ),
                "West": RegionData(
                    exits=[
                        ExitData(
                            Door.Open,
                            subregion(East.LandingSite, "East"),
                            access_rule=can_climb_wall,
                        ),
                        ExitData(
                            Door.Gigadora,
                            East.SurfaceStash,
                            access_rule=can_climb_wall,
                        ),
                        ExitData(
                            Door.Open,
                            East.SurfaceCrumbleChallenge,
                            access_rule=lambda state, player: can_climb_wall(state, player)
                            and can_power_bomb(state, player),
                        ),
                        ExitData(
                            Door.Open,
                            West.TransportArea8,
                            access_rule=lambda state, player: state.has(ItemName.Hatchling, player),
                        ),
                    ]
                ),
            },
        ),
        East.TwistyTunnel: RoomData(
            id="collision_camera_002",
            region_data=RegionData(
                exits=[
                    ExitData(
                        Door.Normal,
                        East.HornoadHallway,
                    ),
                    ExitData(
                        Door.Missile,
                        East.MorphBall,
                    ),
                ],
                pickups=[
                    PickupData(
                        access_rule=lambda state, player: state.has("Morph Ball", player),
                    ),
                ],
            ),
        ),
        East.MorphBall: RoomData(
            id="collision_camera_003",
            region_data={
                "Upper": RegionData(
                    exits=[
                        ExitData(
                            Door.Missile,
                            East.TwistyTunnel,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            subregion(East.MorphBall, "Lower"),
                        ),
                    ],
                    pickups=[
                        PickupData(),
                    ],
                ),
                "Lower": RegionData(
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            subregion(East.MorphBall, "Upper"),
                            access_rule=can_high_ledge,
                        ),
                        ExitData(
                            Door.Normal,
                            subregion(East.ChozoSeal, "Upper"),
                        ),
                    ],
                ),
            },
        ),
        East.ChozoSeal: RoomData(
            id="collision_camera_004",
            region_data={
                "Upper": RegionData(
                    exits=[
                        ExitData(
                            Door.Normal,
                            subregion(East.MorphBall, "Lower"),
                        ),
                        ExitData(
                            Door.Normal,
                            subregion(East.ScanPulse, "Right"),
                        ),
                        ExitData(
                            Door.Open,
                            subregion(East.ChozoSeal, "Lower"),
                        ),
                    ],
                ),
                "Lower": RegionData(
                    exits=[
                        ExitData(
                            Door.Open,
                            subregion(East.ChozoSeal, "Upper"),
                            access_rule=can_high_ledge,
                        ),
                        ExitData(
                            Door.Normal,
                            East.TransportArea1,
                        ),
                    ],
                ),
                "Tunnel": RegionData(
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            East.TransportArea1,
                        ),
                    ],
                    pickups=[
                        PickupData(),
                    ],
                ),
            },
        ),
        East.TransportArea1: RoomData(
            id="collision_camera_006",
            region_data=RegionData(
                exits=[
                    ExitData(
                        Door.Normal,
                        subregion(East.ChozoSeal, "Lower"),
                    ),
                    ExitData(
                        Door.MorphTunnel,
                        subregion(East.ChozoSeal, "Tunnel"),
                        access_rule=can_bomb_block,
                    ),
                    ExitData(
                        Door.Elevator,
                        Area1.TransportSurfaceArea2,
                    ),
                    ExitData(
                        Door.Open,
                        East.TransportCache,
                        access_rule=lambda state, player: state.has(ItemName.Hatchling, player),
                    ),
                ],
                pickups=[
                    PickupData(
                        access_rule=lambda state, player: state.has(ItemName.MorphBall, player)
                        and can_high_ledge(state, player),
                    ),
                ],
            ),
        ),
        East.ChozoCacheE: RoomData(
            id="collision_camera_007",
            region_data=RegionData(
                exits=[
                    ExitData(
                        Door.MorphTunnel,
                        East.ChargeBeamAccess,
                    )
                ],
                pickups=[
                    PickupData(),
                ],
            ),
        ),
        East.ChargeBeam: RoomData(
            id="collision_camera_008",
            region_data=RegionData(
                exits=[
                    ExitData(
                        Door.Missile,
                        East.ChargeBeamAccess,
                        access_rule=can_high_ledge,
                    ),
                    ExitData(
                        Door.Charge,
                        East.ChargeBeamAccess,
                    ),
                ],
                pickups=[
                    PickupData(),
                ],
                pickups_require_exit=True,
            ),
        ),
        East.Alpha: RoomData(
            id="collision_camera_010",
            region_data={
                "Lobby": RegionData(
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            subregion(East.EnergyRechargeShaft, "Lower"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            subregion(East.Alpha, "Arena"),
                            access_rule=can_any_missile,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            East.MoheekMarket,
                        ),
                        ExitData(
                            Door.Gryncore,
                            East.ChozoCacheW,
                        ),
                    ],
                ),
                "Arena": RegionData(
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            subregion(East.Alpha, "Lobby"),
                            access_rule=lambda state, player: can_damage_metroid(state, player)
                            and can_any_missile(state, player),
                        ),
                        ExitData(
                            Door.Normal,
                            East.AmmoRecharge,
                            access_rule=can_damage_metroid,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Alpha Metroid",
                            access_rule=can_damage_metroid,
                        )
                    ],
                ),
                "Pickup": RegionData(
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            East.MoheekMarket,
                        ),
                    ],
                    pickups=[
                        PickupData("Missile"),
                    ],
                ),
            },
        ),
        East.ScanPulse: RoomData(
            id="collision_camera_011",
            region_data={
                "Right": RegionData(
                    exits=[
                        ExitData(
                            Door.Normal,
                            subregion(East.ChozoSeal, "Upper"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            subregion(East.ScanPulse, "Left"),
                        ),
                    ],
                ),
                "Left": RegionData(
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            subregion(East.ScanPulse, "Right"),
                        ),
                        ExitData(
                            Door.Charge,
                            East.ChargeBeamAccess,
                        ),
                        ExitData(
                            Door.Open,
                            East.CavernCavity,
                        ),
                    ],
                ),
            },
        ),
        East.ChozoCacheW: RoomData(
            id="collision_camera_012",
            region_data=RegionData(
                exits=[
                    ExitData(
                        Door.Gryncore,
                        subregion(East.Alpha, "Lobby"),
                    )
                ],
                pickups=[
                    PickupData(),
                ],
            ),
        ),
        East.MoheekMarket: RoomData(
            id="collision_camera_013",
            region_data=RegionData(
                exits=[
                    ExitData(
                        Door.MorphTunnel,
                        subregion(East.Alpha, "Lobby"),
                    ),
                    ExitData(
                        Door.MorphTunnel,
                        subregion(East.Alpha, "Pickup"),
                    ),
                ],
            ),
        ),
        East.CavernCavity: RoomData(
            id="collision_camera_014",
            region_data=RegionData(
                exits=[
                    ExitData(
                        Door.Open,
                        subregion(East.ScanPulse, "Left"),
                        access_rule=can_climb_shaft,
                    ),
                    ExitData(
                        Door.Normal,
                        subregion(East.EnergyRechargeShaft, "Top"),
                    ),
                    ExitData(
                        Door.MorphTunnel,
                        East.CavernCavity,
                    ),
                ],
            ),
        ),
        East.ChargeBeamAccess: RoomData(
            id="collision_camera_015",
            region_data=RegionData(
                exits=[
                    ExitData(
                        Door.Charge,
                        subregion(East.ScanPulse, "Left"),
                    ),
                    ExitData(
                        Door.MorphTunnel,
                        East.ChozoCacheE,
                    ),
                    ExitData(
                        Door.Missile,
                        East.ChargeBeam,
                    ),
                    ExitData(
                        Door.Charge,
                        East.ChargeBeam,
                    ),
                    ExitData(
                        Door.Normal,
                        East.AmmoRecharge,
                    ),
                ],
                pickups=[
                    PickupData(
                        access_rule=lambda state, player: state.has(ItemName.MorphBall, player),
                    ),
                ],
            ),
        ),
        East.HornoadHallway: RoomData(
            id="collision_camera_016",
            region_data={
                "West": RegionData(
                    exits=[
                        ExitData(
                            Door.Open,
                            East.LandingSite,
                        ),
                        ExitData(
                            Door.Open,
                            subregion(East.HornoadHallway, "East"),
                            access_rule=lambda state, player:
                            # Break or morph under the block
                            can_any_missile(state, player)
                            or state.has(ItemName.MorphBall, player)
                            # Climb the shaft overhead
                            or can_fly_straight_up(state, player)
                            or (
                                state.has(ItemName.HighJumpBoots)
                                and can_wall_jump(state, player, WallJump.option_enable)
                            ),
                        ),
                    ]
                ),
                "East": RegionData(
                    exits=[
                        ExitData(
                            Door.Open,
                            subregion(East.HornoadHallway, "West"),
                            access_rule=None,  # Drop down the upper path
                        ),
                        ExitData(
                            Door.Open,
                            East.TwistyTunnel,
                            access_rule=lambda state, player: can_any_missile(state, player)
                            or can_climb_shaft(state, player),
                        ),
                    ]
                ),
            },
        ),
        East.SurfaceStash: RoomData(
            id="collision_camera_018",
            region_data=RegionData(
                exits=[
                    ExitData(
                        Door.Gigadora,
                        subregion(East.LandingSite, "West"),
                    ),
                ],
                pickups=[
                    PickupData(
                        access_rule=lambda state, player:
                        # Reach the top
                        can_any_missile(state, player)
                        and state.has_all((ItemName.GrappleBeam, ItemName.MorphBall))
                        # Cross the pitfall blocks
                        and (can_spider(state, player) or state.has(ItemName.PhaseDrift))
                        # Escape
                        and can_climb_shaft(state, player)
                    )
                ],
            ),
        ),
        East.SurfaceCrumbleChallenge: RoomData(
            id="collision_camera_019",
            region_data=RegionData(
                exits=[
                    ExitData(
                        Door.Open,
                        subregion(East.LandingSite, "West"),
                    )
                ],
                pickups=[
                    PickupData(
                        access_rule=None  # Drop off and power grip for it (movement trick?)
                    ),
                ],
            ),
        ),
        East.TransportCache: RoomData(
            id="collision_camera_020",
            region_data=RegionData(
                exits=[
                    ExitData(
                        Door.Open,
                        East.TransportArea1,
                        access_rule=lambda state, player: state.has(ItemName.Hatchling, player),
                    ),
                ]
            ),
        ),
        East.CavernAlcove: RoomData(
            id="collision_camera_021",
            region_data=RegionData(
                exits=[
                    ExitData(
                        Door.MorphTunnel,
                        East.CavernCavity,
                    )
                ],
                pickups=[
                    PickupData(
                        access_rule=lambda state, player: state.has(ItemName.MorphBall, player)
                        and can_climb_shaft(state, player)
                    )
                ],
            ),
        ),
        East.EnergyRechargeShaft: RoomData(
            id="collision_camera_023",
            region_data={
                "Upper": RegionData(
                    exits=[
                        ExitData(
                            Door.Normal,
                            East.CavernCavity,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            subregion(East.CavernCavity, "Lower"),
                        ),
                    ],
                    pickups=[
                        PickupData(access_rule=lambda state, player: state.has(ItemName.MorphBall, player)),
                    ],
                ),
                "Lower": RegionData(
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            subregion(East.CavernCavity, "Upper"),
                            access_rule=can_high_ledge,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            subregion(East.Alpha, "Lobby"),
                        ),
                    ],
                    pickups=[
                        PickupData(access_rule=lambda state, player: state.has(ItemName.MorphBall, player)),
                    ],
                ),
            },
        ),
        East.AmmoRecharge: RoomData(
            id="collision_camera_024",
            region_data=RegionData(
                exits=[
                    ExitData(
                        Door.Normal,
                        subregion(East.Alpha, "Arena"),
                    ),
                    ExitData(
                        Door.Normal,
                        East.ChargeBeamAccess,
                    ),
                ]
            ),
        ),
    },
)

surface_west_data = AreaData(
    name="Surface West",
    id=AreaId.SURFACE_WEST,
    rooms={
        West.TransportArea8: RoomData(
            id="collision_camera_017",
            region_data={},  # TODO
        ),
    },
)
