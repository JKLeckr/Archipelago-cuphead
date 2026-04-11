### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from ...names import itemnames as i
from ...names import locationnames as l
from ...names import regionnames as lv
from ..dep import deps
from ..dep.depfilter import DepFilter
from ..rb.rbbaserules import Filtered, Has
from ..rb.rbfieldresolvers import ContractReqsResolver, DlcIngredientReqsResolver
from . import levelrulelrdefs as lrd
from . import levelrulepresets as lrp
from .levelrulebase import InheritMode, LevelDef, LevelRules, LocationDef

levelrules = LevelRules(
    {
        lv.level_boss_veggies: LevelDef(
            exit_location=l.loc_level_boss_veggies,
            access=lrp.LrpWeapon,
            locations={
                l.loc_level_boss_veggies: LocationDef(),
                l.loc_level_boss_veggies_topgrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_veggies_secret: LocationDef(),
                l.loc_level_boss_veggies_event_agrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_veggies_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChaliced),
                l.loc_level_boss_veggies_event_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChaliced),
            },
        ),
        lv.level_boss_slime: LevelDef(
            exit_location=l.loc_level_boss_slime,
            access=lrp.LrpWeapon,
            base=lrp.LrpDuckOrDash,
            locations={
                l.loc_level_boss_slime: LocationDef(),
                l.loc_level_boss_slime_topgrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_slime_event_agrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_slime_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChalicedParry),
                l.loc_level_boss_slime_event_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChalicedParry),
            },
        ),
        lv.level_boss_frogs: LevelDef(
            exit_location=l.loc_level_boss_frogs,
            access=lrp.LrpWeapon,
            base=lrp.LrpParryOrPSugar,
            locations={
                l.loc_level_boss_frogs: LocationDef(),
                l.loc_level_boss_frogs_topgrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_frogs_event_agrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_frogs_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChalicedParry),
                l.loc_level_boss_frogs_event_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChalicedParry),
            },
        ),
        lv.level_boss_flower: LevelDef(
            exit_location=l.loc_level_boss_flower,
            access=lrp.LrpWeapon,
            locations={
                l.loc_level_boss_flower: LocationDef(),
                l.loc_level_boss_flower_topgrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_flower_event_agrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_flower_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChaliced),
                l.loc_level_boss_flower_event_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChaliced),
            },
        ),
        lv.level_boss_baroness: LevelDef(
            exit_location=l.loc_level_boss_baroness,
            access=lrp.LrpWeapon,
            base=lrp.LrpParryOrPSugar,
            locations={
                l.loc_level_boss_baroness: LocationDef(
                    rule=Filtered(
                        lrd.LrdBossBaronessChalice,
                        options=[DepFilter(deps.dep_dlc_chalice_only)]
                    )
                ),
                l.loc_level_boss_baroness_topgrade: LocationDef(
                    rule=(
                        Filtered(
                            lrd.LrdBossBaronessChalice,
                            options=[DepFilter(deps.dep_dlc_chalice_only)]
                        ) &
                        lrp.LrpTopgrade
                    )
                ),
                l.loc_level_boss_baroness_phase1: LocationDef(
                    rule=Filtered(
                        lrd.LrdBossBaronessChalice,
                        options=[DepFilter(deps.dep_dlc_chalice_only)]
                    ),
                    inherit=InheritMode.NONE,
                ),
                l.loc_level_boss_baroness_phase2: LocationDef(
                    rule=Filtered(
                        lrd.LrdBossBaronessChalice,
                        options=[DepFilter(deps.dep_dlc_chalice_only)]
                    ),
                    inherit=InheritMode.NONE,
                ),
                l.loc_level_boss_baroness_phase3: LocationDef(
                    rule=Filtered(
                        lrd.LrdBossBaronessChalice,
                        options=[DepFilter(deps.dep_dlc_chalice_only)]
                    ),
                    inherit=InheritMode.NONE,
                ),
                l.loc_level_boss_baroness_phase4: LocationDef(
                    rule=Filtered(
                        lrd.LrdBossBaronessChalice,
                        options=[DepFilter(deps.dep_dlc_chalice_only)]
                    )
                ),
                l.loc_level_boss_baroness_event_agrade: LocationDef(
                    rule=(
                        Filtered(
                            lrd.LrdBossBaronessChalice,
                            options=[DepFilter(deps.dep_dlc_chalice_only)]
                        ) &
                        lrp.LrpTopgrade
                    )
                ),
                l.loc_level_boss_baroness_dlc_chaliced: LocationDef(
                    rule=lrp.LrpDlcBossChalicedParry & lrd.LrdBossBaronessChalice,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_boss_baroness_event_dlc_chaliced: LocationDef(
                    rule=lrp.LrpDlcBossChalicedParry & lrd.LrdBossBaronessChalice,
                    inherit=InheritMode.NONE
                ),
            },
        ),
        lv.level_boss_clown: LevelDef(
            exit_location=l.loc_level_boss_clown,
            access=lrp.LrpWeapon,
            base=lrp.LrpDashOrParry,
            locations={
                l.loc_level_boss_clown: LocationDef(),
                l.loc_level_boss_clown_topgrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_clown_event_agrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_clown_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChalicedParry),
                l.loc_level_boss_clown_event_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChalicedParry),
            },
        ),
        lv.level_boss_dragon: LevelDef(
            exit_location=l.loc_level_boss_dragon,
            access=lrp.LrpWeapon,
            base=Filtered(
                lrp.LrpDash |
                lrp.LrpDlcDoublejump,
                options=[DepFilter(deps.dep_dlc_chalice_only), DepFilter(deps.dep_hard_logic, False)],
            ),
            locations={
                l.loc_level_boss_dragon: LocationDef(),
                l.loc_level_boss_dragon_topgrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_dragon_event_agrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_dragon_dlc_chaliced: LocationDef(
                    rule=(
                        lrp.LrpDlcBossChaliced &
                        Filtered(lrp.LrpDash | lrp.LrpDlcDoublejump, options=[DepFilter(deps.dep_hard_logic, False)])
                    ),
                    inherit=InheritMode.NONE,
                ),
                l.loc_level_boss_dragon_event_dlc_chaliced: LocationDef(
                    rule=(
                        lrp.LrpDlcBossChaliced &
                        Filtered(lrp.LrpDash | lrp.LrpDlcDoublejump, options=[DepFilter(deps.dep_hard_logic, False)])
                    ),
                    inherit=InheritMode.NONE,
                ),
            },
        ),
        lv.level_boss_bee: LevelDef(
            exit_location=l.loc_level_boss_bee,
            access=lrp.LrpWeapon,
            locations={
                l.loc_level_boss_bee: LocationDef(),
                l.loc_level_boss_bee_topgrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_bee_event_agrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_bee_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChaliced),
                l.loc_level_boss_bee_event_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChaliced),
            },
        ),
        lv.level_boss_pirate: LevelDef(
            exit_location=l.loc_level_boss_pirate,
            access=lrp.LrpWeapon,
            base=Filtered(
                lrp.LrpDuck |
                (
                    lrp.LrpDashAndParry &
                    Filtered(
                        lrp.LrpDlcDoublejump, options=[DepFilter(deps.dep_dlc_chalice_only)]
                    )
                ),
                options=[DepFilter(deps.dep_rando_abilities)],
            ),
            locations={
                l.loc_level_boss_pirate: LocationDef(),
                l.loc_level_boss_pirate_topgrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_pirate_phase1: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_boss_pirate_phase2: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_boss_pirate_phase3: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_boss_pirate_phase4: LocationDef(),
                l.loc_level_boss_pirate_event_agrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_pirate_dlc_chaliced: LocationDef(
                    rule=lrp.LrpDlcBossChalicedParry & lrd.LrdBossPirateChalice,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_boss_pirate_event_dlc_chaliced: LocationDef(
                    rule=lrp.LrpDlcBossChalicedParry & lrd.LrdBossPirateChalice,
                    inherit=InheritMode.NONE
                ),
            },
        ),
        lv.level_boss_mouse: LevelDef(
            exit_location=l.loc_level_boss_mouse,
            access=lrp.LrpWeapon,
            base=(
                lrp.LrpDuck &
                Filtered(
                    lrp.LrpParry,
                    options=[DepFilter(deps.dep_rando_abilities), DepFilter(deps.dep_dlc_chalice_only)],
                ) &
                Filtered(
                    lrp.LrpParryOrPSugar,
                    options=[DepFilter(deps.dep_rando_abilities), DepFilter(deps.dep_dlc_chalice_only, False)],
                )
            ),
            locations={
                l.loc_level_boss_mouse: LocationDef(
                    rule=Filtered(
                        lrp.LrpDlcDoublejump, options=[DepFilter(deps.dep_dlc_chalice_only)]
                    )
                ),
                l.loc_level_boss_mouse_topgrade: LocationDef(
                    rule=(
                        lrp.LrpTopgrade &
                        Filtered(
                            lrp.LrpDlcDoublejump, options=[DepFilter(deps.dep_dlc_chalice_only)]
                        )
                    )
                ),
                l.loc_level_boss_mouse_phase1: LocationDef(),
                l.loc_level_boss_mouse_phase2: LocationDef(
                    rule=Filtered(
                        lrp.LrpDlcDoublejump, options=[DepFilter(deps.dep_dlc_chalice_only)]
                    )
                ),
                l.loc_level_boss_mouse_phase3: LocationDef(),
                l.loc_level_boss_mouse_event_agrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_mouse_dlc_chaliced: LocationDef(
                    rule=lrp.LrpDlcBossChalicedParry & lrp.LrpDlcDoublejump
                ),
                l.loc_level_boss_mouse_event_dlc_chaliced: LocationDef(
                    rule=lrp.LrpDlcBossChalicedParry & lrp.LrpDlcDoublejump
                ),
            },
        ),
        lv.level_boss_sallystageplay: LevelDef(
            exit_location=l.loc_level_boss_sallystageplay,
            access=lrp.LrpWeapon,
            base=(
                lrp.LrpParry &
                Filtered(lrp.LrpDlcDoublejump | lrp.LrpDuck, options=[DepFilter(deps.dep_dlc_chalice_only)])
            ),
            locations={
                l.loc_level_boss_sallystageplay: LocationDef(),
                l.loc_level_boss_sallystageplay_topgrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_sallystageplay_phase1: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_boss_sallystageplay_phase1s: LocationDef(
                    rule=lrd.LrdBossSallyStagePlaySecret,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_boss_sallystageplay_phase2: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_boss_sallystageplay_phase2s: LocationDef(
                    rule=lrd.LrdBossSallyStagePlaySecret,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_boss_sallystageplay_phase3: LocationDef(),
                l.loc_level_boss_sallystageplay_phase3s: LocationDef(
                    rule=lrd.LrdBossSallyStagePlaySecret,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_boss_sallystageplay_phase4: LocationDef(),
                l.loc_level_boss_sallystageplay_phase4s: LocationDef(
                    rule=lrd.LrdBossSallyStagePlaySecret,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_boss_sallystageplay_secret: LocationDef(
                    rule=lrd.LrdBossSallyStagePlaySecret,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_boss_sallystageplay_event_agrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_sallystageplay_dlc_chaliced: LocationDef(
                    rule=lrp.LrpDlcBossChalicedParry & (lrp.LrpDlcDoublejump | lrp.LrpDuck),
                    inherit=InheritMode.NONE
                ),
                l.loc_level_boss_sallystageplay_event_dlc_chaliced: LocationDef(
                    rule=lrp.LrpDlcBossChalicedParry & (lrp.LrpDlcDoublejump | lrp.LrpDuck),
                    inherit=InheritMode.NONE
                ),
            },
        ),
        lv.level_boss_train: LevelDef(
            exit_location=l.loc_level_boss_train,
            access=lrp.LrpWeapon,
            base=(
                lrp.LrpParry &
                Filtered(
                    lrp.LrpDlcDoublejump,
                    options=[DepFilter(deps.dep_dlc_chalice_only), DepFilter(deps.dep_hard_logic, False)],
                )
            ),
            locations={
                l.loc_level_boss_train: LocationDef(),
                l.loc_level_boss_train_topgrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_train_event_agrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_train_dlc_chaliced: LocationDef(
                    rule=(
                        lrp.LrpDlcBossChalicedParry &
                        Filtered(
                            lrp.LrpDlcDoublejump,
                            options=[DepFilter(deps.dep_dlc_chalice_only, False), DepFilter(deps.dep_hard_logic, False)]
                        )
                    )
                ),
                l.loc_level_boss_train_event_dlc_chaliced: LocationDef(
                    rule=(
                        lrp.LrpDlcBossChalicedParry &
                        Filtered(
                            lrp.LrpDlcDoublejump,
                            options=[DepFilter(deps.dep_dlc_chalice_only, False), DepFilter(deps.dep_hard_logic, False)]
                        )
                    )
                ),
            },
        ),
        lv.level_boss_kingdice: LevelDef(
            exit_location=l.loc_level_boss_kingdice,
            access=Has(i.item_contract, ContractReqsResolver()) & lrp.LrpWeapon,
            base=(
                lrp.LrpPlane &
                Filtered(lrp.LrpDashAndParry, options=[DepFilter(deps.dep_rando_abilities)])
            ),
            locations={
                l.loc_level_boss_kingdice: LocationDef(),
                l.loc_level_boss_kingdice_topgrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_kingdice_event_agrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_kingdice_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChalicedParry),
                l.loc_level_boss_kingdice_event_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChalicedParry),
            },
        ),
        lv.level_boss_plane_blimp: LevelDef(
            exit_location=l.loc_level_boss_plane_blimp,
            access=lrp.LrpPlane,
            locations={
                l.loc_level_boss_plane_blimp: LocationDef(),
                l.loc_level_boss_plane_blimp_topgrade: LocationDef(rule=lrp.LrpPlaneTopgrade),
                l.loc_level_boss_plane_blimp_event_agrade: LocationDef(rule=lrp.LrpPlaneTopgrade),
                l.loc_level_boss_plane_blimp_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossPlaneChaliced),
                l.loc_level_boss_plane_blimp_event_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossPlaneChaliced),
            },
        ),
        lv.level_boss_plane_genie: LevelDef(
            exit_location=l.loc_level_boss_plane_genie,
            access=lrp.LrpPlane,
            locations={
                l.loc_level_boss_plane_genie: LocationDef(),
                l.loc_level_boss_plane_genie_topgrade: LocationDef(rule=lrp.LrpPlaneTopgrade),
                l.loc_level_boss_plane_genie_secret: LocationDef(rule=lrp.LrpPlaneShrink),
                l.loc_level_boss_plane_genie_event_agrade: LocationDef(rule=lrp.LrpPlaneTopgrade),
                l.loc_level_boss_plane_genie_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossPlaneChaliced),
                l.loc_level_boss_plane_genie_event_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossPlaneChaliced),
            },
        ),
        lv.level_boss_plane_bird: LevelDef(
            exit_location=l.loc_level_boss_plane_bird,
            access=lrp.LrpPlane,
            base=(
                Has(i.item_plane_gun, options=[DepFilter(deps.dep_hard_logic)]) &
                Has(i.item_plane_gun, options=[DepFilter(deps.dep_hard_logic, False)]) &
                Has(i.item_plane_bombs, options=[DepFilter(deps.dep_hard_logic, False)])
            ),
            locations={
                l.loc_level_boss_plane_bird: LocationDef(),
                l.loc_level_boss_plane_bird_topgrade: LocationDef(rule=lrp.LrpPlaneTopgrade),
                l.loc_level_boss_plane_bird_event_agrade: LocationDef(rule=lrp.LrpPlaneTopgrade),
                l.loc_level_boss_plane_bird_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossPlaneChaliced),
                l.loc_level_boss_plane_bird_event_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossPlaneChaliced),
            },
        ),
        lv.level_boss_plane_mermaid: LevelDef(
            exit_location=l.loc_level_boss_plane_mermaid,
            access=lrp.LrpPlane,
            locations={
                l.loc_level_boss_plane_mermaid: LocationDef(),
                l.loc_level_boss_plane_mermaid_topgrade: LocationDef(rule=lrp.LrpPlaneTopgrade),
                l.loc_level_boss_plane_mermaid_event_agrade: LocationDef(rule=lrp.LrpPlaneTopgrade),
                l.loc_level_boss_plane_mermaid_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossPlaneChaliced),
                l.loc_level_boss_plane_mermaid_event_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossPlaneChaliced),
            },
        ),
        lv.level_boss_plane_robot: LevelDef(
            exit_location=l.loc_level_boss_plane_robot,
            access=(
                lrp.LrpPlane &
                Filtered(lrp.LrpPlaneParry, options=[DepFilter(deps.dep_rando_abilities)])
            ),
            locations={
                l.loc_level_boss_plane_robot: LocationDef(),
                l.loc_level_boss_plane_robot_topgrade: LocationDef(rule=lrp.LrpPlaneTopgrade),
                l.loc_level_boss_plane_robot_event_agrade: LocationDef(rule=lrp.LrpPlaneTopgrade),
                l.loc_level_boss_plane_robot_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossPlaneChaliced),
                l.loc_level_boss_plane_robot_event_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossPlaneChaliced),
            },
        ),
        lv.level_boss_devil: LevelDef(
            exit_location=None,
            access=lrp.LrpWeapon,
            base=(
                Filtered(
                    lrp.LrpDlcDoublejump | lrp.LrpDashAndParry,
                    options=[
                        DepFilter(deps.dep_rando_abilities),
                        DepFilter(deps.dep_dlc_chalice_not_separate),
                        DepFilter(deps.dep_hard_logic),
                    ],
                ) &
                Filtered(
                    lrp.LrpDashAndParry,
                    options=[
                        DepFilter(deps.dep_rando_abilities),
                        DepFilter(
                            (deps.dep_dlc_chalice_not_separate, deps.dep_hard_logic),
                            value=False,
                            any=True
                        ),
                    ],
                )
            ),
            locations={
                l.loc_level_boss_devil: LocationDef(),
                l.loc_level_boss_devil_topgrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_devil_event_agrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_boss_devil_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChalicedParry),
                l.loc_level_boss_devil_event_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChalicedParry),
                l.loc_event_goal_devil: LocationDef(),
            },
        ),
        lv.level_dlc_boss_oldman: LevelDef(
            exit_location=l.loc_level_dlc_boss_oldman,
            access=lrp.LrpWeapon,
            base=Filtered(lrp.LrpDash & lrp.LrpParryOrPSugar, options=[DepFilter(deps.dep_rando_abilities)]),
            locations={
                l.loc_level_dlc_boss_oldman: LocationDef(),
                l.loc_level_dlc_boss_oldman_topgrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_dlc_boss_oldman_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChalicedParry),
                l.loc_level_dlc_boss_oldman_event_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChalicedParry),
            },
        ),
        lv.level_dlc_boss_rumrunners: LevelDef(
            exit_location=l.loc_level_dlc_boss_rumrunners,
            access=lrp.LrpWeapon,
            base=(
                lrp.LrpDuckAndParry &
                Filtered(lrp.LrpDlcDoublejump, options=[DepFilter(deps.dep_dlc_chalice_only)])
            ),
            locations={
                l.loc_level_dlc_boss_rumrunners: LocationDef(),
                l.loc_level_dlc_boss_rumrunners_topgrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_dlc_boss_rumrunners_phase1: LocationDef(
                    rule=lrd.LrdDlcBossRumRunnersEarlyPhase,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_dlc_boss_rumrunners_phase2: LocationDef(
                    rule=lrd.LrdDlcBossRumRunnersEarlyPhase,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_dlc_boss_rumrunners_phase3: LocationDef(),
                l.loc_level_dlc_boss_rumrunners_phase4: LocationDef(),
                l.loc_level_dlc_boss_rumrunners_dlc_chaliced: LocationDef(
                    rule=(
                        lrp.LrpDlcBossChalicedParry &
                        Filtered(
                            lrp.LrpDlcDoublejump,
                            options=[DepFilter(deps.dep_dlc_chalice_only, False)]
                        )
                    )
                ),
                l.loc_level_dlc_boss_rumrunners_event_dlc_chaliced: LocationDef(
                    rule=(
                        lrp.LrpDlcBossChalicedParry &
                        Filtered(
                            lrp.LrpDlcDoublejump,
                            options=[DepFilter(deps.dep_dlc_chalice_only, False)]
                        )
                    )
                ),
            },
        ),
        lv.level_dlc_boss_snowcult: LevelDef(
            exit_location=l.loc_level_dlc_boss_snowcult,
            access=lrp.LrpWeapon,
            base=Filtered(
                lrp.LrpDlcDoublejump,
                options=[DepFilter(deps.dep_dlc_chalice_only), DepFilter(deps.dep_hard_logic, False)],
            ),
            locations={
                l.loc_level_dlc_boss_snowcult: LocationDef(),
                l.loc_level_dlc_boss_snowcult_topgrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_dlc_boss_snowcult_dlc_chaliced: LocationDef(rule=lrd.LrdDlcBossSnowcultChaliced),
                l.loc_level_dlc_boss_snowcult_event_dlc_chaliced: LocationDef(rule=lrd.LrdDlcBossSnowcultChaliced),
            },
        ),
        lv.level_dlc_boss_airplane: LevelDef(
            exit_location=l.loc_level_dlc_boss_airplane,
            access=lrp.LrpWeapon,
            base=(
                Filtered(
                    lrp.LrpDuckOrDash, options=[DepFilter(deps.dep_dlc_chalice_only, False)]
                ) &
                Filtered(
                    lrp.LrpDuckOrDash,
                    options=[DepFilter(deps.dep_dlc_chalice_only), DepFilter(deps.dep_hard_logic)],
                ) &
                Filtered(
                    lrp.LrpDuck | (lrp.LrpDash & lrp.LrpDlcDoublejump),
                    options=[DepFilter(deps.dep_dlc_chalice_only), DepFilter(deps.dep_hard_logic, False)],
                )
            ),
            locations={
                l.loc_level_dlc_boss_airplane: LocationDef(),
                l.loc_level_dlc_boss_airplane_topgrade: LocationDef(rule=lrp.LrpPlaneTopgrade),
                l.loc_level_dlc_boss_airplane_secret: LocationDef(),
                l.loc_level_dlc_boss_airplane_dlc_chaliced: LocationDef(rule=lrd.LrdDlcBossAirplaneChaliced),
                l.loc_level_dlc_boss_airplane_event_dlc_chaliced: LocationDef(rule=lrd.LrdDlcBossAirplaneChaliced),
            },
        ),
        lv.level_dlc_boss_plane_cowboy: LevelDef(
            exit_location=l.loc_level_dlc_boss_plane_cowboy,
            access=lrp.LrpPlane,
            locations={
                l.loc_level_dlc_boss_plane_cowboy: LocationDef(),
                l.loc_level_dlc_boss_plane_cowboy_topgrade: LocationDef(rule=lrp.LrpPlaneTopgrade),
                l.loc_level_dlc_boss_plane_cowboy_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossPlaneChaliced),
                l.loc_level_dlc_boss_plane_cowboy_event_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossPlaneChaliced),
            },
        ),
        lv.level_dlc_boss_saltbaker: LevelDef(
            exit_location=None,
            access=Has(i.item_dlc_ingredient, DlcIngredientReqsResolver()) & lrp.LrpWeapon,
            base=(
                Filtered(lrp.LrpParry, options=[DepFilter(deps.dep_rando_abilities)]) &
                Filtered(lrp.LrpDlcDoublejump, options=[DepFilter(deps.dep_dlc_chalice_only)])
            ),
            locations={
                l.loc_level_dlc_boss_saltbaker: LocationDef(),
                l.loc_level_dlc_boss_saltbaker_topgrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_dlc_boss_saltbaker_phase1: LocationDef(
                    rule=Filtered(
                        lrp.LrpDlcDoublejump,
                        options=[DepFilter(deps.dep_dlc_chalice_only), DepFilter(deps.dep_hard_logic, False)]
                    ),
                    inherit=InheritMode.NONE,
                ),
                l.loc_level_dlc_boss_saltbaker_phase2: LocationDef(
                    rule=(
                        Filtered(lrp.LrpParry, options=[DepFilter(deps.dep_rando_abilities)]) &
                        Filtered(
                            lrp.LrpDlcDoublejump,
                            options=[DepFilter(deps.dep_dlc_chalice_only), DepFilter(deps.dep_hard_logic, False)]
                        )
                    ),
                    inherit=InheritMode.NONE,
                ),
                l.loc_level_dlc_boss_saltbaker_phase3: LocationDef(
                    rule=(
                        Filtered(lrp.LrpParry, options=[DepFilter(deps.dep_rando_abilities)]) &
                        Filtered(
                            lrp.LrpDlcDoublejump,
                            options=[DepFilter(deps.dep_dlc_chalice_only), DepFilter(deps.dep_hard_logic, False)]
                        )
                    ),
                    inherit=InheritMode.NONE,
                ),
                l.loc_level_dlc_boss_saltbaker_phase4: LocationDef(),
                l.loc_level_dlc_boss_saltbaker_event_agrade: LocationDef(rule=lrp.LrpTopgrade),
                l.loc_level_dlc_boss_saltbaker_dlc_chaliced: LocationDef(
                    rule=lrp.LrpDlcBossChalicedParry & lrp.LrpDlcDoublejump,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_dlc_boss_saltbaker_event_dlc_chaliced: LocationDef(
                    rule=lrp.LrpDlcBossChalicedParry & lrp.LrpDlcDoublejump,
                    inherit=InheritMode.NONE
                ),
                l.loc_event_dlc_goal_saltbaker: LocationDef(),
            },
        ),
        lv.level_dicepalace_boss_booze: LevelDef(
            exit_location=None,
            access=lrp.LrpWeapon,
            locations={
                l.loc_level_dicepalace_boss_booze: LocationDef(),
                l.loc_level_dicepalace_boss_booze_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChaliced),
            },
        ),
        lv.level_dicepalace_boss_chips: LevelDef(
            exit_location=None,
            access=lrp.LrpWeapon,
            locations={
                l.loc_level_dicepalace_boss_chips: LocationDef(),
                l.loc_level_dicepalace_boss_chips_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChaliced),
            },
        ),
        lv.level_dicepalace_boss_cigar: LevelDef(
            exit_location=None,
            access=lrp.LrpWeapon,
            base=lrp.LrpDash,
            locations={
                l.loc_level_dicepalace_boss_cigar: LocationDef(),
                l.loc_level_dicepalace_boss_cigar_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChaliced),
            },
        ),
        lv.level_dicepalace_boss_domino: LevelDef(
            exit_location=None,
            access=lrp.LrpWeapon,
            locations={
                l.loc_level_dicepalace_boss_domino: LocationDef(),
                l.loc_level_dicepalace_boss_domino_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChaliced),
            },
        ),
        lv.level_dicepalace_boss_rabbit: LevelDef(
            exit_location=None,
            access=lrp.LrpWeapon,
            base=lrp.LrpParry,
            locations={
                l.loc_level_dicepalace_boss_rabbit: LocationDef(
                    rule=(
                        Filtered(
                            lrp.LrpDlcDoublejump, options=[DepFilter(deps.dep_dlc_chalice_only)]
                        )
                    )
                ),
                l.loc_level_dicepalace_boss_rabbit_dlc_chaliced: LocationDef(
                    rule=lrp.LrpDlcBossChaliced & lrp.LrpDlcDoublejump
                ),
            },
        ),
        lv.level_dicepalace_boss_plane_horse: LevelDef(
            exit_location=None,
            access=lrp.LrpPlane,
            locations={
                l.loc_level_dicepalace_boss_plane_horse: LocationDef(),
                l.loc_level_dicepalace_boss_plane_horse_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossPlaneChaliced),
            },
        ),
        lv.level_dicepalace_boss_roulette: LevelDef(
            exit_location=None,
            access=lrp.LrpWeapon,
            locations={
                l.loc_level_dicepalace_boss_roulette: LocationDef(),
                l.loc_level_dicepalace_boss_roulette_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChaliced),
            },
        ),
        lv.level_dicepalace_boss_eightball: LevelDef(
            exit_location=None,
            access=lrp.LrpWeapon,
            locations={
                l.loc_level_dicepalace_boss_eightball: LocationDef(),
                l.loc_level_dicepalace_boss_eightball_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossChaliced),
            },
        ),
        lv.level_dicepalace_boss_plane_memory: LevelDef(
            exit_location=None,
            access=lrp.LrpPlane,
            locations={
                l.loc_level_dicepalace_boss_plane_memory: LocationDef(),
                l.loc_level_dicepalace_boss_plane_memory_dlc_chaliced: LocationDef(rule=lrp.LrpDlcBossPlaneChaliced),
            },
        ),
        lv.level_rungun_forest: LevelDef(
            exit_location=l.loc_level_rungun_forest,
            base=lrp.LrpRungunWeapon & lrp.LrpDash,
            locations={
                l.loc_level_rungun_forest: LocationDef(),
                l.loc_level_rungun_forest_agrade: LocationDef(rule=lrp.LrpRungunTopgrade),
                l.loc_level_rungun_forest_pacifist: LocationDef(),
                l.loc_level_rungun_forest_coin1: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_rungun_forest_coin2: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_rungun_forest_coin3: LocationDef(rule=lrp.LrpParry, inherit=InheritMode.NONE),
                l.loc_level_rungun_forest_coin4: LocationDef(rule=lrp.LrpDash, inherit=InheritMode.NONE),
                l.loc_level_rungun_forest_coin5: LocationDef(
                    rule=lrp.LrpRungunWeapon & lrp.LrpDash,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_forest_dlc_chaliced: LocationDef(rule=lrp.LrpDlcRungunChaliced),
                l.loc_level_rungun_forest_event_agrade: LocationDef(rule=lrp.LrpRungunTopgrade),
                l.loc_level_rungun_forest_event_pacifist: LocationDef(),
            },
        ),
        lv.level_rungun_tree: LevelDef(
            exit_location=l.loc_level_rungun_tree,
            base=(
                lrp.LrpDash &
                Filtered(lrp.LrpDlcDoublejump, options=[DepFilter(deps.dep_dlc_chalice_only)])
            ),
            locations={
                l.loc_level_rungun_tree: LocationDef(rule=lrp.LrpRungunWeapon),
                l.loc_level_rungun_tree_agrade: LocationDef(rule=lrp.LrpRungunWeapon & lrp.LrpRungunTopgrade),
                l.loc_level_rungun_tree_pacifist: LocationDef(),
                l.loc_level_rungun_tree_coin1: LocationDef(rule=lrp.LrpParry, inherit=InheritMode.NONE),
                l.loc_level_rungun_tree_coin2: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_rungun_tree_coin3: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_rungun_tree_coin4: LocationDef(),
                l.loc_level_rungun_tree_coin5: LocationDef(),
                l.loc_level_rungun_tree_dlc_chaliced: LocationDef(
                    rule=(
                        lrp.LrpRungunWeapon &
                        lrp.LrpDlcRungunChaliced &
                        Filtered(
                            lrp.LrpDlcDoublejump,
                            options=[DepFilter(deps.dep_dlc_chalice_only, False)]
                        )
                    )
                ),
                l.loc_level_rungun_tree_event_agrade: LocationDef(rule=lrp.LrpRungunWeapon & lrp.LrpRungunTopgrade),
                l.loc_level_rungun_tree_event_pacifist: LocationDef(),
            },
        ),
        lv.level_rungun_circus: LevelDef(
            exit_location=l.loc_level_rungun_circus,
            base=(
                lrp.LrpRungunWeapon &
                lrp.LrpParryOrPSugar &
                Filtered(
                    lrp.LrpDlcDoublejump,
                    options=[DepFilter(deps.dep_dlc_chalice_only), DepFilter(deps.dep_hard_logic, False)],
                )
            ),
            locations={
                l.loc_level_rungun_circus: LocationDef(),
                l.loc_level_rungun_circus_agrade: LocationDef(
                    rule=Filtered(
                        lrp.LrpRungunTopgrade, options=[DepFilter(deps.dep_hard_logic, False)]
                    )
                ),
                l.loc_level_rungun_circus_pacifist: LocationDef(),
                l.loc_level_rungun_circus_coin1: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_rungun_circus_coin2: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_rungun_circus_coin3: LocationDef(),
                l.loc_level_rungun_circus_coin4: LocationDef(),
                l.loc_level_rungun_circus_coin5: LocationDef(),
                l.loc_level_rungun_circus_dlc_chaliced: LocationDef(
                    rule=(
                        lrp.LrpDlcRungunChaliced &
                        lrp.LrpDashAndParry &
                        Filtered(
                            lrp.LrpDlcDoublejump,
                            options=[DepFilter(deps.dep_dlc_chalice_only, False), DepFilter(deps.dep_hard_logic, False)]
                        )
                    ),
                    inherit=InheritMode.NONE,
                ),
                l.loc_level_rungun_circus_event_agrade: LocationDef(
                    rule=(
                        Filtered(
                            lrp.LrpRungunTopgrade, options=[DepFilter(deps.dep_hard_logic, False)]
                        )
                    )
                ),
                l.loc_level_rungun_circus_event_pacifist: LocationDef(),
            },
        ),
        lv.level_rungun_funhouse: LevelDef(
            exit_location=l.loc_level_rungun_funhouse,
            base=(
                lrp.LrpRungunWeapon &
                Filtered(
                    lrp.LrpParry,
                    options=[DepFilter(deps.dep_rando_abilities), DepFilter(deps.dep_dlc_chalice_only)],
                ) &
                Filtered(
                    lrp.LrpParry | (Has(i.item_charm_psugar) & lrp.LrpDash),
                    options=[DepFilter(deps.dep_rando_abilities), DepFilter(deps.dep_dlc_chalice_only, False)],
                )
            ),
            locations={
                l.loc_level_rungun_funhouse: LocationDef(),
                l.loc_level_rungun_funhouse_agrade: LocationDef(rule=lrp.LrpRungunTopgrade),
                l.loc_level_rungun_funhouse_pacifist: LocationDef(),
                l.loc_level_rungun_funhouse_coin1: LocationDef(rule=lrp.LrpParryOrPSugar, inherit=InheritMode.NONE),
                l.loc_level_rungun_funhouse_coin2: LocationDef(
                    rule=lrp.LrpRungunWeapon & lrp.LrpParryOrPSugar,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_funhouse_coin3: LocationDef(
                    rule=lrp.LrpRungunWeapon & lrp.LrpParryOrPSugar,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_funhouse_coin4: LocationDef(
                    rule=lrp.LrpRungunWeapon & lrp.LrpParryOrPSugar,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_funhouse_coin5: LocationDef(),
                l.loc_level_rungun_funhouse_dlc_chaliced: LocationDef(rule=lrp.LrpDlcRungunChaliced),
                l.loc_level_rungun_funhouse_event_agrade: LocationDef(rule=lrp.LrpRungunTopgrade),
                l.loc_level_rungun_funhouse_event_pacifist: LocationDef(),
            },
        ),
        lv.level_rungun_harbour: LevelDef(
            exit_location=l.loc_level_rungun_harbour,
            base=(
                lrp.LrpRungunWeapon &
                lrp.LrpDashAndParry &
                Filtered(lrp.LrpDlcDoublejump, options=[DepFilter(deps.dep_dlc_chalice_only)])
            ),
            locations={
                l.loc_level_rungun_harbour: LocationDef(),
                l.loc_level_rungun_harbour_agrade: LocationDef(rule=lrp.LrpRungunTopgrade),
                l.loc_level_rungun_harbour_pacifist: LocationDef(),
                l.loc_level_rungun_harbour_coin1: LocationDef(
                    rule=lrp.LrpRungunWeapon & lrp.LrpDashParryOrPSugar,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_harbour_coin2: LocationDef(rule=lrp.LrpRungunWeapon, inherit=InheritMode.NONE),
                l.loc_level_rungun_harbour_coin3: LocationDef(
                    rule=lrp.LrpRungunWeapon & lrp.LrpParryOrPSugar,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_harbour_coin4: LocationDef(
                    rule=(
                        lrp.LrpRungunWeapon &
                        (lrp.LrpParry | (Has(i.item_charm_psugar) & lrp.LrpDash)) &
                        Filtered(
                            lrp.LrpDlcDoublejump, options=[DepFilter(deps.dep_dlc_chalice_only)]
                        )
                    ),
                    inherit=InheritMode.NONE,
                ),
                l.loc_level_rungun_harbour_coin5: LocationDef(),
                l.loc_level_rungun_harbour_dlc_chaliced: LocationDef(
                    rule=(
                        lrp.LrpDlcRungunChaliced &
                        Filtered(
                            lrp.LrpDlcDoublejump,
                            options=[DepFilter(deps.dep_dlc_chalice_only, False)]
                        )
                    )
                ),
                l.loc_level_rungun_harbour_event_agrade: LocationDef(rule=lrp.LrpRungunTopgrade),
                l.loc_level_rungun_harbour_event_pacifist: LocationDef(),
            },
        ),
        lv.level_rungun_mountain: LevelDef(
            exit_location=l.loc_level_rungun_mountain,
            base=(
                lrp.LrpRungunWeapon &
                Filtered(lrp.LrpDash, options=[DepFilter(deps.dep_dlc_chalice, False)]) &
                Filtered(lrp.LrpDash | lrp.LrpDlcDoublejump, options=[DepFilter(deps.dep_dlc_chalice)])
            ),
            locations={
                l.loc_level_rungun_mountain: LocationDef(),
                l.loc_level_rungun_mountain_agrade: LocationDef(rule=lrp.LrpRungunTopgrade),
                l.loc_level_rungun_mountain_pacifist: LocationDef(),
                l.loc_level_rungun_mountain_coin1: LocationDef(rule=lrp.LrpRungunWeapon, inherit=InheritMode.NONE),
                l.loc_level_rungun_mountain_coin2: LocationDef(
                    rule=lrp.LrpRungunWeapon & lrp.LrpDashOrDlcDoublejump,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_mountain_coin3: LocationDef(rule=lrp.LrpRungunWeapon, inherit=InheritMode.NONE),
                l.loc_level_rungun_mountain_coin4: LocationDef(
                    rule=(
                        lrp.LrpRungunWeapon &
                        Filtered(
                            lrp.LrpDlcDoublejump, options=[DepFilter(deps.dep_dlc_chalice_only)]
                        )
                    ),
                    inherit=InheritMode.NONE,
                ),
                l.loc_level_rungun_mountain_coin5: LocationDef(
                    rule=lrp.LrpRungunWeapon & lrp.LrpDashOrDlcDoublejump,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_mountain_dlc_chaliced: LocationDef(rule=lrp.LrpDlcRungunChaliced),
                l.loc_level_rungun_mountain_event_agrade: LocationDef(rule=lrp.LrpRungunTopgrade),
                l.loc_level_rungun_mountain_event_pacifist: LocationDef(),
            },
        ),
        lv.level_mausoleum_i: LevelDef(exit_location=None, access=lrp.LrpParry, locations={}),
        lv.level_mausoleum_ii: LevelDef(exit_location=None, access=lrp.LrpParry, locations={}),
        lv.level_mausoleum_iii: LevelDef(exit_location=None, access=lrp.LrpParry, locations={}),
        lv.level_dlc_chesscastle_pawn: LevelDef(
            exit_location=None,
            access=lrp.LrpParry,
            locations={
                l.loc_level_dlc_chesscastle_pawn: LocationDef(),
                l.loc_level_dlc_chesscastle_pawn_dlc_chaliced: LocationDef(),
            },
        ),
        lv.level_dlc_chesscastle_knight: LevelDef(
            exit_location=None,
            access=lrp.LrpParry,
            locations={
                l.loc_level_dlc_chesscastle_knight: LocationDef(
                    rule=(
                        Filtered(
                            lrp.LrpDlcDoublejump, options=[DepFilter(deps.dep_dlc_chalice_only)]
                        )
                    )
                ),
                l.loc_level_dlc_chesscastle_knight_dlc_chaliced: LocationDef(rule=lrp.LrpDlcDoublejump),
            },
        ),
        lv.level_dlc_chesscastle_bishop: LevelDef(
            exit_location=None,
            access=lrp.LrpParry,
            locations={
                l.loc_level_dlc_chesscastle_bishop: LocationDef(),
                l.loc_level_dlc_chesscastle_bishop_dlc_chaliced: LocationDef(),
            },
        ),
        lv.level_dlc_chesscastle_rook: LevelDef(
            exit_location=None,
            access=lrp.LrpParry,
            locations={
                l.loc_level_dlc_chesscastle_rook: LocationDef(),
                l.loc_level_dlc_chesscastle_rook_dlc_chaliced: LocationDef(),
            },
        ),
        lv.level_dlc_chesscastle_queen: LevelDef(
            exit_location=None,
            access=lrp.LrpParry,
            locations={
                l.loc_level_dlc_chesscastle_queen: LocationDef(),
                l.loc_level_dlc_chesscastle_queen_dlc_chaliced: LocationDef(),
            },
        ),
        lv.level_dlc_chesscastle_run: LevelDef(
            exit_location=None,
            access=lrp.LrpParry,
            locations={
                l.loc_level_dlc_chesscastle_run: LocationDef(),
                l.loc_level_dlc_chesscastle_run_dlc_chaliced: LocationDef(),
            },
        ),
        lv.level_tutorial: LevelDef(exit_location=None, access=lrp.LrpWeapon & lrp.LrpDuckDashAndParry, locations={}),
        lv.level_dlc_tutorial: LevelDef(
            exit_location=None,
            access=lrp.LrpDlcCookie,
            locations={
                l.loc_level_dlc_tutorial_coin: LocationDef(rule=lrp.LrpDashAndParry & lrp.LrpDlcDoublejump)
            },
        ),
        lv.level_dlc_graveyard: LevelDef(
            exit_location=None,
            access=lrp.LrpWeapon & Has(i.item_charm_dlc_broken_relic),
            locations={
                l.loc_level_dlc_graveyard: LocationDef(rule=lrp.LrpDashAndParry & lrp.LrpDlcDoublejump)
            },
        ),
    }
)
