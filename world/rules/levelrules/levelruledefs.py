### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from ...names import locationnames as l
from ...names import regionnames as lv
from . import levelrulepresets as lrp
from .levelrulebase import LevelDef, LevelRules, LocationDef, RulePreset

levelrules = LevelRules({
    lv.level_boss_veggies: LevelDef(
        exit_location=l.loc_level_boss_veggies,
        locations={
            l.loc_level_boss_veggies: LocationDef(),
            l.loc_level_boss_veggies_topgrade: LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            l.loc_level_boss_veggies_secret: LocationDef(),
            l.loc_level_boss_veggies_event_agrade: LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            l.loc_level_boss_veggies_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced),
                ]
            ),
            l.loc_level_boss_veggies_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced),
                ]
            ),
        },
    ),
    lv.level_boss_slime: LevelDef(
        exit_location=l.loc_level_boss_slime,
        base=[RulePreset(lrp.lrp_duck_or_dash)],
        locations={
            l.loc_level_boss_slime: LocationDef(),
            l.loc_level_boss_slime_topgrade: LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            l.loc_level_boss_slime_event_agrade: LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            l.loc_level_boss_slime_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                ]
            ),
            l.loc_level_boss_slime_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                ]
            ),
        },
    ),
})
