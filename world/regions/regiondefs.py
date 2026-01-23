### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from collections.abc import Iterable

from ..names import itemnames, locationnames, regionnames
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
    [Target(regionnames.level_house)],
    flags=DefFlags.TGT_IGNORE_FREEMOVE
)
region_house: RegionData = RegionData(regionnames.level_house, None, [
        LevelTarget(regionnames.level_tutorial),
        Target(regionnames.world_inkwell_1)
    ], flags=DefFlags.TGT_IGNORE_FREEMOVE)

region_house_level_tutorial: RegionData = LevelRegionData(
    regionnames.level_tutorial, None, None, flags=DefFlags.TGT_IGNORE_FREEMOVE
)

region_dlc_start: list[RegionData] = [
    RegionData(
        locationnames.loc_event_mausoleum, [locationnames.loc_event_mausoleum], None, deps.dep_dlc_boat_mausoleum
    ),
    RegionData(
        regionnames.reg_dlc_boat, [locationnames.loc_event_dlc_boatarrival], None, flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
]

# Shop Regions are defined in shop.py

region_worlds: list[RegionData] = [
    WorldRegionData(regionnames.world_inkwell_1, [
        locationnames.loc_npc_mac,
        locationnames.loc_coin_isle1_secret,
    ], [
        Target(regionnames.shop_set1),
        Target(regionnames.reg_dlc_boat, None, deps.dep_and(deps.dep_dlc, deps.dep_freemove)),
        Target(regionnames.world_dlc_inkwell_4, rule_has(itemnames.item_event_dlc_boataccess), deps.dep_dlc),
        LevelTarget(regionnames.level_boss_veggies),
        LevelTarget(regionnames.level_boss_slime),
        LevelTarget(regionnames.level_rungun_forest),
        LevelTarget(regionnames.level_boss_flower, None, deps.dep_or(deps.dep_shortcuts, deps.dep_freemove)),
        LevelTarget(regionnames.level_rungun_tree, None, deps.dep_or(deps.dep_shortcuts, deps.dep_freemove)),
        Target(regionnames.world_inkwell_2, None, deps.dep_freemove),
        LevelTarget(regionnames.level_boss_frogs, None, deps.dep_freemove),
        LevelTarget(regionnames.level_boss_plane_blimp, None, deps.dep_freemove),
        LevelTarget(regionnames.level_mausoleum_i, None, deps.dep_freemove),
    ]),
    WorldRegionData(regionnames.world_inkwell_2, [
        locationnames.loc_npc_canteen,
        locationnames.loc_quest_4mel,
    ], [
        Target(regionnames.shop_set2, None, deps.dep_freemove),
        LevelTarget(regionnames.level_boss_baroness),
        LevelTarget(regionnames.level_boss_clown),
        LevelTarget(regionnames.level_boss_plane_genie),
        Target(regionnames.world_inkwell_3, None, deps.dep_freemove),
        LevelTarget(regionnames.level_boss_plane_bird, None, deps.dep_freemove),
        LevelTarget(regionnames.level_boss_dragon, None, deps.dep_freemove),
        LevelTarget(regionnames.level_rungun_circus, None, deps.dep_freemove),
        LevelTarget(regionnames.level_rungun_funhouse, None, deps.dep_freemove),
        LevelTarget(regionnames.level_mausoleum_ii, None, deps.dep_freemove),
        Target(locationnames.loc_event_isle2_shortcut, None, deps.dep_freemove),
        Target(regionnames.reg_dlc_boat, None, deps.dep_dlc),
    ]),
    WorldRegionData(regionnames.world_inkwell_3, None, [
        Target(regionnames.shop_set3, None, deps.dep_freemove),
        LevelTarget(regionnames.level_boss_bee),
        LevelTarget(regionnames.level_boss_pirate),
        Target(regionnames.world_inkwell_hell, None, deps.dep_freemove),
        LevelTarget(regionnames.level_boss_plane_robot, None, deps.dep_freemove),
        LevelTarget(regionnames.level_rungun_mountain, None, deps.dep_freemove),
        LevelTarget(regionnames.level_boss_sallystageplay, None, deps.dep_freemove),
        LevelTarget(regionnames.level_boss_mouse, None, deps.dep_freemove),
        LevelTarget(regionnames.level_boss_train, None, deps.dep_freemove),
        LevelTarget(regionnames.level_boss_plane_mermaid, None, deps.dep_freemove),
        LevelTarget(regionnames.level_rungun_harbour, None, deps.dep_freemove),
        LevelTarget(regionnames.level_mausoleum_iii, None, deps.dep_freemove),
        Target(locationnames.loc_quest_ludwig, None, deps.dep_and(deps.dep_freemove, deps.dep_music_quest)),
        Target(locationnames.loc_quest_silverworth, None, deps.dep_and(deps.dep_freemove, deps.dep_agrade_quest)),
        Target(locationnames.loc_quest_pacifist, None, deps.dep_and(deps.dep_freemove, deps.dep_pacifist_quest)),
        Target(regionnames.reg_dlc_boat, None, deps.dep_and(deps.dep_dlc, deps.dep_not(deps.dep_freemove))),
    ]),
    WorldRegionData(regionnames.world_inkwell_hell, [locationnames.loc_coin_isleh_secret], [
        Target(regionnames.level_boss_kingdice)
    ]),
]
region_dlc_worlds = [
    WorldRegionData(regionnames.world_dlc_inkwell_4, [
        locationnames.loc_dlc_cookie,
        locationnames.loc_event_dlc_cookie,
        locationnames.loc_dlc_npc_newscat,
        locationnames.loc_dlc_coin_isle4_secret,
    ], [
        Target(regionnames.shop_set4),
        Target(regionnames.level_dlc_chesscastle),
        Target(
            locationnames.loc_dlc_quest_cactusgirl, None, deps.dep_and(deps.dep_freemove, deps.dep_dlc_cactusgirl_quest)
        ),
        LevelTarget(regionnames.level_dlc_tutorial, None, deps.dep_dlc_chalice),
        LevelTarget(regionnames.level_dlc_boss_oldman),
        LevelTarget(regionnames.level_dlc_boss_rumrunners),
        LevelTarget(regionnames.level_dlc_boss_plane_cowboy, None, deps.dep_freemove),
        LevelTarget(regionnames.level_dlc_boss_snowcult, None, deps.dep_freemove),
        LevelTarget(regionnames.level_dlc_boss_airplane, None, deps.dep_or(deps.dep_shortcuts, deps.dep_freemove)),
        #LevelTarget(regionnames.level_dlc_graveyard, None, dep.dep_freemove),
        LevelTarget(regionnames.level_dlc_boss_saltbaker, None)
    ]),
]

region_isle1 =  [
    LevelRegionData(regionnames.level_boss_veggies, [locationnames.loc_event_isle1_secret_prereq1],
        [LevelTarget(regionnames.level_boss_frogs)]),
    LevelRegionData(regionnames.level_boss_slime, [locationnames.loc_event_isle1_secret_prereq2],
        [LevelTarget(regionnames.level_boss_plane_blimp)]),
    LevelRegionData(regionnames.level_boss_plane_blimp, [locationnames.loc_event_isle1_secret_prereq3],
        [LevelTarget(regionnames.level_boss_flower), LevelTarget(regionnames.level_rungun_tree)]),
    LevelRegionData(regionnames.level_boss_frogs, [locationnames.loc_event_isle1_secret_prereq4],
        [LevelTarget(regionnames.level_mausoleum_i), Target(regionnames.reg_dlc_boat, None, deps.dep_dlc)]),
    LevelRegionData(regionnames.level_boss_flower, [locationnames.loc_event_isle1_secret_prereq5],
        [Target(regionnames.world_inkwell_2, None, deps.dep_not(deps.dep_freemove))]),
    LevelRegionData(regionnames.level_rungun_tree, None,
        [LevelTarget(regionnames.level_mausoleum_i), Target(regionnames.reg_dlc_boat, None, deps.dep_dlc)]),
    LevelRegionData(regionnames.level_rungun_forest, None,
        [LevelTarget(regionnames.level_mausoleum_i), Target(regionnames.reg_dlc_boat, None, deps.dep_dlc)]),
    LevelRegionData(regionnames.level_mausoleum_i, None,
        [Target(locationnames.loc_event_mausoleum, None, deps.dep_dlc_boat_mausoleum)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    )
]
region_isle2: list[RegionData] = [
    LevelRegionData(regionnames.level_boss_baroness, None, [
        LevelTarget(regionnames.level_boss_plane_bird),
        LevelTarget(regionnames.level_rungun_circus),
        Target(locationnames.loc_event_isle2_shortcut)
    ]),
    LevelRegionData(regionnames.level_boss_plane_genie, None, [
        LevelTarget(regionnames.level_mausoleum_ii),
        Target(locationnames.loc_quest_lucien, None, deps.dep_lucien_quest),
        Target(regionnames.shop_set2),
    ]),
    LevelRegionData(regionnames.level_boss_clown, None, [
        LevelTarget(regionnames.level_boss_dragon),
        LevelTarget(regionnames.level_rungun_funhouse),
        Target(locationnames.loc_event_isle2_shortcut),
        Target(regionnames.world_inkwell_3, None, deps.dep_not(deps.dep_freemove))
    ]),
    LevelRegionData(regionnames.level_boss_plane_bird, None, [
        LevelTarget(regionnames.level_mausoleum_ii),
        Target(locationnames.loc_quest_lucien, None, deps.dep_lucien_quest),
        Target(regionnames.shop_set2),
    ]),
    LevelRegionData(regionnames.level_boss_dragon, [
        locationnames.loc_quest_buster,
    ], [
        LevelTarget(regionnames.level_mausoleum_ii),
        Target(locationnames.loc_quest_lucien, None, deps.dep_lucien_quest),
        Target(regionnames.shop_set2),
    ]),
    LevelRegionData(regionnames.level_rungun_circus, [
        locationnames.loc_event_quest_4mel_4th,
        locationnames.loc_quest_ginger,
    ], [
        LevelTarget(regionnames.level_mausoleum_ii),
        Target(locationnames.loc_quest_lucien, None, deps.dep_lucien_quest),
        Target(regionnames.shop_set2),
    ]),
    LevelRegionData(regionnames.level_rungun_funhouse, [locationnames.loc_coin_isle2_secret], [
        LevelTarget(regionnames.level_mausoleum_ii),
        Target(locationnames.loc_quest_lucien, None, deps.dep_lucien_quest),
        Target(regionnames.shop_set2),
    ]),
    LevelRegionData(
        regionnames.level_mausoleum_ii, None,
        [Target(locationnames.loc_event_mausoleum, None, deps.dep_dlc_boat_mausoleum)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    RegionData(locationnames.loc_quest_lucien, [locationnames.loc_quest_lucien], None, deps.dep_lucien_quest),
    RegionData(locationnames.loc_event_isle2_shortcut, [
        locationnames.loc_event_isle2_shortcut
    ], [
        LevelTarget(
            regionnames.level_boss_dragon, None, deps.dep_and(deps.dep_shortcuts, deps.dep_not(deps.dep_freemove))
        ),
        LevelTarget(
            regionnames.level_rungun_funhouse, None, deps.dep_and(deps.dep_shortcuts, deps.dep_not(deps.dep_freemove))
        ),
        LevelTarget(
            regionnames.level_boss_plane_bird, None, deps.dep_and(deps.dep_shortcuts, deps.dep_not(deps.dep_freemove))
        ),
        LevelTarget(
            regionnames.level_rungun_circus, None, deps.dep_and(deps.dep_shortcuts, deps.dep_not(deps.dep_freemove))
        ),
    ])
]
region_isle3: list[RegionData] = [
    LevelRegionData(regionnames.level_boss_bee, None, [
        LevelTarget(regionnames.level_boss_plane_robot),
        LevelTarget(regionnames.level_rungun_mountain),
        Target(locationnames.loc_quest_ludwig, None, deps.dep_music_quest)
    ]),
    LevelRegionData(regionnames.level_boss_pirate, None, [
        LevelTarget(regionnames.level_boss_plane_mermaid),
        LevelTarget(regionnames.level_rungun_harbour),
        Target(locationnames.loc_quest_pacifist, None, deps.dep_pacifist_quest),
        Target(regionnames.reg_dlc_boat, None, deps.dep_dlc),
    ]),
    LevelRegionData(regionnames.level_boss_plane_robot, None, [
        LevelTarget(regionnames.level_boss_sallystageplay),
        Target(locationnames.loc_quest_wolfgang, None, deps.dep_music_quest)
    ]),
    LevelRegionData(regionnames.level_boss_plane_mermaid, [locationnames.loc_coin_isle3_secret], [
        LevelTarget(regionnames.level_boss_sallystageplay),
        Target(locationnames.loc_quest_wolfgang, None, deps.dep_music_quest)
    ]),
    LevelRegionData(regionnames.level_boss_sallystageplay, None, [
        LevelTarget(regionnames.level_boss_mouse),
        LevelTarget(regionnames.level_mausoleum_iii),
        LevelTarget(regionnames.level_boss_train),
        Target(regionnames.shop_set3),
        Target(locationnames.loc_quest_silverworth, None, deps.dep_agrade_quest)
    ]),
    LevelRegionData(regionnames.level_boss_mouse, None, [
        LevelTarget(regionnames.level_boss_sallystageplay),
        Target(locationnames.loc_quest_wolfgang, None, deps.dep_music_quest)
    ]),
    LevelRegionData(regionnames.level_boss_train, None, [Target(regionnames.world_inkwell_hell)]),
    LevelRegionData(regionnames.level_rungun_harbour, None, [
        LevelTarget(regionnames.level_boss_mouse),
        LevelTarget(regionnames.level_mausoleum_iii),
        Target(regionnames.shop_set3),
        Target(locationnames.loc_quest_silverworth, None, deps.dep_agrade_quest)
    ]),
    LevelRegionData(regionnames.level_rungun_mountain, None, [
        LevelTarget(regionnames.level_boss_mouse),
        LevelTarget(regionnames.level_mausoleum_iii),
        Target(regionnames.shop_set3),
        Target(locationnames.loc_quest_silverworth, None, deps.dep_agrade_quest)
    ]),
    LevelRegionData(
        regionnames.level_mausoleum_iii, None,
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
        regionnames.level_boss_kingdice, None,
        [LevelTarget(regionnames.level_boss_devil)],
        flags=DefFlags.DICE_PALACE
    ),
    LevelRegionData(regionnames.level_boss_devil, None, None),
]
region_dlc_isle4: list[RegionData] = [
    RegionData(regionnames.level_dlc_tutorial, [
        locationnames.loc_level_dlc_tutorial,
        locationnames.loc_level_dlc_tutorial_coin,
    ], None, deps.dep_dlc_chalice),
    LevelRegionData(regionnames.level_dlc_boss_oldman, None, [LevelTarget(regionnames.level_dlc_boss_snowcult)]),
    LevelRegionData(regionnames.level_dlc_boss_rumrunners, None, [
        LevelTarget(regionnames.level_dlc_boss_plane_cowboy),
        Target(locationnames.loc_dlc_quest_cactusgirl, None, deps.dep_dlc_cactusgirl_quest),
    ]),
    LevelRegionData(regionnames.level_dlc_boss_plane_cowboy, None, [
        LevelTarget(regionnames.level_dlc_boss_airplane)
        #LevelTarget(regionnames.level_dlc_graveyard),
    ]),
    LevelRegionData(regionnames.level_dlc_boss_snowcult, None, [
        LevelTarget(regionnames.level_dlc_boss_airplane),
        #LevelTarget(regionnames.level_dlc_graveyard),
    ]),
    LevelRegionData(regionnames.level_dlc_boss_airplane, None, [
        LevelTarget(regionnames.level_dlc_boss_snowcult),
        LevelTarget(regionnames.level_dlc_boss_plane_cowboy),
        Target(locationnames.loc_dlc_quest_cactusgirl, None, deps.dep_dlc_cactusgirl_quest),
    ]),
    LevelRegionData(regionnames.level_dlc_boss_saltbaker, None, None),
    #LevelRegionData(regionnames.level_dlc_graveyard, None),
    RegionData(regionnames.level_dlc_chesscastle, None, [
        LevelTarget(regionnames.level_dlc_chesscastle_pawn)
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
        regionnames.level_dlc_chesscastle_pawn, None,
        [LevelTarget(regionnames.level_dlc_chesscastle_knight)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    LevelRegionData(
        regionnames.level_dlc_chesscastle_knight, None,
        [LevelTarget(regionnames.level_dlc_chesscastle_bishop)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    LevelRegionData(
        regionnames.level_dlc_chesscastle_bishop, None,
        [LevelTarget(regionnames.level_dlc_chesscastle_rook)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    LevelRegionData(
        regionnames.level_dlc_chesscastle_rook, None,
        [LevelTarget(regionnames.level_dlc_chesscastle_queen)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    LevelRegionData(
        regionnames.level_dlc_chesscastle_queen, None,
        [LevelTarget(regionnames.level_dlc_chesscastle_run)],
        flags=DefFlags.TGT_IGNORE_FREEMOVE
    ),
    LevelRegionData(
        regionnames.level_dlc_chesscastle_run, None, None,
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
