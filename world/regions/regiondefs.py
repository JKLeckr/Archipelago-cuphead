### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from collections.abc import Iterable

from ..names import itemnames, locationnames
from ..rules import deps
from ..rules.rulebase import RegionRule, rrule_has, rrule_has_all
from .regionbase import DefFlags, LevelRegionData, LevelTarget, RegionData, Target, WorldRegionData


def rule_has(item: str, count: int = 1) -> RegionRule:
    return rrule_has(item, count)
def rule_has_all(items: Iterable[str]) -> RegionRule:
    return rrule_has_all(items)

region_begin: RegionData = RegionData(
    "Start",
    [locationnames.loc_event_start_weapon, locationnames.loc_event_start_weapon_ex],
    [Target(locationnames.level_house)],
    flags=DefFlags.TGT_IGNORE_FREEMOVE
)
region_house: RegionData = RegionData(locationnames.level_house, None, [
        LevelTarget(locationnames.level_tutorial),
        Target(locationnames.world_inkwell_1)
    ], flags=DefFlags.TGT_IGNORE_FREEMOVE)

region_house_level_tutorial: RegionData = LevelRegionData(
    locationnames.level_tutorial, None, None, flags=DefFlags.TGT_IGNORE_FREEMOVE
)

region_dlc_start: list[RegionData] = [
    RegionData(
        locationnames.loc_event_mausoleum, [locationnames.loc_event_mausoleum], None, deps.dep_dlc_boat_mausoleum
    ),
    RegionData(
        locationnames.reg_dlc_boat, [locationnames.loc_event_dlc_boatarrival], None, flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
]

# Shop Regions are defined in shop.py

region_worlds: list[RegionData] = [
    WorldRegionData(locationnames.world_inkwell_1, [
        locationnames.loc_npc_mac,
        locationnames.loc_coin_isle1_secret,
    ], [
        Target(locationnames.shop_set1),
        Target(locationnames.reg_dlc_boat, None, deps.dep_and(deps.dep_dlc, deps.dep_freemove)),
        Target(locationnames.world_dlc_inkwell_4, rule_has(itemnames.item_event_dlc_boataccess), deps.dep_dlc),
        LevelTarget(locationnames.level_boss_veggies),
        LevelTarget(locationnames.level_boss_slime),
        LevelTarget(locationnames.level_rungun_forest),
        LevelTarget(locationnames.level_boss_flower, None, deps.dep_or(deps.dep_shortcuts, deps.dep_freemove)),
        LevelTarget(locationnames.level_rungun_tree, None, deps.dep_or(deps.dep_shortcuts, deps.dep_freemove)),
        Target(locationnames.world_inkwell_2, None, deps.dep_freemove),
        LevelTarget(locationnames.level_boss_frogs, None, deps.dep_freemove),
        LevelTarget(locationnames.level_boss_plane_blimp, None, deps.dep_freemove),
        LevelTarget(locationnames.level_mausoleum_i, None, deps.dep_freemove),
    ]),
    WorldRegionData(locationnames.world_inkwell_2, [
        locationnames.loc_npc_canteen,
        locationnames.loc_quest_4mel,
    ], [
        Target(locationnames.shop_set2, None, deps.dep_freemove),
        LevelTarget(locationnames.level_boss_baroness),
        LevelTarget(locationnames.level_boss_clown),
        LevelTarget(locationnames.level_boss_plane_genie),
        Target(locationnames.world_inkwell_3, None, deps.dep_freemove),
        LevelTarget(locationnames.level_boss_plane_bird, None, deps.dep_freemove),
        LevelTarget(locationnames.level_boss_dragon, None, deps.dep_freemove),
        LevelTarget(locationnames.level_rungun_circus, None, deps.dep_freemove),
        LevelTarget(locationnames.level_rungun_funhouse, None, deps.dep_freemove),
        LevelTarget(locationnames.level_mausoleum_ii, None, deps.dep_freemove),
        Target(locationnames.loc_event_isle2_shortcut, None, deps.dep_freemove),
        Target(locationnames.reg_dlc_boat, None, deps.dep_dlc),
    ]),
    WorldRegionData(locationnames.world_inkwell_3, None, [
        Target(locationnames.shop_set3, None, deps.dep_freemove),
        LevelTarget(locationnames.level_boss_bee),
        LevelTarget(locationnames.level_boss_pirate),
        Target(locationnames.world_inkwell_hell, None, deps.dep_freemove),
        LevelTarget(locationnames.level_boss_plane_robot, None, deps.dep_freemove),
        LevelTarget(locationnames.level_rungun_mountain, None, deps.dep_freemove),
        LevelTarget(locationnames.level_boss_sallystageplay, None, deps.dep_freemove),
        LevelTarget(locationnames.level_boss_mouse, None, deps.dep_freemove),
        LevelTarget(locationnames.level_boss_train, None, deps.dep_freemove),
        LevelTarget(locationnames.level_boss_plane_mermaid, None, deps.dep_freemove),
        LevelTarget(locationnames.level_rungun_harbour, None, deps.dep_freemove),
        LevelTarget(locationnames.level_mausoleum_iii, None, deps.dep_freemove),
        Target(locationnames.loc_quest_ludwig, None, deps.dep_and(deps.dep_freemove, deps.dep_music_quest)),
        Target(locationnames.loc_quest_silverworth, None, deps.dep_and(deps.dep_freemove, deps.dep_agrade_quest)),
        Target(locationnames.loc_quest_pacifist, None, deps.dep_and(deps.dep_freemove, deps.dep_pacifist_quest)),
        Target(locationnames.reg_dlc_boat, None, deps.dep_and(deps.dep_dlc, deps.dep_not(deps.dep_freemove))),
    ]),
    WorldRegionData(locationnames.world_inkwell_hell, [locationnames.loc_coin_isleh_secret], [
        Target(locationnames.level_boss_kingdice)
    ]),
]
region_dlc_worlds = [
    WorldRegionData(locationnames.world_dlc_inkwell_4, [
        locationnames.loc_dlc_cookie,
        locationnames.loc_event_dlc_cookie,
        locationnames.loc_dlc_npc_newscat,
        locationnames.loc_dlc_coin_isle4_secret,
    ], [
        Target(locationnames.shop_set4),
        Target(locationnames.level_dlc_chesscastle),
        Target(
            locationnames.loc_dlc_quest_cactusgirl, None, deps.dep_and(deps.dep_freemove, deps.dep_dlc_cactusgirl_quest)
        ),
        LevelTarget(locationnames.level_dlc_tutorial, None, deps.dep_dlc_chalice),
        LevelTarget(locationnames.level_dlc_boss_oldman),
        LevelTarget(locationnames.level_dlc_boss_rumrunners),
        LevelTarget(locationnames.level_dlc_boss_plane_cowboy, None, deps.dep_freemove),
        LevelTarget(locationnames.level_dlc_boss_snowcult, None, deps.dep_freemove),
        LevelTarget(locationnames.level_dlc_boss_airplane, None, deps.dep_or(deps.dep_shortcuts, deps.dep_freemove)),
        #LevelTarget(locationnames.level_dlc_graveyard, None, dep.dep_freemove),
        LevelTarget(locationnames.level_dlc_boss_saltbaker, None)
    ]),
]

region_isle1 =  [
    LevelRegionData(locationnames.level_boss_veggies, [locationnames.loc_event_isle1_secret_prereq1],
        [LevelTarget(locationnames.level_boss_frogs)]),
    LevelRegionData(locationnames.level_boss_slime, [locationnames.loc_event_isle1_secret_prereq2],
        [LevelTarget(locationnames.level_boss_plane_blimp)]),
    LevelRegionData(locationnames.level_boss_plane_blimp, [locationnames.loc_event_isle1_secret_prereq3],
        [LevelTarget(locationnames.level_boss_flower), LevelTarget(locationnames.level_rungun_tree)]),
    LevelRegionData(locationnames.level_boss_frogs, [locationnames.loc_event_isle1_secret_prereq4],
        [LevelTarget(locationnames.level_mausoleum_i), Target(locationnames.reg_dlc_boat, None, deps.dep_dlc)]),
    LevelRegionData(locationnames.level_boss_flower, [locationnames.loc_event_isle1_secret_prereq5],
        [Target(locationnames.world_inkwell_2, None, deps.dep_not(deps.dep_freemove))]),
    LevelRegionData(locationnames.level_rungun_tree, None,
        [LevelTarget(locationnames.level_mausoleum_i), Target(locationnames.reg_dlc_boat, None, deps.dep_dlc)]),
    LevelRegionData(locationnames.level_rungun_forest, None,
        [LevelTarget(locationnames.level_mausoleum_i), Target(locationnames.reg_dlc_boat, None, deps.dep_dlc)]),
    LevelRegionData(locationnames.level_mausoleum_i, None,
        [Target(locationnames.loc_event_mausoleum, None, deps.dep_dlc_boat_mausoleum)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    )
]
region_isle2: list[RegionData] = [
    LevelRegionData(locationnames.level_boss_baroness, None, [
        LevelTarget(locationnames.level_boss_plane_bird),
        LevelTarget(locationnames.level_rungun_circus),
        Target(locationnames.loc_event_isle2_shortcut)
    ]),
    LevelRegionData(locationnames.level_boss_plane_genie, None, [
        LevelTarget(locationnames.level_mausoleum_ii),
        Target(locationnames.loc_quest_lucien, None, deps.dep_lucien_quest),
        Target(locationnames.shop_set2),
    ]),
    LevelRegionData(locationnames.level_boss_clown, None, [
        LevelTarget(locationnames.level_boss_dragon),
        LevelTarget(locationnames.level_rungun_funhouse),
        Target(locationnames.loc_event_isle2_shortcut),
        Target(locationnames.world_inkwell_3, None, deps.dep_not(deps.dep_freemove))
    ]),
    LevelRegionData(locationnames.level_boss_plane_bird, None, [
        LevelTarget(locationnames.level_mausoleum_ii),
        Target(locationnames.loc_quest_lucien, None, deps.dep_lucien_quest),
        Target(locationnames.shop_set2),
    ]),
    LevelRegionData(locationnames.level_boss_dragon, [
        locationnames.loc_quest_buster,
    ], [
        LevelTarget(locationnames.level_mausoleum_ii),
        Target(locationnames.loc_quest_lucien, None, deps.dep_lucien_quest),
        Target(locationnames.shop_set2),
    ]),
    LevelRegionData(locationnames.level_rungun_circus, [
        locationnames.loc_event_quest_4mel_4th,
        locationnames.loc_quest_ginger,
    ], [
        LevelTarget(locationnames.level_mausoleum_ii),
        Target(locationnames.loc_quest_lucien, None, deps.dep_lucien_quest),
        Target(locationnames.shop_set2),
    ]),
    LevelRegionData(locationnames.level_rungun_funhouse, [locationnames.loc_coin_isle2_secret], [
        LevelTarget(locationnames.level_mausoleum_ii),
        Target(locationnames.loc_quest_lucien, None, deps.dep_lucien_quest),
        Target(locationnames.shop_set2),
    ]),
    LevelRegionData(
        locationnames.level_mausoleum_ii, None,
        [Target(locationnames.loc_event_mausoleum, None, deps.dep_dlc_boat_mausoleum)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    RegionData(locationnames.loc_quest_lucien, [locationnames.loc_quest_lucien], None, deps.dep_lucien_quest),
    RegionData(locationnames.loc_event_isle2_shortcut, [
        locationnames.loc_event_isle2_shortcut
    ], [
        LevelTarget(
            locationnames.level_boss_dragon, None, deps.dep_and(deps.dep_shortcuts, deps.dep_not(deps.dep_freemove))
        ),
        LevelTarget(
            locationnames.level_rungun_funhouse, None, deps.dep_and(deps.dep_shortcuts, deps.dep_not(deps.dep_freemove))
        ),
        LevelTarget(
            locationnames.level_boss_plane_bird, None, deps.dep_and(deps.dep_shortcuts, deps.dep_not(deps.dep_freemove))
        ),
        LevelTarget(
            locationnames.level_rungun_circus, None, deps.dep_and(deps.dep_shortcuts, deps.dep_not(deps.dep_freemove))
        ),
    ])
]
region_isle3: list[RegionData] = [
    LevelRegionData(locationnames.level_boss_bee, None, [
        LevelTarget(locationnames.level_boss_plane_robot),
        LevelTarget(locationnames.level_rungun_mountain),
        Target(locationnames.loc_quest_ludwig, None, deps.dep_music_quest)
    ]),
    LevelRegionData(locationnames.level_boss_pirate, None, [
        LevelTarget(locationnames.level_boss_plane_mermaid),
        LevelTarget(locationnames.level_rungun_harbour),
        Target(locationnames.loc_quest_pacifist, None, deps.dep_pacifist_quest),
        Target(locationnames.reg_dlc_boat, None, deps.dep_dlc),
    ]),
    LevelRegionData(locationnames.level_boss_plane_robot, None, [
        LevelTarget(locationnames.level_boss_sallystageplay),
        Target(locationnames.loc_quest_wolfgang, None, deps.dep_music_quest)
    ]),
    LevelRegionData(locationnames.level_boss_plane_mermaid, [locationnames.loc_coin_isle3_secret], [
        LevelTarget(locationnames.level_boss_sallystageplay),
        Target(locationnames.loc_quest_wolfgang, None, deps.dep_music_quest)
    ]),
    LevelRegionData(locationnames.level_boss_sallystageplay, None, [
        LevelTarget(locationnames.level_boss_mouse),
        LevelTarget(locationnames.level_mausoleum_iii),
        LevelTarget(locationnames.level_boss_train),
        Target(locationnames.shop_set3),
        Target(locationnames.loc_quest_silverworth, None, deps.dep_agrade_quest)
    ]),
    LevelRegionData(locationnames.level_boss_mouse, None, [
        LevelTarget(locationnames.level_boss_sallystageplay),
        Target(locationnames.loc_quest_wolfgang, None, deps.dep_music_quest)
    ]),
    LevelRegionData(locationnames.level_boss_train, None, [Target(locationnames.world_inkwell_hell)]),
    LevelRegionData(locationnames.level_rungun_harbour, None, [
        LevelTarget(locationnames.level_boss_mouse),
        LevelTarget(locationnames.level_mausoleum_iii),
        Target(locationnames.shop_set3),
        Target(locationnames.loc_quest_silverworth, None, deps.dep_agrade_quest)
    ]),
    LevelRegionData(locationnames.level_rungun_mountain, None, [
        LevelTarget(locationnames.level_boss_mouse),
        LevelTarget(locationnames.level_mausoleum_iii),
        Target(locationnames.shop_set3),
        Target(locationnames.loc_quest_silverworth, None, deps.dep_agrade_quest)
    ]),
    LevelRegionData(
        locationnames.level_mausoleum_iii, None,
        [Target(locationnames.loc_event_mausoleum, None, deps.dep_dlc_boat_mausoleum)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    RegionData(locationnames.loc_quest_wolfgang, [
        locationnames.loc_quest_music
    ], None, deps.dep_music_quest),
    RegionData(locationnames.loc_quest_ludwig, [
        locationnames.loc_event_quest_ludwig,
    ], None, deps.dep_music_quest),
    RegionData(locationnames.loc_quest_silverworth, [locationnames.loc_quest_silverworth], None, deps.dep_agrade_quest),
    RegionData(locationnames.loc_quest_pacifist, [locationnames.loc_quest_pacifist], None, deps.dep_pacifist_quest),
]
region_isleh: list[RegionData] = [
    LevelRegionData(
        locationnames.level_boss_kingdice, None,
        [LevelTarget(locationnames.level_boss_devil)],
        flags=DefFlags.DICE_PALACE
    ),
    LevelRegionData(locationnames.level_boss_devil, None, None),
]
region_dlc_isle4: list[RegionData] = [
    RegionData(locationnames.level_dlc_tutorial, [
        locationnames.loc_level_dlc_tutorial,
        locationnames.loc_level_dlc_tutorial_coin,
    ], None, deps.dep_dlc_chalice),
    LevelRegionData(locationnames.level_dlc_boss_oldman, None, [LevelTarget(locationnames.level_dlc_boss_snowcult)]),
    LevelRegionData(locationnames.level_dlc_boss_rumrunners, None, [
        LevelTarget(locationnames.level_dlc_boss_plane_cowboy),
        Target(locationnames.loc_dlc_quest_cactusgirl, None, deps.dep_dlc_cactusgirl_quest),
    ]),
    LevelRegionData(locationnames.level_dlc_boss_plane_cowboy, None, [
        LevelTarget(locationnames.level_dlc_boss_airplane)
        #LevelTarget(locationnames.level_dlc_graveyard),
    ]),
    LevelRegionData(locationnames.level_dlc_boss_snowcult, None, [
        LevelTarget(locationnames.level_dlc_boss_airplane),
        #LevelTarget(locationnames.level_dlc_graveyard),
    ]),
    LevelRegionData(locationnames.level_dlc_boss_airplane, None, [
        LevelTarget(locationnames.level_dlc_boss_snowcult),
        LevelTarget(locationnames.level_dlc_boss_plane_cowboy),
        Target(locationnames.loc_dlc_quest_cactusgirl, None, deps.dep_dlc_cactusgirl_quest),
    ]),
    LevelRegionData(locationnames.level_dlc_boss_saltbaker, None, None),
    #LevelRegionData(locationnames.level_dlc_graveyard, None),
    RegionData(locationnames.level_dlc_chesscastle, None, [
        LevelTarget(locationnames.level_dlc_chesscastle_pawn)
    ], flags=DefFlags.TGT_IGNORE_FREEMOVE),
    RegionData(
        locationnames.loc_dlc_quest_cactusgirl,
        [locationnames.loc_dlc_quest_cactusgirl],
        None,
        deps.dep_dlc_cactusgirl_quest
    ),
]
region_dlc_chesscastle: list[RegionData] = [
    LevelRegionData(
        locationnames.level_dlc_chesscastle_pawn, None,
        [LevelTarget(locationnames.level_dlc_chesscastle_knight)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    LevelRegionData(
        locationnames.level_dlc_chesscastle_knight, None,
        [LevelTarget(locationnames.level_dlc_chesscastle_bishop)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    LevelRegionData(
        locationnames.level_dlc_chesscastle_bishop, None,
        [LevelTarget(locationnames.level_dlc_chesscastle_rook)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    LevelRegionData(
        locationnames.level_dlc_chesscastle_rook, None,
        [LevelTarget(locationnames.level_dlc_chesscastle_queen)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    LevelRegionData(
        locationnames.level_dlc_chesscastle_queen, None,
        [LevelTarget(locationnames.level_dlc_chesscastle_run)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    LevelRegionData(
        locationnames.level_dlc_chesscastle_run, None, None,
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
