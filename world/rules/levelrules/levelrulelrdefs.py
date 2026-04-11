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
    #(Preset(LrpDuck) | DepFilter(deps.dep_hard_logic))
)

LrdBossPirateChalice = (
    (Preset(LrpDuck) | (Preset(LrpDashAndParry) & Preset(LrpDlcDoublejump))) |
    DepFilter(deps.dep_rando_abilities, value=False)
)

LrdBossSallyStagePlaySecret = (
    Preset(LrpParry) &
    (Preset(LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice_only, value=False))
)

LrdDlcBossRumRunnersEarlyPhase = (
    Preset(LrpDuck) &
    (Preset(LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice_only, value=False))
)

LrdDlcBossSnowCultChaliced = (
    Preset(LrpDlcBossChaliced) &
    (Preset(LrpDlcDoublejump) | DepFilter(deps.dep_hard_logic))
)

LrdDlcBossAirplaneChaliced = (
    Preset(LrpDlcCookie) &
    Filtered(
        Preset(LrpDuckOrDash) &
        (Preset(LrpDuck) | (Preset(LrpDash) & Preset(LrpDlcDoublejump))),
        options=[DepFilter(deps.dep_hard_logic, False)],
        filtered_resolution=True
    )
)
