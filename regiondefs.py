from __future__ import annotations
import typing
from typing import Optional, Callable
from enum import IntEnum, IntFlag
from BaseClasses import CollectionState
from .names import LocationNames, ItemNames
if typing.TYPE_CHECKING:
    from . import CupheadWorld
    Dep = Callable[[CupheadWorld], bool]

class DefType(IntEnum):
    SIMPLE = 0,
    LEVEL = 1,

class DefFlags(IntFlag):
    NONE = 0,
    LV_IGNORE_FREEMOVE = 1,

Rule = Callable[[CollectionState, int], bool]
def rule_has(item: str, count: int = 1) -> Rule:
    return lambda state, player: state.has(item, player, count)

# Deps determine if a region or target is enabled
def dep_and(a: Dep, b: Dep) -> Dep:
    return lambda w: a(w) and b(w)
def dep_not(a: Dep) -> Dep:
    return lambda w: not a(w)
def dep_or(a: Dep, b: Dep) -> Dep:
    return lambda w: a(w) or b(w)
def dep_none(w: CupheadWorld) -> bool:
    return True
def dep_dlc(w: CupheadWorld) -> bool:
    return w.use_dlc
def dep_freemove(w: CupheadWorld) -> bool:
    return w.wsettings.freemove_isles
def dep_shortcuts(w: CupheadWorld) -> bool:
    return w.wsettings.require_secret_shortcuts
def dep_agrade_quest(w: CupheadWorld) -> bool:
    return w.wsettings.agrade_quest
def dep_pacifist_quest(w: CupheadWorld) -> bool:
    return w.wsettings.pacifist_quest
def dep_wolfgang_quest(w: CupheadWorld) -> bool:
    return w.wsettings.wolfgang_quest
def dep_dlc_cactusgirl_quest(w: CupheadWorld) -> bool:
    return w.wsettings.dlc_cactusgirl_quest

class Target:
    name: str
    rule: Optional[Rule]
    depends: Dep
    tgt_type: DefType
    def __init__(self, name: str, rule: Optional[Rule] = None, depends: Optional[Dep] = None, tgt_type: DefType = DefType.SIMPLE):
        self.name = name
        self.rule = rule
        self.depends = depends if depends else dep_none
        self.tgt_type = tgt_type
class RegionData:
    name: str
    locations: list[str]
    connect_to: list[Target]
    depends: Dep
    region_type: DefType
    flags: DefFlags
    def __init__(self, name: str, locations: list[str] = None, connect_to: list[Target] = None, depends: Optional[Dep] = None, region_type: DefType = DefType.SIMPLE, flags: DefFlags = 0):
        self.name = name
        self.locations = locations
        self.connect_to = connect_to
        self.depends = depends if depends else dep_none
        self.region_type = region_type
        self.flags = flags
class LevelTarget(Target):
    def __init__(self, name: str, add_rule: Optional[Rule] = None, depends: Optional[Dep] = None):
        super().__init__(name, add_rule, depends, DefType.LEVEL)
class LevelRegionData(RegionData):
    def __init__(self, name: str, add_locations: list[str] = None, connect_to: list[Target] = None, depends: Optional[Dep] = None, flags: DefFlags = 0):
        super().__init__(name, add_locations, connect_to, depends, DefType.LEVEL, flags)

region_begin = RegionData("Menu", None, [Target(LocationNames.level_house)])
region_house = RegionData(LocationNames.level_house, None, [
    Target(LocationNames.level_tutorial), Target(LocationNames.world_inkwell_1)])

region_house_level_tutorial = RegionData(LocationNames.level_tutorial, [
    LocationNames.loc_level_tutorial,
    LocationNames.loc_level_tutorial_coin,
], None)

region_worlds = [
    RegionData(LocationNames.world_inkwell_1, [
        LocationNames.loc_npc_mac,
        LocationNames.loc_coin_isle1_secret,
    ], [
        Target(LocationNames.level_shop1),
        Target(LocationNames.world_dlc_inkwell_4, rule_has(ItemNames.item_event_dlc_boataccess), dep_dlc),
        LevelTarget(LocationNames.level_boss_veggies),
        LevelTarget(LocationNames.level_boss_slime),
        LevelTarget(LocationNames.level_rungun_forest),
        LevelTarget(LocationNames.level_boss_flower, None, dep_or(dep_shortcuts, dep_freemove)),
        LevelTarget(LocationNames.level_rungun_tree, None, dep_or(dep_shortcuts, dep_freemove)),
        Target(LocationNames.world_inkwell_2, None, dep_freemove),
        LevelTarget(LocationNames.level_boss_frogs, None, dep_freemove),
        LevelTarget(LocationNames.level_boss_plane_blimp, None, dep_freemove),
        Target(LocationNames.level_mausoleum_i, None, dep_freemove)
    ]),
    RegionData(LocationNames.world_inkwell_2, [
        LocationNames.loc_npc_canteen,
        LocationNames.loc_quest_4mel,
    ], [
        Target(LocationNames.level_shop2, None, dep_freemove),
        LevelTarget(LocationNames.level_boss_baroness),
        LevelTarget(LocationNames.level_boss_clown),
        LevelTarget(LocationNames.level_boss_plane_genie),
        Target(LocationNames.world_inkwell_3, None, dep_freemove),
        LevelTarget(LocationNames.level_boss_plane_bird, None, dep_freemove),
        LevelTarget(LocationNames.level_boss_dragon, None, dep_freemove),
        LevelTarget(LocationNames.level_rungun_circus, None, dep_freemove),
        LevelTarget(LocationNames.level_rungun_funhouse, None, dep_freemove),
        LevelTarget(LocationNames.level_mausoleum_ii, None, dep_freemove),
        Target(LocationNames.loc_event_isle2_shortcut, None, dep_freemove)
    ]),
    RegionData(LocationNames.world_inkwell_3, None, [
        Target(LocationNames.level_shop3, None, dep_freemove),
        LevelTarget(LocationNames.level_boss_bee),
        LevelTarget(LocationNames.level_boss_pirate),
        Target(LocationNames.world_inkwell_hell, None, dep_freemove),
        LevelTarget(LocationNames.level_boss_plane_robot, None, dep_freemove),
        LevelTarget(LocationNames.level_rungun_mountain, None, dep_freemove),
        LevelTarget(LocationNames.level_boss_sallystageplay, None, dep_freemove),
        LevelTarget(LocationNames.level_boss_mouse, None, dep_freemove),
        LevelTarget(LocationNames.level_boss_train, None, dep_freemove),
        LevelTarget(LocationNames.level_boss_plane_mermaid, None, dep_freemove),
        LevelTarget(LocationNames.level_rungun_harbour, None, dep_freemove),
        LevelTarget(LocationNames.level_mausoleum_iii, None, dep_freemove),
        Target(LocationNames.loc_quest_ludwig, None, dep_freemove),
    ]),
    RegionData(LocationNames.world_inkwell_hell, [LocationNames.loc_coin_isleh_secret], [
        Target(LocationNames.level_boss_kingdice)
    ]),
]
region_dlc_worlds = [
    RegionData(LocationNames.world_dlc_inkwell_4, [
        LocationNames.loc_event_dlc_start,
        LocationNames.loc_dlc_npc_newscat,
        LocationNames.loc_dlc_coin_isle4_secret,
    ], [
        Target(LocationNames.level_dlc_tutorial),
        Target(LocationNames.level_dlc_shop4),
        Target(LocationNames.level_dlc_chesscastle),
        LevelTarget(LocationNames.level_dlc_boss_oldman),
        LevelTarget(LocationNames.level_dlc_boss_rumrunners),
        LevelTarget(LocationNames.level_dlc_boss_plane_cowboy, None, dep_freemove),
        LevelTarget(LocationNames.level_dlc_boss_snowcult, None, dep_freemove),
        LevelTarget(LocationNames.level_dlc_boss_airplane, None, dep_freemove),
        #LevelTarget(LocationNames.level_dlc_graveyard, None, dep_freemove),
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
        [LevelTarget(LocationNames.level_mausoleum_i)]),
    LevelRegionData(LocationNames.level_boss_flower, [LocationNames.loc_event_isle1_secret_prereq5], [
        Target(LocationNames.world_inkwell_2, None, dep_not(dep_freemove))]),
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
        Target(LocationNames.world_inkwell_3, None, dep_not(dep_freemove))]),
    LevelRegionData(LocationNames.level_boss_plane_bird, None, [
        LevelTarget(LocationNames.level_mausoleum_ii),
        Target(LocationNames.level_shop2),
    ]),
    LevelRegionData(LocationNames.level_boss_dragon, [
        LocationNames.loc_quest_4parries,
    ], [
        LevelTarget(LocationNames.level_mausoleum_ii),
        Target(LocationNames.level_shop2),
    ]),
    LevelRegionData(LocationNames.level_rungun_circus, [
        LocationNames.loc_event_quest_4mel_4th,
        LocationNames.loc_quest_ginger,
    ], [
        LevelTarget(LocationNames.level_mausoleum_ii),
        Target(LocationNames.level_shop2),
    ]),
    LevelRegionData(LocationNames.level_rungun_funhouse, [LocationNames.loc_coin_isle2_secret], [
        LevelTarget(LocationNames.level_mausoleum_ii),
        Target(LocationNames.level_shop2),
    ]),
    LevelRegionData(LocationNames.level_mausoleum_ii, [
        LocationNames.loc_quest_lucien,
    ], None),
    RegionData(LocationNames.loc_event_isle2_shortcut, [
        LocationNames.loc_event_isle2_shortcut
    ], [
        LevelTarget(LocationNames.level_boss_dragon, None, dep_and(dep_shortcuts, dep_not(dep_freemove))),
        LevelTarget(LocationNames.level_rungun_funhouse, None, dep_and(dep_shortcuts, dep_not(dep_freemove))),
        LevelTarget(LocationNames.level_boss_plane_bird, None, dep_and(dep_shortcuts, dep_not(dep_freemove))),
        LevelTarget(LocationNames.level_rungun_circus, None, dep_and(dep_shortcuts, dep_not(dep_freemove))),
    ])
]
region_isle3 = [
    LevelRegionData(LocationNames.level_boss_bee, None, [
        LevelTarget(LocationNames.level_boss_plane_robot),
        LevelTarget(LocationNames.level_rungun_mountain),
        Target(LocationNames.loc_quest_ludwig, None, dep_wolfgang_quest)
    ]),
    LevelRegionData(LocationNames.level_boss_pirate, None, [
        LevelTarget(LocationNames.level_boss_plane_mermaid),
        LevelTarget(LocationNames.level_rungun_harbour),
        Target(LocationNames.loc_quest_pacifist, None, dep_pacifist_quest),
    ]),
    LevelRegionData(LocationNames.level_boss_plane_robot, None, [
        LevelTarget(LocationNames.level_boss_sallystageplay),
        Target(LocationNames.loc_quest_wolfgang, None, dep_wolfgang_quest)
    ]),
    LevelRegionData(LocationNames.level_boss_plane_mermaid, [LocationNames.loc_coin_isle3_secret], [
        LevelTarget(LocationNames.level_boss_sallystageplay),
        Target(LocationNames.loc_quest_wolfgang, None, dep_wolfgang_quest)
    ]),
    LevelRegionData(LocationNames.level_boss_sallystageplay, None, [
        LevelTarget(LocationNames.level_boss_mouse),
        LevelTarget(LocationNames.level_mausoleum_iii),
        LevelTarget(LocationNames.level_boss_train),
        Target(LocationNames.level_shop3), # FIXME: Verify that this connection is legit
        Target(LocationNames.loc_quest_15agrades, None, dep_agrade_quest)
    ]),
    LevelRegionData(LocationNames.level_boss_mouse, None, [
        LevelTarget(LocationNames.level_boss_sallystageplay), # FIXME: Verify that this connection is legit
        Target(LocationNames.loc_quest_wolfgang, None, dep_wolfgang_quest)
    ]),
    LevelRegionData(LocationNames.level_boss_train, None, [Target(LocationNames.world_inkwell_hell)]),
    LevelRegionData(LocationNames.level_rungun_harbour, None, [
        LevelTarget(LocationNames.level_boss_mouse),
        LevelTarget(LocationNames.level_mausoleum_iii),
        Target(LocationNames.level_shop3),
        Target(LocationNames.loc_quest_15agrades, None, dep_agrade_quest)
    ]),
    LevelRegionData(LocationNames.level_rungun_mountain, None, [
        LevelTarget(LocationNames.level_boss_mouse),
        LevelTarget(LocationNames.level_mausoleum_iii),
        Target(LocationNames.level_shop3),
        Target(LocationNames.loc_quest_15agrades, None, dep_agrade_quest)
    ]),
    LevelRegionData(LocationNames.level_mausoleum_iii, None, None),
    RegionData(LocationNames.loc_quest_wolfgang, [
        LocationNames.loc_quest_wolfgang
    ], None, dep_wolfgang_quest),
    RegionData(LocationNames.loc_quest_ludwig, [
        LocationNames.loc_quest_ludwig,
        LocationNames.loc_event_music
    ], None, dep_wolfgang_quest),
    RegionData(LocationNames.loc_quest_15agrades, [LocationNames.loc_quest_15agrades], None, dep_agrade_quest),
    RegionData(LocationNames.loc_quest_pacifist, [LocationNames.loc_quest_pacifist], None, dep_pacifist_quest),
]
region_isleh = [
    LevelRegionData(LocationNames.level_boss_kingdice, None, [LevelTarget(LocationNames.level_boss_devil)]),
    #LevelRegionData(LocationNames.level_boss_devil, None, None),
    RegionData(LocationNames.level_boss_devil, [LocationNames.loc_event_goal_devil]), #FIXME: Temp
]
region_dlc_isle4 = [
    RegionData(LocationNames.level_dlc_tutorial, [
        LocationNames.loc_level_dlc_tutorial,
        LocationNames.loc_level_dlc_tutorial_coin,
    ], None),
    LevelRegionData(LocationNames.level_dlc_boss_oldman, None, [LevelTarget(LocationNames.level_dlc_boss_snowcult)]),
    LevelRegionData(LocationNames.level_dlc_boss_rumrunners, None, [
        LevelTarget(LocationNames.level_dlc_boss_plane_cowboy),
        Target(LocationNames.loc_dlc_quest_cactusgirl, None, dep_dlc_cactusgirl_quest),
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
        Target(LocationNames.loc_dlc_quest_cactusgirl, None, dep_dlc_cactusgirl_quest),
    ]),
    #LevelRegionData(LocationNames.level_dlc_boss_saltbaker, None),
    RegionData(LocationNames.level_dlc_boss_saltbaker, [LocationNames.loc_event_dlc_goal_saltbaker]), #FIXME: Temp
    #LevelRegionData(LocationNames.level_dlc_graveyard, None),
    RegionData(LocationNames.level_dlc_chesscastle, None, [
        LevelTarget(LocationNames.level_dlc_chesscastle_pawn)
    ]),
    RegionData(LocationNames.loc_dlc_quest_cactusgirl, [LocationNames.loc_dlc_quest_cactusgirl], None, dep_dlc_cactusgirl_quest),
]
region_dlc_chesscastle = [
    # Setup Regions later
    LevelRegionData(LocationNames.level_dlc_chesscastle_pawn, None, [LevelTarget(LocationNames.level_dlc_chesscastle_knight)]),
    LevelRegionData(LocationNames.level_dlc_chesscastle_knight, None, [LevelTarget(LocationNames.level_dlc_chesscastle_bishop)]),
    LevelRegionData(LocationNames.level_dlc_chesscastle_bishop, None, [LevelTarget(LocationNames.level_dlc_chesscastle_rook)]),
    LevelRegionData(LocationNames.level_dlc_chesscastle_rook, None, [LevelTarget(LocationNames.level_dlc_chesscastle_queen)]),
    LevelRegionData(LocationNames.level_dlc_chesscastle_queen, None, [LevelTarget(LocationNames.level_dlc_chesscastle_run)]),
    LevelRegionData(LocationNames.level_dlc_chesscastle_run, None)
]
region_dlc_special = [
    # Add Logic Regions and connections to curse_complete
]

regions_start = [
    region_begin,
    region_house,
    region_house_level_tutorial,
]
regions_base = region_worlds + region_isle1 + region_isle2 + region_isle3 + region_isleh
regions_dlc = region_dlc_worlds + region_dlc_isle4 + region_dlc_chesscastle #+ region_dlc_special

def get_regions(world: CupheadWorld) -> list[RegionData]:
    shop_locations = world.shop_locations
    using_dlc = world.wsettings.use_dlc

    region_shops = []
    region_dlc_shops = []

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
