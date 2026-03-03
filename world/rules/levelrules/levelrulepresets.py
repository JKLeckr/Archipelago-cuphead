### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from rule_builder.rules import False_, Has, HasAll, HasAny, HasGroup

from ...names import itemnames as i
from ..dep import deps
from ..dep.depfilter import DepFilter
from . import levelruleselectors as lrs
from .levelrulebase import And, Or, RBRule, RuleList, RulePreset, SelectRule, lrpreset


@lrpreset
def lrp_plane() -> RuleList:
    return RuleList([
        RBRule(
            Has(i.item_plane_gun, options=[DepFilter(deps.dep_hard_logic, value=False)])
        ),
        RBRule(
            HasAny(i.item_plane_gun, i.item_plane_bombs, options=[DepFilter(deps.dep_hard_logic)])
        )
    ])


@lrpreset
def lrp_duck() -> RuleList:
    return RuleList([
        RBRule(
            Has(i.item_ability_duck, options=[DepFilter(deps.dep_rando_abilities)])
        )
    ])


@lrpreset
def lrp_dash() -> RuleList:
    return RuleList([
        RBRule(
            Has(i.item_ability_dash, options=[DepFilter(deps.dep_rando_abilities)])
        )
    ])


@lrpreset
def lrp_parry() -> RuleList:
    return RuleList([
        RBRule(
            Has(
                i.item_ability_parry,
                options=[
                    DepFilter(deps.dep_rando_abilities),
                    DepFilter(deps.dep_dlc_chalice_only, value=False)
                ]
            )
        ),
        RBRule(
            HasAll(
                i.item_ability_parry,
                i.item_ability_dash,
                options=[
                    DepFilter(deps.dep_rando_abilities),
                    DepFilter(deps.dep_dlc_chalice_only)
                ]
            )
        )
    ])


@lrpreset
def lrp_plane_parry() -> RuleList:
    return RuleList([
        RBRule(
            Has(i.item_ability_plane_parry, options=[DepFilter(deps.dep_rando_abilities)])
        )
    ])


@lrpreset
def lrp_plane_shrink() -> RuleList:
    return RuleList([
        RBRule(
            Has(i.item_ability_plane_shrink, options=[DepFilter(deps.dep_rando_abilities)])
        )
    ])


@lrpreset
def lrp_duck_or_dash() -> RuleList:
    return RuleList([
        RBRule(
            HasAny(
                i.item_ability_duck,
                i.item_ability_dash,
                options=[DepFilter(deps.dep_rando_abilities)]
            )
        )
    ])


@lrpreset
def lrp_duck_and_dash() -> RuleList:
    return RuleList([
        RBRule(
            HasAll(
                i.item_ability_duck,
                i.item_ability_dash,
                options=[DepFilter(deps.dep_rando_abilities)]
            )
        )
    ])


@lrpreset
def lrp_parry_or_psugar() -> RuleList:
    return RuleList([
        RBRule(
            HasAny(
                i.item_ability_parry,
                i.item_charm_psugar,
                options=[
                    DepFilter(deps.dep_rando_abilities),
                    DepFilter(deps.dep_dlc_chalice_only, value=False)
                ]
            )
        ),
        RBRule(
            HasAll(
                i.item_ability_parry,
                i.item_ability_dash,
                options=[
                    DepFilter(deps.dep_rando_abilities),
                    DepFilter(deps.dep_dlc_chalice_only)
                ]
            )
        )
    ])


@lrpreset
def lrp_dash_or_parry() -> RuleList:
    return RuleList([
        RBRule(
            HasAny(
                i.item_ability_dash,
                i.item_ability_parry,
                options=[
                    DepFilter(deps.dep_rando_abilities),
                    DepFilter(deps.dep_dlc_chalice_only, value=False)
                ]
            )
        ),
        RBRule(
            Has(
                i.item_ability_dash,
                options=[
                    DepFilter(deps.dep_rando_abilities),
                    DepFilter(deps.dep_dlc_chalice_only)
                ]
            )
        )
    ])


@lrpreset
def lrp_dash_and_parry() -> RuleList:
    return RuleList([
        RBRule(
            HasAll(
                i.item_ability_dash,
                i.item_ability_parry,
                options=[DepFilter(deps.dep_rando_abilities)]
            )
        )
    ])


@lrpreset
def lrp_dash_parry_or_psugar() -> RuleList:
    return RuleList([
        RBRule(
            HasAny(
                i.item_ability_dash,
                i.item_ability_parry,
                i.item_charm_psugar,
                options=[
                    DepFilter(deps.dep_rando_abilities),
                    DepFilter(deps.dep_dlc_chalice_only, value=False)
                ]
            )
        ),
        RBRule(
            Has(
                i.item_ability_dash,
                options=[
                    DepFilter(deps.dep_rando_abilities),
                    DepFilter(deps.dep_dlc_chalice_only)
                ]
            )
        )
    ])


@lrpreset
def lrp_duck_and_parry() -> RuleList:
    return RuleList([
        RBRule(
            HasAll(
                i.item_ability_duck,
                i.item_ability_parry,
                options=[DepFilter(deps.dep_rando_abilities)]
            )
        ),
        RBRule(
            Has(
                i.item_ability_dash,
                options=[
                    DepFilter(deps.dep_rando_abilities),
                    DepFilter(deps.dep_dlc_chalice_only)
                ]
            )
        )
    ])


@lrpreset
def lrp_duck_dash_and_parry() -> RuleList:
    return RuleList([
        RBRule(
            HasAll(
                i.item_ability_duck,
                i.item_ability_dash,
                i.item_ability_parry,
                options=[DepFilter(deps.dep_rando_abilities)]
            )
        )
    ])


@lrpreset
def lrp_any_super() -> RuleList:
    return RuleList([
        RBRule(HasGroup("Super", 1))
    ])


@lrpreset
def lrp_weapon_ex() -> RuleList:
    return RuleList([
        SelectRule(lrs.lrs_all_weapon_ex, True, [DepFilter(deps.dep_weapon_ex_rando)])
    ])


@lrpreset
def lrp_topgrade() -> RuleList:
    return RuleList([
        RulePreset(lrp_parry),
        Or(
            RulePreset(lrp_any_super),
            RulePreset(lrp_weapon_ex),
            options=[DepFilter(deps.dep_weapon_ex_rando)]
        )
    ])


@lrpreset
def lrp_plane_topgrade() -> RuleList:
    return RuleList([
        RulePreset(lrp_plane_parry),
        RBRule(
            HasAny(
                i.item_plane_ex,
                i.item_plane_super,
                i.item_dlc_cplane_ex,
                i.item_dlc_cplane_super,
                options=[DepFilter(deps.dep_weapon_ex_rando)]
            )
        )
    ])


@lrpreset
def lrp_rungun_topgrade() -> RuleList:
    return RuleList([
        RulePreset(lrp_parry)
    ])


@lrpreset
def lrp_dlc_cookie() -> RuleList:
    return RuleList([
        RBRule(
            False_(options=[DepFilter(deps.dep_dlc_chalice, value=False)])
        ),
        RBRule(
            Has(i.item_charm_dlc_cookie, options=[DepFilter(deps.dep_dlc_cookie)])
        )
    ])


@lrpreset
def lrp_dlc_doublejump() -> RuleList:
    return RuleList([
        RBRule(
            False_(options=[DepFilter(deps.dep_dlc_chalice, value=False)])
        ),
        And(
            RulePreset(lrp_dlc_cookie),
            RBRule(Has(i.item_ability_dlc_cdoublejump)),
            options=[DepFilter(deps.dep_rando_abilities)]
        )
    ])


@lrpreset
def lrp_dash_or_dlc_doublejump() -> RuleList:
    return RuleList([
        RBRule(
            Has(
                i.item_ability_dash,
                options=[DepFilter(deps.dep_dlc_chalice, value=False), DepFilter(deps.dep_rando_abilities)]
            )
        ),
        RBRule(
            HasAll(
                i.item_ability_dash,
                i.item_ability_dlc_cdoublejump,
                options=[DepFilter(deps.dep_dlc_chalice), DepFilter(deps.dep_rando_abilities)]
            )
        )
    ])


@lrpreset
def lrp_dlc_boss_chaliced() -> RuleList:
    return RuleList([
        RulePreset(lrp_dlc_cookie),
        RulePreset(lrp_topgrade, options=[DepFilter(deps.dep_dlc_chaliced_grade_required)]),
        RulePreset(
            lrp_dash,
            options=[
                DepFilter(deps.dep_dlc_chaliced_grade_required),
                DepFilter(deps.dep_dlc_chalice_only, value=False)
            ]
        )
    ])


@lrpreset
def lrp_dlc_boss_plane_chaliced() -> RuleList:
    return RuleList([
        RulePreset(lrp_dlc_cookie),
        RulePreset(lrp_plane_topgrade, options=[DepFilter(deps.dep_dlc_chaliced_grade_required)])
    ])


@lrpreset
def lrp_dlc_boss_chaliced_parry() -> RuleList:
    return RuleList([
        RulePreset(lrp_dlc_boss_chaliced),
        RulePreset(lrp_dash_and_parry, options=[DepFilter(deps.dep_dlc_chaliced_grade_required, value=False)])
    ])


@lrpreset
def lrp_dlc_rungun_chaliced() -> RuleList:
    return RuleList([
        RulePreset(lrp_dlc_cookie),
        RulePreset(lrp_rungun_topgrade, options=[DepFilter(deps.dep_dlc_rungun_chaliced_grade_required)]),
        RulePreset(
            lrp_dash,
            options=[
                DepFilter(deps.dep_dlc_rungun_chaliced_grade_required),
                DepFilter(deps.dep_dlc_chalice_only, value=False)
            ]
        )
    ])


@lrpreset
def lrp_dlc_rungun_chaliced_parry() -> RuleList:
    return RuleList([
        RulePreset(lrp_dlc_rungun_chaliced),
        RulePreset(lrp_dash, options=[DepFilter(deps.dep_dlc_chaliced_grade_required, value=False)])
    ])


@lrpreset
def lrp_dlc_relic() -> RuleList:
    return RuleList([
        RBRule(
            Has(i.item_charm_dlc_broken_relic)
        )
    ])

