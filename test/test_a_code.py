### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

import unittest

from ..levels import levelids
from ..options.optionbase import _levelset


class TestCode(unittest.TestCase):
    def test_level_set(self):
        self.assertEqual(_levelset.levels, set(levelids.level_ids.values()))
