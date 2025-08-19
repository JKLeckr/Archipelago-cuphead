from __future__ import annotations
from collections.abc import Iterable
from ..names import LocationNames, ItemNames
from ..rules.rulebase import RegionRule, rrule_has, rrule_has_all
from .regionbase import DefFlags, Target, LevelTarget, RegionData, LevelRegionData, WorldRegionData
from . import dep

def rule_has(item: str, count: int = 1) -> RegionRule:
    return rrule_has(item, count)
def rule_has_all(items: Iterable[str]) -> RegionRule:
    return rrule_has_all(items)

region_begin: RegionData = RegionData(
    "Start",
    [LocationNames.loc_event_start_weapon, LocationNames.loc_event_start_weapon_ex],
    [Target(LocationNames.level_house)],
    flags=DefFlags.TGT_IGNORE_FREEMOVE
)
region_house: RegionData = RegionData(LocationNames.level_house, None, [
        LevelTarget(LocationNames.level_tutorial),
        Target(LocationNames.world_inkwell_1)
    ], flags=DefFlags.TGT_IGNORE_FREEMOVE)

region_house_level_tutorial: RegionData = LevelRegionData(
    LocationNames.level_tutorial, None, None, flags=DefFlags.TGT_IGNORE_FREEMOVE
)

region_dlc_start: list[RegionData] = [
    RegionData(
        LocationNames.loc_event_mausoleum, [LocationNames.loc_event_mausoleum], None, dep.dep_dlc_boat_mausoleum
    ),
    RegionData(
        LocationNames.reg_dlc_boat, [LocationNames.loc_event_dlc_boatarrival], None, flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
]

# Shop Regions are defined in shop.py

region_worlds: list[RegionData] = [
    WorldRegionData(LocationNames.world_inkwell_1, [
        LocationNames.loc_npc_mac,
        LocationNames.loc_coin_isle1_secret,
    ], [
        Target(LocationNames.shop_set1),
        Target(LocationNames.reg_dlc_boat, None, dep.dep_and(dep.dep_dlc, dep.dep_freemove)),
        Target(LocationNames.world_dlc_inkwell_4, rule_has(ItemNames.item_event_dlc_boataccess), dep.dep_dlc),
        LevelTarget(LocationNames.level_boss_veggies),
        LevelTarget(LocationNames.level_boss_slime),
        LevelTarget(LocationNames.level_rungun_forest),
        LevelTarget(LocationNames.level_boss_flower, None, dep.dep_or(dep.dep_shortcuts, dep.dep_freemove)),
        LevelTarget(LocationNames.level_rungun_tree, None, dep.dep_or(dep.dep_shortcuts, dep.dep_freemove)),
        Target(LocationNames.world_inkwell_2, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_boss_frogs, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_boss_plane_blimp, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_mausoleum_i, None, dep.dep_freemove),
    ]),
    WorldRegionData(LocationNames.world_inkwell_2, [
        LocationNames.loc_npc_canteen,
        LocationNames.loc_quest_4mel,
    ], [
        Target(LocationNames.shop_set2, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_boss_baroness),
        LevelTarget(LocationNames.level_boss_clown),
        LevelTarget(LocationNames.level_boss_plane_genie),
        Target(LocationNames.world_inkwell_3, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_boss_plane_bird, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_boss_dragon, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_rungun_circus, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_rungun_funhouse, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_mausoleum_ii, None, dep.dep_freemove),
        Target(LocationNames.loc_event_isle2_shortcut, None, dep.dep_freemove),
        Target(LocationNames.reg_dlc_boat, None, dep.dep_dlc),
    ]),
    WorldRegionData(LocationNames.world_inkwell_3, None, [
        Target(LocationNames.shop_set3, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_boss_bee),
        LevelTarget(LocationNames.level_boss_pirate),
        Target(LocationNames.world_inkwell_hell, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_boss_plane_robot, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_rungun_mountain, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_boss_sallystageplay, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_boss_mouse, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_boss_train, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_boss_plane_mermaid, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_rungun_harbour, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_mausoleum_iii, None, dep.dep_freemove),
        Target(LocationNames.loc_quest_ludwig, None, dep.dep_and(dep.dep_freemove, dep.dep_music_quest)),
        Target(LocationNames.loc_quest_silverworth, None, dep.dep_and(dep.dep_freemove, dep.dep_agrade_quest)),
        Target(LocationNames.loc_quest_pacifist, None, dep.dep_and(dep.dep_freemove, dep.dep_pacifist_quest)),
        Target(LocationNames.reg_dlc_boat, None, dep.dep_and(dep.dep_dlc, dep.dep_not(dep.dep_freemove))),
    ]),
    WorldRegionData(LocationNames.world_inkwell_hell, [LocationNames.loc_coin_isleh_secret], [
        Target(LocationNames.level_boss_kingdice)
    ]),
]
region_dlc_worlds = [
    WorldRegionData(LocationNames.world_dlc_inkwell_4, [
        LocationNames.loc_dlc_cookie,
        LocationNames.loc_event_dlc_cookie,
        LocationNames.loc_dlc_npc_newscat,
        LocationNames.loc_dlc_coin_isle4_secret,
    ], [
        Target(LocationNames.shop_set4),
        Target(LocationNames.level_dlc_chesscastle),
        Target(
            LocationNames.loc_dlc_quest_cactusgirl, None, dep.dep_and(dep.dep_freemove, dep.dep_dlc_cactusgirl_quest)
        ),
        LevelTarget(LocationNames.level_dlc_tutorial, None, dep.dep_dlc_chalice),
        LevelTarget(LocationNames.level_dlc_boss_oldman),
        LevelTarget(LocationNames.level_dlc_boss_rumrunners),
        LevelTarget(LocationNames.level_dlc_boss_plane_cowboy, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_dlc_boss_snowcult, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_dlc_boss_airplane, None, dep.dep_freemove),
        #LevelTarget(LocationNames.level_dlc_graveyard, None, dep.dep_freemove),
        LevelTarget(LocationNames.level_dlc_boss_saltbaker, None)
    ]),
]

region_isle1 =  [
    LevelRegionData(LocationNames.level_boss_veggies, [LocationNames.loc_event_isle1_secret_prereq1],
        [LevelTarget(LocationNames.level_boss_frogs)]),
    LevelRegionData(LocationNames.level_boss_slime, [LocationNames.loc_event_isle1_secret_prereq2],
        [LevelTarget(LocationNames.level_boss_plane_blimp)]),
    LevelRegionData(LocationNames.level_boss_plane_blimp, [LocationNames.loc_event_isle1_secret_prereq3],
        [LevelTarget(LocationNames.level_boss_flower), LevelTarget(LocationNames.level_rungun_tree)]),
    LevelRegionData(LocationNames.level_boss_frogs, [LocationNames.loc_event_isle1_secret_prereq4],
        [LevelTarget(LocationNames.level_mausoleum_i), Target(LocationNames.reg_dlc_boat, None, dep.dep_dlc)]),
    LevelRegionData(LocationNames.level_boss_flower, [LocationNames.loc_event_isle1_secret_prereq5],
        [Target(LocationNames.world_inkwell_2, None, dep.dep_not(dep.dep_freemove))]),
    LevelRegionData(LocationNames.level_rungun_tree, None,
        [LevelTarget(LocationNames.level_mausoleum_i), Target(LocationNames.reg_dlc_boat, None, dep.dep_dlc)]),
    LevelRegionData(LocationNames.level_rungun_forest, None,
        [LevelTarget(LocationNames.level_mausoleum_i), Target(LocationNames.reg_dlc_boat, None, dep.dep_dlc)]),
    LevelRegionData(LocationNames.level_mausoleum_i, None,
        [Target(LocationNames.loc_event_mausoleum, None, dep.dep_dlc_boat_mausoleum)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    )
]
region_isle2: list[RegionData] = [
    LevelRegionData(LocationNames.level_boss_baroness, None, [
        LevelTarget(LocationNames.level_boss_plane_bird),
        LevelTarget(LocationNames.level_rungun_circus),
        Target(LocationNames.loc_event_isle2_shortcut)
    ]),
    LevelRegionData(LocationNames.level_boss_plane_genie, None, [
        LevelTarget(LocationNames.level_mausoleum_ii),
        Target(LocationNames.loc_quest_lucien, None, dep.dep_lucien_quest),
        Target(LocationNames.shop_set2),
    ]),
    LevelRegionData(LocationNames.level_boss_clown, None, [
        LevelTarget(LocationNames.level_boss_dragon),
        LevelTarget(LocationNames.level_rungun_funhouse),
        Target(LocationNames.loc_event_isle2_shortcut),
        Target(LocationNames.world_inkwell_3, None, dep.dep_not(dep.dep_freemove))
    ]),
    LevelRegionData(LocationNames.level_boss_plane_bird, None, [
        LevelTarget(LocationNames.level_mausoleum_ii),
        Target(LocationNames.loc_quest_lucien, None, dep.dep_lucien_quest),
        Target(LocationNames.shop_set2),
    ]),
    LevelRegionData(LocationNames.level_boss_dragon, [
        LocationNames.loc_quest_buster,
    ], [
        LevelTarget(LocationNames.level_mausoleum_ii),
        Target(LocationNames.loc_quest_lucien, None, dep.dep_lucien_quest),
        Target(LocationNames.shop_set2),
    ]),
    LevelRegionData(LocationNames.level_rungun_circus, [
        LocationNames.loc_event_quest_4mel_4th,
        LocationNames.loc_quest_ginger,
    ], [
        LevelTarget(LocationNames.level_mausoleum_ii),
        Target(LocationNames.loc_quest_lucien, None, dep.dep_lucien_quest),
        Target(LocationNames.shop_set2),
    ]),
    LevelRegionData(LocationNames.level_rungun_funhouse, [LocationNames.loc_coin_isle2_secret], [
        LevelTarget(LocationNames.level_mausoleum_ii),
        Target(LocationNames.loc_quest_lucien, None, dep.dep_lucien_quest),
        Target(LocationNames.shop_set2),
    ]),
    LevelRegionData(
        LocationNames.level_mausoleum_ii, None,
        [Target(LocationNames.loc_event_mausoleum, None, dep.dep_dlc_boat_mausoleum)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    RegionData(LocationNames.loc_quest_lucien, [LocationNames.loc_quest_lucien], None, dep.dep_lucien_quest),
    RegionData(LocationNames.loc_event_isle2_shortcut, [
        LocationNames.loc_event_isle2_shortcut
    ], [
        LevelTarget(
            LocationNames.level_boss_dragon, None, dep.dep_and(dep.dep_shortcuts, dep.dep_not(dep.dep_freemove))
        ),
        LevelTarget(
            LocationNames.level_rungun_funhouse, None, dep.dep_and(dep.dep_shortcuts, dep.dep_not(dep.dep_freemove))
        ),
        LevelTarget(
            LocationNames.level_boss_plane_bird, None, dep.dep_and(dep.dep_shortcuts, dep.dep_not(dep.dep_freemove))
        ),
        LevelTarget(
            LocationNames.level_rungun_circus, None, dep.dep_and(dep.dep_shortcuts, dep.dep_not(dep.dep_freemove))
        ),
    ])
]
region_isle3: list[RegionData] = [
    LevelRegionData(LocationNames.level_boss_bee, None, [
        LevelTarget(LocationNames.level_boss_plane_robot),
        LevelTarget(LocationNames.level_rungun_mountain),
        Target(LocationNames.loc_quest_ludwig, None, dep.dep_music_quest)
    ]),
    LevelRegionData(LocationNames.level_boss_pirate, None, [
        LevelTarget(LocationNames.level_boss_plane_mermaid),
        LevelTarget(LocationNames.level_rungun_harbour),
        Target(LocationNames.loc_quest_pacifist, None, dep.dep_pacifist_quest),
        Target(LocationNames.reg_dlc_boat, None, dep.dep_dlc),
    ]),
    LevelRegionData(LocationNames.level_boss_plane_robot, None, [
        LevelTarget(LocationNames.level_boss_sallystageplay),
        Target(LocationNames.loc_quest_wolfgang, None, dep.dep_music_quest)
    ]),
    LevelRegionData(LocationNames.level_boss_plane_mermaid, [LocationNames.loc_coin_isle3_secret], [
        LevelTarget(LocationNames.level_boss_sallystageplay),
        Target(LocationNames.loc_quest_wolfgang, None, dep.dep_music_quest)
    ]),
    LevelRegionData(LocationNames.level_boss_sallystageplay, None, [
        LevelTarget(LocationNames.level_boss_mouse),
        LevelTarget(LocationNames.level_mausoleum_iii),
        LevelTarget(LocationNames.level_boss_train),
        Target(LocationNames.shop_set3),
        Target(LocationNames.loc_quest_silverworth, None, dep.dep_agrade_quest)
    ]),
    LevelRegionData(LocationNames.level_boss_mouse, None, [
        LevelTarget(LocationNames.level_boss_sallystageplay),
        Target(LocationNames.loc_quest_wolfgang, None, dep.dep_music_quest)
    ]),
    LevelRegionData(LocationNames.level_boss_train, None, [Target(LocationNames.world_inkwell_hell)]),
    LevelRegionData(LocationNames.level_rungun_harbour, None, [
        LevelTarget(LocationNames.level_boss_mouse),
        LevelTarget(LocationNames.level_mausoleum_iii),
        Target(LocationNames.shop_set3),
        Target(LocationNames.loc_quest_silverworth, None, dep.dep_agrade_quest)
    ]),
    LevelRegionData(LocationNames.level_rungun_mountain, None, [
        LevelTarget(LocationNames.level_boss_mouse),
        LevelTarget(LocationNames.level_mausoleum_iii),
        Target(LocationNames.shop_set3),
        Target(LocationNames.loc_quest_silverworth, None, dep.dep_agrade_quest)
    ]),
    LevelRegionData(
        LocationNames.level_mausoleum_iii, None,
        [Target(LocationNames.loc_event_mausoleum, None, dep.dep_dlc_boat_mausoleum)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    RegionData(LocationNames.loc_quest_wolfgang, [
        LocationNames.loc_quest_music
    ], None, dep.dep_music_quest),
    RegionData(LocationNames.loc_quest_ludwig, [
        LocationNames.loc_event_quest_ludwig,
    ], None, dep.dep_music_quest),
    RegionData(LocationNames.loc_quest_silverworth, [LocationNames.loc_quest_silverworth], None, dep.dep_agrade_quest),
    RegionData(LocationNames.loc_quest_pacifist, [LocationNames.loc_quest_pacifist], None, dep.dep_pacifist_quest),
]
region_isleh: list[RegionData] = [
    LevelRegionData(
        LocationNames.level_boss_kingdice, None,
        [LevelTarget(LocationNames.level_boss_devil)],
        flags=DefFlags.DICE_PALACE
    ),
    LevelRegionData(LocationNames.level_boss_devil, None, None),
]
region_dlc_isle4: list[RegionData] = [
    RegionData(LocationNames.level_dlc_tutorial, [
        LocationNames.loc_level_dlc_tutorial,
        LocationNames.loc_level_dlc_tutorial_coin,
    ], None, dep.dep_dlc_chalice),
    LevelRegionData(LocationNames.level_dlc_boss_oldman, None, [LevelTarget(LocationNames.level_dlc_boss_snowcult)]),
    LevelRegionData(LocationNames.level_dlc_boss_rumrunners, None, [
        LevelTarget(LocationNames.level_dlc_boss_plane_cowboy),
        Target(LocationNames.loc_dlc_quest_cactusgirl, None, dep.dep_dlc_cactusgirl_quest),
    ]),
    LevelRegionData(LocationNames.level_dlc_boss_plane_cowboy, None, [
        LevelTarget(LocationNames.level_dlc_boss_airplane)
        #LevelTarget(LocationNames.level_dlc_graveyard),
    ]),
    LevelRegionData(LocationNames.level_dlc_boss_snowcult, None, [
        LevelTarget(LocationNames.level_dlc_boss_airplane),
        #LevelTarget(LocationNames.level_dlc_graveyard),
    ]),
    LevelRegionData(LocationNames.level_dlc_boss_airplane, None, [
        LevelTarget(LocationNames.level_dlc_boss_snowcult),
        LevelTarget(LocationNames.level_dlc_boss_plane_cowboy),
        Target(LocationNames.loc_dlc_quest_cactusgirl, None, dep.dep_dlc_cactusgirl_quest),
    ]),
    LevelRegionData(LocationNames.level_dlc_boss_saltbaker, None, None),
    #LevelRegionData(LocationNames.level_dlc_graveyard, None),
    RegionData(LocationNames.level_dlc_chesscastle, None, [
        LevelTarget(LocationNames.level_dlc_chesscastle_pawn)
    ], flags=DefFlags.TGT_IGNORE_FREEMOVE),
    RegionData(
        LocationNames.loc_dlc_quest_cactusgirl,
        [LocationNames.loc_dlc_quest_cactusgirl],
        None,
        dep.dep_dlc_cactusgirl_quest
    ),
]
region_dlc_chesscastle: list[RegionData] = [
    LevelRegionData(
        LocationNames.level_dlc_chesscastle_pawn, None,
        [LevelTarget(LocationNames.level_dlc_chesscastle_knight)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    LevelRegionData(
        LocationNames.level_dlc_chesscastle_knight, None,
        [LevelTarget(LocationNames.level_dlc_chesscastle_bishop)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    LevelRegionData(
        LocationNames.level_dlc_chesscastle_bishop, None,
        [LevelTarget(LocationNames.level_dlc_chesscastle_rook)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    LevelRegionData(
        LocationNames.level_dlc_chesscastle_rook, None,
        [LevelTarget(LocationNames.level_dlc_chesscastle_queen)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    LevelRegionData(
        LocationNames.level_dlc_chesscastle_queen, None,
        [LevelTarget(LocationNames.level_dlc_chesscastle_run)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    LevelRegionData(
        LocationNames.level_dlc_chesscastle_run, None, None,
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    )
]
region_dlc_special: list[RegionData] = []

regions_start: list[RegionData] = [
    region_begin,
    region_house,
    region_house_level_tutorial,
]
regions_base: list[RegionData] = (
    region_worlds + region_isle1 + region_isle2 + region_isle3 + region_isleh
)
regions_dlc: list[RegionData] = (
    region_dlc_start + region_dlc_worlds + region_dlc_isle4 + region_dlc_chesscastle + region_dlc_special
)

regions_all: list[RegionData] = regions_start + regions_base + regions_dlc
