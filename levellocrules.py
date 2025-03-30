from __future__ import annotations
from .names import LocationNames
from .levellocrulebase import LevelRuleData, LRule, LevelRuleModes
from . import levelrules as lr

level_loc_rule_locs: set[str] = set()

def register_level_loc_rules(
        base_region: str,
        base_rule: lr.LevelRule | None,
        loc_rules: dict[str, LRule | None]
    ) -> LevelRuleData:
    res = LevelRuleData(base_region, base_rule, loc_rules)
    for loc in loc_rules.keys():
        level_loc_rule_locs.union(loc)
    return res

level_loc_rule_forest = LevelRuleData(LocationNames.level_rungun_forest, lr.level_rule_dash, {
    LocationNames.loc_level_rungun_forest_coin1: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_forest_coin2: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_forest_coin3: LRule(lr.level_rule_parry),
    LocationNames.loc_level_rungun_forest_coin4: LRule(lr.level_rule_dash),
    LocationNames.loc_level_rungun_forest_coin5: LRule(lr.level_rule_dash),
    LocationNames.loc_level_rungun_forest_agrade: LRule(lr.level_rule_parry, LevelRuleModes.INHERIT),
    #LocationNames.loc_level_rungun_forest_pacifist: LRule(lr.level_rule_none, LevelRuleModes.INHERIT),
})

level_loc_rule_tree = LevelRuleData(LocationNames.level_rungun_tree, lr.level_rule_dash, {
    LocationNames.loc_level_rungun_tree_coin1: LRule(lr.level_rule_parry),
    LocationNames.loc_level_rungun_tree_coin2: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_tree_coin3: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_tree_coin4: LRule(lr.level_rule_dash),
    LocationNames.loc_level_rungun_tree_coin5: LRule(lr.level_rule_dash),
    LocationNames.loc_level_rungun_tree_agrade: LRule(lr.level_rule_parry, LevelRuleModes.INHERIT),
    #LocationNames.loc_level_rungun_tree_pacifist: LRule(lr.level_rule_none, LevelRuleModes.INHERIT),
})

level_loc_rule_circus = LevelRuleData(LocationNames.level_rungun_circus, lr.level_rule_parry_or_psugar, {
    LocationNames.loc_level_rungun_circus_coin1: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_circus_coin2: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_circus_coin3: LRule(lr.level_rule_parry_or_psugar),
    LocationNames.loc_level_rungun_circus_coin4: LRule(lr.level_rule_parry_or_psugar),
    LocationNames.loc_level_rungun_circus_coin5: LRule(lr.level_rule_parry_or_psugar),
    LocationNames.loc_level_rungun_circus_agrade: LRule(lr.level_rule_parry, LevelRuleModes.INHERIT),
    #LocationNames.loc_level_rungun_circus_pacifist: LRule(lr.level_rule_none, LevelRuleModes.INHERIT),
})

level_loc_rule_funhouse = LevelRuleData(LocationNames.level_rungun_funhouse, lr.level_rule_funhouse, {
    LocationNames.loc_level_rungun_funhouse_coin1: LRule(lr.level_rule_parry_or_psugar),
    LocationNames.loc_level_rungun_funhouse_coin2: LRule(lr.level_rule_parry_or_psugar),
    LocationNames.loc_level_rungun_funhouse_coin3: LRule(lr.level_rule_parry_or_psugar),
    LocationNames.loc_level_rungun_funhouse_coin4: LRule(lr.level_rule_parry_or_psugar),
    LocationNames.loc_level_rungun_funhouse_coin5: LRule(lr.level_rule_funhouse),
    LocationNames.loc_level_rungun_funhouse_agrade: LRule(lr.level_rule_parry, LevelRuleModes.INHERIT),
    #LocationNames.loc_level_rungun_funhouse_pacifist: LRule(lr.level_rule_none, LevelRuleModes.INHERIT),
})

level_loc_rule_harbour = LevelRuleData(LocationNames.level_rungun_harbour, lr.level_rule_harbour, {
    LocationNames.loc_level_rungun_harbour_coin1: LRule(lr.level_rule_dash_parry_or_psugar),
    LocationNames.loc_level_rungun_harbour_coin2: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_harbour_coin3: LRule(lr.level_rule_parry_or_psugar),
    LocationNames.loc_level_rungun_harbour_coin4: LRule(lr.level_rule_or(lr.level_rule_parry, lr.level_rule_and(lr.level_rule_psugar, lr.level_rule_dash))),
    LocationNames.loc_level_rungun_harbour_coin5: LRule(lr.level_rule_harbour),
    LocationNames.loc_level_rungun_harbour_agrade: LRule(lr.level_rule_parry, LevelRuleModes.INHERIT),
    #LocationNames.loc_level_rungun_harbour_pacifist: LRule(lr.level_rule_none, LevelRuleModes.INHERIT),
})

level_loc_rule_mountain = LevelRuleData(LocationNames.level_rungun_mountain, lr.level_rule_dash, {
    LocationNames.loc_level_rungun_mountain_coin1: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_mountain_coin2: LRule(lr.level_rule_dash),
    LocationNames.loc_level_rungun_mountain_coin3: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_mountain_coin4: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_mountain_coin5: LRule(lr.level_rule_dash),
    LocationNames.loc_level_rungun_mountain_agrade: LRule(lr.level_rule_parry, LevelRuleModes.INHERIT),
    #LocationNames.loc_level_rungun_mountain_pacifist: LRule(lr.level_rule_none, LevelRuleModes.INHERIT),
})

level_loc_rules: list[LevelRuleData] = [
    level_loc_rule_forest,
    level_loc_rule_tree,
    level_loc_rule_circus,
    level_loc_rule_funhouse,
    level_loc_rule_harbour,
    level_loc_rule_mountain
]
