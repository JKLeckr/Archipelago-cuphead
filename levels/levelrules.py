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
def lrule_and(*rules: LevelRule) -> LevelRule:
    return lambda s: lambda state, player: all(p(p(rule)(s)(state, player)) for rule in rules)
def lrule_or(*rules: LevelRule) -> LevelRule:
    return lambda s: lambda state, player: any(p(p(rule)(s)(state, player)) for rule in rules)
def lrule_not(rule: LevelRule) -> LevelRule:
    return lambda s: lambda state, player: not rule(s)(state, player)

def lrule_none(wconf: WorldConfig) -> RegionRule:
    return rb.rrule_none()
def lrule_false(wconf: WorldConfig) -> RegionRule:
    return rb.rrule_false()

def lrule_plane_gun(wconf: WorldConfig) -> RegionRule:
    return rb.rrule_has(ItemNames.item_plane_gun)
def lrule_plane_bombs(wconf: WorldConfig) -> RegionRule:
    return rb.rrule_has(ItemNames.item_plane_bombs)
def lrule_plane(wconf: WorldConfig) -> RegionRule:
    if wconf.hard_logic:
        return lrule_or(lrule_plane_gun, lrule_plane_bombs)(wconf)
    else:
        return lrule_plane_gun(wconf)

def lrule_duck(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    return rb.rrule_has(ItemNames.item_ability_duck)
def lrule_dash(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    return rb.rrule_has(ItemNames.item_ability_dash)
def lrule_duck_or_dash(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    return lrule_or(lrule_duck, lrule_dash)(wconf)
def lrule_duck_and_dash(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    return lrule_and(lrule_duck, lrule_dash)(wconf)
def lrule_parry(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    if wconf.dlc_chalice == ChaliceMode.CHALICE_ONLY:
        return rb.rrule_and(
            rb.rrule_has(ItemNames.item_ability_parry),
            rb.rrule_has(ItemNames.item_ability_dash)
        )
    return rb.rrule_has(ItemNames.item_ability_parry)
def lrule_psugar(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    return rb.rrule_has(ItemNames.item_charm_psugar)
def lrule_parry_or_psugar(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    return lrule_or(lrule_parry, lrule_psugar)(wconf)
def lrule_dash_or_parry(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    return lrule_or(lrule_dash, lrule_parry)(wconf)
def lrule_dash_parry_or_psugar(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    return lrule_or(lrule_dash, lrule_or(lrule_parry, lrule_psugar))(wconf)
def lrule_dash_and_parry(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    return lrule_and(lrule_dash, lrule_parry)(wconf)
def lrule_duck_and_parry(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    return lrule_and(lrule_duck, lrule_parry)(wconf)
def lrule_duck_dash_and_parry(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    return lrule_and(lrule_duck, lrule_dash_and_parry)(wconf)
def lrule_plane_parry(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    return rb.rrule_has(ItemNames.item_ability_plane_parry)
def lrule_plane_shrink(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    return rb.rrule_has(ItemNames.item_ability_plane_shrink)

def lrule_bird(wconf: WorldConfig):
    if wconf.hard_logic:
        return lrule_plane_gun(wconf)
    else:
        return lrule_and(lrule_plane_gun, lrule_plane_bombs)(wconf)
def lrule_funhouse(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    if wconf.dlc_chalice == ChaliceMode.CHALICE_ONLY:
        return lrule_parry(wconf)
    return lrule_or(lrule_parry, lrule_and(lrule_psugar, lrule_dash))(wconf)
def lrule_mouse(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    if wconf.dlc_chalice == ChaliceMode.CHALICE_ONLY:
        return lrule_and(lrule_parry, lrule_duck)(wconf)
    return lrule_and(lrule_parry_or_psugar, lrule_duck)(wconf)
def lrule_pirate(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    if wconf.dlc_chalice == ChaliceMode.CHALICE_ONLY:
        return lrule_duck(wconf)
    return lrule_or(lrule_duck, lrule_and(lrule_parry, lrule_dash))(wconf)
def lrule_robot(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_plane(wconf)
    return lrule_and(lrule_plane, lrule_plane_parry)(wconf)
def lrule_sallystageplay_secret(wconf: WorldConfig) -> RegionRule:
    if wconf.dlc_chalice == ChaliceMode.CHALICE_ONLY:
        return lrule_and(lrule_parry, lrule_dlc_doublejump)(wconf)
    return lrule_parry(wconf)
def lrule_harbour(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    return lrule_and(lrule_dash, lrule_parry)(wconf)
def lrule_kingdice(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_plane(wconf)
    return lrule_and(lrule_plane, lrule_and(lrule_parry, lrule_dash))(wconf)
def lrule_final(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    if wconf.dlc_chalice == ChaliceMode.CHALICE_ONLY:
        return lrule_parry(wconf)
    return lrule_and(lrule_parry, lrule_dash)(wconf)

def lrule_weapon_ex(wconf: WorldConfig) -> RegionRule:
    if (wconf.weapon_mode & WeaponMode.PROGRESSIVE) > 0:
        _rule = rb.rrule_has_any_count(
            {x: 2 for x in weapons.weapon_p_dict.values()}
        )
    elif (wconf.weapon_mode & WeaponMode.EX_SEPARATE) > 0:
        _rule = rb.rrule_has_any(
            {x for x in weapons.weapon_ex_dict.values()}
        )
    else:
        _rule = rb.rrule_none()
    return _rule

def lrule_topgrade(wconf: WorldConfig) -> RegionRule:
    _rule = rb.rrule_none()
    if wconf.randomize_abilities:
        _rule = rb.rrule_has(ItemNames.item_ability_parry)
        if wconf.dlc_chalice == ChaliceMode.CHALICE_ONLY:
            _rule = rb.rrule_and(_rule, rb.rrule_has(ItemNames.item_ability_dash))
    if (wconf.weapon_mode & (WeaponMode.PROGRESSIVE | WeaponMode.EX_SEPARATE)) > 0:
        _rule = rb.rrule_and(
            _rule,
            rb.rrule_or(rb.rrule_has_group("Super"), lrule_weapon_ex(wconf))
        )
    return _rule
def lrule_plane_topgrade(wconf: WorldConfig) -> RegionRule:
    _rule = rb.rrule_none()
    if wconf.randomize_abilities:
        _rule = rb.rrule_has(ItemNames.item_ability_plane_parry)
    if (wconf.weapon_mode & (WeaponMode.PROGRESSIVE | WeaponMode.EX_SEPARATE)) > 0:
        _rule = rb.rrule_and(_rule, rb.rrule_has_any({
            ItemNames.item_plane_ex,
            ItemNames.item_plane_super,
            ItemNames.item_dlc_cplane_ex,
            ItemNames.item_dlc_cplane_super,
        }))
    return _rule
def lrule_rungun_topgrade(wconf: WorldConfig) -> RegionRule:
    _rule = rb.rrule_none()
    if wconf.randomize_abilities:
        _rule = rb.rrule_has(ItemNames.item_ability_parry)
        if wconf.dlc_chalice == ChaliceMode.CHALICE_ONLY:
            _rule = rb.rrule_and(_rule, rb.rrule_has(ItemNames.item_ability_dash))
    return _rule

def lrule_dlc_cookie(wconf: WorldConfig) -> RegionRule:
    if wconf.dlc_chalice <= ChaliceMode.START or wconf.dlc_chalice == ChaliceMode.CHALICE_ONLY:
        return lrule_none(wconf)
    return rb.rrule_has(ItemNames.item_charm_dlc_cookie)
def lrule_dlc_doublejump(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    return rb.rrule_has(ItemNames.item_ability_dlc_cdoublejump)
def lrule_dash_or_dlc_doublejump(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    _rule = lrule_dash
    if wconf.use_dlc and wconf.dlc_chalice > 0:
        _rule = lrule_or(_rule, lrule_dlc_doublejump)
    return _rule(wconf)
def lrule_dlc_tutorial_coin(wconf: WorldConfig) -> RegionRule:
    return lrule_and(lrule_dash_and_parry, lrule_dlc_doublejump)(wconf)
def lrule_dlc_oldman(wconf: WorldConfig) -> RegionRule:
    if not wconf.randomize_abilities:
        return lrule_none(wconf)
    return lrule_and(lrule_parry_or_psugar, lrule_dash)(wconf)

def lrule_dlc_boss_chaliced(wconf: WorldConfig) -> RegionRule:
    _rule = lrule_dlc_cookie
    if (wconf.dlc_boss_chalice_checks & ChaliceCheckMode.GRADE_REQUIRED) > 0:
        _rule = lrule_and(_rule, lrule_topgrade)
        if (wconf.dlc_chalice != ChaliceMode.CHALICE_ONLY):
            _rule = lrule_and(_rule, lrule_dash)
    return _rule(wconf)
def lrule_dlc_boss_plane_chaliced(wconf: WorldConfig) -> RegionRule:
    _rule = lrule_dlc_cookie
    if (wconf.dlc_boss_chalice_checks & ChaliceCheckMode.GRADE_REQUIRED) > 0:
        _rule = lrule_and(_rule, lrule_plane_topgrade)
    return _rule(wconf)
def lrule_dlc_boss_chaliced_parry(wconf: WorldConfig) -> RegionRule:
    _rule = lrule_dlc_boss_chaliced
    if (wconf.dlc_boss_chalice_checks & ChaliceCheckMode.GRADE_REQUIRED) == 0:
        _rule = lrule_and(_rule, lrule_dash)
    return _rule(wconf)
def lrule_dlc_rungun_chaliced(wconf: WorldConfig) -> RegionRule:
    _rule = lrule_dlc_cookie
    if (wconf.dlc_rungun_chalice_checks & ChaliceCheckMode.GRADE_REQUIRED) > 0:
        _rule = lrule_and(_rule, lrule_rungun_topgrade)
        if (wconf.dlc_chalice != ChaliceMode.CHALICE_ONLY):
            _rule = lrule_and(_rule, lrule_dash)
    return _rule(wconf)
def lrule_dlc_rungun_chaliced_parry(wconf: WorldConfig) -> RegionRule:
    _rule = lrule_dlc_rungun_chaliced
    if (wconf.dlc_boss_chalice_checks & ChaliceCheckMode.GRADE_REQUIRED) == 0:
        _rule = lrule_and(_rule, lrule_dash)
    return _rule(wconf)

def lrule_dlc_relic(wconf: WorldConfig) -> RegionRule:
    return rb.rrule_has(ItemNames.item_charm_dlc_broken_relic, 1)
