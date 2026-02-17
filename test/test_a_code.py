### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

import unittest

from ..world.levels import levelids
from ..world.options.optionbase import _levelset
from ..world.rules.levelrules.legacy.levelruledata import LevelRuleData


class TestCode(unittest.TestCase):
    def test_level_set(self):
        self.assertEqual(_levelset.levels, set(levelids.level_ids.values()))

    def test_levelrule_data_parser(self):
        data = LevelRuleData.get_data()
        self.assertTrue(data)
