### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from rule_builder.rules import Filtered

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

LrdBossBaronessChalice = (
    Preset(LrpDlcDoublejump) #&
    ## Maybe need duck?
    #Preset(LrpDuck, options=[DepFilter(deps.dep_hard_logic)])
)

LrdBossPirateChalice = Filtered(
    Preset(LrpDuck) |
    (Preset(LrpDashAndParry) & Preset(LrpDlcDoublejump)),
    options=[DepFilter(deps.dep_rando_abilities)]
)

LrdBossSallyStagePlaySecret = (
    Preset(LrpParry) &
    Preset(
        LrpDlcDoublejump,
        options=[DepFilter(deps.dep_dlc_chalice_only)],
        filtered_resolution=True
    )
)

LrdDlcBossRumRunnersEarlyPhase = (
    Preset(LrpDuck) &
    Preset(
        LrpDlcDoublejump,
        options=[DepFilter(deps.dep_dlc_chalice_only)],
        filtered_resolution=True
    )
)

LrdDlcBossSnowCultChaliced = (
    Preset(LrpDlcBossChaliced) &
    Preset(
        LrpDlcDoublejump,
        options=[DepFilter(deps.dep_hard_logic, False)],
        filtered_resolution=True
    )
)

LrdDlcBossAirplaneChaliced = (
    Preset(LrpDlcCookie) &
    Preset(
        LrpDuckOrDash,
        options=[DepFilter(deps.dep_hard_logic, False)],
        filtered_resolution=True
    ) &
    Filtered(
        Preset(LrpDuck) |
        (Preset(LrpDash) & Preset(LrpDlcDoublejump)),
        options=[DepFilter(deps.dep_hard_logic, False)]
    )
)
