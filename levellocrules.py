from __future__ import annotations
from enum import IntEnum
from typing import Optional, NamedTuple
from .names import LocationNames
from .levels import levels_all
from .levelrules import LevelRule
from . import levelrules as lr

class LevelRuleModes(IntEnum):
    NONE = 0
    INHERIT = 1
    INHERIT_OR = 2

class LRule(NamedTuple):
    rule: LevelRule
    mode: LevelRuleModes | int = LevelRuleModes.NONE

class LevelRuleData:
    base_region: str
    base_rule: Optional[LevelRule]
    loc_rules: dict[str, LevelRule]

    def _get_loc_rules(self, loc_rules: dict[str, Optional[LRule]]) -> dict[str, LevelRule]:
        _loc_rules = loc_rules.copy()
        _event_locs: set[str] = set()
        nloc_rules: dict[str, LevelRule] = {}
        if levels_all[self.base_region]:
            for _loc in levels_all[self.base_region].locations:
                if _loc not in _loc_rules:
                    if _loc.startswith(LocationNames.loc_event_pfx):
                        _event_locs.add(_loc)
                        print(f"Adding event location {_loc}...")
                    else:
                        _loc_rules[_loc] = LRule(self.base_rule) if self.base_rule else None
                        print(f"Adding location rule {_loc}...")
        for _loc, lrule in _loc_rules.items():
            if lrule:
                _nrule = lrule.rule
                if self.base_rule:
                    if lrule.mode == LevelRuleModes.INHERIT:
                        _nrule = lr.level_rule_and(_nrule, self.base_rule)
                        print(f"Inheriting rule for {_loc}...")
                    elif lrule.mode == LevelRuleModes.INHERIT_OR:
                        _nrule = lr.level_rule_or(_nrule, self.base_rule)
                        print(f"Inheriting OR rule for {_loc}...")
                nloc_rules[_loc] = _nrule
            else:
                print(f"No rule for {_loc}. Skipping.")
        for _eloc in _event_locs:
            _loc = _eloc.removeprefix(LocationNames.loc_event_pfx)
            if _loc in nloc_rules:
                nloc_rules[_eloc] = nloc_rules[_loc]
                print(f"Adding event rule {_eloc}...")
        return nloc_rules

    def __init__(self, base_region: str, base_rule: Optional[LevelRule], loc_rules: dict[str, Optional[LRule]]):
        self.base_region = base_region
        self.base_rule = base_rule
        self.loc_rules = self._get_loc_rules(loc_rules)

level_loc_rule_forest = LevelRuleData(LocationNames.level_rungun_forest, lr.level_rule_dash, {
    LocationNames.loc_level_rungun_forest_coin1: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_forest_coin2: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_forest_coin3: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_forest_coin4: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_forest_coin5: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_forest_agrade: LRule(lr.level_rule_parry, LevelRuleModes.INHERIT),
    #LocationNames.loc_level_rungun_forest_pacifist: LRule(lr.level_rule_none, LevelRuleModes.INHERIT),
})

level_loc_rule_tree = LevelRuleData(LocationNames.level_rungun_tree, lr.level_rule_dash, {
    LocationNames.loc_level_rungun_tree_coin1: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_tree_coin2: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_tree_coin3: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_tree_coin4: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_tree_coin5: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_tree_agrade: LRule(lr.level_rule_parry, LevelRuleModes.INHERIT),
    #LocationNames.loc_level_rungun_tree_pacifist: LRule(lr.level_rule_none, LevelRuleModes.INHERIT),
})

level_loc_rule_circus = LevelRuleData(LocationNames.level_rungun_circus, lr.level_rule_parry_or_psugar, {
    LocationNames.loc_level_rungun_circus_coin1: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_circus_coin2: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_circus_coin3: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_circus_coin4: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_circus_coin5: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_circus_agrade: LRule(lr.level_rule_parry, LevelRuleModes.INHERIT),
    #LocationNames.loc_level_rungun_circus_pacifist: LRule(lr.level_rule_none, LevelRuleModes.INHERIT),
})

level_loc_rule_funhouse = LevelRuleData(LocationNames.level_rungun_funhouse, lr.level_rule_funhouse, {
    LocationNames.loc_level_rungun_funhouse_coin1: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_funhouse_coin2: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_funhouse_coin3: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_funhouse_coin4: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_funhouse_coin5: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_funhouse_agrade: LRule(lr.level_rule_parry, LevelRuleModes.INHERIT),
    #LocationNames.loc_level_rungun_funhouse_pacifist: LRule(lr.level_rule_none, LevelRuleModes.INHERIT),
})

level_loc_rule_harbour = LevelRuleData(LocationNames.level_rungun_harbour, lr.level_rule_dash_and_parry, {
    LocationNames.loc_level_rungun_harbour_coin1: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_harbour_coin2: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_harbour_coin3: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_harbour_coin4: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_harbour_coin5: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_harbour_agrade: LRule(lr.level_rule_parry, LevelRuleModes.INHERIT),
    #LocationNames.loc_level_rungun_harbour_pacifist: LRule(lr.level_rule_none, LevelRuleModes.INHERIT),
})

level_loc_rule_mountain = LevelRuleData(LocationNames.level_rungun_mountain, lr.level_rule_dash, {
    LocationNames.loc_level_rungun_mountain_coin1: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_mountain_coin2: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_mountain_coin3: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_mountain_coin4: LRule(lr.level_rule_none),
    LocationNames.loc_level_rungun_mountain_coin5: LRule(lr.level_rule_none),
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
