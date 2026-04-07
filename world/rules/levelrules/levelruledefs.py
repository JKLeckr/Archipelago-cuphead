### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from rule_builder.rules import Has

from ...names import itemnames as i
from ...names import locationnames as l
from ...names import regionnames as lv
from ..dep import deps
from ..dep.depfilter import DepFilter
from . import levelrulepresets as lrp
from . import levelruleselectors as lrs
from .levelrulebase import (
    And,
    InheritMode,
    LevelDef,
    LevelRules,
    LocationDef,
    Or,
    RBRule,
    RulePreset,
    RuleRef,
    SelectRule,
)

levelrules = LevelRules({
    lv.level_boss_veggies: LevelDef(
        exit_location=l.loc_level_boss_veggies,
        access=[RulePreset(lrp.lrp_weapon)],
        locations={
            l.loc_level_boss_veggies: LocationDef(),
            l.loc_level_boss_veggies_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_veggies_secret: LocationDef(),
            l.loc_level_boss_veggies_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_veggies_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced),
                ],
            ),
            l.loc_level_boss_veggies_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced),
                ],
            ),
        },
    ),
    lv.level_boss_slime: LevelDef(
        exit_location=l.loc_level_boss_slime,
        access=[RulePreset(lrp.lrp_weapon)],
        base=[
            RulePreset(lrp.lrp_duck_or_dash),
        ],
        locations={
            l.loc_level_boss_slime: LocationDef(),
            l.loc_level_boss_slime_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_slime_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_slime_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                ],
            ),
            l.loc_level_boss_slime_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                ],
            ),
        },
    ),
    lv.level_boss_frogs: LevelDef(
        exit_location=l.loc_level_boss_frogs,
        access=[RulePreset(lrp.lrp_weapon)],
        base=[
            RulePreset(lrp.lrp_parry_or_psugar),
        ],
        locations={
            l.loc_level_boss_frogs: LocationDef(),
            l.loc_level_boss_frogs_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_frogs_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_frogs_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                ],
            ),
            l.loc_level_boss_frogs_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                ],
            ),
        },
    ),
    lv.level_boss_flower: LevelDef(
        exit_location=l.loc_level_boss_flower,
        access=[RulePreset(lrp.lrp_weapon)],
        locations={
            l.loc_level_boss_flower: LocationDef(),
            l.loc_level_boss_flower_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_flower_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_flower_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced),
                ],
            ),
            l.loc_level_boss_flower_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced),
                ],
            ),
        },
    ),
    lv.level_boss_baroness: LevelDef(
        exit_location=l.loc_level_boss_baroness,
        access=[RulePreset(lrp.lrp_weapon)],
        base=[
            RulePreset(lrp.lrp_parry_or_psugar),
        ],
        ruledefs={
            "chalice": [
                RulePreset(
                    lrp.lrp_dlc_doublejump,
                    options=[DepFilter(deps.dep_hard_logic, False)]
                ),
                ## Maybe need duck?
                #RulePreset(
                #    lrp.lrp_duck,
                #    options=[DepFilter(deps.dep_hard_logic)]
                #),
            ]
        },
        locations={
            l.loc_level_boss_baroness: LocationDef(
                rules=[RuleRef("chalice", options=[DepFilter(deps.dep_dlc_chalice_only)])]
            ),
            l.loc_level_boss_baroness_topgrade: LocationDef(
                rules=[
                    RuleRef("chalice", options=[DepFilter(deps.dep_dlc_chalice_only)]),
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_baroness_phase1: LocationDef(
                rules=[RuleRef("chalice", options=[DepFilter(deps.dep_dlc_chalice_only)])],
                inherit=InheritMode.NONE
            ),
            l.loc_level_boss_baroness_phase2: LocationDef(
                rules=[RuleRef("chalice", options=[DepFilter(deps.dep_dlc_chalice_only)])],
                inherit=InheritMode.NONE
            ),
            l.loc_level_boss_baroness_phase3: LocationDef(
                rules=[RuleRef("chalice", options=[DepFilter(deps.dep_dlc_chalice_only)])],
                inherit=InheritMode.NONE
            ),
            l.loc_level_boss_baroness_phase4: LocationDef(
                rules=[RuleRef("chalice", options=[DepFilter(deps.dep_dlc_chalice_only)])]
            ),
            l.loc_level_boss_baroness_event_agrade: LocationDef(
                rules=[
                    RuleRef("chalice", options=[DepFilter(deps.dep_dlc_chalice_only)]),
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_baroness_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                    RuleRef("chalice"),
                ],
                inherit=InheritMode.NONE
            ),
            l.loc_level_boss_baroness_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                    RuleRef("chalice")
                ],
                inherit=InheritMode.NONE
            ),
        },
    ),
    lv.level_boss_clown: LevelDef(
        exit_location=l.loc_level_boss_clown,
        access=[RulePreset(lrp.lrp_weapon)],
        base=[
            RulePreset(lrp.lrp_dash_or_parry),
        ],
        locations={
            l.loc_level_boss_clown: LocationDef(),
            l.loc_level_boss_clown_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_clown_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_clown_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                ],
            ),
            l.loc_level_boss_clown_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                ],
            ),
        },
    ),
    lv.level_boss_dragon: LevelDef(
        exit_location=l.loc_level_boss_dragon,
        access=[RulePreset(lrp.lrp_weapon)],
        base=[
            Or(
                RulePreset(lrp.lrp_dash),
                RulePreset(lrp.lrp_dlc_doublejump),
                options=[
                    DepFilter(deps.dep_dlc_chalice_only),
                    DepFilter(deps.dep_hard_logic, False)
                ]
            )
        ],
        locations={
            l.loc_level_boss_dragon: LocationDef(),
            l.loc_level_boss_dragon_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_dragon_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_dragon_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced),
                    Or(
                        RulePreset(lrp.lrp_dash),
                        RulePreset(lrp.lrp_dlc_doublejump),
                        options=[DepFilter(deps.dep_hard_logic, False)]
                    )
                ],
                inherit=InheritMode.NONE
            ),
            l.loc_level_boss_dragon_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced),
                    Or(
                        RulePreset(lrp.lrp_dash),
                        RulePreset(lrp.lrp_dlc_doublejump),
                        options=[DepFilter(deps.dep_hard_logic, False)]
                    )
                ],
                inherit=InheritMode.NONE
            ),
        },
    ),
    lv.level_boss_bee: LevelDef(
        exit_location=l.loc_level_boss_bee,
        access=[RulePreset(lrp.lrp_weapon)],
        locations={
            l.loc_level_boss_bee: LocationDef(),
            l.loc_level_boss_bee_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_bee_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_bee_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced),
                ],
            ),
            l.loc_level_boss_bee_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced),
                ],
            ),
        },
    ),
    lv.level_boss_pirate: LevelDef(
        exit_location=l.loc_level_boss_pirate,
        access=[RulePreset(lrp.lrp_weapon)],
        base=[
            Or(
                RulePreset(lrp.lrp_duck),
                And(
                    RulePreset(lrp.lrp_dash_and_parry),
                    RulePreset(
                        lrp.lrp_dlc_doublejump,
                        options=[
                            DepFilter(deps.dep_dlc_chalice_only)
                        ]
                    )
                ),
                options=[
                    DepFilter(deps.dep_rando_abilities),
                ]
            ),
        ],
        ruledefs={
            "chaliced": [
                Or(
                    RulePreset(lrp.lrp_duck),
                    And(
                        RulePreset(lrp.lrp_dash_and_parry),
                        RulePreset(lrp.lrp_dlc_doublejump)
                    ),
                    options=[
                        DepFilter(deps.dep_rando_abilities),
                    ]
                ),
            ]
        },
        locations={
            l.loc_level_boss_pirate: LocationDef(),
            l.loc_level_boss_pirate_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_pirate_phase1: LocationDef(
                inherit=InheritMode.NONE
            ),
            l.loc_level_boss_pirate_phase2: LocationDef(
                inherit=InheritMode.NONE
            ),
            l.loc_level_boss_pirate_phase3: LocationDef(
                inherit=InheritMode.NONE
            ),
            l.loc_level_boss_pirate_phase4: LocationDef(),
            l.loc_level_boss_pirate_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_pirate_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                    RuleRef("chaliced")
                ],
                inherit=InheritMode.NONE
            ),
            l.loc_level_boss_pirate_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                    RuleRef("chaliced")
                ],
                inherit=InheritMode.NONE
            ),
        },
    ),
    lv.level_boss_mouse: LevelDef(
        exit_location=l.loc_level_boss_mouse,
        access=[RulePreset(lrp.lrp_weapon)],
        base=[
            RulePreset(lrp.lrp_duck),
            RulePreset(
                lrp.lrp_parry,
                options=[
                    DepFilter(deps.dep_rando_abilities),
                    DepFilter(deps.dep_dlc_chalice_only)
                ]
            ),
            RulePreset(
                lrp.lrp_parry_or_psugar,
                options=[
                    DepFilter(deps.dep_rando_abilities),
                    DepFilter(deps.dep_dlc_chalice_only, False)
                ]
            ),
        ],
        locations={
            l.loc_level_boss_mouse: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_doublejump, options=[DepFilter(deps.dep_dlc_chalice_only)]),
                ]
            ),
            l.loc_level_boss_mouse_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                    RulePreset(lrp.lrp_dlc_doublejump, options=[DepFilter(deps.dep_dlc_chalice_only)])
                ],
            ),
            l.loc_level_boss_mouse_phase1: LocationDef(),
            l.loc_level_boss_mouse_phase2: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_doublejump, options=[DepFilter(deps.dep_dlc_chalice_only)]),
                ]
            ),
            l.loc_level_boss_mouse_phase3: LocationDef(),
            l.loc_level_boss_mouse_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_mouse_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                    RulePreset(lrp.lrp_dlc_doublejump)
                ],
            ),
            l.loc_level_boss_mouse_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                    RulePreset(lrp.lrp_dlc_doublejump)
                ],
            ),
        },
    ),
    lv.level_boss_sallystageplay: LevelDef(
        exit_location=l.loc_level_boss_sallystageplay,
        access=[RulePreset(lrp.lrp_weapon)],
        base=[
            RulePreset(lrp.lrp_parry),
            Or(
                RulePreset(lrp.lrp_dlc_doublejump),
                RulePreset(lrp.lrp_duck),
                options=[DepFilter(deps.dep_dlc_chalice_only)]
            ),
        ],
        ruledefs={
            "secret": [
                RulePreset(lrp.lrp_parry),
                RulePreset(
                    lrp.lrp_dlc_doublejump,
                    options=[DepFilter(deps.dep_dlc_chalice_only)]
                ),
            ]
        },
        locations={
            l.loc_level_boss_sallystageplay: LocationDef(),
            l.loc_level_boss_sallystageplay_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_sallystageplay_phase1: LocationDef(
                inherit=InheritMode.NONE
            ),
            l.loc_level_boss_sallystageplay_phase1s: LocationDef(
                rules=[RuleRef("secret")],
                inherit=InheritMode.NONE
            ),
            l.loc_level_boss_sallystageplay_phase2: LocationDef(
                inherit=InheritMode.NONE
            ),
            l.loc_level_boss_sallystageplay_phase2s: LocationDef(
                rules=[RuleRef("secret")],
                inherit=InheritMode.NONE
            ),
            l.loc_level_boss_sallystageplay_phase3: LocationDef(),
            l.loc_level_boss_sallystageplay_phase3s: LocationDef(
                rules=[RuleRef("secret")],
                inherit=InheritMode.NONE
            ),
            l.loc_level_boss_sallystageplay_phase4: LocationDef(),
            l.loc_level_boss_sallystageplay_phase4s: LocationDef(
                rules=[RuleRef("secret")],
                inherit=InheritMode.NONE
            ),
            l.loc_level_boss_sallystageplay_secret: LocationDef(
                rules=[RuleRef("secret")],
                inherit=InheritMode.NONE
            ),
            l.loc_level_boss_sallystageplay_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_sallystageplay_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                    Or(
                        RulePreset(lrp.lrp_dlc_doublejump),
                        RulePreset(lrp.lrp_duck),
                    ),
                ],
                inherit=InheritMode.NONE
            ),
            l.loc_level_boss_sallystageplay_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                    Or(
                        RulePreset(lrp.lrp_dlc_doublejump),
                        RulePreset(lrp.lrp_duck),
                    ),
                ],
                inherit=InheritMode.NONE
            ),
        },
    ),
    lv.level_boss_train: LevelDef(
        exit_location=l.loc_level_boss_train,
        access=[RulePreset(lrp.lrp_weapon)],
        base=[
            RulePreset(lrp.lrp_parry),
            RulePreset(
                lrp.lrp_dlc_doublejump,
                options=[
                    DepFilter(deps.dep_dlc_chalice_only),
                    DepFilter(deps.dep_hard_logic, False)
                ]
            ),
        ],
        locations={
            l.loc_level_boss_train: LocationDef(),
            l.loc_level_boss_train_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_train_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_train_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                    RulePreset(
                        lrp.lrp_dlc_doublejump,
                        options=[
                            DepFilter(deps.dep_dlc_chalice_only, False),
                            DepFilter(deps.dep_hard_logic, False)
                        ]
                    ),
                ],
            ),
            l.loc_level_boss_train_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                    RulePreset(
                        lrp.lrp_dlc_doublejump,
                        options=[
                            DepFilter(deps.dep_dlc_chalice_only, False),
                            DepFilter(deps.dep_hard_logic, False)
                        ]
                    ),
                ],
            ),
        },
    ),
    lv.level_boss_kingdice: LevelDef(
        exit_location=l.loc_level_boss_kingdice,
        access=[
            SelectRule(lrs.lrs_contract_req, False),
            RulePreset(lrp.lrp_weapon),
        ],
        base=[
            RulePreset(lrp.lrp_plane),
            RulePreset(lrp.lrp_dash_and_parry, options=[DepFilter(deps.dep_rando_abilities)]),
        ],
        locations={
            l.loc_level_boss_kingdice: LocationDef(),
            l.loc_level_boss_kingdice_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_kingdice_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_kingdice_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                ],
            ),
            l.loc_level_boss_kingdice_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                ],
            ),
        },
    ),
    lv.level_boss_plane_blimp: LevelDef(
        exit_location=l.loc_level_boss_plane_blimp,
        access=[
            RulePreset(lrp.lrp_plane),
        ],
        locations={
            l.loc_level_boss_plane_blimp: LocationDef(),
            l.loc_level_boss_plane_blimp_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_plane_topgrade),
                ],
            ),
            l.loc_level_boss_plane_blimp_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_plane_topgrade),
                ],
            ),
            l.loc_level_boss_plane_blimp_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
                ],
            ),
            l.loc_level_boss_plane_blimp_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
                ],
            ),
        },
    ),
    lv.level_boss_plane_genie: LevelDef(
        exit_location=l.loc_level_boss_plane_genie,
        access=[
            RulePreset(lrp.lrp_plane),
        ],
        locations={
            l.loc_level_boss_plane_genie: LocationDef(),
            l.loc_level_boss_plane_genie_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_plane_topgrade),
                ],
            ),
            l.loc_level_boss_plane_genie_secret: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_plane_shrink),
                ],
            ),
            l.loc_level_boss_plane_genie_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_plane_topgrade),
                ],
            ),
            l.loc_level_boss_plane_genie_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
                ],
            ),
            l.loc_level_boss_plane_genie_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
                ],
            ),
        },
    ),
    lv.level_boss_plane_bird: LevelDef(
        exit_location=l.loc_level_boss_plane_bird,
        access=[
            RulePreset(lrp.lrp_plane),
        ],
        base=[
            RBRule(Has(i.item_plane_gun, options=[DepFilter(deps.dep_hard_logic)])),
            RBRule(Has(i.item_plane_gun, options=[DepFilter(deps.dep_hard_logic, False)])),
            RBRule(Has(i.item_plane_bombs, options=[DepFilter(deps.dep_hard_logic, False)])),
        ],
        locations={
            l.loc_level_boss_plane_bird: LocationDef(),
            l.loc_level_boss_plane_bird_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_plane_topgrade),
                ],
            ),
            l.loc_level_boss_plane_bird_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_plane_topgrade),
                ],
            ),
            l.loc_level_boss_plane_bird_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
                ],
            ),
            l.loc_level_boss_plane_bird_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
                ],
            ),
        },
    ),
    lv.level_boss_plane_mermaid: LevelDef(
        exit_location=l.loc_level_boss_plane_mermaid,
        access=[
            RulePreset(lrp.lrp_plane),
        ],
        locations={
            l.loc_level_boss_plane_mermaid: LocationDef(),
            l.loc_level_boss_plane_mermaid_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_plane_topgrade),
                ],
            ),
            l.loc_level_boss_plane_mermaid_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_plane_topgrade),
                ],
            ),
            l.loc_level_boss_plane_mermaid_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
                ],
            ),
            l.loc_level_boss_plane_mermaid_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
                ],
            ),
        },
    ),
    lv.level_boss_plane_robot: LevelDef(
        exit_location=l.loc_level_boss_plane_robot,
        access=[
            RulePreset(lrp.lrp_plane),
            RulePreset(lrp.lrp_plane_parry, options=[DepFilter(deps.dep_rando_abilities)]),
        ],
        locations={
            l.loc_level_boss_plane_robot: LocationDef(),
            l.loc_level_boss_plane_robot_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_plane_topgrade),
                ],
            ),
            l.loc_level_boss_plane_robot_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_plane_topgrade),
                ],
            ),
            l.loc_level_boss_plane_robot_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
                ],
            ),
            l.loc_level_boss_plane_robot_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
                ],
            ),
        },
    ),
    lv.level_boss_devil: LevelDef(
        exit_location=None,
        access=[RulePreset(lrp.lrp_weapon)],
        base=[
            Or(
                RulePreset(lrp.lrp_dlc_doublejump),
                RulePreset(lrp.lrp_dash_and_parry),
                options=[
                    DepFilter(deps.dep_rando_abilities),
                    DepFilter(deps.dep_dlc_chalice_not_separate),
                    DepFilter(deps.dep_hard_logic)
                ]
            ),
            RulePreset(
                lrp.lrp_dash_and_parry,
                options=[
                    DepFilter(deps.dep_rando_abilities),
                    DepFilter(
                        (deps.dep_dlc_chalice_not_separate, deps.dep_hard_logic),
                        value=False,
                        any=True,
                    )
                ]
            ),
        ],
        locations={
            l.loc_level_boss_devil: LocationDef(),
            l.loc_level_boss_devil_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_devil_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_boss_devil_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                ],
            ),
            l.loc_level_boss_devil_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                ],
            ),
            l.loc_event_goal_devil: LocationDef(),
        },
    ),
    lv.level_dlc_boss_oldman: LevelDef(
        exit_location=l.loc_level_dlc_boss_oldman,
        access=[RulePreset(lrp.lrp_weapon)],
        base=[
            And(
                RulePreset(lrp.lrp_dash),
                RulePreset(lrp.lrp_parry_or_psugar),
                options=[DepFilter(deps.dep_rando_abilities)]
            ),
        ],
        locations={
            l.loc_level_dlc_boss_oldman: LocationDef(),
            l.loc_level_dlc_boss_oldman_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_dlc_boss_oldman_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                ],
            ),
            l.loc_level_dlc_boss_oldman_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                ],
            ),
        },
    ),
    lv.level_dlc_boss_rumrunners: LevelDef(
        exit_location=l.loc_level_dlc_boss_rumrunners,
        access=[RulePreset(lrp.lrp_weapon)],
        base=[
            RulePreset(lrp.lrp_duck_and_parry),
            RulePreset(
                lrp.lrp_dlc_doublejump,
                options=[
                    DepFilter(deps.dep_dlc_chalice_only)
                ]
            ),
        ],
        ruledefs={
            "early_phase": [
                RulePreset(lrp.lrp_duck),
                RulePreset(
                    lrp.lrp_dlc_doublejump,
                    options=[
                        DepFilter(deps.dep_dlc_chalice_only)
                    ]
                ),
            ]
        },
        locations={
            l.loc_level_dlc_boss_rumrunners: LocationDef(),
            l.loc_level_dlc_boss_rumrunners_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_dlc_boss_rumrunners_phase1: LocationDef(
                rules=[RuleRef("early_phase")],
                inherit=InheritMode.NONE
            ),
            l.loc_level_dlc_boss_rumrunners_phase2: LocationDef(
                rules=[RuleRef("early_phase")],
                inherit=InheritMode.NONE
            ),
            l.loc_level_dlc_boss_rumrunners_phase3: LocationDef(),
            l.loc_level_dlc_boss_rumrunners_phase4: LocationDef(),
            l.loc_level_dlc_boss_rumrunners_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                    RulePreset(
                        lrp.lrp_dlc_doublejump,
                        options=[
                            DepFilter(deps.dep_dlc_chalice_only, False)
                        ]
                    )
                ],
            ),
            l.loc_level_dlc_boss_rumrunners_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                    RulePreset(
                        lrp.lrp_dlc_doublejump,
                        options=[
                            DepFilter(deps.dep_dlc_chalice_only, False)
                        ]
                    )
                ],
            ),
        },
    ),
    lv.level_dlc_boss_snowcult: LevelDef(
        exit_location=l.loc_level_dlc_boss_snowcult,
        access=[RulePreset(lrp.lrp_weapon)],
        base=[
            RulePreset(
                lrp.lrp_dlc_doublejump,
                options=[
                    DepFilter(deps.dep_dlc_chalice_only),
                    DepFilter(deps.dep_hard_logic, False)
                ]
            ),
        ],
        ruledefs={
            "chaliced": [
                RulePreset(lrp.lrp_dlc_boss_chaliced),
                RulePreset(lrp.lrp_dlc_doublejump, options=[DepFilter(deps.dep_hard_logic, False)]),
            ],
        },
        locations={
            l.loc_level_dlc_boss_snowcult: LocationDef(),
            l.loc_level_dlc_boss_snowcult_topgrade: LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)],
            ),
            l.loc_level_dlc_boss_snowcult_dlc_chaliced: LocationDef(
                rules=[RuleRef("chaliced")],
            ),
            l.loc_level_dlc_boss_snowcult_event_dlc_chaliced: LocationDef(
                rules=[RuleRef("chaliced")],
            ),
        },
    ),
    lv.level_dlc_boss_airplane: LevelDef(
        exit_location=l.loc_level_dlc_boss_airplane,
        access=[RulePreset(lrp.lrp_weapon)],
        base=[
            RulePreset(lrp.lrp_duck_or_dash, options=[DepFilter(deps.dep_dlc_chalice_only, False)]),
            RulePreset(
                lrp.lrp_duck_or_dash,
                options=[
                    DepFilter(deps.dep_dlc_chalice_only), DepFilter(deps.dep_hard_logic)
                ]
            ),
            Or(
                RulePreset(lrp.lrp_duck),
                And(
                    RulePreset(lrp.lrp_dash),
                    RulePreset(lrp.lrp_dlc_doublejump)
                ),
                options=[
                    DepFilter(deps.dep_dlc_chalice_only),
                    DepFilter(deps.dep_hard_logic, False)
                ]
            ),
        ],
        ruledefs={
            "chaliced": [
                RulePreset(lrp.lrp_dlc_cookie),
                RulePreset(lrp.lrp_duck_or_dash, options=[DepFilter(deps.dep_hard_logic)]),
                Or(
                    RulePreset(lrp.lrp_duck),
                    And(
                        RulePreset(lrp.lrp_dash),
                        RulePreset(lrp.lrp_dlc_doublejump)
                    ),
                    options=[DepFilter(deps.dep_hard_logic, False)]
                ),
            ],
        },
        locations={
            l.loc_level_dlc_boss_airplane: LocationDef(),
            l.loc_level_dlc_boss_airplane_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_plane_topgrade),
                ],
            ),
            l.loc_level_dlc_boss_airplane_secret: LocationDef(),
            l.loc_level_dlc_boss_airplane_dlc_chaliced: LocationDef(
                rules=[RuleRef("chaliced")],
            ),
            l.loc_level_dlc_boss_airplane_event_dlc_chaliced: LocationDef(
                rules=[RuleRef("chaliced")],
            ),
        },
    ),
    lv.level_dlc_boss_plane_cowboy: LevelDef(
        exit_location=l.loc_level_dlc_boss_plane_cowboy,
        access=[
            RulePreset(lrp.lrp_plane),
        ],
        locations={
            l.loc_level_dlc_boss_plane_cowboy: LocationDef(),
            l.loc_level_dlc_boss_plane_cowboy_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_plane_topgrade),
                ],
            ),
            l.loc_level_dlc_boss_plane_cowboy_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
                ],
            ),
            l.loc_level_dlc_boss_plane_cowboy_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
                ],
            ),
        },
    ),
    lv.level_dlc_boss_saltbaker: LevelDef(
        exit_location=None,
        access=[
            SelectRule(lrs.lrs_dlc_ingredient_req, False),
            RulePreset(lrp.lrp_weapon)
        ],
        base=[
            RulePreset(lrp.lrp_parry, options=[DepFilter(deps.dep_rando_abilities)]),
            RulePreset(
                lrp.lrp_dlc_doublejump,
                options=[DepFilter(deps.dep_dlc_chalice_only)]
            )
        ],
        locations={
            l.loc_level_dlc_boss_saltbaker: LocationDef(),
            l.loc_level_dlc_boss_saltbaker_topgrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_dlc_boss_saltbaker_phase1: LocationDef(
                rules=[
                    RulePreset(
                        lrp.lrp_dlc_doublejump,
                        options=[
                            DepFilter(deps.dep_dlc_chalice_only),
                            DepFilter(deps.dep_hard_logic, False)
                        ]
                    )
                ],
                inherit=InheritMode.NONE
            ),
            l.loc_level_dlc_boss_saltbaker_phase2: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_parry, options=[DepFilter(deps.dep_rando_abilities)]),
                    RulePreset(
                        lrp.lrp_dlc_doublejump,
                        options=[
                            DepFilter(deps.dep_dlc_chalice_only),
                            DepFilter(deps.dep_hard_logic, False)
                        ]
                    )
                ],
                inherit=InheritMode.NONE
            ),
            l.loc_level_dlc_boss_saltbaker_phase3: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_parry, options=[DepFilter(deps.dep_rando_abilities)]),
                    RulePreset(
                        lrp.lrp_dlc_doublejump,
                        options=[
                            DepFilter(deps.dep_dlc_chalice_only),
                            DepFilter(deps.dep_hard_logic, False)
                        ]
                    )
                ],
                inherit=InheritMode.NONE
            ),
            l.loc_level_dlc_boss_saltbaker_phase4: LocationDef(),
            l.loc_level_dlc_boss_saltbaker_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_topgrade),
                ],
            ),
            l.loc_level_dlc_boss_saltbaker_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                    RulePreset(lrp.lrp_dlc_doublejump),
                ],
                inherit=InheritMode.NONE
            ),
            l.loc_level_dlc_boss_saltbaker_event_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                    RulePreset(lrp.lrp_dlc_doublejump),
                ],
                inherit=InheritMode.NONE
            ),
            l.loc_event_dlc_goal_saltbaker: LocationDef(),
        },
    ),
    lv.level_dicepalace_boss_booze: LevelDef(
        exit_location=None,
        access=[RulePreset(lrp.lrp_weapon)],
        locations={
            l.loc_level_dicepalace_boss_booze: LocationDef(),
            l.loc_level_dicepalace_boss_booze_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced),
                ],
            ),
        },
    ),
    lv.level_dicepalace_boss_chips: LevelDef(
        exit_location=None,
        access=[RulePreset(lrp.lrp_weapon)],
        locations={
            l.loc_level_dicepalace_boss_chips: LocationDef(),
            l.loc_level_dicepalace_boss_chips_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced),
                ],
            ),
        },
    ),
    lv.level_dicepalace_boss_cigar: LevelDef(
        exit_location=None,
        access=[RulePreset(lrp.lrp_weapon)],
        base=[RulePreset(lrp.lrp_dash)],
        locations={
            l.loc_level_dicepalace_boss_cigar: LocationDef(),
            l.loc_level_dicepalace_boss_cigar_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced),
                ],
            ),
        },
    ),
    lv.level_dicepalace_boss_domino: LevelDef(
        exit_location=None,
        access=[RulePreset(lrp.lrp_weapon)],
        locations={
            l.loc_level_dicepalace_boss_domino: LocationDef(),
            l.loc_level_dicepalace_boss_domino_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced),
                ],
            ),
        },
    ),
    lv.level_dicepalace_boss_rabbit: LevelDef(
        exit_location=None,
        access=[RulePreset(lrp.lrp_weapon)],
        base=[
            RulePreset(lrp.lrp_parry),
        ],
        locations={
            l.loc_level_dicepalace_boss_rabbit: LocationDef(
                rules=[
                    RulePreset(
                        lrp.lrp_dlc_doublejump,
                        options=[DepFilter(deps.dep_dlc_chalice_only)]
                    )
                ]
            ),
            l.loc_level_dicepalace_boss_rabbit_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced),
                    RulePreset(lrp.lrp_dlc_doublejump)
                ],
            ),
        },
    ),
    lv.level_dicepalace_boss_plane_horse: LevelDef(
        exit_location=None,
        access=[
            RulePreset(lrp.lrp_plane),
        ],
        locations={
            l.loc_level_dicepalace_boss_plane_horse: LocationDef(),
            l.loc_level_dicepalace_boss_plane_horse_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
                ],
            ),
        },
    ),
    lv.level_dicepalace_boss_roulette: LevelDef(
        exit_location=None,
        access=[RulePreset(lrp.lrp_weapon)],
        locations={
            l.loc_level_dicepalace_boss_roulette: LocationDef(),
            l.loc_level_dicepalace_boss_roulette_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced),
                ],
            ),
        },
    ),
    lv.level_dicepalace_boss_eightball: LevelDef(
        exit_location=None,
        access=[RulePreset(lrp.lrp_weapon)],
        locations={
            l.loc_level_dicepalace_boss_eightball: LocationDef(),
            l.loc_level_dicepalace_boss_eightball_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_chaliced),
                ],
            ),
        },
    ),
    lv.level_dicepalace_boss_plane_memory: LevelDef(
        exit_location=None,
        access=[
            RulePreset(lrp.lrp_plane),
        ],
        locations={
            l.loc_level_dicepalace_boss_plane_memory: LocationDef(),
            l.loc_level_dicepalace_boss_plane_memory_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
                ],
            ),
        },
    ),
    lv.level_rungun_forest: LevelDef(
        exit_location=l.loc_level_rungun_forest,
        base=[
            RulePreset(lrp.lrp_rungun_weapon),
            RulePreset(lrp.lrp_dash),
        ],
        locations={
            l.loc_level_rungun_forest: LocationDef(),
            l.loc_level_rungun_forest_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_topgrade),
                ],
            ),
            l.loc_level_rungun_forest_pacifist: LocationDef(),
            l.loc_level_rungun_forest_coin1: LocationDef(
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_forest_coin2: LocationDef(
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_forest_coin3: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_parry),
                ],
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_forest_coin4: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dash),
                ],
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_forest_coin5: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_weapon),
                    RulePreset(lrp.lrp_dash),
                ],
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_forest_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_rungun_chaliced),
                ],
            ),
            l.loc_level_rungun_forest_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_topgrade),
                ],
            ),
            l.loc_level_rungun_forest_event_pacifist: LocationDef(),
        },
    ),
    lv.level_rungun_tree: LevelDef(
        exit_location=l.loc_level_rungun_tree,
        base=[
            RulePreset(lrp.lrp_dash),
            RulePreset(lrp.lrp_dlc_doublejump, options=[DepFilter(deps.dep_dlc_chalice_only)])
        ],
        locations={
            l.loc_level_rungun_tree: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_weapon),
                ],
            ),
            l.loc_level_rungun_tree_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_weapon),
                    RulePreset(lrp.lrp_rungun_topgrade),
                ],
            ),
            l.loc_level_rungun_tree_pacifist: LocationDef(),
            l.loc_level_rungun_tree_coin1: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_parry),
                ],
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_tree_coin2: LocationDef(
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_tree_coin3: LocationDef(
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_tree_coin4: LocationDef(),
            l.loc_level_rungun_tree_coin5: LocationDef(),
            l.loc_level_rungun_tree_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_weapon),
                    RulePreset(lrp.lrp_dlc_rungun_chaliced),
                    RulePreset(lrp.lrp_dlc_doublejump, options=[DepFilter(deps.dep_dlc_chalice_only, False)]),
                ],
            ),
            l.loc_level_rungun_tree_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_weapon),
                    RulePreset(lrp.lrp_rungun_topgrade),
                ],
            ),
            l.loc_level_rungun_tree_event_pacifist: LocationDef(),
        },
    ),
    lv.level_rungun_circus: LevelDef(
        exit_location=l.loc_level_rungun_circus,
        base=[
            RulePreset(lrp.lrp_rungun_weapon),
            RulePreset(lrp.lrp_parry_or_psugar),
            RulePreset(
                lrp.lrp_dlc_doublejump,
                options=[
                    DepFilter(deps.dep_dlc_chalice_only),
                    DepFilter(deps.dep_hard_logic, False)
                ]
            )
        ],
        locations={
            l.loc_level_rungun_circus: LocationDef(),
            l.loc_level_rungun_circus_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_topgrade, options=[DepFilter(deps.dep_hard_logic, False)]),
                ],
            ),
            l.loc_level_rungun_circus_pacifist: LocationDef(),
            l.loc_level_rungun_circus_coin1: LocationDef(
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_circus_coin2: LocationDef(
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_circus_coin3: LocationDef(),
            l.loc_level_rungun_circus_coin4: LocationDef(),
            l.loc_level_rungun_circus_coin5: LocationDef(),
            l.loc_level_rungun_circus_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_rungun_chaliced),
                    RulePreset(lrp.lrp_dash_and_parry),
                    RulePreset(
                        lrp.lrp_dlc_doublejump,
                        options=[
                            DepFilter(deps.dep_dlc_chalice_only, False),
                            DepFilter(deps.dep_hard_logic, False)
                        ]
                    )
                ],
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_circus_event_agrade: LocationDef(
                rules=[
                    RulePreset(
                        lrp.lrp_rungun_topgrade,
                        options=[DepFilter(deps.dep_hard_logic, False)]
                    ),
                ],
            ),
            l.loc_level_rungun_circus_event_pacifist: LocationDef(),
        },
    ),
    lv.level_rungun_funhouse: LevelDef(
        exit_location=l.loc_level_rungun_funhouse,
        base=[
            RulePreset(lrp.lrp_rungun_weapon),
            RulePreset(
                lrp.lrp_parry,
                options=[
                    DepFilter(deps.dep_rando_abilities),
                    DepFilter(deps.dep_dlc_chalice_only)
                ]
            ),
            Or(
                RulePreset(lrp.lrp_parry),
                And(RBRule(Has(i.item_charm_psugar)), RulePreset(lrp.lrp_dash)),
                options=[
                    DepFilter(deps.dep_rando_abilities),
                    DepFilter(deps.dep_dlc_chalice_only, False)
                ]
            ),
        ],
        locations={
            l.loc_level_rungun_funhouse: LocationDef(),
            l.loc_level_rungun_funhouse_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_topgrade),
                ],
            ),
            l.loc_level_rungun_funhouse_pacifist: LocationDef(),
            l.loc_level_rungun_funhouse_coin1: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_parry_or_psugar),
                ],
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_funhouse_coin2: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_weapon),
                    RulePreset(lrp.lrp_parry_or_psugar),
                ],
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_funhouse_coin3: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_weapon),
                    RulePreset(lrp.lrp_parry_or_psugar),
                ],
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_funhouse_coin4: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_weapon),
                    RulePreset(lrp.lrp_parry_or_psugar),
                ],
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_funhouse_coin5: LocationDef(),
            l.loc_level_rungun_funhouse_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_rungun_chaliced),
                ],
            ),
            l.loc_level_rungun_funhouse_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_topgrade),
                ],
            ),
            l.loc_level_rungun_funhouse_event_pacifist: LocationDef(),
        },
    ),
    lv.level_rungun_harbour: LevelDef(
        exit_location=l.loc_level_rungun_harbour,
        base=[
            RulePreset(lrp.lrp_rungun_weapon),
            RulePreset(lrp.lrp_dash_and_parry),
            RulePreset(lrp.lrp_dlc_doublejump, options=[DepFilter(deps.dep_dlc_chalice_only)])
        ],
        locations={
            l.loc_level_rungun_harbour: LocationDef(),
            l.loc_level_rungun_harbour_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_topgrade),
                ],
            ),
            l.loc_level_rungun_harbour_pacifist: LocationDef(),
            l.loc_level_rungun_harbour_coin1: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_weapon),
                    RulePreset(lrp.lrp_dash_parry_or_psugar),
                ],
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_harbour_coin2: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_weapon),
                ],
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_harbour_coin3: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_weapon),
                    RulePreset(lrp.lrp_parry_or_psugar),
                ],
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_harbour_coin4: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_weapon),
                    Or(RulePreset(lrp.lrp_parry), And(RBRule(Has(i.item_charm_psugar)), RulePreset(lrp.lrp_dash))),
                    RulePreset(lrp.lrp_dlc_doublejump, options=[DepFilter(deps.dep_dlc_chalice_only)])
                ],
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_harbour_coin5: LocationDef(),
            l.loc_level_rungun_harbour_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_rungun_chaliced),
                    RulePreset(lrp.lrp_dlc_doublejump, options=[DepFilter(deps.dep_dlc_chalice_only, False)])
                ],
            ),
            l.loc_level_rungun_harbour_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_topgrade),
                ],
            ),
            l.loc_level_rungun_harbour_event_pacifist: LocationDef(),
        },
    ),
    lv.level_rungun_mountain: LevelDef(
        exit_location=l.loc_level_rungun_mountain,
        base=[
            RulePreset(lrp.lrp_rungun_weapon),
            RulePreset(lrp.lrp_dash, options=[DepFilter(deps.dep_dlc_chalice, False)]),
            Or(RulePreset(lrp.lrp_dash), RulePreset(lrp.lrp_dlc_doublejump), options=[DepFilter(deps.dep_dlc_chalice)]),
        ],
        locations={
            l.loc_level_rungun_mountain: LocationDef(),
            l.loc_level_rungun_mountain_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_topgrade),
                ],
            ),
            l.loc_level_rungun_mountain_pacifist: LocationDef(),
            l.loc_level_rungun_mountain_coin1: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_weapon),
                ],
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_mountain_coin2: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_weapon),
                    RulePreset(lrp.lrp_dash_or_dlc_doublejump),
                ],
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_mountain_coin3: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_weapon),
                ],
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_mountain_coin4: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_weapon),
                    RulePreset(lrp.lrp_dlc_doublejump, options=[DepFilter(deps.dep_dlc_chalice_only)])
                ],
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_mountain_coin5: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_weapon),
                    RulePreset(lrp.lrp_dash_or_dlc_doublejump),
                ],
                inherit=InheritMode.NONE,
            ),
            l.loc_level_rungun_mountain_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_rungun_chaliced),
                ],
            ),
            l.loc_level_rungun_mountain_event_agrade: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_rungun_topgrade),
                ],
            ),
            l.loc_level_rungun_mountain_event_pacifist: LocationDef(),
        },
    ),
    lv.level_mausoleum_i: LevelDef(
        exit_location=None,
        access=[
            RulePreset(lrp.lrp_parry),
        ],
        locations={
        },
    ),
    lv.level_mausoleum_ii: LevelDef(
        exit_location=None,
        access=[
            RulePreset(lrp.lrp_parry),
        ],
        locations={
        },
    ),
    lv.level_mausoleum_iii: LevelDef(
        exit_location=None,
        access=[
            RulePreset(lrp.lrp_parry),
        ],
        locations={
        },
    ),
    lv.level_dlc_chesscastle_pawn: LevelDef(
        exit_location=None,
        access=[
            RulePreset(lrp.lrp_parry),
        ],
        locations={
            l.loc_level_dlc_chesscastle_pawn: LocationDef(),
            l.loc_level_dlc_chesscastle_pawn_dlc_chaliced: LocationDef(),
        },
    ),
    lv.level_dlc_chesscastle_knight: LevelDef(
        exit_location=None,
        access=[
            RulePreset(lrp.lrp_parry),
        ],
        locations={
            l.loc_level_dlc_chesscastle_knight: LocationDef(
                rules=[
                    RulePreset(
                        lrp.lrp_dlc_doublejump,
                        options=[DepFilter(deps.dep_dlc_chalice_only)]
                    ),
                ],
            ),
            l.loc_level_dlc_chesscastle_knight_dlc_chaliced: LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_doublejump),
                ],
            ),
        },
    ),
    lv.level_dlc_chesscastle_bishop: LevelDef(
        exit_location=None,
        access=[
            RulePreset(lrp.lrp_parry),
        ],
        locations={
            l.loc_level_dlc_chesscastle_bishop: LocationDef(),
            l.loc_level_dlc_chesscastle_bishop_dlc_chaliced: LocationDef(),
        },
    ),
    lv.level_dlc_chesscastle_rook: LevelDef(
        exit_location=None,
        access=[
            RulePreset(lrp.lrp_parry),
        ],
        locations={
            l.loc_level_dlc_chesscastle_rook: LocationDef(),
            l.loc_level_dlc_chesscastle_rook_dlc_chaliced: LocationDef(),
        },
    ),
    lv.level_dlc_chesscastle_queen: LevelDef(
        exit_location=None,
        access=[
            RulePreset(lrp.lrp_parry),
        ],
        locations={
            l.loc_level_dlc_chesscastle_queen: LocationDef(),
            l.loc_level_dlc_chesscastle_queen_dlc_chaliced: LocationDef(),
        },
    ),
    lv.level_dlc_chesscastle_run: LevelDef(
        exit_location=None,
        access=[
            RulePreset(lrp.lrp_parry),
        ],
        locations={
            l.loc_level_dlc_chesscastle_run: LocationDef(),
            l.loc_level_dlc_chesscastle_run_dlc_chaliced: LocationDef(),
        },
    ),
    lv.level_tutorial: LevelDef(
        exit_location=None,
        access=[
            RulePreset(lrp.lrp_weapon),
            RulePreset(lrp.lrp_duck_dash_and_parry),
        ],
        locations={},
    ),
    lv.level_dlc_tutorial: LevelDef(
        exit_location=None,
        access=[
            RulePreset(lrp.lrp_dlc_cookie),
        ],
        locations={
            l.loc_level_dlc_tutorial_coin: LocationDef(
                rules=[
                    And(RulePreset(lrp.lrp_dash_and_parry), RulePreset(lrp.lrp_dlc_doublejump)),
                ],
            ),
        },
    ),
    lv.level_dlc_graveyard: LevelDef(
        exit_location=None,
        access=[
            RulePreset(lrp.lrp_weapon),
            RBRule(Has(i.item_charm_dlc_broken_relic)),
        ],
        locations={
            l.loc_level_dlc_graveyard: LocationDef(
                rules=[
                    And(RulePreset(lrp.lrp_dash_and_parry), RulePreset(lrp.lrp_dlc_doublejump)),
                ],
            ),
        },
    ),
})
