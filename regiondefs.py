from __future__ import annotations
import typing
from typing import Optional, Iterable
from typing_extensions import override
from enum import IntEnum, IntFlag
from .names import LocationNames, ItemNames
from .rulebase import RegionRule, region_rule_has, region_rule_has_all
from .dep import Dep
from . import dep
if typing.TYPE_CHECKING:
    from . import CupheadWorld

class DefType(IntEnum):
    SIMPLE = 0
    LEVEL = 1
    WORLD = 2
class DefFlags(IntFlag):
    NONE = 0
    TGT_IGNORE_FREEMOVE = 1
    DICE_PALACE = 3

def rule_has(item: str, count: int = 1) -> RegionRule:
    return region_rule_has(item, count)
def rule_has_all(items: Iterable[str]) -> RegionRule:
    return region_rule_has_all(items)

class Target:
    name: str
    rule: Optional[RegionRule]
    depends: Dep
    tgt_type: DefType
    def __init__(self, name: str, rule: Optional[RegionRule] = None, depends: Optional[Dep] = None, tgt_type: DefType = DefType.SIMPLE):
        self.name = name
        self.rule = rule
        self.depends = depends if depends else dep.dep_none
        self.tgt_type = tgt_type
    @override
    def __str__(self) -> str:
        return self.name
class LevelTarget(Target):
    def __init__(self, name: str, add_rule: Optional[RegionRule] = None, depends: Optional[Dep] = None):
        super().__init__(name, add_rule, depends, DefType.LEVEL)
class RegionData:
    name: str
    locations: Optional[list[str]]
    connect_to: Optional[list[Target]]
    depends: Dep
    region_type: DefType
    flags: DefFlags
    def __init__(
            self,
            name: str,
            locations: Optional[list[str]] = None,
            connect_to: Optional[list[Target]] = None,
            depends: Optional[Dep] = None,
            region_type: DefType = DefType.SIMPLE,
            flags: DefFlags = DefFlags.NONE):
        self.name = name
        self.locations = locations
        self.connect_to = connect_to
        self.depends = depends if depends else dep.dep_none
        self.region_type = region_type
        self.flags = flags
    @override
    def __str__(self) -> str:
        return self.name
class LevelRegionData(RegionData):
    def __init__(
            self,
            name: str,
            add_locations: Optional[list[str]] = None,
            connect_to: Optional[list[Target]] = None,
            depends: Optional[Dep] = None,
            flags: DefFlags = DefFlags.NONE):
        super().__init__(name, add_locations, connect_to, depends, DefType.LEVEL, flags)
class WorldRegionData(RegionData):
    def __init__(
            self,
            name: str,
            add_locations: Optional[list[str]] = None,
            connect_to: Optional[list[Target]] = None,
            depends: Optional[Dep] = None,
            flags: DefFlags = DefFlags.TGT_IGNORE_FREEMOVE):
        super().__init__(name, add_locations, connect_to, depends, DefType.WORLD, flags)

region_begin: RegionData = RegionData("Menu", None, [Target(LocationNames.level_house)], flags=DefFlags.TGT_IGNORE_FREEMOVE)
region_house: RegionData = RegionData(LocationNames.level_house, None, [
        LevelTarget(LocationNames.level_tutorial),
        Target(LocationNames.world_inkwell_1)
    ], flags=DefFlags.TGT_IGNORE_FREEMOVE)

region_house_level_tutorial: RegionData = LevelRegionData(LocationNames.level_tutorial, None, None, flags=DefFlags.TGT_IGNORE_FREEMOVE)

region_dlc_start: list[RegionData] = [
    RegionData(LocationNames.loc_event_mausoleum, [LocationNames.loc_event_mausoleum], None, dep.dep_dlc_boat_mausoleum),
    RegionData(LocationNames.reg_dlc_boat, [LocationNames.loc_event_dlc_boatarrival], None, flags=DefFlags.TGT_IGNORE_FREEMOVE),
]

region_worlds: list[RegionData] = [
    WorldRegionData(LocationNames.world_inkwell_1, [
        LocationNames.loc_npc_mac,
        LocationNames.loc_coin_isle1_secret,
    ], [
        Target(LocationNames.level_shop1),
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
        Target(LocationNames.level_shop2, None, dep.dep_freemove),
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
        Target(LocationNames.level_shop3, None, dep.dep_freemove),
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
        LocationNames.loc_dlc_npc_newscat,
        LocationNames.loc_dlc_coin_isle4_secret,
    ], [
        Target(LocationNames.level_dlc_tutorial, rule_has(ItemNames.item_charm_dlc_cookie), dep.dep_dlc_chalice),
        Target(LocationNames.level_dlc_shop4),
        Target(LocationNames.level_dlc_chesscastle),
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
    LevelRegionData(LocationNames.level_boss_veggies, [LocationNames.loc_event_isle1_secret_prereq1], #FIXME: Secret Prereq should stick to absolute location
        [LevelTarget(LocationNames.level_boss_frogs)]),
    LevelRegionData(LocationNames.level_boss_slime, [LocationNames.loc_event_isle1_secret_prereq2],
        [LevelTarget(LocationNames.level_boss_plane_blimp)]),
    LevelRegionData(LocationNames.level_boss_plane_blimp, [LocationNames.loc_event_isle1_secret_prereq3],
        [LevelTarget(LocationNames.level_boss_flower), LevelTarget(LocationNames.level_rungun_tree)]),
    LevelRegionData(LocationNames.level_boss_frogs, [LocationNames.loc_event_isle1_secret_prereq4],
        [LevelTarget(LocationNames.level_mausoleum_i), Target(LocationNames.reg_dlc_boat, None, dep.dep_dlc)]),
    LevelRegionData(LocationNames.level_boss_flower, [LocationNames.loc_event_isle1_secret_prereq5], [
        Target(LocationNames.world_inkwell_2, None, dep.dep_not(dep.dep_freemove))]),
    LevelRegionData(LocationNames.level_rungun_tree, None, [LevelTarget(LocationNames.level_mausoleum_i), Target(LocationNames.reg_dlc_boat, None, dep.dep_dlc)]),
    LevelRegionData(LocationNames.level_rungun_forest, None, [LevelTarget(LocationNames.level_mausoleum_i), Target(LocationNames.reg_dlc_boat, None, dep.dep_dlc)]),
    LevelRegionData(LocationNames.level_mausoleum_i, None, [Target(LocationNames.loc_event_mausoleum, None, dep.dep_dlc_boat_mausoleum)], flags=DefFlags.TGT_IGNORE_FREEMOVE)
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
        Target(LocationNames.level_shop2),
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
        Target(LocationNames.level_shop2),
    ]),
    LevelRegionData(LocationNames.level_boss_dragon, [
        LocationNames.loc_quest_4parries,
    ], [
        LevelTarget(LocationNames.level_mausoleum_ii),
        Target(LocationNames.loc_quest_lucien, None, dep.dep_lucien_quest),
        Target(LocationNames.level_shop2),
    ]),
    LevelRegionData(LocationNames.level_rungun_circus, [
        LocationNames.loc_event_quest_4mel_4th,
        LocationNames.loc_quest_ginger,
    ], [
        LevelTarget(LocationNames.level_mausoleum_ii),
        Target(LocationNames.loc_quest_lucien, None, dep.dep_lucien_quest),
        Target(LocationNames.level_shop2),
    ]),
    LevelRegionData(LocationNames.level_rungun_funhouse, [LocationNames.loc_coin_isle2_secret], [
        LevelTarget(LocationNames.level_mausoleum_ii),
        Target(LocationNames.loc_quest_lucien, None, dep.dep_lucien_quest),
        Target(LocationNames.level_shop2),
    ]),
    LevelRegionData(LocationNames.level_mausoleum_ii, None, [Target(LocationNames.loc_event_mausoleum, None, dep.dep_dlc_boat_mausoleum)], flags=DefFlags.TGT_IGNORE_FREEMOVE),
    RegionData(LocationNames.loc_quest_lucien, [LocationNames.loc_quest_lucien], None, dep.dep_lucien_quest),
    RegionData(LocationNames.loc_event_isle2_shortcut, [
        LocationNames.loc_event_isle2_shortcut
    ], [
        LevelTarget(LocationNames.level_boss_dragon, None, dep.dep_and(dep.dep_shortcuts, dep.dep_not(dep.dep_freemove))),
        LevelTarget(LocationNames.level_rungun_funhouse, None, dep.dep_and(dep.dep_shortcuts, dep.dep_not(dep.dep_freemove))),
        LevelTarget(LocationNames.level_boss_plane_bird, None, dep.dep_and(dep.dep_shortcuts, dep.dep_not(dep.dep_freemove))),
        LevelTarget(LocationNames.level_rungun_circus, None, dep.dep_and(dep.dep_shortcuts, dep.dep_not(dep.dep_freemove))),
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
        Target(LocationNames.level_shop3),
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
        Target(LocationNames.level_shop3),
        Target(LocationNames.loc_quest_silverworth, None, dep.dep_agrade_quest)
    ]),
    LevelRegionData(LocationNames.level_rungun_mountain, None, [
        LevelTarget(LocationNames.level_boss_mouse),
        LevelTarget(LocationNames.level_mausoleum_iii),
        Target(LocationNames.level_shop3),
        Target(LocationNames.loc_quest_silverworth, None, dep.dep_agrade_quest)
    ]),
    LevelRegionData(LocationNames.level_mausoleum_iii, None, [Target(LocationNames.loc_event_mausoleum, None, dep.dep_dlc_boat_mausoleum)], flags=DefFlags.TGT_IGNORE_FREEMOVE),
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
    LevelRegionData(LocationNames.level_boss_kingdice, None, [LevelTarget(LocationNames.level_boss_devil)], flags=DefFlags.DICE_PALACE),
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
    RegionData(LocationNames.loc_dlc_quest_cactusgirl, [LocationNames.loc_dlc_quest_cactusgirl], None, dep.dep_dlc_cactusgirl_quest),
]
region_dlc_chesscastle: list[RegionData] = [
    LevelRegionData(LocationNames.level_dlc_chesscastle_pawn, None, [LevelTarget(LocationNames.level_dlc_chesscastle_knight)], flags=DefFlags.TGT_IGNORE_FREEMOVE),
    LevelRegionData(LocationNames.level_dlc_chesscastle_knight, None, [LevelTarget(LocationNames.level_dlc_chesscastle_bishop)], flags=DefFlags.TGT_IGNORE_FREEMOVE),
    LevelRegionData(LocationNames.level_dlc_chesscastle_bishop, None, [LevelTarget(LocationNames.level_dlc_chesscastle_rook)], flags=DefFlags.TGT_IGNORE_FREEMOVE),
    LevelRegionData(LocationNames.level_dlc_chesscastle_rook, None, [LevelTarget(LocationNames.level_dlc_chesscastle_queen)], flags=DefFlags.TGT_IGNORE_FREEMOVE),
    LevelRegionData(LocationNames.level_dlc_chesscastle_queen, None, [LevelTarget(LocationNames.level_dlc_chesscastle_run, None, dep.dep_dlc_chesscastle_run)], flags=DefFlags.TGT_IGNORE_FREEMOVE),
    LevelRegionData(LocationNames.level_dlc_chesscastle_run, None, None, dep.dep_dlc_chesscastle_run, flags=DefFlags.TGT_IGNORE_FREEMOVE)
]
region_dlc_special: list[RegionData] = [
    # Add Logic Regions and connections to curse_complete
]

regions_start: list[RegionData] = [
    region_begin,
    region_house,
    region_house_level_tutorial,
]
regions_base: list[RegionData] = region_worlds + region_isle1 + region_isle2 + region_isle3 + region_isleh
regions_dlc: list[RegionData] = region_dlc_start + region_dlc_worlds + region_dlc_isle4 + region_dlc_chesscastle #+ region_dlc_special

def get_regions(world: CupheadWorld) -> list[RegionData]:
    shop_locations = world.shop_locations
    using_dlc = world.wsettings.use_dlc

    region_shops: list[RegionData] = []
    region_dlc_shops: list[RegionData] = []

    for shop_name, locs in shop_locations.items():
        shop_region = RegionData(shop_name, locs, None)
        if shop_name == LocationNames.level_dlc_shop4:
            region_dlc_shops.append(shop_region)
        else:
            region_shops.append(shop_region)

    total_regions = regions_start + region_shops + regions_base
    if using_dlc:
        total_regions += region_dlc_shops + regions_dlc

    return total_regions

def list_regiondata_locations(region: RegionData) -> list[str]:
    return [loc for loc in region.locations] if region.locations else []
