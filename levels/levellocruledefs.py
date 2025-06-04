from __future__ import annotations
from ..names import LocationNames
from .levellocrulebase import LevelLocRuleData, LRule, LevelRuleModes
from . import levelrules as lr

level_loc_rule_locs: set[str] = set()

def register_level_loc_rules(
        base_region: str,
        base_rule: lr.LevelRule | None,
        loc_rules: dict[str, LRule | None]
    ) -> LevelLocRuleData:
    res = LevelLocRuleData(base_region, base_rule, loc_rules)
    for loc in loc_rules.keys():
        level_loc_rule_locs.union(loc)
    return res

level_loc_rules_boss: list[LevelLocRuleData] = [
    LevelLocRuleData(LocationNames.level_boss_plane_genie, None, {
        LocationNames.loc_level_boss_plane_genie_secret: LRule(lr.level_rule_plane_shrink),
    }),
    LevelLocRuleData(LocationNames.level_boss_sallystageplay, None, {
        LocationNames.loc_level_boss_sallystageplay_secret: LRule(lr.level_rule_sallystageplay_secret),
    }),
]

level_loc_rules_dlc_boss: list[LevelLocRuleData] = [
    LevelLocRuleData(LocationNames.level_dlc_boss_oldman, None, {
        LocationNames.loc_level_dlc_boss_oldman_dlc_chaliced: LRule(lr.level_rule_dash_and_parry),
        LocationNames.loc_level_dlc_boss_oldman_event_dlc_chaliced: LRule(lr.level_rule_dash_and_parry)
    }),
    LevelLocRuleData(LocationNames.level_dlc_boss_rumrunners, None, {
        LocationNames.loc_level_dlc_boss_rumrunners_dlc_chaliced: LRule(lr.level_rule_dash_and_parry),
        LocationNames.loc_level_dlc_boss_rumrunners_event_dlc_chaliced: LRule(lr.level_rule_dash_and_parry)
    }),
]

level_loc_rules_rungun: list[LevelLocRuleData] = [
    LevelLocRuleData(LocationNames.level_rungun_forest, lr.level_rule_dash, {
        LocationNames.loc_level_rungun_forest_coin1: LRule(lr.level_rule_none),
        LocationNames.loc_level_rungun_forest_coin2: LRule(lr.level_rule_none),
        LocationNames.loc_level_rungun_forest_coin3: LRule(lr.level_rule_parry),
        LocationNames.loc_level_rungun_forest_coin4: LRule(lr.level_rule_dash),
        LocationNames.loc_level_rungun_forest_coin5: LRule(lr.level_rule_dash),
        LocationNames.loc_level_rungun_forest_agrade: LRule(lr.level_rule_parry, LevelRuleModes.INHERIT),
        #LocationNames.loc_level_rungun_forest_pacifist: LRule(lr.level_rule_none, LevelRuleModes.INHERIT),
        LocationNames.loc_level_rungun_forest_dlc_chaliced: LRule(lr.level_rule_dlc_cookie, LevelRuleModes.INHERIT),
    }),
    LevelLocRuleData(LocationNames.level_rungun_tree, lr.level_rule_dash, {
        LocationNames.loc_level_rungun_tree_coin1: LRule(lr.level_rule_parry),
        LocationNames.loc_level_rungun_tree_coin2: LRule(lr.level_rule_none),
        LocationNames.loc_level_rungun_tree_coin3: LRule(lr.level_rule_none),
        LocationNames.loc_level_rungun_tree_coin4: LRule(lr.level_rule_dash),
        LocationNames.loc_level_rungun_tree_coin5: LRule(lr.level_rule_dash),
        LocationNames.loc_level_rungun_tree_agrade: LRule(lr.level_rule_parry, LevelRuleModes.INHERIT),
        #LocationNames.loc_level_rungun_tree_pacifist: LRule(lr.level_rule_none, LevelRuleModes.INHERIT),
        LocationNames.loc_level_rungun_tree_dlc_chaliced: LRule(lr.level_rule_dlc_cookie, LevelRuleModes.INHERIT),
    }),
    LevelLocRuleData(LocationNames.level_rungun_circus, lr.level_rule_parry_or_psugar, {
        LocationNames.loc_level_rungun_circus_coin1: LRule(lr.level_rule_none),
        LocationNames.loc_level_rungun_circus_coin2: LRule(lr.level_rule_none),
        LocationNames.loc_level_rungun_circus_coin3: LRule(lr.level_rule_parry_or_psugar),
        LocationNames.loc_level_rungun_circus_coin4: LRule(lr.level_rule_parry_or_psugar),
        LocationNames.loc_level_rungun_circus_coin5: LRule(lr.level_rule_parry_or_psugar),
        LocationNames.loc_level_rungun_circus_agrade: LRule(lr.level_rule_parry, LevelRuleModes.INHERIT),
        #LocationNames.loc_level_rungun_circus_pacifist: LRule(lr.level_rule_none, LevelRuleModes.INHERIT),
        LocationNames.loc_level_rungun_circus_dlc_chaliced: LRule(lr.level_rule_dlc_cookie, LevelRuleModes.INHERIT),
    }),
    LevelLocRuleData(LocationNames.level_rungun_funhouse, lr.level_rule_funhouse, {
        LocationNames.loc_level_rungun_funhouse_coin1: LRule(lr.level_rule_parry_or_psugar),
        LocationNames.loc_level_rungun_funhouse_coin2: LRule(lr.level_rule_parry_or_psugar),
        LocationNames.loc_level_rungun_funhouse_coin3: LRule(lr.level_rule_parry_or_psugar),
        LocationNames.loc_level_rungun_funhouse_coin4: LRule(lr.level_rule_parry_or_psugar),
        LocationNames.loc_level_rungun_funhouse_coin5: LRule(lr.level_rule_funhouse),
        LocationNames.loc_level_rungun_funhouse_agrade: LRule(lr.level_rule_parry, LevelRuleModes.INHERIT),
        #LocationNames.loc_level_rungun_funhouse_pacifist: LRule(lr.level_rule_none, LevelRuleModes.INHERIT),
        LocationNames.loc_level_rungun_funhouse_dlc_chaliced: LRule(lr.level_rule_dlc_cookie, LevelRuleModes.INHERIT),
    }),
    LevelLocRuleData(LocationNames.level_rungun_harbour, lr.level_rule_harbour, {
        LocationNames.loc_level_rungun_harbour_coin1: LRule(lr.level_rule_dash_parry_or_psugar),
        LocationNames.loc_level_rungun_harbour_coin2: LRule(lr.level_rule_none),
        LocationNames.loc_level_rungun_harbour_coin3: LRule(lr.level_rule_parry_or_psugar),
        LocationNames.loc_level_rungun_harbour_coin4: LRule(
            lr.level_rule_or(lr.level_rule_parry, lr.level_rule_and(lr.level_rule_psugar, lr.level_rule_dash))
        ),
        LocationNames.loc_level_rungun_harbour_coin5: LRule(lr.level_rule_harbour),
        LocationNames.loc_level_rungun_harbour_agrade: LRule(lr.level_rule_parry, LevelRuleModes.INHERIT),
        #LocationNames.loc_level_rungun_harbour_pacifist: LRule(lr.level_rule_none, LevelRuleModes.INHERIT),
        LocationNames.loc_level_rungun_harbour_dlc_chaliced: LRule(lr.level_rule_dlc_cookie, LevelRuleModes.INHERIT),
    }),
    LevelLocRuleData(LocationNames.level_rungun_mountain, lr.level_rule_dash, {
        LocationNames.loc_level_rungun_mountain_coin1: LRule(lr.level_rule_none),
        LocationNames.loc_level_rungun_mountain_coin2: LRule(lr.level_rule_dash),
        LocationNames.loc_level_rungun_mountain_coin3: LRule(lr.level_rule_none),
        LocationNames.loc_level_rungun_mountain_coin4: LRule(lr.level_rule_none),
        LocationNames.loc_level_rungun_mountain_coin5: LRule(lr.level_rule_dash),
        LocationNames.loc_level_rungun_mountain_agrade: LRule(lr.level_rule_parry, LevelRuleModes.INHERIT),
        #LocationNames.loc_level_rungun_mountain_pacifist: LRule(lr.level_rule_none, LevelRuleModes.INHERIT),
        LocationNames.loc_level_rungun_mountain_dlc_chaliced: LRule(lr.level_rule_dlc_cookie, LevelRuleModes.INHERIT),
    }),
]

level_loc_rules_dlc_tutorial: list[LevelLocRuleData] = [
    LevelLocRuleData(LocationNames.level_dlc_tutorial, lr.level_rule_dlc_cookie, {
        LocationNames.loc_level_dlc_tutorial: LRule(lr.level_rule_none),
        LocationNames.loc_level_dlc_tutorial_coin: LRule(lr.level_rule_dlc_tutorial_coin),
    }),
]

level_loc_rules_dlc_chesscastle: list[LevelLocRuleData] = [
    LevelLocRuleData(LocationNames.level_dlc_chesscastle_pawn, None, {
        LocationNames.loc_level_dlc_chesscastle_pawn_dlc_chaliced: LRule(lr.level_rule_dash_and_parry)
    }),
    LevelLocRuleData(LocationNames.level_dlc_chesscastle_knight, None, {
        LocationNames.loc_level_dlc_chesscastle_knight_dlc_chaliced: LRule(lr.level_rule_dash_and_parry)
    }),
    LevelLocRuleData(LocationNames.level_dlc_chesscastle_bishop, None, {
        LocationNames.loc_level_dlc_chesscastle_bishop_dlc_chaliced: LRule(lr.level_rule_dash_and_parry)
    }),
    LevelLocRuleData(LocationNames.level_dlc_chesscastle_rook, None, {
        LocationNames.loc_level_dlc_chesscastle_rook_dlc_chaliced: LRule(lr.level_rule_dash_and_parry)
    }),
    LevelLocRuleData(LocationNames.level_dlc_chesscastle_queen, None, {
        LocationNames.loc_level_dlc_chesscastle_queen_dlc_chaliced: LRule(lr.level_rule_dash_and_parry)
    }),
    LevelLocRuleData(LocationNames.level_dlc_chesscastle_run, None, {
        LocationNames.loc_level_dlc_chesscastle_run_dlc_chaliced: LRule(lr.level_rule_dash_and_parry)
    })
]

level_loc_rules: list[LevelLocRuleData] = [
    *level_loc_rules_boss,
    *level_loc_rules_dlc_boss,
    *level_loc_rules_rungun,
    *level_loc_rules_dlc_tutorial,
    *level_loc_rules_dlc_chesscastle,
]
