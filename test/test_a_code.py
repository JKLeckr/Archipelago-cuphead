import unittest
from ..options.optionbase import _levelset
from ..levels import levelids

class TestCode(unittest.TestCase):
    def test_level_set(self):
        self.assertEqual(_levelset.levels, set(levelids.level_ids.values()))
