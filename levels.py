from __future__ import annotations
from typing import NamedTuple, Optional, Callable
from random import Random
from .names import LocationNames, ItemNames
from .locations import LocationData
from .settings import WorldSettings
from .auxiliary import scrub_list
from .rulebase import RegionRule, region_rule_none, region_rule_has, region_rule_has_any

LevelRule = Callable[[WorldSettings], RegionRule]

# Level Rules
def level_rule_and(a: LevelRule, b: LevelRule) -> LevelRule:
    return lambda s: lambda state, player: a(s)(state, player) and b(s)(state, player)
def level_rule_not(a: LevelRule) -> LevelRule:
    return lambda s: lambda state, player: not a(s)(state, player)
def level_rule_or(a: LevelRule, b: LevelRule) -> LevelRule:
    return lambda s: lambda state, player: a(s)(state, player) or b(s)(state, player)
def level_rule_none(settings: WorldSettings) -> RegionRule:
    return region_rule_none()
def level_rule_plane_gun(settings: WorldSettings) -> RegionRule:
    return region_rule_has(ItemNames.item_plane_gun)
def level_rule_plane_bombs(settings: WorldSettings) -> RegionRule:
    return region_rule_has(ItemNames.item_plane_bombs)
def level_rule_plane(settings: WorldSettings) -> RegionRule:
    if settings.hard_logic:
        return level_rule_or(level_rule_plane_gun, level_rule_plane_bombs)(settings)
    else:
        return level_rule_plane_gun(settings)
def level_rule_dash(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return region_rule_has(ItemNames.item_ability_dash)
def level_rule_parry(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return region_rule_has(ItemNames.item_ability_parry)
def level_rule_dash_or_parry(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return level_rule_or(level_rule_dash, level_rule_parry)(settings)
def level_rule_dash_and_parry(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return level_rule_and(level_rule_dash, level_rule_parry)(settings)
def level_rule_plane_parry(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return region_rule_has_any((ItemNames.item_ability_plane_parry, ItemNames.item_charm_psugar))
def level_rule_bird(settings: WorldSettings):
    if settings.hard_logic:
        return level_rule_plane_gun(settings)
    else:
        return level_rule_and(level_rule_plane_gun, level_rule_plane_bombs)(settings)
def level_rule_pirate(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return region_rule_has_any({ItemNames.item_ability_duck, ItemNames.item_ability_parry})
def level_rule_robot(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_plane(settings)
    return level_rule_and(level_rule_plane, level_rule_plane_parry)(settings)
def level_rule_devil(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_plane(settings)
    return level_rule_and(level_rule_dash, level_rule_plane_parry)(settings)
def level_dlc_rule_relic(settings: WorldSettings) -> RegionRule:
    return region_rule_has(ItemNames.item_charm_dlc_broken_relic, 1)

level_map = {
    0: LocationNames.level_boss_veggies,
    1: LocationNames.level_boss_slime,
    2: LocationNames.level_boss_frogs,
    3: LocationNames.level_boss_flower,
    4: LocationNames.level_boss_baroness,
    5: LocationNames.level_boss_clown,
    6: LocationNames.level_boss_dragon,
    7: LocationNames.level_boss_bee,
    8: LocationNames.level_boss_pirate,
    9: LocationNames.level_boss_mouse,
    10: LocationNames.level_boss_sallystageplay,
    11: LocationNames.level_boss_train,
    12: LocationNames.level_boss_plane_blimp,
    13: LocationNames.level_boss_plane_genie,
    14: LocationNames.level_boss_plane_bird,
    15: LocationNames.level_boss_plane_mermaid,
    16: LocationNames.level_boss_plane_robot,
    17: LocationNames.level_boss_kingdice,
    18: LocationNames.level_boss_devil,
    19: LocationNames.level_rungun_forest,
    20: LocationNames.level_rungun_tree,
    21: LocationNames.level_rungun_circus,
    22: LocationNames.level_rungun_funhouse,
    23: LocationNames.level_rungun_harbour,
    24: LocationNames.level_rungun_mountain,
    100: LocationNames.level_dlc_boss_oldman,
    101: LocationNames.level_dlc_boss_rumrunners,
    102: LocationNames.level_dlc_boss_snowcult,
    103: LocationNames.level_dlc_boss_airplane,
    104: LocationNames.level_dlc_boss_plane_cowboy,
    105: LocationNames.level_dlc_boss_saltbaker,
    106: LocationNames.level_dlc_graveyard,
    107: LocationNames.level_dlc_chesscastle_pawn,
    108: LocationNames.level_dlc_chesscastle_knight,
    109: LocationNames.level_dlc_chesscastle_bishop,
    110: LocationNames.level_dlc_chesscastle_rook,
    111: LocationNames.level_dlc_chesscastle_queen,
}
level_id_map = {v: k for k, v in level_map.items()}

class LevelData(NamedTuple):
    world_location: Optional[str]
    locations: list[str] = None
    rule: LevelRule = level_rule_none

# Levels
level_boss = {
    LocationNames.level_boss_veggies: LevelData(LocationNames.world_inkwell_1, [
        LocationNames.loc_level_boss_veggies,
        LocationNames.loc_level_boss_veggies_topgrade,
        LocationNames.loc_level_boss_veggies_secret,
        LocationNames.loc_level_boss_veggies_event_agrade,
        LocationNames.loc_level_boss_veggies_dlc_chaliced,
    ]), # No rules
    LocationNames.level_boss_slime: LevelData(LocationNames.world_inkwell_1, [
        LocationNames.loc_level_boss_slime,
        LocationNames.loc_level_boss_slime_topgrade,
        LocationNames.loc_level_boss_slime_event_agrade,
        LocationNames.loc_level_boss_slime_dlc_chaliced,
    ]), # No rules
    LocationNames.level_boss_frogs: LevelData(LocationNames.world_inkwell_1, [
        LocationNames.loc_level_boss_frogs,
        LocationNames.loc_level_boss_frogs_topgrade,
        LocationNames.loc_level_boss_frogs_event_agrade,
        LocationNames.loc_level_boss_frogs_dlc_chaliced,
    ]), # No rules
    LocationNames.level_boss_flower: LevelData(LocationNames.world_inkwell_1, [
        LocationNames.loc_level_boss_flower,
        LocationNames.loc_level_boss_flower_topgrade,
        LocationNames.loc_level_boss_flower_event_agrade,
        LocationNames.loc_level_boss_flower_dlc_chaliced,
    ]), # No rules
    LocationNames.level_boss_baroness: LevelData(LocationNames.world_inkwell_2, [
        LocationNames.loc_level_boss_baroness,
        LocationNames.loc_level_boss_baroness_topgrade,
        LocationNames.loc_level_boss_baroness_event_agrade,
        LocationNames.loc_level_boss_baroness_dlc_chaliced,
    ]), # No rules
    LocationNames.level_boss_clown: LevelData(LocationNames.world_inkwell_2, [
        LocationNames.loc_level_boss_clown,
        LocationNames.loc_level_boss_clown_topgrade,
        LocationNames.loc_level_boss_clown_event_agrade,
        LocationNames.loc_level_boss_clown_dlc_chaliced,
    ], level_rule_dash_or_parry),
    LocationNames.level_boss_dragon: LevelData(LocationNames.world_inkwell_2, [
        LocationNames.loc_level_boss_dragon,
        LocationNames.loc_level_boss_dragon_topgrade,
        LocationNames.loc_level_boss_dragon_event_agrade,
        LocationNames.loc_level_boss_dragon_dlc_chaliced,
    ]), # No Rules
    LocationNames.level_boss_bee: LevelData(LocationNames.world_inkwell_3, [
        LocationNames.loc_level_boss_bee,
        LocationNames.loc_level_boss_bee_topgrade,
        LocationNames.loc_level_boss_bee_event_agrade,
        LocationNames.loc_level_boss_bee_dlc_chaliced,
    ]), # No Rules
    LocationNames.level_boss_pirate: LevelData(LocationNames.world_inkwell_3, [
        LocationNames.loc_level_boss_pirate,
        LocationNames.loc_level_boss_pirate_topgrade,
        LocationNames.loc_level_boss_pirate_event_agrade,
        LocationNames.loc_level_boss_pirate_dlc_chaliced,
    ], level_rule_pirate),
    LocationNames.level_boss_mouse: LevelData(LocationNames.world_inkwell_3, [
        LocationNames.loc_level_boss_mouse,
        LocationNames.loc_level_boss_mouse_topgrade,
        LocationNames.loc_level_boss_mouse_event_agrade,
        LocationNames.loc_level_boss_mouse_dlc_chaliced,
    ], level_rule_parry),
    LocationNames.level_boss_sallystageplay: LevelData(LocationNames.world_inkwell_3, [
        LocationNames.loc_level_boss_sallystageplay,
        LocationNames.loc_level_boss_sallystageplay_topgrade,
        LocationNames.loc_level_boss_sallystageplay_secret,
        LocationNames.loc_level_boss_sallystageplay_event_agrade,
        LocationNames.loc_level_boss_sallystageplay_dlc_chaliced,
    ], level_rule_parry),
    LocationNames.level_boss_train: LevelData(LocationNames.world_inkwell_3, [
        LocationNames.loc_level_boss_train,
        LocationNames.loc_level_boss_train_topgrade,
        LocationNames.loc_level_boss_train_event_agrade,
        LocationNames.loc_level_boss_train_dlc_chaliced,
    ], level_rule_parry),
    LocationNames.level_boss_kingdice: LevelData(LocationNames.world_inkwell_hell, [
        LocationNames.loc_level_boss_kingdice,
        LocationNames.loc_level_boss_kingdice_topgrade,
        LocationNames.loc_level_boss_kingdice_event_agrade,
        LocationNames.loc_level_boss_kingdice_dlc_chaliced,
    ], level_rule_plane), # Has special rules set in rules.py
    LocationNames.level_boss_plane_blimp: LevelData(LocationNames.world_inkwell_1, [
        LocationNames.loc_level_boss_plane_blimp,
        LocationNames.loc_level_boss_plane_blimp_topgrade,
        LocationNames.loc_level_boss_plane_blimp_event_agrade,
        LocationNames.loc_level_boss_plane_blimp_dlc_chaliced,
    ], level_rule_plane),
    LocationNames.level_boss_plane_genie: LevelData(LocationNames.world_inkwell_2, [
        LocationNames.loc_level_boss_plane_genie,
        LocationNames.loc_level_boss_plane_genie_topgrade,
        LocationNames.loc_level_boss_plane_genie_secret,
        LocationNames.loc_level_boss_plane_genie_event_agrade,
        LocationNames.loc_level_boss_plane_genie_dlc_chaliced,
    ], level_rule_plane),
    LocationNames.level_boss_plane_bird: LevelData(LocationNames.world_inkwell_2, [
        LocationNames.loc_level_boss_plane_bird,
        LocationNames.loc_level_boss_plane_bird_topgrade,
        LocationNames.loc_level_boss_plane_bird_event_agrade,
        LocationNames.loc_level_boss_plane_bird_dlc_chaliced,
    ], level_rule_bird),
    LocationNames.level_boss_plane_mermaid: LevelData(LocationNames.world_inkwell_3, [
        LocationNames.loc_level_boss_plane_mermaid,
        LocationNames.loc_level_boss_plane_mermaid_topgrade,
        LocationNames.loc_level_boss_plane_mermaid_event_agrade,
        LocationNames.loc_level_boss_plane_mermaid_dlc_chaliced,
    ], level_rule_plane),
    LocationNames.level_boss_plane_robot: LevelData(LocationNames.world_inkwell_3, [
        LocationNames.loc_level_boss_plane_robot,
        LocationNames.loc_level_boss_plane_robot_topgrade,
        LocationNames.loc_level_boss_plane_robot_event_agrade,
        LocationNames.loc_level_boss_plane_robot_dlc_chaliced,
    ], level_rule_plane),
}
level_boss_final = {
    LocationNames.level_boss_devil: LevelData(LocationNames.world_inkwell_hell, [
        LocationNames.loc_level_boss_devil,
        LocationNames.loc_level_boss_devil_topgrade,
        LocationNames.loc_level_boss_devil_event_agrade,
        LocationNames.loc_level_boss_devil_dlc_chaliced,
    ], level_rule_devil)
}
level_dlc_boss = {
    LocationNames.level_dlc_boss_oldman: LevelData(LocationNames.world_dlc_inkwell_4, [
        LocationNames.loc_level_dlc_boss_oldman,
        LocationNames.loc_level_dlc_boss_oldman_topgrade,
        LocationNames.loc_level_dlc_boss_oldman_event_agrade,
        LocationNames.loc_level_dlc_boss_oldman_dlc_chaliced,
    ]),
    LocationNames.level_dlc_boss_rumrunners: LevelData(LocationNames.world_dlc_inkwell_4, [
        LocationNames.loc_level_dlc_boss_rumrunners,
        LocationNames.loc_level_dlc_boss_rumrunners_topgrade,
        LocationNames.loc_level_dlc_boss_rumrunners_event_agrade,
        LocationNames.loc_level_dlc_boss_rumrunners_dlc_chaliced,
    ], level_rule_parry),
    LocationNames.level_dlc_boss_snowcult: LevelData(LocationNames.world_dlc_inkwell_4, [
        LocationNames.loc_level_dlc_boss_snowcult,
        LocationNames.loc_level_dlc_boss_snowcult_topgrade,
        LocationNames.loc_level_dlc_boss_snowcult_event_agrade,
        LocationNames.loc_level_dlc_boss_snowcult_dlc_chaliced,
    ]), # No Rules
    LocationNames.level_dlc_boss_airplane: LevelData(LocationNames.world_dlc_inkwell_4, [
        LocationNames.loc_level_dlc_boss_airplane,
        LocationNames.loc_level_dlc_boss_airplane_topgrade,
        LocationNames.loc_level_dlc_boss_airplane_event_agrade,
        LocationNames.loc_level_dlc_boss_airplane_dlc_chaliced,
    ]), # ???
    LocationNames.level_dlc_boss_plane_cowboy: LevelData(LocationNames.world_dlc_inkwell_4, [
        LocationNames.loc_level_dlc_boss_plane_cowboy,
        LocationNames.loc_level_dlc_boss_plane_cowboy_topgrade,
        LocationNames.loc_level_dlc_boss_plane_cowboy_event_agrade,
        LocationNames.loc_level_dlc_boss_plane_cowboy_dlc_chaliced,
    ], level_rule_plane),
}
level_dlc_boss_final = {
    LocationNames.level_dlc_boss_saltbaker: LevelData(LocationNames.world_dlc_inkwell_4, [
        LocationNames.loc_level_dlc_boss_saltbaker,
        LocationNames.loc_level_dlc_boss_saltbaker_topgrade,
        LocationNames.loc_level_dlc_boss_saltbaker_event_agrade,
        LocationNames.loc_level_dlc_boss_saltbaker_dlc_chaliced,
    ]),
}
level_dlc_special = {
    #LocationNames.level_dlc_graveyard: LevelData(LocationNames.world_dlc_inkwell_4, [LocationNames.loc_level_dlc_graveyard,], level_dlc_rule_relic),
}
level_dicepalace_boss = {
    LocationNames.level_dicepalace_boss_booze: LevelData(LocationNames.level_boss_kingdice, [LocationNames.loc_level_dicepalace_boss_booze,]),
    LocationNames.level_dicepalace_boss_chips: LevelData(LocationNames.level_boss_kingdice, [LocationNames.loc_level_dicepalace_boss_chips,]),
    LocationNames.level_dicepalace_boss_cigar: LevelData(LocationNames.level_boss_kingdice, [LocationNames.loc_level_dicepalace_boss_cigar,]),
    LocationNames.level_dicepalace_boss_domino: LevelData(LocationNames.level_boss_kingdice, [LocationNames.loc_level_dicepalace_boss_domino,]),
    LocationNames.level_dicepalace_boss_rabbit: LevelData(LocationNames.level_boss_kingdice, [LocationNames.loc_level_dicepalace_boss_rabbit,]),
    LocationNames.level_dicepalace_boss_plane_horse: LevelData(LocationNames.level_boss_kingdice, [LocationNames.loc_level_dicepalace_boss_plane_horse,], ),
    LocationNames.level_dicepalace_boss_roulette: LevelData(LocationNames.level_boss_kingdice, [LocationNames.loc_level_dicepalace_boss_roulette,]),
    LocationNames.level_dicepalace_boss_eightball: LevelData(LocationNames.level_boss_kingdice, [LocationNames.loc_level_dicepalace_boss_eightball,]),
    LocationNames.level_dicepalace_boss_plane_memory: LevelData(LocationNames.level_boss_kingdice, [LocationNames.loc_level_dicepalace_boss_plane_memory,]),
}
level_rungun = {
    LocationNames.level_rungun_forest: LevelData(LocationNames.world_inkwell_1, [
        LocationNames.loc_level_rungun_forest,
        LocationNames.loc_level_rungun_forest_agrade,
        LocationNames.loc_level_rungun_forest_pacifist,
        LocationNames.loc_level_rungun_forest_coin1,
        LocationNames.loc_level_rungun_forest_coin2,
        LocationNames.loc_level_rungun_forest_coin3,
        LocationNames.loc_level_rungun_forest_coin4,
        LocationNames.loc_level_rungun_forest_coin5,
        LocationNames.loc_level_rungun_forest_event_agrade,
        LocationNames.loc_level_rungun_forest_event_pacifist,
    ]),
    LocationNames.level_rungun_tree: LevelData(LocationNames.world_inkwell_1, [
        LocationNames.loc_level_rungun_tree,
        LocationNames.loc_level_rungun_tree_agrade,
        LocationNames.loc_level_rungun_tree_pacifist,
        LocationNames.loc_level_rungun_tree_coin1,
        LocationNames.loc_level_rungun_tree_coin2,
        LocationNames.loc_level_rungun_tree_coin3,
        LocationNames.loc_level_rungun_tree_coin4,
        LocationNames.loc_level_rungun_tree_coin5,
        LocationNames.loc_level_rungun_tree_event_agrade,
        LocationNames.loc_level_rungun_tree_event_pacifist,
    ], level_rule_dash),
    LocationNames.level_rungun_circus: LevelData(LocationNames.world_inkwell_2, [
        LocationNames.loc_level_rungun_circus,
        LocationNames.loc_level_rungun_circus_agrade,
        LocationNames.loc_level_rungun_circus_pacifist,
        LocationNames.loc_level_rungun_circus_coin1,
        LocationNames.loc_level_rungun_circus_coin2,
        LocationNames.loc_level_rungun_circus_coin3,
        LocationNames.loc_level_rungun_circus_coin4,
        LocationNames.loc_level_rungun_circus_coin5,
        LocationNames.loc_level_rungun_circus_event_agrade,
        LocationNames.loc_level_rungun_circus_event_pacifist,
    ]),
    LocationNames.level_rungun_funhouse: LevelData(LocationNames.world_inkwell_2, [
        LocationNames.loc_level_rungun_funhouse,
        LocationNames.loc_level_rungun_funhouse_agrade,
        LocationNames.loc_level_rungun_funhouse_pacifist,
        LocationNames.loc_level_rungun_funhouse_coin1,
        LocationNames.loc_level_rungun_funhouse_coin2,
        LocationNames.loc_level_rungun_funhouse_coin3,
        LocationNames.loc_level_rungun_funhouse_coin4,
        LocationNames.loc_level_rungun_funhouse_coin5,
        LocationNames.loc_level_rungun_funhouse_event_agrade,
        LocationNames.loc_level_rungun_funhouse_event_pacifist,
    ], level_rule_parry),
    LocationNames.level_rungun_harbour: LevelData(LocationNames.world_inkwell_3, [
        LocationNames.loc_level_rungun_harbour,
        LocationNames.loc_level_rungun_harbour_agrade,
        LocationNames.loc_level_rungun_harbour_pacifist,
        LocationNames.loc_level_rungun_harbour_coin1,
        LocationNames.loc_level_rungun_harbour_coin2,
        LocationNames.loc_level_rungun_harbour_coin3,
        LocationNames.loc_level_rungun_harbour_coin4,
        LocationNames.loc_level_rungun_harbour_coin5,
        LocationNames.loc_level_rungun_harbour_event_agrade,
        LocationNames.loc_level_rungun_harbour_event_pacifist,
    ], level_rule_dash_and_parry),
    LocationNames.level_rungun_mountain: LevelData(LocationNames.world_inkwell_3, [
        LocationNames.loc_level_rungun_mountain,
        LocationNames.loc_level_rungun_mountain_agrade,
        LocationNames.loc_level_rungun_mountain_pacifist,
        LocationNames.loc_level_rungun_mountain_coin1,
        LocationNames.loc_level_rungun_mountain_coin2,
        LocationNames.loc_level_rungun_mountain_coin3,
        LocationNames.loc_level_rungun_mountain_coin4,
        LocationNames.loc_level_rungun_mountain_coin5,
        LocationNames.loc_level_rungun_mountain_event_agrade,
        LocationNames.loc_level_rungun_mountain_event_pacifist,
    ]),
}
level_mausoleum = {
    LocationNames.level_mausoleum_i: LevelData(LocationNames.world_inkwell_1, [LocationNames.loc_level_mausoleum_i]),
    LocationNames.level_mausoleum_ii: LevelData(LocationNames.world_inkwell_2, [LocationNames.loc_level_mausoleum_ii,]),
    LocationNames.level_mausoleum_iii: LevelData(LocationNames.world_inkwell_3, [LocationNames.loc_level_mausoleum_iii,]),
}
level_dlc_chesscastle_boss = {
    LocationNames.level_dlc_chesscastle_pawn: LevelData(LocationNames.level_dlc_chesscastle, [LocationNames.loc_level_dlc_chesscastle_pawn,]),
    LocationNames.level_dlc_chesscastle_knight: LevelData(LocationNames.level_dlc_chesscastle, [LocationNames.loc_level_dlc_chesscastle_knight,]),
    LocationNames.level_dlc_chesscastle_bishop: LevelData(LocationNames.level_dlc_chesscastle, [LocationNames.loc_level_dlc_chesscastle_bishop,]),
    LocationNames.level_dlc_chesscastle_rook: LevelData(LocationNames.level_dlc_chesscastle, [LocationNames.loc_level_dlc_chesscastle_rook,]),
    LocationNames.level_dlc_chesscastle_queen: LevelData(LocationNames.level_dlc_chesscastle, [LocationNames.loc_level_dlc_chesscastle_queen,]),
    LocationNames.level_dlc_chesscastle_run: LevelData(LocationNames.level_dlc_chesscastle, [LocationNames.loc_level_dlc_chesscastle_run,])
}

levels_base: dict[str, LevelData] = {
    **level_boss,
    **level_boss_final,
    **level_rungun,
    **level_mausoleum
}
levels_dlc: dict[str, LevelData] = {
    **level_dlc_boss,
    **level_dlc_boss_final,
    **level_dlc_special,
}

levels_all: dict[str, LevelData] = {
    **levels_base,
    **level_dicepalace_boss,
    **levels_dlc,
    **level_dlc_chesscastle_boss,
}

def setup_levels(settings: WorldSettings, active_locations: dict[str,LocationData]) -> dict[str,LevelData]:
    use_dlc = settings.use_dlc
    levels: dict[str,LevelData] = {}

    for lev,data in {**level_boss, **level_boss_final, **level_rungun}.items():
        levels[lev] = LevelData(data.world_location, scrub_list(data.locations, active_locations.keys()), data.rule)
    levels.update(level_mausoleum)

    if use_dlc:
        for lev,data in {**level_dlc_boss, **level_dlc_boss_final}.items():
            levels[lev] = LevelData(data.world_location, scrub_list(data.locations, active_locations.keys()), data.rule)
        levels.update(level_dlc_special)

    return levels

def setup_level_shuffle_map(rand: Random, settings: WorldSettings) -> dict[int,int]:
    use_dlc = settings.use_dlc
    level_shuffle_map: dict[int,int] = {}

    # level_lists format: (level_list, exclude_list)
    level_lists: list[tuple[list[str],list[str]]] = [
        (list(level_boss.keys()), LocationNames.level_boss_kingdice),
        (list(level_rungun.keys()), None),
    ]
    if use_dlc:
        level_lists[0][0] += list(level_dlc_boss.keys())
        level_lists += (list(level_dlc_chesscastle_boss.keys()), None)

    for level_list in level_lists:
        level_shuffle_map.update(shuffle_levels(rand, level_list[0], level_list[1]))

    return level_shuffle_map

def shuffle_levels(rand: Random, level_list: list[str], level_exclude_list: list[str] = None) -> dict[int, int]:
    res: dict[int, int] = {}
    excludes = level_exclude_list if level_exclude_list else []
    _levels = [level_id_map[x] for x in level_list if (x not in excludes)]

    levels_shuffled = list(_levels)
    rand.shuffle(levels_shuffled)

    for i in range(len(_levels)):
        res[_levels[i]] = levels_shuffled[i]
    for x in excludes:
        res[x] = x

    return res

def level_query(levels: dict[str,LevelData], world_location: Optional[str]) -> dict[str,LevelData]:
    return {level: data for level,data in levels.items() if (not world_location or data.world_location == world_location)}
