### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

import unittest
from collections.abc import Iterable
from typing import cast

from ..world.names import regionnames as lv
from ..world.rules.dep import deps
from ..world.rules.dep.depbase import Dep
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
        names: set[str] = set()
        for filter_ in TestLevelRulesStructure._iter_filters(expr):
            names.update(dep.__name__ for dep in filter_.fns)
        return names

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


class TestDepFilter(unittest.TestCase):
    @staticmethod
    def _dep_true(_: object) -> bool:
        return True

    @staticmethod
    def _dep_false(_: object) -> bool:
        return False

    def test_depfilter_all_mode(self):
        true_dep: Dep = cast(Dep, self._dep_true)
        false_dep: Dep = cast(Dep, self._dep_false)

        self.assertTrue(DepFilter((true_dep, true_dep), value=True, any=False)(object()))  # type: ignore[arg-type]
        self.assertFalse(DepFilter((true_dep, false_dep), value=True, any=False)(object()))  # type: ignore[arg-type]
        self.assertFalse(DepFilter((true_dep, false_dep), value=False, any=False)(object()))  # type: ignore[arg-type]
        self.assertTrue(DepFilter((false_dep, false_dep), value=False, any=False)(object()))  # type: ignore[arg-type]

    def test_depfilter_any_mode(self):
        true_dep: Dep = cast(Dep, self._dep_true)
        false_dep: Dep = cast(Dep, self._dep_false)

        self.assertTrue(DepFilter((false_dep, true_dep), value=True, any=True)(object()))  # type: ignore[arg-type]
        self.assertFalse(DepFilter((false_dep, false_dep), value=True, any=True)(object()))  # type: ignore[arg-type]
        self.assertTrue(DepFilter((true_dep, false_dep), value=False, any=True)(object()))  # type: ignore[arg-type]
        self.assertTrue(DepFilter((false_dep, false_dep), value=False, any=True)(object()))  # type: ignore[arg-type]

    def test_depfilter_dict_roundtrip(self):
        single = DepFilter(deps.dep_hard_logic)
        single_roundtrip = DepFilter.from_dict(single.to_dict())
        self.assertEqual(single.to_dict(), single_roundtrip.to_dict())

        multi = DepFilter((deps.dep_dlc_chalice_not_separate, deps.dep_hard_logic), value=False, any=True)
        multi_roundtrip = DepFilter.from_dict(multi.to_dict())
        self.assertEqual(multi.to_dict(), multi_roundtrip.to_dict())

    def test_depfilter_to_dict_shapes(self):
        single = DepFilter(deps.dep_hard_logic).to_dict()
        self.assertEqual(single["when"], "hard_logic")
        self.assertIs(single["condition"], True)
        self.assertIs(single["any"], False)

        multi = DepFilter((deps.dep_hard_logic, deps.dep_rando_abilities), value=False, any=True).to_dict()
        self.assertEqual(multi["when"], ("hard_logic", "rando_abilities"))
        self.assertIs(multi["condition"], False)
        self.assertIs(multi["any"], True)

    def test_depfilter_from_dict_defaults(self):
        parsed = DepFilter.from_dict({"when": "hard_logic"})
        self.assertEqual(parsed.to_dict(), {"when": "hard_logic", "condition": True, "any": False})

    def test_depfilter_from_dict_invalid_when(self):
        with self.assertRaisesRegex(ValueError, "^Dep dict must contain a non-empty string 'when' value\\.$"):
            DepFilter.from_dict({"when": " "})
        with self.assertRaisesRegex(ValueError, "^Dep dict 'when' tuple/list cannot be empty\\.$"):
            DepFilter.from_dict({"when": []})
        with self.assertRaisesRegex(
            ValueError,
            "^Dep dict 'when' list/tuple must contain only non-empty strings\\.$"
        ):
            DepFilter.from_dict({"when": ["hard_logic", ""]})
        with self.assertRaisesRegex(
            ValueError,
            "^Dep dict must contain either a string or list/tuple of strings for 'when'\\.$"
        ):
            DepFilter.from_dict({"when": 7})  # type: ignore[arg-type]

    def test_depfilter_from_dict_invalid_flags_and_unknown(self):
        with self.assertRaisesRegex(ValueError, "^Dep dict 'condition' must be a bool\\.$"):
            DepFilter.from_dict({"when": "hard_logic", "condition": 1})  # type: ignore[arg-type]
        with self.assertRaisesRegex(ValueError, "^Dep dict 'any' must be a bool\\.$"):
            DepFilter.from_dict({"when": "hard_logic", "any": "no"})  # type: ignore[arg-type]
        with self.assertRaisesRegex(ValueError, "^Unknown dep name\\(s\\): not_real_dep\\.$"):
            DepFilter.from_dict({"when": "not_real_dep"})

    def test_depfilter_init_validation(self):
        with self.assertRaisesRegex(ValueError, "^DepFilter requires at least one dep\\.$"):
            DepFilter(())  # type: ignore[arg-type]
        with self.assertRaisesRegex(ValueError, "^DepFilter deps must be callable\\.$"):
            DepFilter((deps.dep_hard_logic, cast(Dep, 5)))  # type: ignore[arg-type]

    def test_depfilter_check_invalid_options(self):
        with self.assertRaisesRegex(ValueError, "^DepFilter options is invalid\\.$"):
            DepFilter(deps.dep_hard_logic).check(cast(object, object()))  # type: ignore[arg-type]

    def test_depfilter_str(self):
        self.assertEqual(str(DepFilter(deps.dep_hard_logic)), "hard_logic")
        self.assertEqual(str(DepFilter(deps.dep_hard_logic, value=False)), "!hard_logic")
        self.assertEqual(
            str(DepFilter((deps.dep_hard_logic, deps.dep_rando_abilities), value=True, any=False)),
            "(hard_logic&rando_abilities)",
        )
        self.assertEqual(
            str(DepFilter((deps.dep_hard_logic, deps.dep_rando_abilities), value=False, any=True)),
            "!(hard_logic|rando_abilities)",
        )

    def test_level_boss_devil_fallback_depfilter(self):
        devil = ldefs.levelrules.levels[lv.level_boss_devil]
        fallback = devil.base[1]
        if not isinstance(fallback, lrb.RulePreset):
            self.fail("Expected level_boss_devil fallback to be RulePreset.")

        fallback_filter = next(f for f in fallback.options if isinstance(f, DepFilter) and len(f.fns) == 2)
        self.assertEqual(tuple(dep.__name__ for dep in fallback_filter.fns), (
            "dep_dlc_chalice_not_separate",
            "dep_hard_logic",
        ))
        self.assertTrue(fallback_filter.any)
        self.assertFalse(fallback_filter.value)
