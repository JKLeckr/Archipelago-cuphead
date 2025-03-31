from __future__ import annotations
from typing import Callable
from .names import ItemNames
from .wsettings import WorldSettings
from .rulebase import RegionRule, region_rule_none, region_rule_has

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
def level_rule_duck(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return region_rule_has(ItemNames.item_ability_duck)
def level_rule_dash(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return region_rule_has(ItemNames.item_ability_dash)
def level_rule_duck_or_dash(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return level_rule_or(level_rule_duck, level_rule_dash)(settings)
def level_rule_duck_and_dash(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return level_rule_and(level_rule_duck, level_rule_dash)(settings)
def level_rule_parry(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return region_rule_has(ItemNames.item_ability_parry)
def level_rule_psugar(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return region_rule_has(ItemNames.item_charm_psugar)
def level_rule_parry_or_psugar(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return level_rule_or(level_rule_parry, level_rule_psugar)(settings)
def level_rule_dash_or_parry(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return level_rule_or(level_rule_dash, level_rule_parry)(settings)
def level_rule_dash_parry_or_psugar(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return level_rule_or(level_rule_dash, level_rule_or(level_rule_parry, level_rule_psugar))(settings)
def level_rule_dash_and_parry(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return level_rule_and(level_rule_dash, level_rule_parry)(settings)
def level_rule_duck_and_parry(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return level_rule_and(level_rule_dash, level_rule_parry)(settings)
def level_rule_duck_dash_and_parry(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return level_rule_and(level_rule_duck, level_rule_dash_and_parry)(settings)
def level_rule_plane_parry(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return region_rule_has(ItemNames.item_ability_plane_parry)
def level_rule_bird(settings: WorldSettings):
    if settings.hard_logic:
        return level_rule_plane_gun(settings)
    else:
        return level_rule_and(level_rule_plane_gun, level_rule_plane_bombs)(settings)
def level_rule_funhouse(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return level_rule_or(level_rule_parry, level_rule_and(level_rule_psugar, level_rule_dash))(settings)
def level_rule_pirate(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return level_rule_or(level_rule_duck, level_rule_and(level_rule_parry, level_rule_dash))(settings)
def level_rule_robot(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_plane(settings)
    return level_rule_and(level_rule_plane, level_rule_plane_parry)(settings)
def level_rule_harbour(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return level_rule_and(level_rule_dash, level_rule_parry)(settings)
def level_rule_kingdice(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_plane(settings)
    return level_rule_and(level_rule_plane, level_rule_and(level_rule_parry, level_rule_dash))(settings)
def level_rule_final(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return level_rule_and(level_rule_parry, level_rule_dash)(settings)
def level_rule_dlc_oldman(settings: WorldSettings) -> RegionRule:
    if not settings.randomize_abilities:
        return level_rule_none(settings)
    return level_rule_and(level_rule_parry_or_psugar, level_rule_dash)(settings)
def level_rule_dlc_relic(settings: WorldSettings) -> RegionRule:
    return region_rule_has(ItemNames.item_charm_dlc_broken_relic, 1)
