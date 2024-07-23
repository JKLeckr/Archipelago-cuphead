from typing import NamedTuple, Optional, Callable
from .names import LocationNames, ItemNames
from .Settings import WorldSettings
from .Levels import LevelData, level_rule_plane

class Target(NamedTuple):
    name: str
    rule: Optional[Callable] = None
class RegionData:
    name: str
    locations: list[str]
    connect_to: list[Target]
    def __init__(self, name: str, locations: list[str] = None, connect_to: list[Target] = None) -> None:
        self.name = name
        self.locations = locations
        self.connect_to = connect_to

def define_regions(player: int, levels: dict[str, LevelData], level_shuffle_map: dict[str, str], settings: WorldSettings) -> list[RegionData]:
    using_dlc = settings.use_dlc
    freemove_islands = settings.freemove_isles
    contract_requirements = settings.contract_requirements
    dlc_ingredient_requirements = settings.dlc_ingredient_requirements
    agrade_quest = settings.agrade_quest
    pacifist_quest = settings.pacifist_quest
    wolfgang_quest = settings.wolfgang_quest
    dlc_cactusgirl_quest = settings.dlc_cactusgirl_quest
    require_secret_shortcuts = settings.require_secret_shortcuts

    # Overrides for Levels (to automatically account for level shuffling)
    def _level_map(level: str) -> LevelData:
        if level not in levels:
            return LevelData(None,[])
        if level in level_shuffle_map:
            return levels[level_shuffle_map[level]]
        else:
            return levels[level]
    class LevelTarget(Target):
        def __new__(cls, name: str, add_rule: Optional[Callable] = None) -> Target:
            _rule = _level_map(name).rule
            _add_rule = add_rule if add_rule else lambda state: True
            return super().__new__(cls, name, (lambda state: _rule(state,player) and _add_rule(state)) if _rule else None)
    class LevelRegionData(RegionData):
        def __init__(self, name: str, add_locations: list[str] = None, connect_to: list[Target] = None, ignore_freemove_islands: bool = False) -> None:
            _locations = list(_level_map(name).locations)
            if add_locations:
                _locations += add_locations
            super().__init__(name, _locations, connect_to if not freemove_islands or ignore_freemove_islands else None)

    region_begin = RegionData("Menu", None, [Target(LocationNames.level_house)])
    region_house = RegionData(LocationNames.level_house, None, [
        Target(LocationNames.level_tutorial), Target(LocationNames.world_inkwell_1)])

    region_house_level_tutorial = RegionData(LocationNames.level_tutorial, [
        LocationNames.loc_level_tutorial,
        LocationNames.loc_level_tutorial_coin,
    ], None)

    region_shop = RegionData(LocationNames.level_shop, None, [
        Target(LocationNames.loc_shop_weapon1), Target(LocationNames.loc_shop_weapon2), Target(LocationNames.loc_shop_weapon3),
        Target(LocationNames.loc_shop_weapon4), Target(LocationNames.loc_shop_weapon5), Target(LocationNames.loc_shop_charm1),
        Target(LocationNames.loc_shop_charm2), Target(LocationNames.loc_shop_charm3), Target(LocationNames.loc_shop_charm4),
        Target(LocationNames.loc_shop_charm5),  Target(LocationNames.loc_shop_charm6),
        Target(LocationNames.loc_shop_dlc_weapon6) if using_dlc else None, Target(LocationNames.loc_shop_dlc_weapon7) if using_dlc else None,
        Target(LocationNames.loc_shop_dlc_weapon8) if using_dlc else None, Target(LocationNames.loc_shop_dlc_charm7) if using_dlc else None,
        Target(LocationNames.loc_shop_dlc_charm8) if using_dlc else None,
    ])
    #region_dlc_shop = RegionData(LocationNames.level_dlc_shop, None, [
    #    Target(LocationNames.loc_shop_dlc_weapon6), Target(LocationNames.loc_shop_dlc_weapon7), Target(LocationNames.loc_shop_dlc_weapon8),
    #    Target(LocationNames.loc_shop_dlc_charm7), Target(LocationNames.loc_shop_dlc_charm8), Target(LocationNames.loc_shop_weapon1),
    #    Target(LocationNames.loc_shop_weapon2), Target(LocationNames.loc_shop_weapon3), Target(LocationNames.loc_shop_weapon4),
    #    Target(LocationNames.loc_shop_weapon5),
    #])
    region_shop_items = [
        RegionData(LocationNames.loc_shop_weapon1, [
            LocationNames.loc_shop_weapon1,
            #LocationNames.loc_shop_weapon1_bought
        ], None),
        RegionData(LocationNames.loc_shop_weapon2, [
            LocationNames.loc_shop_weapon2,
            #LocationNames.loc_shop_weapon2_bought
        ], None),
        RegionData(LocationNames.loc_shop_weapon3, [
            LocationNames.loc_shop_weapon3,
            #LocationNames.loc_shop_weapon3_bought
        ], None),
        RegionData(LocationNames.loc_shop_weapon4, [
            LocationNames.loc_shop_weapon4,
            #LocationNames.loc_shop_weapon4_bought
        ], None),
        RegionData(LocationNames.loc_shop_weapon5, [
            LocationNames.loc_shop_weapon5,
            #LocationNames.loc_shop_weapon5_bought
        ], None),
        RegionData(LocationNames.loc_shop_charm1, [
            LocationNames.loc_shop_charm1,
            #LocationNames.loc_shop_charm1_bought
        ], None),
        RegionData(LocationNames.loc_shop_charm2, [
            LocationNames.loc_shop_charm2,
            #LocationNames.loc_shop_charm2_bought
        ], None),
        RegionData(LocationNames.loc_shop_charm3, [
            LocationNames.loc_shop_charm3,
            #LocationNames.loc_shop_charm3_bought
        ], None),
        RegionData(LocationNames.loc_shop_charm4, [
            LocationNames.loc_shop_charm4,
            #LocationNames.loc_shop_charm4_bought
        ], None),
        RegionData(LocationNames.loc_shop_charm5, [
            LocationNames.loc_shop_charm5,
            #LocationNames.loc_shop_charm5_bought
        ], None),
        RegionData(LocationNames.loc_shop_charm6, [
            LocationNames.loc_shop_charm6,
            #LocationNames.loc_shop_charm6_bought
        ], None),
    ]
    region_dlc_shop_items = [
        RegionData(LocationNames.loc_shop_dlc_weapon6, [LocationNames.loc_shop_dlc_weapon6, LocationNames.loc_shop_dlc_weapon6_bought], None),
        RegionData(LocationNames.loc_shop_dlc_weapon7, [LocationNames.loc_shop_dlc_weapon7, LocationNames.loc_shop_dlc_weapon7_bought], None),
        RegionData(LocationNames.loc_shop_dlc_weapon8, [LocationNames.loc_shop_dlc_weapon8, LocationNames.loc_shop_dlc_weapon8_bought], None),
        RegionData(LocationNames.loc_shop_dlc_charm7, [LocationNames.loc_shop_dlc_charm7, LocationNames.loc_shop_dlc_charm7_bought], None),
        RegionData(LocationNames.loc_shop_dlc_charm8, [LocationNames.loc_shop_dlc_charm8, LocationNames.loc_shop_dlc_charm8_bought], None),
    ] if using_dlc else []

    region_worlds = [
        RegionData(LocationNames.world_inkwell_1, [
            LocationNames.loc_npc_mac,
            LocationNames.loc_coin_isle1_secret,
        ], [
            Target(LocationNames.level_shop),
            Target(LocationNames.world_dlc_inkwell_4,
                lambda state: (state.has(ItemNames.item_event_dlc_boataccess, player))) if using_dlc else None,
            LevelTarget(LocationNames.level_boss_veggies), LevelTarget(LocationNames.level_boss_slime), LevelTarget(LocationNames.level_rungun_forest),
        ] + ([
            LevelTarget(LocationNames.level_boss_flower),
            LevelTarget(LocationNames.level_rungun_tree),
        ] if require_secret_shortcuts or freemove_islands else []) + ([
            Target(LocationNames.world_inkwell_2,
                lambda state: (state.has(ItemNames.item_contract, player, contract_requirements[0]))),
            LevelTarget(LocationNames.level_boss_frogs), LevelTarget(LocationNames.level_boss_plane_blimp),
            Target(LocationNames.level_mausoleum_i)
        ] if freemove_islands else [])),
        RegionData(LocationNames.world_inkwell_2, [
            LocationNames.loc_npc_canteen,
            LocationNames.loc_quest_4mel,
        ], [
            LevelTarget(LocationNames.level_boss_baroness), LevelTarget(LocationNames.level_boss_clown), LevelTarget(LocationNames.level_boss_plane_genie)
        ] + ([
            Target(LocationNames.world_inkwell_3,
                lambda state: (state.has(ItemNames.item_contract, player, contract_requirements[1]))),
            LevelTarget(LocationNames.level_boss_plane_bird), LevelTarget(LocationNames.level_boss_dragon),
            LevelTarget(LocationNames.level_rungun_circus), LevelTarget(LocationNames.level_rungun_funhouse),
            LevelTarget(LocationNames.level_mausoleum_ii), Target(LocationNames.loc_event_isle2_shortcut)
        ] if freemove_islands else [])),
        RegionData(LocationNames.world_inkwell_3, None, [
            LevelTarget(LocationNames.level_boss_bee), LevelTarget(LocationNames.level_boss_pirate)
        ] + ([
            Target(LocationNames.world_inkwell_hell),
            LevelTarget(LocationNames.level_boss_plane_robot),
            LevelTarget(LocationNames.level_rungun_mountain),
            LevelTarget(LocationNames.level_boss_sallystageplay),
            LevelTarget(LocationNames.level_boss_mouse),
            LevelTarget(LocationNames.level_boss_train),
            LevelTarget(LocationNames.level_boss_plane_mermaid),
            LevelTarget(LocationNames.level_rungun_harbour),
            LevelTarget(LocationNames.level_mausoleum_iii),
            Target(LocationNames.loc_quest_ludwig),
        ] if freemove_islands else [])),
        RegionData(LocationNames.world_inkwell_hell, [LocationNames.loc_coin_isleh_secret], [
            Target(LocationNames.level_boss_kingdice,
                lambda state: (state.has(ItemNames.item_contract, player, contract_requirements[2]) and level_rule_plane(state,player)))]),
    ]
    region_dlc_worlds = [
        RegionData(LocationNames.world_dlc_inkwell_4, [
            LocationNames.loc_dlc_npc_newscat,
            LocationNames.loc_dlc_coin_isle4_secret,
        ], [
            Target(LocationNames.level_dlc_tutorial),
            Target(LocationNames.level_dlc_chesscastle),
            LevelTarget(LocationNames.level_dlc_boss_oldman),
            LevelTarget(LocationNames.level_dlc_boss_rumrunners),
            #Target(LocationNames.level_dlc_shop),
        ] + ([
            LevelTarget(LocationNames.level_dlc_boss_plane_cowboy),
            LevelTarget(LocationNames.level_dlc_boss_snowcult),
            LevelTarget(LocationNames.level_dlc_boss_airplane),
            #LevelTarget(LocationNames.level_dlc_graveyard),
            LevelTarget(LocationNames.level_dlc_boss_saltbaker,
                lambda state: (state.has(ItemNames.item_dlc_ingredient, player, dlc_ingredient_requirements))),
        ] if freemove_islands else [])),
    ] if using_dlc else []

    region_isle1 =  [
        LevelRegionData(LocationNames.level_boss_veggies, [LocationNames.loc_event_isle1_secret_prereq1],
            [LevelTarget(LocationNames.level_boss_frogs)]),
        LevelRegionData(LocationNames.level_boss_slime, [LocationNames.loc_event_isle1_secret_prereq2],
            [LevelTarget(LocationNames.level_boss_plane_blimp)]),
        LevelRegionData(LocationNames.level_boss_plane_blimp, [LocationNames.loc_event_isle1_secret_prereq3],
            [LevelTarget(LocationNames.level_boss_flower), LevelTarget(LocationNames.level_rungun_tree)]),
        LevelRegionData(LocationNames.level_boss_frogs, [LocationNames.loc_event_isle1_secret_prereq4],
            [LevelTarget(LocationNames.level_mausoleum_i)]),
        LevelRegionData(LocationNames.level_boss_flower, [LocationNames.loc_event_isle1_secret_prereq5], [
            Target(LocationNames.world_inkwell_2,
                lambda state: (state.has(ItemNames.item_contract, player, contract_requirements[0])))]),
        LevelRegionData(LocationNames.level_rungun_tree, None, [Target(LocationNames.level_mausoleum_i)]),
        LevelRegionData(LocationNames.level_rungun_forest, None, [Target(LocationNames.level_mausoleum_i)]),
        LevelRegionData(LocationNames.level_mausoleum_i, None, None)
    ]
    region_isle2 = [
        LevelRegionData(LocationNames.level_boss_baroness, None, [
            LevelTarget(LocationNames.level_boss_plane_bird),
            LevelTarget(LocationNames.level_rungun_circus),
            Target(LocationNames.loc_event_isle2_shortcut)]),
        LevelRegionData(LocationNames.level_boss_plane_genie, None, [LevelTarget(LocationNames.level_mausoleum_ii)]),
        LevelRegionData(LocationNames.level_boss_clown, None, [
            LevelTarget(LocationNames.level_boss_dragon),
            LevelTarget(LocationNames.level_rungun_funhouse),
            Target(LocationNames.loc_event_isle2_shortcut),
            Target(LocationNames.world_inkwell_3, lambda state: (state.has(ItemNames.item_contract, player, contract_requirements[1])))]),
        LevelRegionData(LocationNames.level_boss_plane_bird, None, [LevelTarget(LocationNames.level_mausoleum_ii)]),
        LevelRegionData(LocationNames.level_boss_dragon, [
            LocationNames.loc_quest_4parries,
        ], [LevelTarget(LocationNames.level_mausoleum_ii)]),
        LevelRegionData(LocationNames.level_rungun_circus, [
            LocationNames.loc_event_quest_4mel_4th,
            LocationNames.loc_quest_ginger,
        ], [LevelTarget(LocationNames.level_mausoleum_ii)]),
        LevelRegionData(LocationNames.level_rungun_funhouse, [LocationNames.loc_coin_isle2_secret], [LevelTarget(LocationNames.level_mausoleum_ii)]),
        LevelRegionData(LocationNames.level_mausoleum_ii, [
            LocationNames.loc_quest_lucien,
        ], None),
        RegionData(LocationNames.loc_event_isle2_shortcut, [
            LocationNames.loc_event_isle2_shortcut
        ], [
            LevelTarget(LocationNames.level_boss_dragon),
            LevelTarget(LocationNames.level_rungun_funhouse),
            LevelTarget(LocationNames.level_boss_plane_bird),
            LevelTarget(LocationNames.level_rungun_circus),
        ] if require_secret_shortcuts and not freemove_islands else None)
    ]
    region_isle3 = [
        LevelRegionData(LocationNames.level_boss_bee, None, [
            LevelTarget(LocationNames.level_boss_plane_robot),
            LevelTarget(LocationNames.level_rungun_mountain),
            Target(LocationNames.loc_quest_ludwig) if wolfgang_quest else None]),
        LevelRegionData(LocationNames.level_boss_pirate, None, [
            LevelTarget(LocationNames.level_boss_plane_mermaid),
            LevelTarget(LocationNames.level_rungun_harbour),
            Target(LocationNames.loc_quest_pacifist)  if pacifist_quest else None,
        ]),
        LevelRegionData(LocationNames.level_boss_plane_robot, None, [LevelTarget(LocationNames.level_boss_sallystageplay)]),
        LevelRegionData(LocationNames.level_boss_plane_mermaid, [LocationNames.loc_coin_isle3_secret], [
            LevelTarget(LocationNames.level_boss_sallystageplay)]),
        LevelRegionData(LocationNames.level_boss_sallystageplay, [
            LocationNames.loc_quest_wolfgang
        ], [
            LevelTarget(LocationNames.level_boss_mouse),
            LevelTarget(LocationNames.level_mausoleum_iii),
            LevelTarget(LocationNames.level_boss_train),
            Target(LocationNames.loc_quest_15agrades) if agrade_quest else None]),
        LevelRegionData(LocationNames.level_boss_mouse, None, None),
        LevelRegionData(LocationNames.level_boss_train, None, [Target(LocationNames.world_inkwell_hell)]),
        LevelRegionData(LocationNames.level_rungun_harbour, None, [
            LevelTarget(LocationNames.level_boss_mouse),
            LevelTarget(LocationNames.level_mausoleum_iii),
            Target(LocationNames.loc_quest_15agrades) if agrade_quest else None]),
        LevelRegionData(LocationNames.level_rungun_mountain, None, [
            LevelTarget(LocationNames.level_boss_mouse),
            LevelTarget(LocationNames.level_mausoleum_iii),
            Target(LocationNames.loc_quest_15agrades) if agrade_quest else None]),
        LevelRegionData(LocationNames.level_mausoleum_iii, None, None),
        RegionData(LocationNames.loc_quest_ludwig, [
            LocationNames.loc_quest_ludwig,
            LocationNames.loc_event_music
        ], None) if wolfgang_quest else None,
        RegionData(LocationNames.loc_quest_15agrades, [LocationNames.loc_quest_15agrades], None) if agrade_quest else None,
        RegionData(LocationNames.loc_quest_pacifist, [LocationNames.loc_quest_pacifist], None) if pacifist_quest else None,
    ]
    region_isleh = [
        LevelRegionData(LocationNames.level_boss_kingdice, None, [LevelTarget(LocationNames.level_boss_devil)], True),
        LevelRegionData(LocationNames.level_boss_devil, None, None),
    ]
    region_dlc_isle4 = [
        # Setup regions later
        RegionData(LocationNames.level_dlc_tutorial, [
            LocationNames.loc_level_dlc_tutorial,
            LocationNames.loc_level_dlc_tutorial_coin,
        ], None),
        LevelRegionData(LocationNames.level_dlc_boss_oldman, None, [LevelTarget(LocationNames.level_dlc_boss_snowcult)]),
        LevelRegionData(LocationNames.level_dlc_boss_rumrunners, None, [
            LevelTarget(LocationNames.level_dlc_boss_plane_cowboy),
            Target(LocationNames.loc_dlc_quest_cactusgirl)  if dlc_cactusgirl_quest else None,
        ]),
        LevelRegionData(LocationNames.level_dlc_boss_plane_cowboy, None, [
            LevelTarget(LocationNames.level_dlc_boss_airplane)
            #LevelTarget(LocationNames.level_dlc_graveyard),
        ]),
        LevelRegionData(LocationNames.level_dlc_boss_snowcult, None, [
            LevelTarget(LocationNames.level_dlc_boss_airplane),
            #LevelTarget(LocationNames.level_dlc_graveyard),
        ]),
        LevelRegionData(LocationNames.level_dlc_boss_airplane, [
            LevelTarget(LocationNames.level_dlc_boss_snowcult),
            LevelTarget(LocationNames.level_dlc_boss_plane_cowboy),
            Target(LocationNames.loc_dlc_quest_cactusgirl)  if dlc_cactusgirl_quest else None,
        ]),
        LevelRegionData(LocationNames.level_dlc_boss_saltbaker, None),
        #LevelRegionData(LocationNames.level_dlc_graveyard, None),
        RegionData(LocationNames.level_dlc_chesscastle, None, [
            LevelTarget(LocationNames.level_dlc_chesscastle_pawn)
        ]),
        RegionData(LocationNames.loc_dlc_quest_cactusgirl, [LocationNames.loc_dlc_quest_cactusgirl], None) if dlc_cactusgirl_quest else None,
    ] if using_dlc else []
    region_dlc_chesscastle = [
        # Setup Regions later
        LevelRegionData(LocationNames.level_dlc_chesscastle_pawn, None, [LevelTarget(LocationNames.level_dlc_chesscastle_knight)]),
        LevelRegionData(LocationNames.level_dlc_chesscastle_knight, None, [LevelTarget(LocationNames.level_dlc_chesscastle_bishop)]),
        LevelRegionData(LocationNames.level_dlc_chesscastle_bishop, None, [LevelTarget(LocationNames.level_dlc_chesscastle_rook)]),
        LevelRegionData(LocationNames.level_dlc_chesscastle_rook, None, [LevelTarget(LocationNames.level_dlc_chesscastle_queen)]),
        LevelRegionData(LocationNames.level_dlc_chesscastle_queen, None, [LevelTarget(LocationNames.level_dlc_chesscastle_run)]),
        LevelRegionData(LocationNames.level_dlc_chesscastle_run, None)
    ] if using_dlc else []
    region_dlc_special = [
        # Add Logic Regions and connections to curse_complete
    ] if using_dlc else []

    total_regions: list[RegionData] = [
        region_begin,
        region_house,
        region_house_level_tutorial,
        region_shop,
    ]
    total_regions += region_worlds + region_isle1 + region_isle2 + region_isle3 + region_isleh + region_shop_items

    total_dlc_regions = [
        #region_dlc_shop,
        region_dlc_shop_items,
    ]
    if using_dlc:
        total_regions += total_dlc_regions + region_dlc_worlds + region_dlc_isle4 + region_dlc_chesscastle + region_dlc_special + region_dlc_shop_items

    return total_regions
