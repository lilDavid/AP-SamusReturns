from ...items import ItemName
from ...logic import (
    can_any_missile,
    can_beam_block_through_tunnel,
    can_bomb,
    can_bomb_block,
    can_climb_shaft,
    can_climb_wall,
    can_damage_metroid,
    can_fly_straight_up,
    can_high_jump,
    can_high_ledge,
    can_ibj,
    can_movement,
    can_power_bomb,
    can_spider,
)
from ...options import IBJ, Movement
from ..internal_names import AreaId
from ..room_names import Area1
from ..room_names import Area2Entryway as Area2
from ..room_names import SurfaceEast as Surface
from . import AreaData, Door, EventData, ExitData, PickupData, RegionData, RoomData

area_1_data = AreaData(
    name="Area 1",
    id=AreaId.AREA_1,
    rooms=[
        RoomData(
            Area1.TransportSurfaceArea2,
            id="collision_camera_000",
            regions=[
                RegionData(
                    "Surface",
                    exits=[
                        ExitData(
                            Door.Elevator,
                            Surface.TransportArea1,
                        ),
                        ExitData(
                            Door.Normal,
                            Area1.MoheekMount,
                        ),
                        ExitData(
                            Door.Open,
                            Area1.TransportSurfaceArea2.subregion("Area 2"),
                            access_rule=lambda state, player: state.has(ItemName.MorphBall, player)
                            and state.has_any(
                                (ItemName.MissileLauncher, ItemName.PowerBomb, ItemName.ScrewAttack), player
                            ),
                        ),
                    ],
                ),
                RegionData(
                    "Area 2",
                    exits=[
                        ExitData(
                            Door.Open,
                            Area1.TransportSurfaceArea2.subregion("Surface"),
                            access_rule=lambda state, player: state.has(ItemName.MorphBall, player)
                            and (
                                state.has(ItemName.Bomb, player)
                                or (
                                    # Shoot the missile block in the tunnel from the opposite side
                                    can_movement(state, player, Movement.option_enable)
                                    and state.has(ItemName.MissileLauncher, player)
                                )
                                or (
                                    state.has(ItemName.ScrewAttack, player)
                                    and (
                                        can_climb_shaft(state, player)
                                        # Break spin after breaking the screw blocks so you can grab one
                                        or can_movement(state, player, Movement.option_enable)
                                    )
                                )
                            ),
                        ),
                        ExitData(
                            Door.Elevator,
                            Area2.TransportAreas1And3.subregion("Area 1"),
                        ),
                        ExitData(
                            Door.Taramarga,
                            Area1.TransportCache,
                            access_rule=lambda state, player: state.has_any(
                                (ItemName.ScrewAttack, ItemName.MorphBall), player
                            )
                            and can_high_jump(state, player)
                            and can_beam_block_through_tunnel(state, player),
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Area1.MoheekMount,
            id="collision_camera_003",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area1.TransportSurfaceArea2.subregion("Surface"),
                        ),
                        ExitData(
                            Door.Open,
                            Area1.HarmonizedHallway,
                        ),
                        ExitData(
                            Door.Charge,
                            Area1.MagmaPool.subregion("Left"),
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Area1.GulluggGangway,
            id="collision_camera_005",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Open,
                            Area1.ChuteLeechCabin,
                        ),
                        ExitData(
                            Door.Open,
                            Area1.WaterMaze.subregion("Tunnel"),
                        ),
                        ExitData(
                            Door.Gryncore,
                            Area1.WaterMaze.subregion("Maze"),
                            access_rule=lambda state, player: state.has(ItemName.WaveBeam, player),
                        ),
                        ExitData(
                            Door.Charge,
                            Area1.MagmaPool.subregion("Right"),
                        ),
                        ExitData(
                            Door.Open,
                            Area1.HarmonizedHallway,
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Area1.Bomb,
            id="collision_camera_008",
            regions=[
                RegionData(
                    "Chamber",
                    exits=[
                        ExitData(
                            Door.Missile,
                            Area1.BombAccess,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area1.Bomb.subregion("Tunnel"),
                            access_rule=can_bomb_block,
                        ),
                    ],
                    pickups=[
                        PickupData("Statue"),
                    ],
                ),
                RegionData(
                    "Tunnel",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Area1.BombAccess,
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area1.Bomb.subregion("Chamber"),
                            access_rule=can_bomb_block,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Missile",
                            access_rule=can_bomb_block,
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Area1.InnerTempleEHall,
            id="collision_camera_012",
            regions=[
                RegionData(
                    "Upper",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area1.InnerTempleUpperHallway,
                            access_rule=lambda state, player: can_climb_wall(state, player)
                            or (state.has(ItemName.HighJumpBoots, player) and can_climb_shaft(state, player)),
                        ),
                        ExitData(
                            Door.Normal,
                            Area1.TempleExterior.subregion("Southeast"),
                        ),
                        ExitData(
                            Door.Open,
                            Area1.InnerTempleEHall.subregion("Lower"),
                            access_rule=None,  # FIXME: Dangerous action
                        ),
                    ],
                ),
                RegionData(
                    "Lower",
                    exits=[
                        ExitData(
                            Door.Open,
                            Area1.InnerTempleEHall.subregion("Upper"),
                            access_rule=lambda state, player: state.has(ItemName.IceBeam, player)
                            or can_climb_wall(state, player),
                        ),
                        ExitData(
                            Door.Charge,
                            Area1.DestroyedArmory,
                        ),
                        ExitData(
                            Door.Open,
                            Area1.IceBeamAccess,
                            access_rule=None,  # FIXME: Dangerous action
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Area1.DestroyedArmory,
            id="collision_camera_014",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Charge,
                            Area1.InnerTempleEHall.subregion("Lower"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area1.SpiderBall.subregion("Tunnel"),
                            access_rule=can_bomb,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=lambda state, player: state.has_any(
                                (ItemName.SpaceJump, ItemName.IceBeam), player
                            )
                            or can_spider(state, player)
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Area1.SpiderBall,
            id="collision_camera_016",
            regions=[
                RegionData(
                    "Door access",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Area1.TempleExterior.subregion("Southeast"),
                        ),
                        ExitData(
                            Door.Normal,
                            Area1.SpiderBall.subregion("Chamber access"),
                        ),
                    ],
                ),
                RegionData(
                    "Chamber access",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Area1.SpiderBall.subregion("Chamber"),
                            access_rule=None,  # FIXME: Dangerous action
                        ),
                        ExitData(
                            Door.Open,
                            Area1.TempleExterior.subregion("Southeast"),
                        ),
                    ],
                ),
                RegionData(
                    "Chamber",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Area1.SpiderBall.subregion("Chamber access"),
                            access_rule=lambda state, player: state.has(ItemName.SpaceJump, player)
                            or can_spider(state, player)
                            or can_ibj(state, player, IBJ.option_vertical),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Buried Item",
                            access_rule=lambda state, player: state.has(ItemName.MorphBall, player),
                        )
                    ],
                ),
                RegionData(
                    "Tunnel",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Area1.DestroyedArmory,
                            access_rule=can_bomb_block,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Tunnel",
                            access_rule=can_bomb_block,
                        )
                    ],
                ),
            ],
        ),
        RoomData(
            Area1.ExteriorAlpha,
            id="collision_camera_017",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area1.TempleExterior.subregion("Southwest"),
                        ),
                    ],
                    pickups=[
                        PickupData("Alpha Metroid", access_rule=can_damage_metroid),
                        PickupData(
                            "Above Arena",
                            access_rule=lambda state, player: can_bomb_block(state, player)
                            and can_high_ledge(state, player),
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Area1.TempleExterior,
            id="collision_camera_018",
            regions=[
                RegionData(
                    "Southeast",
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area1.InnerTempleEHall.subregion("Upper"),
                        ),
                        # ExitData(
                        #     Door.Locked,
                        #     Area1.SpiderBall.subregion("Chamber"),
                        # ),
                        ExitData(
                            Door.Normal,
                            Area1.ExteriorAlpha,
                            access_rule=can_climb_wall,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area1.SpiderBall.subregion("Door access"),
                        ),
                        ExitData(
                            Door.Open,
                            Area1.TempleExterior.subregion("Center"),
                            access_rule=can_climb_wall,
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Crevice",
                            access_rule=can_high_ledge,
                        ),
                    ],
                ),
                RegionData(
                    "Center",
                    exits=[
                        ExitData(
                            Door.Open,
                            Area1.TempleExterior.subregion("Southeast"),
                        ),
                        ExitData(
                            Door.Open,
                            Area1.TempleExterior.subregion("Top"),
                            access_rule=can_climb_wall,
                        ),
                        ExitData(
                            Door.Open,
                            Area1.TempleExterior.subregion("Southwest"),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Hidden",
                            access_rule=can_bomb_block,
                        ),
                    ],
                ),
                RegionData(
                    "Southwest",
                    exits=[
                        ExitData(
                            Door.Open,
                            Area1.TempleExterior.subregion("Center"),
                            access_rule=can_climb_wall,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area1.InnerTempleVentShaft.subregion("Tunnel"),
                            access_rule=can_bomb,
                        ),
                        ExitData(
                            Door.Open,
                            Area1.ChuteLeechCabin,
                        ),
                        ExitData(
                            Door.Open,
                            Area1.InnerTempleSaveStation,
                        ),
                    ],
                ),
                RegionData(
                    "Top",
                    exits=[
                        ExitData(
                            Door.Open,
                            Area1.TempleExterior.subregion("Center"),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Ceiling",
                            access_rule=lambda state, player: can_bomb_block(state, player)
                            and can_any_missile(state, player),
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Area1.CavernsLobby,
            id="collision_camera_023",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Open,
                            Area1.CavernsHub,
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.Open,
                            Area1.CavernsEnergyRecharge,
                            access_rule=lambda state, player: (
                                can_high_ledge(state, player)
                                # Go through the topmost beam block and unmorph to regrab the ledge in the tunnel
                                or can_movement(state, player, Movement.option_enable)
                            )
                            and can_bomb_block(state, player),
                        ),
                        ExitData(
                            Door.Open,
                            Area1.CavernsAlphaSwAccess,
                        ),
                        ExitData(
                            Door.Open,
                            Area1.CavernsAlphaSe,
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Area1.CavernsAlphaSwAccess,
            id="collision_camera_024",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Open,
                            Area1.CavernsLobby,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area1.CavernsAlphaSw,
                            access_rule=lambda state, player: (
                                can_high_ledge(state, player) or state.has(ItemName.IceBeam, player)
                            )
                            and can_any_missile(state, player)
                            and state.has_any((ItemName.IceBeam, ItemName.SpaceJump), player),
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Area1.CavernsAlphaSe,
            id="collision_camera_025",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area1.CavernsLobby,
                        )
                    ],
                    pickups=[
                        PickupData(
                            access_rule=can_damage_metroid,
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Area1.CavernsAlphaNe,
            id="collision_camera_027",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area1.CavernsAlphaNeAccess,
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
            Area1.WaterMaze,
            id="collision_camera_028",
            regions=[
                RegionData(
                    "Tunnel",
                    exits=[
                        ExitData(
                            Door.Open,
                            Area1.GulluggGangway,
                        ),
                        ExitData(
                            Door.Open,
                            Area1.CavernsSaveStation.subregion("Main"),
                        ),
                    ],
                ),
                RegionData(
                    "Maze",
                    exits=[
                        ExitData(
                            Door.Gryncore,
                            Area1.GulluggGangway,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area1.WaterMaze.subregion("Pickup"),
                            # TODO: Trick for no hatchling?
                            access_rule=lambda state, player: state.has_all(
                                (ItemName.MissileLauncher, ItemName.Hatchling, ItemName.GravitySuit), player
                            ),
                        ),
                    ],
                ),
                RegionData(
                    "Pickup",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Area1.WaterMaze.subregion("Maze"),
                            access_rule=lambda state, player: state.has(ItemName.MissileLauncher, player),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area1.CavernsSaveStation.subregion("Main"),
                            access_rule=lambda state, player: state.has(
                                Area1.WaterMaze.location("Grapple Block"), player
                            ),
                        ),
                    ],
                    pickups=[
                        PickupData(),
                    ],
                    events=[
                        EventData(
                            "Grapple Block", access_rule=lambda state, player: state.has(ItemName.GrappleBeam, player)
                        )
                    ],
                ),
            ],
        ),
        RoomData(
            Area1.IceBeam,
            id="collision_camera_030",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Missile,
                            Area1.IceBeamAccess,
                        )
                    ],
                    pickups=[
                        PickupData("Statue"),
                        PickupData(
                            "Crystals",
                            access_rule=lambda state, player: state.has_all(
                                (ItemName.MorphBall, ItemName.Hatchling), player
                            )
                            and can_any_missile(state, player),
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Area1.CavernsEnergyRecharge,
            id="collision_camera_031",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Area1.CavernsLobby,
                            access_rule=can_bomb_block,
                        )
                    ],
                )
            ],
        ),
        RoomData(
            Area1.MagmaPool,
            id="collision_camera_033",
            regions=[
                RegionData(
                    "Left",
                    exits=[
                        ExitData(
                            Door.Charge,
                            Area1.MoheekMount,
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player)
                            and can_climb_wall(state, player),
                        ),
                        ExitData(
                            Door.Charge,
                            Area1.MagmaPool.subregion("Right"),
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player)
                            and (state.has(ItemName.GravitySuit, player) or can_spider(state, player)),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            "Alcove",
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player)
                            and (state.has(ItemName.SpaceJump, player) or can_spider(state, player)),
                        ),
                        PickupData(
                            "Magma",
                            access_rule=lambda state, player: state.has_all(
                                (ItemName.VariaSuit, ItemName.GravitySuit, ItemName.SuperMissile, ItemName.MorphBall),
                                player,
                            )
                            and (
                                can_fly_straight_up(state, player)
                                or (
                                    can_high_jump(state, player)
                                    and (
                                        can_spider(state, player)
                                        or (
                                            can_climb_shaft(state, player)
                                            and (
                                                state.has(ItemName.HighJumpBoots, player)
                                                # DBJ and then unmorph
                                                or can_movement(state, player, Movement.option_enable)
                                            )
                                        )
                                    )
                                )
                            ),
                        ),
                    ],
                ),
                RegionData(
                    "Right",
                    exits=[
                        ExitData(
                            Door.Charge,
                            Area1.MagmaPool.subregion("Left"),
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player)
                            and (state.has(ItemName.GravitySuit, player) or can_spider(state, player)),
                        ),
                        ExitData(
                            Door.Charge,
                            Area1.GulluggGangway,
                            access_rule=lambda state, player: state.has(ItemName.VariaSuit, player),
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Area1.InnerTempleWHall,
            id="collision_camera_035",
            regions=[
                RegionData(
                    "Upper",
                    exits=[
                        ExitData(
                            Door.Open,
                            Area1.InnerTempleSaveStation,
                            access_rule=can_climb_wall,
                        ),
                        ExitData(
                            Door.Normal,
                            Area1.InnerTempleTeleporterAccess,
                        ),
                        ExitData(
                            Door.Open,
                            Area1.BombAccess,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area1.InnerTempleWHall.subregion("Lower"),
                        ),
                    ],
                ),
                RegionData(
                    "Lower",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Area1.InnerTempleWHall.subregion("Upper"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area1.CavernsHub,
                            access_rule=can_climb_wall,
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Area1.CavernsSaveStation,
            id="collision_camera_041",
            regions=[
                RegionData(
                    "Main",
                    exits=[
                        ExitData(
                            Door.Open,
                            Area1.WaterMaze.subregion("Tunnel"),
                        ),
                        ExitData(
                            Door.Open,
                            Area1.CavernsHub,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area1.WaterMaze.subregion("Pickup"),
                            access_rule=lambda state, player: state.has(
                                Area1.WaterMaze.location("Grapple Block"), player
                            )
                            and (
                                can_spider(state, player)
                                or (state.has(ItemName.GravitySuit, player) and can_climb_shaft(state, player))
                            ),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area1.CavernsSaveStation.subregion("Pickup tunnel"),
                            access_rule=can_power_bomb,
                        ),
                    ],
                ),
                RegionData(
                    "Pickup tunnel",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Area1.CavernsHub,
                            access_rule=can_bomb_block,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area1.CavernsSaveStation.subregion("Main"),
                            access_rule=can_bomb_block,
                        ),
                    ],
                    pickups=[
                        PickupData(),
                    ],
                ),
            ],
        ),
        RoomData(
            Area1.InnerTempleTeleporterAccess,
            id="collision_camera_042",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Normal,
                            Area1.InnerTempleWHall.subregion("Upper"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area1.InnerTempleTeleporter,
                            access_rule=can_bomb_block,
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Area1.InnerTempleVentShaft,
            id="collision_camera_043",
            regions=[
                RegionData(
                    "Tunnel",
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Area1.InnerTempleUpperHallway,
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area1.TempleExterior.subregion("Southwest"),
                            access_rule=can_bomb_block,
                        ),
                    ],
                ),
                RegionData(
                    "Shaft",
                    exits=[
                        ExitData(
                            Door.Gigadora,
                            Area1.InnerTempleUpperHallway,
                        ),
                        ExitData(
                            Door.Open,
                            Area1.InnerTempleTeleporterAccess,
                            access_rule=None,  # FIXME: Dangerous action
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=lambda state, player: state.has(ItemName.SpaceJump, player)
                            or can_spider(state, player)
                        )
                    ],
                ),
            ],
        ),
        RoomData(
            Area1.CavernsHub,
            id="collision_camera_044",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Open,
                            Area1.CavernsSaveStation.subregion("Main"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area1.InnerTempleWHall.subregion("Lower"),
                            access_rule=None,  # FIXME: Dangerous action
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area1.CavernsSaveStation.subregion("Pickup tunnel"),
                            access_rule=lambda state, player: can_power_bomb(state, player)
                            or (
                                can_bomb(state, player)
                                and (can_spider(state, player) or can_ibj(state, player, IBJ.option_vertical))
                            ),
                        ),
                        ExitData(
                            Door.Open,
                            Area1.CavernsAlphaNeAccess,
                        ),
                        ExitData(
                            Door.Open,
                            Area1.CavernsLobby,
                            access_rule=can_bomb_block,
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Area1.CavernsAlphaNeAccess,
            id="collision_camera_045",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Open,
                            Area1.CavernsHub,
                        ),
                        ExitData(
                            Door.Normal,
                            Area1.CavernsAlphaNe,
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Area1.BombAccess,
            id="collision_camera_046",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Open,
                            Area1.InnerTempleWHall.subregion("Upper"),
                        ),
                        ExitData(
                            Door.Missile,
                            Area1.Bomb.subregion("Chamber"),
                        ),
                        ExitData(
                            Door.MorphTunnel,
                            Area1.Bomb.subregion("Tunnel"),
                            access_rule=can_bomb_block,
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Area1.InnerTempleSaveStation,
            id="collision_camera_047",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Open,
                            Area1.InnerTempleWHall.subregion("Upper"),
                            access_rule=None,  # FIXME: Dangerous action
                        ),
                        ExitData(
                            Door.Open,
                            Area1.TempleExterior.subregion("Southwest"),
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Area1.InnerTempleUpperHallway,
            id="collision_camera_048",
            regions=[
                RegionData(
                    exits=[
                        # ExitData(
                        #     Door.Locked,
                        #     Area1.InnerTempleEHall.subregion("Upper"),
                        # ),
                        ExitData(
                            Door.MorphTunnel,
                            Area1.InnerTempleVentShaft.subregion("Tunnel"),
                        ),
                        ExitData(
                            Door.Gigadora,
                            Area1.InnerTempleVentShaft.subregion("Shaft"),
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Area1.InnerTempleTeleporter,
            id="collision_camera_049",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Area1.InnerTempleTeleporterAccess,
                            access_rule=can_bomb,
                        ),
                        ExitData(
                            Door.Open,
                            Area1.InnerTempleEHall.subregion("Lower"),
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Area1.IceBeamAccess,
            id="collision_camera_050",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Open,
                            Area1.InnerTempleEHall.subregion("Lower"),
                            access_rule=lambda state, player: state.has(ItemName.IceBeam, player)
                            or can_high_jump(state, player),
                        ),
                        ExitData(
                            Door.Missile,
                            Area1.IceBeam,
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Area1.TransportCache,
            id="collision_camera_051",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Taramarga,
                            Area1.TransportSurfaceArea2.subregion("Area 2"),
                        ),
                    ],
                    pickups=[
                        PickupData(
                            access_rule=can_bomb_block,
                        ),
                    ],
                )
            ],
        ),
        RoomData(
            Area1.HarmonizedHallway,
            id="collision_camera_052",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Open,
                            Area1.MoheekMount,
                        ),
                        ExitData(
                            Door.Open,
                            Area1.GulluggGangway,
                        ),
                    ],
                ),
            ],
        ),
        RoomData(
            Area1.CavernsAlphaSw,
            id="collision_camera_054",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.MorphTunnel,
                            Area1.CavernsAlphaSwAccess,
                            access_rule=can_bomb_block,
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
            Area1.ChuteLeechCabin,
            id="collision_camera_055",
            regions=[
                RegionData(
                    exits=[
                        ExitData(
                            Door.Open,
                            Area1.GulluggGangway,
                        ),
                        ExitData(
                            Door.Open,
                            Area1.TempleExterior.subregion("Southwest"),
                        ),
                    ],
                )
            ],
        ),
    ],
)
