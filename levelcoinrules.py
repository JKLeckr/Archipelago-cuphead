from __future__ import annotations
from .names import LocationNames
from .levelrules import LevelRule
from . import levelrules as lr

level_coin_rule_forest: dict[str, LevelRule] = {
    LocationNames.loc_level_rungun_forest_coin1: lr.level_rule_none,
    LocationNames.loc_level_rungun_forest_coin2: lr.level_rule_none,
    LocationNames.loc_level_rungun_forest_coin3: lr.level_rule_none,
    LocationNames.loc_level_rungun_forest_coin4: lr.level_rule_none,
    LocationNames.loc_level_rungun_forest_coin5: lr.level_rule_none,
}

level_coin_rule_tree: dict[str, LevelRule] = {
    LocationNames.loc_level_rungun_tree_coin1: lr.level_rule_none,
    LocationNames.loc_level_rungun_tree_coin2: lr.level_rule_none,
    LocationNames.loc_level_rungun_tree_coin3: lr.level_rule_none,
    LocationNames.loc_level_rungun_tree_coin4: lr.level_rule_none,
    LocationNames.loc_level_rungun_tree_coin5: lr.level_rule_none,
}

level_coin_rule_circus: dict[str, LevelRule] = {
    LocationNames.loc_level_rungun_circus_coin1: lr.level_rule_none,
    LocationNames.loc_level_rungun_circus_coin2: lr.level_rule_none,
    LocationNames.loc_level_rungun_circus_coin3: lr.level_rule_none,
    LocationNames.loc_level_rungun_circus_coin4: lr.level_rule_none,
    LocationNames.loc_level_rungun_circus_coin5: lr.level_rule_none,
}

level_coin_rule_funhouse: dict[str, LevelRule] = {
    LocationNames.loc_level_rungun_funhouse_coin1: lr.level_rule_none,
    LocationNames.loc_level_rungun_funhouse_coin2: lr.level_rule_none,
    LocationNames.loc_level_rungun_funhouse_coin3: lr.level_rule_none,
    LocationNames.loc_level_rungun_funhouse_coin4: lr.level_rule_none,
    LocationNames.loc_level_rungun_funhouse_coin5: lr.level_rule_none,
}

level_coin_rule_harbour: dict[str, LevelRule] = {
    LocationNames.loc_level_rungun_harbour_coin1: lr.level_rule_none,
    LocationNames.loc_level_rungun_harbour_coin2: lr.level_rule_none,
    LocationNames.loc_level_rungun_harbour_coin3: lr.level_rule_none,
    LocationNames.loc_level_rungun_harbour_coin4: lr.level_rule_none,
    LocationNames.loc_level_rungun_harbour_coin5: lr.level_rule_none,
}

level_coin_rule_mountain: dict[str, LevelRule] = {
    LocationNames.loc_level_rungun_mountain_coin1: lr.level_rule_none,
    LocationNames.loc_level_rungun_mountain_coin2: lr.level_rule_none,
    LocationNames.loc_level_rungun_mountain_coin3: lr.level_rule_none,
    LocationNames.loc_level_rungun_mountain_coin4: lr.level_rule_none,
    LocationNames.loc_level_rungun_mountain_coin5: lr.level_rule_none,
}

level_coin_rules: dict[str, LevelRule] = {
    **level_coin_rule_forest,
    **level_coin_rule_tree,
    **level_coin_rule_circus,
    **level_coin_rule_funhouse,
    **level_coin_rule_harbour,
    **level_coin_rule_mountain
}
