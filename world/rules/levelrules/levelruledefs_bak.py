### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from rule_builder.rules import Has

from ...names import itemnames as n
from ..dep import deps
from ..dep.depfilter import DepFilter
from . import levelrulepresets as lrp
from .levelrulebase import (
    And,
    InheritMode,
    LevelDef,
    LevelRules,
    LocationDef,
    Or,
    RBRule,
    RuleList,
    RulePreset,
    RuleRef,
    SelectRule,
)
from .levelruleselectors import LRSELECTORS

_ruledefs_level_dlc_boss_airplane: dict[str, RuleList] = {
    "chaliced":
        RuleList([
            RulePreset(lrp.lrp_dlc_cookie),
            RulePreset(lrp.lrp_duck_or_dash, options=[DepFilter(deps.dep_hard_logic)]),
            Or(
                RulePreset(lrp.lrp_duck),
                And(
                    RulePreset(lrp.lrp_dash),
                    RulePreset(lrp.lrp_dlc_doublejump),
                ),
                options=[
                    DepFilter(deps.dep_hard_logic, False),
                ],
            ),
        ])
    ,
}

_ruledefs_level_dlc_boss_snowcult: dict[str, RuleList] = {
    "chaliced":
        RuleList([
            RulePreset(lrp.lrp_dlc_boss_chaliced),
            RulePreset(lrp.lrp_dlc_doublejump, options=[DepFilter(deps.dep_hard_logic, False)]),
        ])
    ,
}

levelrule_boss: dict[str, LevelDef] = {
    "level_boss_baroness": LevelDef(
        exit_location="loc_level_boss_baroness",
        access=[],
        base=
            RuleList([
                RulePreset(lrp.lrp_parry_or_psugar),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_boss_baroness": LocationDef(
                rules=[]
            ),
            "loc_level_boss_baroness_topgrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_baroness_event_agrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_baroness_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
            "loc_level_boss_baroness_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
        },
    ),
    "level_boss_bee": LevelDef(
        exit_location="loc_level_boss_bee",
        access=[],
        base=[],
        ruledefs={},
        locations={
            "loc_level_boss_bee": LocationDef(
                rules=[]
            ),
            "loc_level_boss_bee_topgrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_bee_event_agrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_bee_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced),
            ]),
            "loc_level_boss_bee_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced),
            ]),
        },
    ),
    "level_boss_clown": LevelDef(
        exit_location="loc_level_boss_clown",
        access=[],
        base=
            RuleList([
                RulePreset(lrp.lrp_dash_or_parry),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_boss_clown": LocationDef(
                rules=[]
            ),
            "loc_level_boss_clown_topgrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_clown_event_agrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_clown_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
            "loc_level_boss_clown_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
        },
    ),
    "level_boss_dragon": LevelDef(
        exit_location="loc_level_boss_dragon",
        access=[],
        base=[],
        ruledefs={},
        locations={
            "loc_level_boss_dragon": LocationDef(
                rules=[]
            ),
            "loc_level_boss_dragon_topgrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_dragon_event_agrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_dragon_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced),
            ]),
            "loc_level_boss_dragon_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced),
            ]),
        },
    ),
    "level_boss_flower": LevelDef(
        exit_location="loc_level_boss_flower",
        access=[],
        base=[],
        ruledefs={},
        locations={
            "loc_level_boss_flower": LocationDef(
                rules=[]
            ),
            "loc_level_boss_flower_topgrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_flower_event_agrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_flower_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced),
            ]),
            "loc_level_boss_flower_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced),
            ]),
        },
    ),
    "level_boss_frogs": LevelDef(
        exit_location="loc_level_boss_frogs",
        access=[],
        base=
            RuleList([
                RulePreset(lrp.lrp_parry_or_psugar),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_boss_frogs": LocationDef(
                rules=[]
            ),
            "loc_level_boss_frogs_topgrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_frogs_event_agrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_frogs_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
            "loc_level_boss_frogs_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
        },
    ),
    "level_boss_kingdice": LevelDef(
        exit_location="loc_level_boss_kingdice",
        access=
            RuleList([
                SelectRule(LRSELECTORS["contract_req"], False),
            ])
        ,
        base=
            RuleList([
                RulePreset(lrp.lrp_plane),
                RulePreset(lrp.lrp_dash_and_parry, options=[DepFilter(deps.dep_rando_abilities)]),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_boss_kingdice": LocationDef(
                rules=[]
            ),
            "loc_level_boss_kingdice_topgrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_kingdice_event_agrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_kingdice_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
            "loc_level_boss_kingdice_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
        },
    ),
    "level_boss_mouse": LevelDef(
        exit_location="loc_level_boss_mouse",
        access=[],
        base=
            RuleList([
                RulePreset(lrp.lrp_duck),
                RulePreset(
                    lrp.lrp_parry,
                    options=[
                        DepFilter(deps.dep_rando_abilities),
                        DepFilter(deps.dep_dlc_chalice_only),
                    ],
                ),
                RulePreset(
                    lrp.lrp_parry_or_psugar,
                    options=[
                        DepFilter(deps.dep_rando_abilities),
                        DepFilter(deps.dep_dlc_chalice_only, False),
                    ],
                ),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_boss_mouse": LocationDef(
                rules=[]
            ),
            "loc_level_boss_mouse_topgrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_mouse_event_agrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_mouse_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
            "loc_level_boss_mouse_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
        },
    ),
    "level_boss_pirate": LevelDef(
        exit_location="loc_level_boss_pirate",
        access=[],
        base=
            RuleList([
                RulePreset(
                    lrp.lrp_duck,
                    options=[
                        DepFilter(deps.dep_rando_abilities),
                        DepFilter(deps.dep_dlc_chalice_only),
                    ],
                ),
                Or(
                    RulePreset(lrp.lrp_duck),
                    And(
                        RulePreset(lrp.lrp_parry),
                        RulePreset(lrp.lrp_dash),
                    ),
                    options=[
                        DepFilter(deps.dep_rando_abilities),
                        DepFilter(deps.dep_dlc_chalice_only, False),
                    ],
                ),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_boss_pirate": LocationDef(
                rules=[]
            ),
            "loc_level_boss_pirate_topgrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_pirate_event_agrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_pirate_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
            "loc_level_boss_pirate_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
        },
    ),
    "level_boss_sallystageplay": LevelDef(
        exit_location="loc_level_boss_sallystageplay",
        access=[],
        base=
            RuleList([
                RulePreset(lrp.lrp_parry),
                RulePreset(lrp.lrp_dlc_doublejump, options=[DepFilter(deps.dep_dlc_chalice_only)]),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_boss_sallystageplay": LocationDef(
                rules=[]
            ),
            "loc_level_boss_sallystageplay_topgrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_sallystageplay_secret": LocationDef(
                rules=[]
            ),
            "loc_level_boss_sallystageplay_event_agrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_sallystageplay_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
            "loc_level_boss_sallystageplay_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
        },
    ),
    "level_boss_slime": LevelDef(
        exit_location="loc_level_boss_slime",
        access=[],
        base=
            RuleList([
                RulePreset(lrp.lrp_duck_or_dash),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_boss_slime": LocationDef(
                rules=[]
            ),
            "loc_level_boss_slime_topgrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_slime_event_agrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_slime_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
            "loc_level_boss_slime_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
        },
    ),
    "level_boss_train": LevelDef(
        exit_location="loc_level_boss_train",
        access=[],
        base=
            RuleList([
                RulePreset(lrp.lrp_parry),
                RulePreset(lrp.lrp_dlc_doublejump, options=[DepFilter(deps.dep_dlc_chalice_only)]),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_boss_train": LocationDef(
                rules=[]
            ),
            "loc_level_boss_train_topgrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_train_event_agrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_train_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
            "loc_level_boss_train_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
        },
    ),
    "level_boss_veggies": LevelDef(
        exit_location="loc_level_boss_veggies",
        access=[],
        base=[],
        ruledefs={},
        locations={
            "loc_level_boss_veggies": LocationDef(
                rules=[]
            ),
            "loc_level_boss_veggies_topgrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_veggies_secret": LocationDef(
                rules=[]
            ),
            "loc_level_boss_veggies_event_agrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_veggies_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced),
            ]),
            "loc_level_boss_veggies_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced),
            ]),
        },
    ),
}

levelrule_boss_plane: dict[str, LevelDef] = {
    "level_boss_plane_bird": LevelDef(
        exit_location="loc_level_boss_plane_bird",
        access=
            RuleList([
                RulePreset(lrp.lrp_plane),
            ])
        ,
        base=
            RuleList([
                And(
                    RBRule(Has(n.item_plane_gun)),
                    options=[
                        DepFilter(deps.dep_hard_logic),
                    ],
                ),
                And(
                    RBRule(Has(n.item_plane_gun)),
                    options=[
                        DepFilter(deps.dep_hard_logic, False),
                    ],
                ),
                And(
                    RBRule(Has(n.item_plane_bombs)),
                    options=[
                        DepFilter(deps.dep_hard_logic, False),
                    ],
                ),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_boss_plane_bird": LocationDef(
                rules=[]
            ),
            "loc_level_boss_plane_bird_topgrade": LocationDef(rules=[
                RulePreset(lrp.lrp_plane_topgrade),
            ]),
            "loc_level_boss_plane_bird_event_agrade": LocationDef(rules=[
                RulePreset(lrp.lrp_plane_topgrade),
            ]),
            "loc_level_boss_plane_bird_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
            ]),
            "loc_level_boss_plane_bird_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
            ]),
        },
    ),
    "level_boss_plane_blimp": LevelDef(
        exit_location="loc_level_boss_plane_blimp",
        access=
            RuleList([
                RulePreset(lrp.lrp_plane),
            ])
        ,
        base=[],
        ruledefs={},
        locations={
            "loc_level_boss_plane_blimp": LocationDef(
                rules=[]
            ),
            "loc_level_boss_plane_blimp_topgrade": LocationDef(rules=[
                RulePreset(lrp.lrp_plane_topgrade),
            ]),
            "loc_level_boss_plane_blimp_event_agrade": LocationDef(rules=[
                RulePreset(lrp.lrp_plane_topgrade),
            ]),
            "loc_level_boss_plane_blimp_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
            ]),
            "loc_level_boss_plane_blimp_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
            ]),
        },
    ),
    "level_boss_plane_genie": LevelDef(
        exit_location="loc_level_boss_plane_genie",
        access=
            RuleList([
                RulePreset(lrp.lrp_plane),
            ])
        ,
        base=[],
        ruledefs={},
        locations={
            "loc_level_boss_plane_genie": LocationDef(
                rules=[]
            ),
            "loc_level_boss_plane_genie_topgrade": LocationDef(rules=[
                RulePreset(lrp.lrp_plane_topgrade),
            ]),
            "loc_level_boss_plane_genie_secret": LocationDef(rules=[
                RulePreset(lrp.lrp_plane_shrink),
            ]),
            "loc_level_boss_plane_genie_event_agrade": LocationDef(rules=[
                RulePreset(lrp.lrp_plane_topgrade),
            ]),
            "loc_level_boss_plane_genie_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
            ]),
            "loc_level_boss_plane_genie_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
            ]),
        },
    ),
    "level_boss_plane_mermaid": LevelDef(
        exit_location="loc_level_boss_plane_mermaid",
        access=
            RuleList([
                RulePreset(lrp.lrp_plane),
            ])
        ,
        base=[],
        ruledefs={},
        locations={
            "loc_level_boss_plane_mermaid": LocationDef(
                rules=[]
            ),
            "loc_level_boss_plane_mermaid_topgrade": LocationDef(rules=[
                RulePreset(lrp.lrp_plane_topgrade),
            ]),
            "loc_level_boss_plane_mermaid_event_agrade": LocationDef(rules=[
                RulePreset(lrp.lrp_plane_topgrade),
            ]),
            "loc_level_boss_plane_mermaid_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
            ]),
            "loc_level_boss_plane_mermaid_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
            ]),
        },
    ),
    "level_boss_plane_robot": LevelDef(
        exit_location="loc_level_boss_plane_robot",
        access=
            RuleList([
                RulePreset(lrp.lrp_plane),
                RulePreset(lrp.lrp_plane_parry, options=[DepFilter(deps.dep_rando_abilities)]),
            ])
        ,
        base=[],
        ruledefs={},
        locations={
            "loc_level_boss_plane_robot": LocationDef(
                rules=[]
            ),
            "loc_level_boss_plane_robot_topgrade": LocationDef(rules=[
                RulePreset(lrp.lrp_plane_topgrade),
            ]),
            "loc_level_boss_plane_robot_event_agrade": LocationDef(rules=[
                RulePreset(lrp.lrp_plane_topgrade),
            ]),
            "loc_level_boss_plane_robot_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
            ]),
            "loc_level_boss_plane_robot_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
            ]),
        },
    ),
}

levelrule_boss_final: dict[str, LevelDef] = {
    "level_boss_devil": LevelDef(
        exit_location="",
        access=[],
        base=
            RuleList([
                RulePreset(
                    lrp.lrp_parry,
                    options=[
                        DepFilter(deps.dep_rando_abilities),
                        DepFilter(deps.dep_dlc_chalice_only),
                    ],
                ),
                RulePreset(
                    lrp.lrp_dash_and_parry,
                    options=[
                        DepFilter(deps.dep_rando_abilities),
                        DepFilter(deps.dep_dlc_chalice_only, False),
                    ],
                ),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_boss_devil": LocationDef(
                rules=[]
            ),
            "loc_level_boss_devil_topgrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_devil_event_agrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_boss_devil_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
            "loc_level_boss_devil_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
            "loc_event_goal_devil": LocationDef(
                rules=[]
            ),
        },
    ),
}

levelrule_dlc_boss: dict[str, LevelDef] = {
    "level_dlc_boss_airplane": LevelDef(
        exit_location="loc_level_dlc_boss_airplane",
        access=[],
        base=
            RuleList([
                RulePreset(lrp.lrp_duck_or_dash, options=[DepFilter(deps.dep_dlc_chalice_only, False)]),
                RulePreset(
                    lrp.lrp_duck_or_dash,
                    options=[
                        DepFilter(deps.dep_dlc_chalice_only),
                        DepFilter(deps.dep_hard_logic),
                    ],
                ),
                Or(
                    RulePreset(lrp.lrp_duck),
                    And(
                        RulePreset(lrp.lrp_dash),
                        RulePreset(lrp.lrp_dlc_doublejump),
                    ),
                    options=[
                        DepFilter(deps.dep_dlc_chalice_only),
                        DepFilter(deps.dep_hard_logic, False),
                    ],
                ),
            ])
        ,
        ruledefs=_ruledefs_level_dlc_boss_airplane,
        locations={
            "loc_level_dlc_boss_airplane": LocationDef(
                rules=[]
            ),
            "loc_level_dlc_boss_airplane_topgrade": LocationDef(rules=[
                RulePreset(lrp.lrp_plane_topgrade),
            ]),
            "loc_level_dlc_boss_airplane_secret": LocationDef(
                rules=[]
            ),
            "loc_level_dlc_boss_airplane_dlc_chaliced": LocationDef(rules=[
                RuleRef(_ruledefs_level_dlc_boss_airplane, "chaliced"),
            ]),
            "loc_level_dlc_boss_airplane_event_dlc_chaliced": LocationDef(rules=[
                RuleRef(_ruledefs_level_dlc_boss_airplane, "chaliced"),
            ]),
        },
    ),
    "level_dlc_boss_oldman": LevelDef(
        exit_location="loc_level_dlc_boss_oldman",
        access=[],
        base=
            RuleList([
                And(
                    RulePreset(lrp.lrp_dash),
                    RulePreset(lrp.lrp_parry_or_psugar),
                    options=[
                        DepFilter(deps.dep_rando_abilities),
                    ],
                ),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_dlc_boss_oldman": LocationDef(
                rules=[]
            ),
            "loc_level_dlc_boss_oldman_topgrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_dlc_boss_oldman_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
            "loc_level_dlc_boss_oldman_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
        },
    ),
    "level_dlc_boss_rumrunners": LevelDef(
        exit_location="loc_level_dlc_boss_rumrunners",
        access=[],
        base=
            RuleList([
                RulePreset(lrp.lrp_duck_and_parry),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_dlc_boss_rumrunners": LocationDef(
                rules=[]
            ),
            "loc_level_dlc_boss_rumrunners_topgrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_dlc_boss_rumrunners_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
            "loc_level_dlc_boss_rumrunners_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
            ]),
        },
    ),
    "level_dlc_boss_snowcult": LevelDef(
        exit_location="loc_level_dlc_boss_snowcult",
        access=[],
        base=
            RuleList([
                RulePreset(
                    lrp.lrp_dlc_doublejump,
                    options=[
                        DepFilter(deps.dep_dlc_chalice_only),
                        DepFilter(deps.dep_hard_logic, False),
                    ],
                ),
            ])
        ,
        ruledefs=_ruledefs_level_dlc_boss_snowcult,
        locations={
            "loc_level_dlc_boss_snowcult": LocationDef(
                rules=[]
            ),
            "loc_level_dlc_boss_snowcult_topgrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_dlc_boss_snowcult_dlc_chaliced": LocationDef(rules=[
                RuleRef(_ruledefs_level_dlc_boss_snowcult, "chaliced"),
            ]),
            "loc_level_dlc_boss_snowcult_event_dlc_chaliced": LocationDef(rules=[
                RuleRef(_ruledefs_level_dlc_boss_snowcult, "chaliced"),
            ]),
        },
    ),
}

levelrule_dlc_boss_plane: dict[str, LevelDef] = {
    "level_dlc_boss_plane_cowboy": LevelDef(
        exit_location="loc_level_dlc_boss_plane_cowboy",
        access=
            RuleList([
                RulePreset(lrp.lrp_plane),
            ])
        ,
        base=[],
        ruledefs={},
        locations={
            "loc_level_dlc_boss_plane_cowboy": LocationDef(
                rules=[]
            ),
            "loc_level_dlc_boss_plane_cowboy_topgrade": LocationDef(rules=[
                RulePreset(lrp.lrp_plane_topgrade),
            ]),
            "loc_level_dlc_boss_plane_cowboy_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
            ]),
            "loc_level_dlc_boss_plane_cowboy_event_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
            ]),
        },
    ),
}

levelrule_dlc_boss_final: dict[str, LevelDef] = {
    "level_dlc_boss_saltbaker": LevelDef(
        exit_location="",
        access=
            RuleList([
                SelectRule(LRSELECTORS["dlc_ingredient_req"], False),
            ])
        ,
        base=
            RuleList([
                RulePreset(lrp.lrp_parry, options=[DepFilter(deps.dep_rando_abilities)]),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_dlc_boss_saltbaker": LocationDef(
                rules=[]
            ),
            "loc_level_dlc_boss_saltbaker_topgrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_dlc_boss_saltbaker_event_agrade": LocationDef(
                rules=[RulePreset(lrp.lrp_topgrade)]
            ),
            "loc_level_dlc_boss_saltbaker_dlc_chaliced": LocationDef(rules=[
                And(
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                    RulePreset(lrp.lrp_dlc_doublejump),
                ),
            ]),
            "loc_level_dlc_boss_saltbaker_event_dlc_chaliced": LocationDef(rules=[
                And(
                    RulePreset(lrp.lrp_dlc_boss_chaliced_parry),
                    RulePreset(lrp.lrp_dlc_doublejump),
                ),
            ]),
            "loc_event_dlc_goal_saltbaker": LocationDef(
                rules=[]
            ),
        },
    ),
}

levelrule_dicepalace: dict[str, LevelDef] = {
    "level_dicepalace_boss_booze": LevelDef(
        exit_location="",
        access=[],
        base=[],
        ruledefs={},
        locations={
            "loc_level_dicepalace_boss_booze": LocationDef(
                rules=[]
            ),
            "loc_level_dicepalace_boss_booze_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced),
            ]),
        },
    ),
    "level_dicepalace_boss_chips": LevelDef(
        exit_location="",
        access=[],
        base=[],
        ruledefs={},
        locations={
            "loc_level_dicepalace_boss_chips": LocationDef(
                rules=[]
            ),
            "loc_level_dicepalace_boss_chips_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced),
            ]),
        },
    ),
    "level_dicepalace_boss_cigar": LevelDef(
        exit_location="",
        access=[],
        base=[],
        ruledefs={},
        locations={
            "loc_level_dicepalace_boss_cigar": LocationDef(
                rules=[]
            ),
            "loc_level_dicepalace_boss_cigar_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced),
            ]),
        },
    ),
    "level_dicepalace_boss_domino": LevelDef(
        exit_location="",
        access=[],
        base=[],
        ruledefs={},
        locations={
            "loc_level_dicepalace_boss_domino": LocationDef(
                rules=[]
            ),
            "loc_level_dicepalace_boss_domino_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced),
            ]),
        },
    ),
    "level_dicepalace_boss_eightball": LevelDef(
        exit_location="",
        access=[],
        base=[],
        ruledefs={},
        locations={
            "loc_level_dicepalace_boss_eightball": LocationDef(
                rules=[]
            ),
            "loc_level_dicepalace_boss_eightball_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced),
            ]),
        },
    ),
    "level_dicepalace_boss_plane_horse": LevelDef(
        exit_location="",
        access=
            RuleList([
                RulePreset(lrp.lrp_plane),
            ])
        ,
        base=[],
        ruledefs={},
        locations={
            "loc_level_dicepalace_boss_plane_horse": LocationDef(
                rules=[]
            ),
            "loc_level_dicepalace_boss_plane_horse_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
            ]),
        },
    ),
    "level_dicepalace_boss_plane_memory": LevelDef(
        exit_location="",
        access=
            RuleList([
                RulePreset(lrp.lrp_plane),
            ])
        ,
        base=[],
        ruledefs={},
        locations={
            "loc_level_dicepalace_boss_plane_memory": LocationDef(
                rules=[]
            ),
            "loc_level_dicepalace_boss_plane_memory_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_plane_chaliced),
            ]),
        },
    ),
    "level_dicepalace_boss_rabbit": LevelDef(
        exit_location="",
        access=[],
        base=[],
        ruledefs={},
        locations={
            "loc_level_dicepalace_boss_rabbit": LocationDef(
                rules=[]
            ),
            "loc_level_dicepalace_boss_rabbit_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced),
            ]),
        },
    ),
    "level_dicepalace_boss_roulette": LevelDef(
        exit_location="",
        access=[],
        base=[],
        ruledefs={},
        locations={
            "loc_level_dicepalace_boss_roulette": LocationDef(
                rules=[]
            ),
            "loc_level_dicepalace_boss_roulette_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_boss_chaliced),
            ]),
        },
    ),
}

levelrule_rungun: dict[str, LevelDef] = {
    "level_rungun_circus": LevelDef(
        exit_location="loc_level_rungun_circus",
        access=[],
        base=
            RuleList([
                RulePreset(lrp.lrp_parry_or_psugar),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_rungun_circus": LocationDef(
                rules=[]
            ),
            "loc_level_rungun_circus_agrade": LocationDef(rules=[
                RulePreset(lrp.lrp_rungun_topgrade, options=[DepFilter(deps.dep_hard_logic, False)]),
            ]),
            "loc_level_rungun_circus_pacifist": LocationDef(
                rules=[]
            ),
            "loc_level_rungun_circus_coin1": LocationDef(
                rules=[],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_circus_coin2": LocationDef(
                rules=[],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_circus_coin3": LocationDef(
                rules=[
                    RulePreset(lrp.lrp_parry_or_psugar)
                ],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_circus_coin4": LocationDef(
                rules=[
                    RulePreset(lrp.lrp_parry_or_psugar)
                ],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_circus_coin5": LocationDef(
                rules=[
                    RulePreset(lrp.lrp_parry_or_psugar)
                ],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_circus_dlc_chaliced": LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dlc_rungun_chaliced)
                ],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_circus_event_agrade": LocationDef(rules=[
                RulePreset(lrp.lrp_rungun_topgrade, options=[DepFilter(deps.dep_hard_logic, False)]),
            ]),
            "loc_level_rungun_circus_event_pacifist": LocationDef(
                rules=[]
            ),
        },
    ),
    "level_rungun_forest": LevelDef(
        exit_location="loc_level_rungun_forest",
        access=[],
        base=
            RuleList([
                RulePreset(lrp.lrp_dash),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_rungun_forest": LocationDef(
                rules=[]
            ),
            "loc_level_rungun_forest_agrade": LocationDef(rules=[
                RulePreset(lrp.lrp_rungun_topgrade),
            ]),
            "loc_level_rungun_forest_pacifist": LocationDef(
                rules=[]
            ),
            "loc_level_rungun_forest_coin1": LocationDef(
                rules=[],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_forest_coin2": LocationDef(
                rules=[],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_forest_coin3": LocationDef(
                rules=[
                    RulePreset(lrp.lrp_parry)
                ],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_forest_coin4": LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dash)
                ],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_forest_coin5": LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dash)
                ],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_forest_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_rungun_chaliced),
            ]),
            "loc_level_rungun_forest_event_agrade": LocationDef(rules=[
                RulePreset(lrp.lrp_rungun_topgrade),
            ]),
            "loc_level_rungun_forest_event_pacifist": LocationDef(
                rules=[]
            ),
        },
    ),
    "level_rungun_funhouse": LevelDef(
        exit_location="loc_level_rungun_funhouse",
        access=[],
        base=
            RuleList([
                RulePreset(
                    lrp.lrp_parry,
                    options=[
                        DepFilter(deps.dep_rando_abilities),
                        DepFilter(deps.dep_dlc_chalice_only),
                    ],
                ),
                Or(
                    RulePreset(lrp.lrp_parry),
                    And(
                        RBRule(Has(n.item_charm_psugar)),
                        RulePreset(lrp.lrp_dash),
                    ),
                    options=[
                        DepFilter(deps.dep_rando_abilities),
                        DepFilter(deps.dep_dlc_chalice_only, False),
                    ],
                ),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_rungun_funhouse": LocationDef(
                rules=[]
            ),
            "loc_level_rungun_funhouse_agrade": LocationDef(rules=[
                RulePreset(lrp.lrp_rungun_topgrade),
            ]),
            "loc_level_rungun_funhouse_pacifist": LocationDef(
                rules=[]
            ),
            "loc_level_rungun_funhouse_coin1": LocationDef(
                rules=[
                    RulePreset(lrp.lrp_parry_or_psugar)
                ],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_funhouse_coin2": LocationDef(
                rules=[
                    RulePreset(lrp.lrp_parry_or_psugar)
                ],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_funhouse_coin3": LocationDef(
                rules=[
                    RulePreset(lrp.lrp_parry_or_psugar)
                ],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_funhouse_coin4": LocationDef(
                rules=[
                    RulePreset(lrp.lrp_parry_or_psugar)
                ],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_funhouse_coin5": LocationDef(
                rules=[]
            ),
            "loc_level_rungun_funhouse_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_rungun_chaliced),
            ]),
            "loc_level_rungun_funhouse_event_agrade": LocationDef(rules=[
                RulePreset(lrp.lrp_rungun_topgrade),
            ]),
            "loc_level_rungun_funhouse_event_pacifist": LocationDef(
                rules=[]
            ),
        },
    ),
    "level_rungun_harbour": LevelDef(
        exit_location="loc_level_rungun_harbour",
        access=[],
        base=
            RuleList([
                RulePreset(lrp.lrp_dash_and_parry),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_rungun_harbour": LocationDef(
                rules=[]
            ),
            "loc_level_rungun_harbour_agrade": LocationDef(rules=[
                RulePreset(lrp.lrp_rungun_topgrade),
            ]),
            "loc_level_rungun_harbour_pacifist": LocationDef(
                rules=[]
            ),
            "loc_level_rungun_harbour_coin1": LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dash_parry_or_psugar)
                ],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_harbour_coin2": LocationDef(
                rules=[],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_harbour_coin3": LocationDef(
                rules=[
                    RulePreset(lrp.lrp_parry_or_psugar)
                ],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_harbour_coin4": LocationDef(
                rules=[
                    Or(
                        RulePreset(lrp.lrp_parry),
                        And(
                            RBRule(Has(n.item_charm_psugar)),
                            RulePreset(lrp.lrp_dash),
                        ),
                    ),
                ],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_harbour_coin5": LocationDef(
                rules=[]
            ),
            "loc_level_rungun_harbour_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_rungun_chaliced),
            ]),
            "loc_level_rungun_harbour_event_agrade": LocationDef(rules=[
                RulePreset(lrp.lrp_rungun_topgrade),
            ]),
            "loc_level_rungun_harbour_event_pacifist": LocationDef(
                rules=[]
            ),
        },
    ),
    "level_rungun_mountain": LevelDef(
        exit_location="loc_level_rungun_mountain",
        access=[],
        base=
            RuleList([
                RulePreset(lrp.lrp_dash, options=[DepFilter(deps.dep_dlc_chalice, False)]),
                Or(
                    RulePreset(lrp.lrp_dash),
                    RulePreset(lrp.lrp_dlc_doublejump),
                    options=[
                        DepFilter(deps.dep_dlc_chalice),
                    ],
                ),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_rungun_mountain": LocationDef(
                rules=[]
            ),
            "loc_level_rungun_mountain_agrade": LocationDef(rules=[
                RulePreset(lrp.lrp_rungun_topgrade),
            ]),
            "loc_level_rungun_mountain_pacifist": LocationDef(
                rules=[]
            ),
            "loc_level_rungun_mountain_coin1": LocationDef(
                rules=[],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_mountain_coin2": LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dash_or_dlc_doublejump)
                ],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_mountain_coin3": LocationDef(
                rules=[],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_mountain_coin4": LocationDef(
                rules=[],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_mountain_coin5": LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dash_or_dlc_doublejump)
                ],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_mountain_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_rungun_chaliced),
            ]),
            "loc_level_rungun_mountain_event_agrade": LocationDef(rules=[
                RulePreset(lrp.lrp_rungun_topgrade),
            ]),
            "loc_level_rungun_mountain_event_pacifist": LocationDef(
                rules=[]
            ),
        },
    ),
    "level_rungun_tree": LevelDef(
        exit_location="loc_level_rungun_tree",
        access=[],
        base=
            RuleList([
                RulePreset(lrp.lrp_dash),
            ])
        ,
        ruledefs={},
        locations={
            "loc_level_rungun_tree": LocationDef(
                rules=[]
            ),
            "loc_level_rungun_tree_agrade": LocationDef(rules=[
                RulePreset(lrp.lrp_rungun_topgrade),
            ]),
            "loc_level_rungun_tree_pacifist": LocationDef(
                rules=[]
            ),
            "loc_level_rungun_tree_coin1": LocationDef(
                rules=[
                    RulePreset(lrp.lrp_parry)
                ],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_tree_coin2": LocationDef(
                rules=[],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_tree_coin3": LocationDef(
                rules=[],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_tree_coin4": LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dash)
                ],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_tree_coin5": LocationDef(
                rules=[
                    RulePreset(lrp.lrp_dash)
                ],
                inherit=InheritMode.NONE,
            ),
            "loc_level_rungun_tree_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dlc_rungun_chaliced),
            ]),
            "loc_level_rungun_tree_event_agrade": LocationDef(rules=[
                RulePreset(lrp.lrp_rungun_topgrade),
            ]),
            "loc_level_rungun_tree_event_pacifist": LocationDef(
                rules=[]
            ),
        },
    ),
}

levelrule_mausoleum: dict[str, LevelDef] = {
    "level_mausoleum_i": LevelDef(
        exit_location="",
        access=
            RuleList([
                RulePreset(lrp.lrp_parry),
            ])
        ,
        base=[],
        ruledefs={},
        locations={
        },
    ),
    "level_mausoleum_ii": LevelDef(
        exit_location="",
        access=
            RuleList([
                RulePreset(lrp.lrp_parry),
            ])
        ,
        base=[],
        ruledefs={},
        locations={
        },
    ),
    "level_mausoleum_iii": LevelDef(
        exit_location="",
        access=
            RuleList([
                RulePreset(lrp.lrp_parry),
            ])
        ,
        base=[],
        ruledefs={},
        locations={
        },
    ),
}

levelrule_dlc_chesscastle: dict[str, LevelDef] = {
    "level_dlc_chesscastle_bishop": LevelDef(
        exit_location="",
        access=
            RuleList([
                RulePreset(lrp.lrp_parry),
            ])
        ,
        base=[],
        ruledefs={},
        locations={
            "loc_level_dlc_chesscastle_bishop_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dash_and_parry),
            ]),
        },
    ),
    "level_dlc_chesscastle_knight": LevelDef(
        exit_location="",
        access=
            RuleList([
                RulePreset(lrp.lrp_parry),
            ])
        ,
        base=[],
        ruledefs={},
        locations={
            "loc_level_dlc_chesscastle_knight_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dash_and_parry),
            ]),
        },
    ),
    "level_dlc_chesscastle_pawn": LevelDef(
        exit_location="",
        access=
            RuleList([
                RulePreset(lrp.lrp_parry),
            ])
        ,
        base=[],
        ruledefs={},
        locations={
            "loc_level_dlc_chesscastle_pawn_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dash_and_parry),
            ]),
        },
    ),
    "level_dlc_chesscastle_queen": LevelDef(
        exit_location="",
        access=
            RuleList([
                RulePreset(lrp.lrp_parry),
            ])
        ,
        base=[],
        ruledefs={},
        locations={
            "loc_level_dlc_chesscastle_queen_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dash_and_parry),
            ]),
        },
    ),
    "level_dlc_chesscastle_rook": LevelDef(
        exit_location="",
        access=
            RuleList([
                RulePreset(lrp.lrp_parry),
            ])
        ,
        base=[],
        ruledefs={},
        locations={
            "loc_level_dlc_chesscastle_rook_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dash_and_parry),
            ]),
        },
    ),
    "level_dlc_chesscastle_run": LevelDef(
        exit_location="",
        access=
            RuleList([
                RulePreset(lrp.lrp_parry),
            ])
        ,
        base=[],
        ruledefs={},
        locations={
            "loc_level_dlc_chesscastle_run_dlc_chaliced": LocationDef(rules=[
                RulePreset(lrp.lrp_dash_and_parry),
            ]),
        },
    ),
}

levelrule_special: dict[str, LevelDef] = {
    "level_dlc_graveyard": LevelDef(
        exit_location="",
        access=
            RuleList([
                RBRule(Has(n.item_charm_dlc_broken_relic)),
            ])
        ,
        base=[],
        ruledefs={},
        locations={
            "loc_level_dlc_graveyard": LocationDef(rules=[
                And(
                    RulePreset(lrp.lrp_dash_and_parry),
                    RulePreset(lrp.lrp_dlc_doublejump),
                ),
            ]),
        },
    ),
    "level_dlc_tutorial": LevelDef(
        exit_location="",
        access=
            RuleList([
                RulePreset(lrp.lrp_dlc_cookie),
            ])
        ,
        base=[],
        ruledefs={},
        locations={
            "loc_level_dlc_tutorial_coin": LocationDef(rules=[
                And(
                    RulePreset(lrp.lrp_dash_and_parry),
                    RulePreset(lrp.lrp_dlc_doublejump),
                ),
            ]),
        },
    ),
    "level_tutorial": LevelDef(
        exit_location="",
        access=
            RuleList([
                RulePreset(lrp.lrp_duck_dash_and_parry),
            ])
        ,
        base=[],
        ruledefs={},
        locations={
        },
    ),
}

levelrules_all = LevelRules({
    **levelrule_boss,
    **levelrule_boss_plane,
    **levelrule_boss_final,
    **levelrule_dlc_boss,
    **levelrule_dlc_boss_plane,
    **levelrule_dlc_boss_final,
    **levelrule_dicepalace,
    **levelrule_rungun,
    **levelrule_mausoleum,
    **levelrule_dlc_chesscastle,
    **levelrule_special,
})
