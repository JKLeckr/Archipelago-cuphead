### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from ...names import itemnames as i
from ..dep import deps
from ..dep.depfilter import DepFilter
from ..rb.rbbaserules import Filtered, Has, HasAll, HasAny, HasGroup
from ..rb.rbrules import HasAnyWeaponEx, Preset

LrpPlane = Preset(
    Has(i.item_plane_gun, options=[DepFilter(deps.dep_hard_logic, value=False)]) &
    HasAny(i.item_plane_gun, i.item_plane_bombs, options=[DepFilter(deps.dep_hard_logic)]),
    "Plane"
)

LrpDuck = Preset(
    Has(i.item_ability_duck, options=[DepFilter(deps.dep_rando_abilities)]),
    "Duck"
)

LrpDash = Preset(
    Has(i.item_ability_dash, options=[DepFilter(deps.dep_rando_abilities)]),
    "Dash"
)

LrpParry = Preset(
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

LrpPlaneParry = Preset(
    Has(i.item_ability_plane_parry, options=[DepFilter(deps.dep_rando_abilities)]),
    "Plane Parry"
)

LrpPlaneShrink = Preset(
    Has(i.item_ability_plane_shrink, options=[DepFilter(deps.dep_rando_abilities)]),
    "Plane Shrink"
)

LrpDuckOrDash = Preset(
    HasAny(
        i.item_ability_duck,
        i.item_ability_dash,
        options=[DepFilter(deps.dep_rando_abilities)]
    ),
    "Duck or Dash"
)

LrpDuckAndDash = Preset(
    HasAll(
        i.item_ability_duck,
        i.item_ability_dash,
        options=[DepFilter(deps.dep_rando_abilities)]
    ),
    "Duck and Dash"
)

LrpParryOrPSugar = Preset(
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

LrpDashOrParry = Preset(
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

LrpDashAndParry = Preset(
    HasAll(
        i.item_ability_dash,
        i.item_ability_parry,
        options=[DepFilter(deps.dep_rando_abilities)]
    ),
    "Dash and Parry"
)

LrpDashParryOrPSugar = Preset(
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

LrpDuckAndParry = Preset(
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

LrpDuckDashAndParry = Preset(
    HasAll(
        i.item_ability_duck,
        i.item_ability_dash,
        i.item_ability_parry,
        options=[DepFilter(deps.dep_rando_abilities)]
    ),
    "Duck, Dash and Parry"
)

LrpAnySuper = Preset(
    HasGroup(i.item_group_super, 1),
    "Any Super"
)

LrpWeaponEx = Preset(
    HasAnyWeaponEx(options=[DepFilter(deps.dep_weapon_ex_rando)]),
    "Weapon EX"
)

LrpTopgrade = Preset(
    LrpParry &
    Filtered(
        LrpAnySuper | LrpWeaponEx,
        options=[DepFilter(deps.dep_weapon_ex_rando)]
    ),
    "Topgrade"
)

LrpPlaneTopgrade = Preset(
    LrpPlaneParry &
    HasAny(
        i.item_plane_ex,
        i.item_plane_super,
        i.item_dlc_cplane_ex,
        i.item_dlc_cplane_super,
        options=[DepFilter(deps.dep_weapon_ex_rando)]
    ),
    "Plane Topgrade"
)

LrpRungunTopgrade = Preset(
    LrpParry,
    "Run n Gun Topgrade"
)

LrpWeapon = Preset(
    HasGroup(i.item_group_weapon) |
    Filtered(
        HasAnyWeaponEx() & Has(i.item_charm_coffee),
        options=[
            DepFilter(deps.dep_hard_logic),
            DepFilter(deps.dep_weapon_ex_separate)
        ],
    ) |
    Filtered(
        LrpParry & Has(i.item_charm_whetstone),
        options=[DepFilter(deps.dep_hard_logic)],
    ), #|
    ## Or if we want to make things more difficult, go even more lax.
    #(HasGroup(i.item_group_super) & Has(i.item_charm_coffee)),
    "Weapon",
    options=[DepFilter(deps.dep_no_start_weapon)],
)

LrpRungunWeapon = Preset(
    HasGroup(i.item_group_weapon) |
    Filtered(
        HasAnyWeaponEx() | Has(i.item_charm_coffee),
        options=[DepFilter(deps.dep_weapon_ex_separate)]
    ) |
    (LrpParry & Has(i.item_charm_whetstone)), #|
    #(HasGroup(i.item_group_super) & Has(i.item_charm_coffee))
    "Run n Gun Weapon",
    options=[DepFilter(deps.dep_no_start_weapon), DepFilter(deps.dep_hard_logic, False)],
)

LrpDlcCookie = Preset(
    Has(i.item_charm_dlc_cookie, options=[DepFilter(deps.dep_dlc_cookie)]),
    "DLC Cookie",
    options=[DepFilter(deps.dep_dlc_chalice, value=False)],
    filtered_resolution=False
)

LrpDlcDoublejump = Preset(
    LrpDlcCookie &
    Has(i.item_ability_dlc_cdoublejump, options=[DepFilter(deps.dep_rando_abilities)]),
    "DLC Double Jump",
    options=[DepFilter(deps.dep_dlc_chalice, value=False)],
    filtered_resolution=False
)

LrpDashOrDlcDoublejump = Preset(
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

LrpDlcBossChaliced = Preset(
    LrpDlcCookie &
    Filtered(
        LrpTopgrade,
        options=[DepFilter(deps.dep_dlc_chaliced_grade_required)]
    ) &
    Filtered(
        LrpDash,
        options=[
            DepFilter(deps.dep_dlc_chaliced_grade_required),
            DepFilter(deps.dep_dlc_chalice_only, value=False)
        ]
    ),
    "DLC Boss Chaliced"
)

LrpDlcBossPlaneChaliced = Preset(
    LrpDlcCookie &
    Filtered(
        LrpPlaneTopgrade,
        options=[DepFilter(deps.dep_dlc_chaliced_grade_required)]
    ),
    "DLC Boss Plane Chaliced"
)

LrpDlcBossChalicedParry = Preset(
    LrpDlcBossChaliced &
    Filtered(
        LrpDashAndParry,
        options=[DepFilter(deps.dep_dlc_chaliced_grade_required,value=False)]
    ),
    "DLC Boss Chaliced Parry"
)

LrpDlcRungunChaliced = Preset(
    LrpDlcCookie &
    Filtered(LrpRungunTopgrade, options=[DepFilter(deps.dep_dlc_rungun_chaliced_grade_required)]) &
    Filtered(
        LrpDash,
        options=[
            DepFilter(deps.dep_dlc_rungun_chaliced_grade_required),
            DepFilter(deps.dep_dlc_chalice_only, value=False)
        ]
    ),
    "DLC Run n Gun Chaliced"
)

LrpDlcRungunChalicedParry = Preset(
    LrpDlcRungunChaliced &
    Filtered(LrpDash, options=[DepFilter(deps.dep_dlc_chaliced_grade_required, value=False)]),
    "DLC Run n Gun Chaliced Parry"
)

LrpDlcRelic = Preset(
    Has(i.item_charm_dlc_broken_relic),
    "DLC Relic"
)
