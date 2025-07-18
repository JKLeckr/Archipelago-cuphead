from __future__ import annotations
from collections.abc import Callable
from ..names import ItemNames
from ..wconf import WorldConfig
from ..enums import WeaponMode, ChaliceMode, ChaliceCheckMode
from ..items import weapons
from ..rules import rulebase as rb
from ..debug import p
from ..rules.rulebase import RegionRule

LevelRule = Callable[[WorldConfig], RegionRule]

# Level Rules
def level_rule_and(*rules: LevelRule) -> LevelRule:
    return lambda s: lambda state, player: all(p(p(rule)(s)(state, player)) for rule in rules)
def level_rule_or(*rules: LevelRule) -> LevelRule:
    return lambda s: lambda state, player: any(p(p(rule)(s)(state, player)) for rule in rules)
def level_rule_not(rule: LevelRule) -> LevelRule:
    return lambda s: lambda state, player: not rule(s)(state, player)

def level_rule_none(wconf: WorldConfig) -> RegionRule:
    return rb.region_rule_none()

def level_rule_plane_gun(wconf: WorldConfig) -> RegionRule:
    return rb.region_rule_has(ItemNames.item_plane_gun)
def level_rule_plane_bombs(wconf: WorldConfig) -> RegionRule:
    return rb.region_rule_has(ItemNames.item_plane_bombs)
def level_rule_plane(wconf: WorldConfig) -> RegionRule:
    if wconf.hard_logic:
        return level_rule_or(level_rule_plane_gun, level_rule_plane_bombs)(wconf)
    else:
        return level_rule_plane_gun(wconf)

def level_rule_duck(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return rb.region_rule_has(ItemNames.item_ability_duck)
def level_rule_dash(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return rb.region_rule_has(ItemNames.item_ability_dash)
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
    if wconf.dlc_chalice == ChaliceMode.CHALICE_ONLY:
        return rb.region_rule_and(
            rb.region_rule_has(ItemNames.item_ability_parry),
            rb.region_rule_has(ItemNames.item_ability_dash)
        )
    return rb.region_rule_has(ItemNames.item_ability_parry)
def level_rule_psugar(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return rb.region_rule_has(ItemNames.item_charm_psugar)
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
    return level_rule_and(level_rule_duck, level_rule_parry)(wconf)
def level_rule_duck_dash_and_parry(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return level_rule_and(level_rule_duck, level_rule_dash_and_parry)(wconf)
def level_rule_plane_parry(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return rb.region_rule_has(ItemNames.item_ability_plane_parry)
def level_rule_plane_shrink(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return rb.region_rule_has(ItemNames.item_ability_plane_shrink)

def level_rule_bird(wconf: WorldConfig):
    if wconf.hard_logic:
        return level_rule_plane_gun(wconf)
    else:
        return level_rule_and(level_rule_plane_gun, level_rule_plane_bombs)(wconf)
def level_rule_funhouse(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    if wconf.dlc_chalice == ChaliceMode.CHALICE_ONLY:
        return level_rule_parry(wconf)
    return level_rule_or(level_rule_parry, level_rule_and(level_rule_psugar, level_rule_dash))(wconf)
def level_rule_mouse(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    if wconf.dlc_chalice == ChaliceMode.CHALICE_ONLY:
        return level_rule_and(level_rule_parry, level_rule_duck)(wconf)
    return level_rule_and(level_rule_parry_or_psugar, level_rule_duck)(wconf)
def level_rule_pirate(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    if wconf.dlc_chalice == ChaliceMode.CHALICE_ONLY:
        return level_rule_duck(wconf)
    return level_rule_or(level_rule_duck, level_rule_and(level_rule_parry, level_rule_dash))(wconf)
def level_rule_robot(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_plane(wconf)
    return level_rule_and(level_rule_plane, level_rule_plane_parry)(wconf)
def level_rule_sallystageplay_secret(wconf: WorldConfig) -> RegionRule:
    if wconf.dlc_chalice == ChaliceMode.CHALICE_ONLY:
        return level_rule_and(level_rule_parry, level_rule_dlc_doublejump)(wconf)
    return level_rule_parry(wconf)
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
    if wconf.dlc_chalice == ChaliceMode.CHALICE_ONLY:
        return level_rule_parry(wconf)
    return level_rule_and(level_rule_parry, level_rule_dash)(wconf)

def level_rule_weapon_ex(wconf: WorldConfig) -> RegionRule:
    if (wconf.weapon_mode & WeaponMode.PROGRESSIVE) > 0:
        _rule = rb.region_rule_has_any_count(
            {x: 2 for x in weapons.weapon_p_dict.values()}
        )
    elif (wconf.weapon_mode & WeaponMode.EX_SEPARATE) > 0:
        _rule = rb.region_rule_has_any(
            {x for x in weapons.weapon_ex_dict.values()}
        )
    else:
        _rule = rb.region_rule_none()
    return _rule

def level_rule_topgrade(wconf: WorldConfig) -> RegionRule:
    _rule = rb.region_rule_none()
    if wconf.randomize_abilities:
        _rule = rb.region_rule_has(ItemNames.item_ability_parry)
        if wconf.dlc_chalice == ChaliceMode.CHALICE_ONLY:
            _rule = rb.region_rule_and(_rule, rb.region_rule_has(ItemNames.item_ability_dash))
    if (wconf.weapon_mode & (WeaponMode.PROGRESSIVE | WeaponMode.EX_SEPARATE)) > 0:
        _rule = rb.region_rule_and(
            _rule,
            rb.region_rule_or(rb.region_rule_has("Super"), level_rule_weapon_ex(wconf))
        )
    return _rule
def level_rule_plane_topgrade(wconf: WorldConfig) -> RegionRule:
    _rule = rb.region_rule_none()
    if wconf.randomize_abilities:
        _rule = rb.region_rule_has(ItemNames.item_ability_plane_parry)
    if (wconf.weapon_mode & WeaponMode.PROGRESSIVE | WeaponMode.EX_SEPARATE) > 0:
        _rule = rb.region_rule_and(_rule, rb.region_rule_has_any({
                ItemNames.item_plane_ex,
                ItemNames.item_plane_super,
                ItemNames.item_dlc_cplane_ex,
                ItemNames.item_dlc_cplane_super,
        }))
    return _rule
def level_rule_rungun_topgrade(wconf: WorldConfig) -> RegionRule:
    _rule = rb.region_rule_none()
    if wconf.randomize_abilities:
        _rule = rb.region_rule_has(ItemNames.item_ability_parry)
        if wconf.dlc_chalice == ChaliceMode.CHALICE_ONLY:
            _rule = rb.region_rule_and(_rule, rb.region_rule_has(ItemNames.item_ability_dash))
    return _rule

def level_rule_dlc_cookie(wconf: WorldConfig) -> RegionRule:
    if wconf.dlc_chalice <= ChaliceMode.START or wconf.dlc_chalice == ChaliceMode.CHALICE_ONLY:
        return level_rule_none(wconf)
    return rb.region_rule_has(ItemNames.item_charm_dlc_cookie)
def level_rule_dlc_doublejump(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return rb.region_rule_has(ItemNames.item_ability_dlc_cdoublejump)
def level_rule_dlc_tutorial_coin(wconf: WorldConfig) -> RegionRule:
    return level_rule_and(level_rule_dash_and_parry, level_rule_dlc_doublejump)(wconf)
def level_rule_dlc_oldman(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return level_rule_none(wconf)
    return level_rule_and(level_rule_parry_or_psugar, level_rule_dash)(wconf)

def level_rule_dlc_boss_chaliced(wconf: WorldConfig) -> RegionRule:
    _rule = level_rule_dlc_cookie
    if (wconf.dlc_boss_chalice_checks & ChaliceCheckMode.GRADE_REQUIRED) > 0:
        _rule = level_rule_and(_rule, level_rule_topgrade)
        if (wconf.dlc_chalice != ChaliceMode.CHALICE_ONLY):
            _rule = level_rule_and(_rule, level_rule_dash)
    return _rule(wconf)
def level_rule_dlc_boss_plane_chaliced(wconf: WorldConfig) -> RegionRule:
    _rule = level_rule_dlc_cookie
    if (wconf.dlc_boss_chalice_checks & ChaliceCheckMode.GRADE_REQUIRED) > 0:
        _rule = level_rule_and(_rule, level_rule_plane_topgrade)
    return _rule(wconf)
def level_rule_dlc_boss_chaliced_parry(wconf: WorldConfig) -> RegionRule:
    _rule = level_rule_dlc_boss_chaliced
    if (wconf.dlc_boss_chalice_checks & ChaliceCheckMode.GRADE_REQUIRED) == 0:
        _rule = level_rule_and(_rule, level_rule_dash)
    return _rule(wconf)
def level_rule_dlc_rungun_chaliced(wconf: WorldConfig) -> RegionRule:
    _rule = level_rule_dlc_cookie
    if (wconf.dlc_rungun_chalice_checks & ChaliceCheckMode.GRADE_REQUIRED) > 0:
        _rule = level_rule_and(_rule, level_rule_rungun_topgrade)
        if (wconf.dlc_chalice != ChaliceMode.CHALICE_ONLY):
            _rule = level_rule_and(_rule, level_rule_dash)
    return _rule(wconf)
def level_rule_dlc_rungun_chaliced_parry(wconf: WorldConfig) -> RegionRule:
    _rule = level_rule_dlc_rungun_chaliced
    if (wconf.dlc_boss_chalice_checks & ChaliceCheckMode.GRADE_REQUIRED) == 0:
        _rule = level_rule_and(_rule, level_rule_dash)
    return _rule(wconf)

def level_rule_dlc_relic(wconf: WorldConfig) -> RegionRule:
    return rb.region_rule_has(ItemNames.item_charm_dlc_broken_relic, 1)
