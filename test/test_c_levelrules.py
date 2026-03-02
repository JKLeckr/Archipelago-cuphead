### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

import unittest
from collections.abc import Iterable

from ..world.rules.dep.depfilter import DepFilter
from ..world.rules.levelrules import levelrulebase as lrb
from ..world.rules.levelrules import levelruledefs as ldefs
from ..world.rules.levelrules import levelrulepresets as lrp


class TestLevelRulesStructure(unittest.TestCase):
    @staticmethod
    def _iter_exprs(rule_list: Iterable[lrb.RuleExpr]) -> Iterable[lrb.RuleExpr]:
        for expr in rule_list:
            yield expr
            match expr:
                case lrb.And() | lrb.Or():
                    yield from TestLevelRulesStructure._iter_exprs(expr.items)
                case lrb.RulePreset():
                    yield from TestLevelRulesStructure._iter_exprs(expr.rules)
                case _:
                    continue

    @staticmethod
    def _iter_filters(expr: lrb.RuleExpr) -> Iterable[DepFilter]:
        expr_filters = getattr(expr, "options", ())
        for f in expr_filters:
            if isinstance(f, DepFilter):
                yield f

        if isinstance(expr, lrb.RBRule):
            for f in getattr(expr.rule, "options", ()):
                if isinstance(f, DepFilter):
                    yield f

    @staticmethod
    def _filter_names(expr: lrb.RuleExpr) -> set[str]:
        return {f.fn.__name__ for f in TestLevelRulesStructure._iter_filters(expr)}

    def test_rulepreset_refs_are_registered(self):
        preset_names = {fn.__name__ for fn in lrb.LRPRESETS.values()}

        for level_name, level in ldefs.levelrules.levels.items():
            source_lists = [level.access, level.base]
            source_lists.extend(level.ruledefs.values())
            source_lists.extend(loc.rules for loc in level.locations.values())
            for expr in self._iter_exprs([x for y in source_lists for x in y]):
                if isinstance(expr, lrb.RulePreset):
                    with self.subTest(level=level_name, preset=expr.preset_name):
                        self.assertIn(expr.preset_name, preset_names)

    def test_ruleref_is_level_local(self):
        for level_name, level in ldefs.levelrules.levels.items():
            local_defs = set(level.ruledefs.keys())
            source_lists = [level.access, level.base]
            source_lists.extend(loc.rules for loc in level.locations.values())

            for expr in self._iter_exprs([x for y in source_lists for x in y]):
                if isinstance(expr, lrb.RuleRef):
                    with self.subTest(level=level_name, ref=expr.ref_name):
                        self.assertIn(expr.ref_name, local_defs)

    def test_ruledefs_do_not_contain_ruleref(self):
        for level_name, level in ldefs.levelrules.levels.items():
            for def_name, rule_list in level.ruledefs.items():
                for expr in self._iter_exprs(rule_list):
                    with self.subTest(level=level_name, ruledef=def_name, expr=type(expr).__name__):
                        self.assertNotIsInstance(expr, lrb.RuleRef)

    def test_ability_sensitive_presets_have_rando_filter(self):
        dash_and_parry = lrp.lrp_dash_and_parry()
        self.assertTrue(dash_and_parry)
        for expr in dash_and_parry:
            with self.subTest(preset="lrp_dash_and_parry", expr=type(expr).__name__):
                self.assertIn("dep_rando_abilities", self._filter_names(expr))

        dash_or_doublejump = lrp.lrp_dash_or_dlc_doublejump()
        self.assertTrue(dash_or_doublejump)
        for expr in dash_or_doublejump:
            if isinstance(expr, lrb.RBRule):
                with self.subTest(preset="lrp_dash_or_dlc_doublejump", expr=type(expr).__name__):
                    self.assertIn("dep_rando_abilities", self._filter_names(expr))
