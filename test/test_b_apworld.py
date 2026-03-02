### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

import unittest
from dataclasses import fields
from types import SimpleNamespace
from typing import ClassVar

from Options import PerGameCommonOptions

from ..world.enums import WeaponMode
from ..world.items import itemdefs as idefs
from ..world.items import itemsetup, weapons
from ..world.names import itemnames


class TestAPWorldOptionsWConf(unittest.TestCase):
    exclude_options: ClassVar[set[str]] = {
        "version",
        "start_maxhealth",
        "start_maxhealth_p2",
        "deathlink",
        "deathlink_grace_count",
        "extra_coins",
        "music_shuffle",
        "ducklock_platdrop",
    }
    exclude_options_start: ClassVar[set[str]] = {
        "filler_weight_",
        "trap_weight_",
    }

    _base_options: ClassVar[set[str]] = {x.name for x in fields(PerGameCommonOptions)}

    @classmethod
    def _check_option_name_is_valid(cls, oname: str) -> bool:
        if oname in cls.exclude_options or oname in cls._base_options:
            return False

        for eopt in cls.exclude_options_start:
            if oname.startswith(eopt):
                return False

        return True

class TestAPWorldItemSetup(unittest.TestCase):
    @staticmethod
    def _options_for_weapon_mode(mode: WeaponMode):
        return SimpleNamespace(
            weapon_mode=SimpleNamespace(evalue=mode),
            use_dlc=SimpleNamespace(bvalue=True),
            boss_grade_checks=SimpleNamespace(evalue=0),
            rungun_grade_checks=SimpleNamespace(evalue=0),
            dlc_boss_chalice_checks=SimpleNamespace(evalue=0),
        )

    def test_setup_weapons(self):
        _start_weapon = itemnames.item_weapon_peashooter

        self.assertEqual(weapons.weapon_dict[0], _start_weapon)

        modes: list[tuple[str, WeaponMode]] = [
            ("Normal", WeaponMode.NORMAL),
            ("Progressive", WeaponMode.PROGRESSIVE),
            ("Progressive Except Start", WeaponMode.PROGRESSIVE_EXCEPT_START),
            ("Ex Separate", WeaponMode.EX_SEPARATE),
            ("Ex Separate Except Start", WeaponMode.EX_SEPARATE_EXCEPT_START),
        ]

        for mode_name, mode_value in modes:
            with self.subTest(mode_name):
                options = self._options_for_weapon_mode(mode_value)
                items = {**idefs.items_base}
                itemsetup.setup_weapons(items, options)  # type: ignore[arg-type]

                expected_weapons = set(weapons.get_weapon_dict(options, True).values())  # type: ignore[arg-type]
                self.assertTrue(expected_weapons.issubset(items.keys()))

                if (mode_value & WeaponMode.EX_SEPARATE) > 0:
                    expected_ex = {
                        x
                        for i, x in weapons.weapon_ex_dict.items()
                        if i in weapons.get_weapon_dict(options, True)  # type: ignore[arg-type]
                    }
                    self.assertTrue(expected_ex.issubset(items.keys()))
                else:
                    self.assertTrue(set(idefs.item_all_weapon_ex.keys()).isdisjoint(items.keys()))

                if (mode_value & WeaponMode.PROGRESSIVE) > 0 or (mode_value & WeaponMode.EX_SEPARATE) > 0:
                    self.assertEqual(items[itemnames.item_plane_ex].quantity, 1)
                else:
                    self.assertEqual(items[itemnames.item_plane_ex].quantity, 0)
