### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from rule_builder.rules import Filtered

from ...names import regionnames as lv
from ..dep import deps
from ..dep.depfilter import DepFilter
from ..rb.rbrules import Preset
from .levelrulepresets import (
    LrpDash,
    LrpDashAndParry,
    LrpDlcBossChaliced,
    LrpDlcCookie,
    LrpDlcDoublejump,
    LrpDuck,
    LrpDuckOrDash,
    LrpParry,
)

LrdBossBaronessChalice = Preset(
    LrpDlcDoublejump, #&
    ## Maybe need duck?
    #Filtered(LrpDuck, options=[DepFilter(deps.dep_hard_logic)]),
    lv.level_boss_baroness + " Chalice"
)

LrdBossPirateChalice = Preset(
    LrpDuck |
    (LrpDashAndParry & LrpDlcDoublejump),
    lv.level_boss_pirate + " Chalice",
    options=[
        DepFilter(deps.dep_rando_abilities)
    ]
)

LrdBossSallyStagePlaySecret = Preset(
    LrpParry &
    Filtered(
        LrpDlcDoublejump,
        options=[DepFilter(deps.dep_dlc_chalice_only)],
        filtered_resolution=True
    ),
    lv.level_boss_sallystageplay + " Secret"
)

LrdDlcBossRumRunnersEarlyPhase = Preset(
    LrpDuck &
    Filtered(
        LrpDlcDoublejump,
        options=[DepFilter(deps.dep_dlc_chalice_only)],
        filtered_resolution=True
    ),
    lv.level_dlc_boss_rumrunners + " Secret"
)

LrdDlcBossSnowcultChaliced = Preset(
    LrpDlcBossChaliced &
    Filtered(
        LrpDlcDoublejump,
        options=[DepFilter(deps.dep_hard_logic, False)],
        filtered_resolution=True
    ),
    lv.level_dlc_boss_snowcult + " Chaliced"
)

LrdDlcBossAirplaneChaliced = Preset(
    LrpDlcCookie &
    Filtered(
        LrpDuckOrDash,
        options=[DepFilter(deps.dep_hard_logic, False)],
        filtered_resolution=True
    ) &
    Filtered(
        LrpDuck |
        (LrpDash & LrpDlcDoublejump),
        options=[DepFilter(deps.dep_hard_logic, False)]
    ),
    lv.level_dlc_boss_airplane + " Chaliced"
)
