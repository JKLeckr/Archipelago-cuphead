### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from rule_builder.rules import Filtered, Has, HasAll, HasAny, HasGroup

from ...names import itemnames as i
from ..dep import deps
from ..dep.depfilter import DepFilter
from ..rb.rbbase import PresetData
from ..rb.rbrules import HasAnyWeapon, HasAnyWeaponEx, Preset

LrpPlane = PresetData(
    Has(i.item_plane_gun, options=[DepFilter(deps.dep_hard_logic, value=False)]) &
    HasAny(i.item_plane_gun, i.item_plane_bombs, options=[DepFilter(deps.dep_hard_logic)]),
    "Plane"
)

LrpDuck = PresetData(
    Has(i.item_ability_duck, options=[DepFilter(deps.dep_rando_abilities)]),
    "Duck"
)

LrpDash = PresetData(
    Has(i.item_ability_dash, options=[DepFilter(deps.dep_rando_abilities)]),
    "Dash"
)

LrpParry = PresetData(
    Has(
        i.item_ability_parry,
        options=[
            DepFilter(deps.dep_rando_abilities),
            DepFilter(deps.dep_dlc_chalice_only, value=False)
        ]
    ) &
    HasAll(
        i.item_ability_parry,
        i.item_ability_dash,
        options=[
            DepFilter(deps.dep_rando_abilities),
            DepFilter(deps.dep_dlc_chalice_only)
        ]
    ),
    "Parry"
)

LrpPlaneParry = PresetData(
    Has(i.item_ability_plane_parry, options=[DepFilter(deps.dep_rando_abilities)]),
    "Plane Parry"
)

LrpPlaneShrink = PresetData(
    Has(i.item_ability_plane_shrink, options=[DepFilter(deps.dep_rando_abilities)]),
    "Plane Shrink"
)

LrpDuckOrDash = PresetData(
    HasAny(
        i.item_ability_duck,
        i.item_ability_dash,
        options=[DepFilter(deps.dep_rando_abilities)]
    ),
    "Duck or Dash"
)

LrpDuckAndDash = PresetData(
    HasAll(
        i.item_ability_duck,
        i.item_ability_dash,
        options=[DepFilter(deps.dep_rando_abilities)]
    ),
    "Duck and Dash"
)

LrpParryOrPSugar = PresetData(
    HasAny(
        i.item_ability_parry,
        i.item_charm_psugar,
        options=[
            DepFilter(deps.dep_rando_abilities),
            DepFilter(deps.dep_dlc_chalice_only, value=False)
        ]
    ) &
    HasAll(
        i.item_ability_parry,
        i.item_ability_dash,
        options=[
            DepFilter(deps.dep_rando_abilities),
            DepFilter(deps.dep_dlc_chalice_only)
        ]
    ),
    "Parry or P. Sugar"
)

LrpDashOrParry = PresetData(
    HasAny(
        i.item_ability_dash,
        i.item_ability_parry,
        options=[
            DepFilter(deps.dep_rando_abilities),
            DepFilter(deps.dep_dlc_chalice_only, value=False)
        ]
    ) &
    Has(
        i.item_ability_dash,
        options=[
            DepFilter(deps.dep_rando_abilities),
            DepFilter(deps.dep_dlc_chalice_only)
        ]
    ),
    "Dash or Parry"
)

LrpDashAndParry = PresetData(
    HasAll(
        i.item_ability_dash,
        i.item_ability_parry,
        options=[DepFilter(deps.dep_rando_abilities)]
    ),
    "Dash and Parry"
)

LrpDashParryOrPSugar = PresetData(
    HasAny(
        i.item_ability_dash,
        i.item_ability_parry,
        i.item_charm_psugar,
        options=[
            DepFilter(deps.dep_rando_abilities),
            DepFilter(deps.dep_dlc_chalice_only, value=False)
        ]
    ) &
    Has(
        i.item_ability_dash,
        options=[
            DepFilter(deps.dep_rando_abilities),
            DepFilter(deps.dep_dlc_chalice_only)
        ]
    ),
    "Dash, Parry, or P. Sugar"
)

LrpDuckAndParry = PresetData(
    HasAll(
        i.item_ability_duck,
        i.item_ability_parry,
        options=[DepFilter(deps.dep_rando_abilities)]
    ) &
    Has(
        i.item_ability_dash,
        options=[
            DepFilter(deps.dep_rando_abilities),
            DepFilter(deps.dep_dlc_chalice_only)
        ]
    ),
    "Duck and Parry"
)

LrpDuckDashAndParry = PresetData(
    HasAll(
        i.item_ability_duck,
        i.item_ability_dash,
        i.item_ability_parry,
        options=[DepFilter(deps.dep_rando_abilities)]
    ),
    "Duck, Dash and Parry"
)

LrpAnySuper = PresetData(
    HasGroup(i.item_group_super, 1),
    "Any Super"
)

LrpWeaponEx = PresetData(
    HasAnyWeaponEx(options=[DepFilter(deps.dep_weapon_ex_rando)]),
    "Weapon EX"
)

LrpTopgrade = PresetData(
    Preset(LrpParry) &
    Filtered(
        Preset(LrpAnySuper) | Preset(LrpWeaponEx),
        options=[DepFilter(deps.dep_weapon_ex_rando)]
    ),
    "Topgrade"
)

LrpPlaneTopgrade = PresetData(
    Preset(LrpPlaneParry) &
    HasAny(
        i.item_plane_ex,
        i.item_plane_super,
        i.item_dlc_cplane_ex,
        i.item_dlc_cplane_super,
        options=[DepFilter(deps.dep_weapon_ex_rando)]
    ),
    "Plane Topgrade"
)

LrpRungunTopgrade = PresetData(
    Preset(LrpParry),
    "Run n Gun Topgrade"
)

LrpWeapon = PresetData(
    Filtered(
        HasAnyWeapon() |
        Filtered(
            HasAnyWeaponEx() & Has(i.item_charm_coffee),
            options=[
                DepFilter(deps.dep_hard_logic),
                DepFilter(deps.dep_weapon_ex_separate)
            ],
        ) |
        Filtered(
            Preset(LrpParry) & Has(i.item_charm_whetstone),
            options=[DepFilter(deps.dep_hard_logic)],
        ), #|
        ## Or if we want to make things more difficult, go even more lax.
        #(HasGroup(i.item_group_super) & Has(i.item_charm_coffee)),
        options=[DepFilter(deps.dep_no_start_weapon)]
    ),
    "Weapon"
)

LrpRungunWeapon = PresetData(
    Filtered(
        HasAnyWeapon() |
        Filtered(
            HasAnyWeaponEx() | Has(i.item_charm_coffee),
            options=[DepFilter(deps.dep_weapon_ex_separate)]
        ) |
        (Preset(LrpParry) & Has(i.item_charm_whetstone)), #|
        #(HasGroup(i.item_group_super) & Has(i.item_charm_coffee))
        options=[DepFilter(deps.dep_no_start_weapon), DepFilter(deps.dep_hard_logic, False)]
    ),
    "Run n Gun Weapon",
)

LrpDlcCookie = PresetData(
    Filtered(
        Has(i.item_charm_dlc_cookie, options=[DepFilter(deps.dep_dlc_cookie)]),
        options=[DepFilter(deps.dep_dlc_chalice, value=False)],
        filtered_resolution=False
    ),
    "DLC Cookie"
)

LrpDlcDoublejump = PresetData(
    Filtered(
        Preset(LrpDlcCookie) &
        Has(i.item_ability_dlc_cdoublejump, options=[DepFilter(deps.dep_rando_abilities)]),
        options=[DepFilter(deps.dep_dlc_chalice, value=False)],
        filtered_resolution=False
    ),
    "DLC Double Jump"
)

LrpDashOrDlcDoublejump = PresetData(
    Has(
        i.item_ability_dash,
        options=[DepFilter(deps.dep_dlc_chalice, value=False), DepFilter(deps.dep_rando_abilities)]
    ) &
    HasAll(
        i.item_ability_dash,
        i.item_ability_dlc_cdoublejump,
        options=[DepFilter(deps.dep_dlc_chalice), DepFilter(deps.dep_rando_abilities)]
    ),
    "Dash or DLC Double Jump"
)

LrpDlcBossChaliced = PresetData(
    Preset(LrpDlcCookie) &
    Preset(
        LrpTopgrade,
        options=[DepFilter(deps.dep_dlc_chaliced_grade_required)]
    ) &
    Preset(
        LrpDash,
        options=[
            DepFilter(deps.dep_dlc_chaliced_grade_required),
            DepFilter(deps.dep_dlc_chalice_only, value=False)
        ]
    ),
    "DLC Boss Chaliced"
)

LrpDlcBossPlaneChaliced = PresetData(
    Preset(LrpDlcCookie) &
    Preset(
        LrpPlaneTopgrade,
        options=[DepFilter(deps.dep_dlc_chaliced_grade_required)]
    ),
    "DLC Boss Plane Chaliced"
)

LrpDlcBossChalicedParry = PresetData(
    Preset(LrpDlcBossChaliced) &
    Preset(
        LrpDashAndParry,
        options=[DepFilter(deps.dep_dlc_chaliced_grade_required,value=False)]
    ),
    "DLC Boss Chaliced Parry"
)

LrpDlcRungunChaliced = PresetData(
    Preset(LrpDlcCookie) &
    Preset(LrpRungunTopgrade, options=[DepFilter(deps.dep_dlc_rungun_chaliced_grade_required)]) &
    Preset(
        LrpDash,
        options=[
            DepFilter(deps.dep_dlc_rungun_chaliced_grade_required),
            DepFilter(deps.dep_dlc_chalice_only, value=False)
        ]
    ),
    "DLC Run n Gun Chaliced"
)

LrpDlcRungunChalicedParry = PresetData(
    Preset(LrpDlcRungunChaliced) &
    Preset(LrpDash, options=[DepFilter(deps.dep_dlc_chaliced_grade_required, value=False)]),
    "DLC Run n Gun Chaliced Parry"
)

LrpDlcRelic = PresetData(
    Has(i.item_charm_dlc_broken_relic),
    "DLC Relic"
)
