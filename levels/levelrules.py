from __future__ import annotations
from collections.abc import Callable
from ..names import ItemNames
from ..wconf import WorldConfig
from ..enums import ChaliceMode
from ..rules.rulebase import RegionRule, region_rule_none, region_rule_has

LevelRule = Callable[[WorldConfig], RegionRule]

# Level Rules
def level_rule_and(a: LevelRule, b: LevelRule) -> LevelRule:
    return lambda s: lambda state, player: a(s)(state, player) and b(s)(state, player)
def level_rule_not(a: LevelRule) -> LevelRule:
    return lambda s: lambda state, player: not a(s)(state, player)
def level_rule_or(a: LevelRule, b: LevelRule) -> LevelRule:
    return lambda s: lambda state, player: a(s)(state, player) or b(s)(state, player)
def level_rule_none(wconf: WorldConfig) -> RegionRule:
    return region_rule_none()
def level_rule_plane_gun(wconf: WorldConfig) -> RegionRule:
    return region_rule_has(ItemNames.item_plane_gun)
def level_rule_plane_bombs(wconf: WorldConfig) -> RegionRule:
    return region_rule_has(ItemNames.item_plane_bombs)
def level_rule_plane(wconf: WorldConfig) -> RegionRule:
    if wconf.hard_logic:
        return level_rule_or(level_rule_plane_gun, level_rule_plane_bombs)(wconf)
    else:
        return level_rule_plane_gun(wconf)
def level_rule_duck(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return region_rule_has(ItemNames.item_ability_duck)
def level_rule_dash(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return region_rule_has(ItemNames.item_ability_dash)
def level_rule_duck_or_dash(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return level_rule_or(level_rule_duck, level_rule_dash)(wconf)
def level_rule_duck_and_dash(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return level_rule_and(level_rule_duck, level_rule_dash)(wconf)
def level_rule_parry(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return region_rule_has(ItemNames.item_ability_parry)
def level_rule_psugar(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return region_rule_has(ItemNames.item_charm_psugar)
def level_rule_parry_or_psugar(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return level_rule_or(level_rule_parry, level_rule_psugar)(wconf)
def level_rule_dash_or_parry(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return level_rule_or(level_rule_dash, level_rule_parry)(wconf)
def level_rule_dash_parry_or_psugar(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return level_rule_or(level_rule_dash, level_rule_or(level_rule_parry, level_rule_psugar))(wconf)
def level_rule_dash_and_parry(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return level_rule_and(level_rule_dash, level_rule_parry)(wconf)
def level_rule_duck_and_parry(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return level_rule_and(level_rule_dash, level_rule_parry)(wconf)
def level_rule_duck_dash_and_parry(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return level_rule_and(level_rule_duck, level_rule_dash_and_parry)(wconf)
def level_rule_plane_parry(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return region_rule_has(ItemNames.item_ability_plane_parry)
def level_rule_bird(wconf: WorldConfig):
    if wconf.hard_logic:
        return level_rule_plane_gun(wconf)
    else:
        return level_rule_and(level_rule_plane_gun, level_rule_plane_bombs)(wconf)
def level_rule_funhouse(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return level_rule_or(level_rule_parry, level_rule_and(level_rule_psugar, level_rule_dash))(wconf)
def level_rule_pirate(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return level_rule_or(level_rule_duck, level_rule_and(level_rule_parry, level_rule_dash))(wconf)
def level_rule_robot(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_plane(wconf)
    return level_rule_and(level_rule_plane, level_rule_plane_parry)(wconf)
def level_rule_harbour(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return level_rule_and(level_rule_dash, level_rule_parry)(wconf)
def level_rule_kingdice(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_plane(wconf)
    return level_rule_and(level_rule_plane, level_rule_and(level_rule_parry, level_rule_dash))(wconf)
def level_rule_final(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return level_rule_and(level_rule_parry, level_rule_dash)(wconf)
def level_rule_dlc_cookie(wconf: WorldConfig) -> RegionRule:
    if wconf.dlc_chalice <= ChaliceMode.START:
        return level_rule_none(wconf)
    return region_rule_has(ItemNames.item_charm_dlc_cookie)
def level_rule_dlc_doublejump(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return region_rule_has(ItemNames.item_ability_dlc_cdoublejump)
def level_rule_dlc_tutorial_coin(wconf: WorldConfig) -> RegionRule:
    return level_rule_and(level_rule_dash_and_parry, level_rule_dlc_doublejump)(wconf)
def level_rule_dlc_oldman(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return level_rule_and(level_rule_parry_or_psugar, level_rule_dash)(wconf)
def level_rule_dlc_relic(wconf: WorldConfig) -> RegionRule:
    return region_rule_has(ItemNames.item_charm_dlc_broken_relic, 1)
