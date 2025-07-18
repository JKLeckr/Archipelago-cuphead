import unittest
from ..enums import WeaponMode
from ..items import itemsetup, weapons, itemdefs as idefs
from ..names import ItemNames
from .. import wconf

class TestAPWorldItemSetup(unittest.TestCase):
    def test_setup_weapons(self):
        _wconf = wconf.WorldConfig()
        _wconf.use_dlc = True
        _wconf.start_weapon = 0

        _start_weapon = ItemNames.item_weapon_peashooter

        self.assertEqual(weapons.weapon_dict[0], _start_weapon)

        item_weapons = set(idefs.item_all_weapons.keys())
        item_weapon_ex = set(idefs.item_all_weapon_ex.keys())
        item_p_weapons = set(idefs.item_all_p_weapons.keys())
        item_weapon_ex_nostart = {x for x in idefs.item_all_weapon_ex.keys() if x != _start_weapon}
        item_p_weapons_nostart = {x for x in idefs.item_all_p_weapons.keys() if x != _start_weapon}

        modes: list[tuple[str, WeaponMode, set[str]]] = [
            ("Normal", WeaponMode.NORMAL, item_weapons),
            ("Progressive", WeaponMode.PROGRESSIVE, item_p_weapons),
            ("Progressive Except Start", WeaponMode.PROGRESSIVE_EXCEPT_START, item_p_weapons_nostart),
            ("Ex Separate", WeaponMode.EX_SEPARATE, item_weapon_ex),
            ("Ex Separate Except Start", WeaponMode.EX_SEPARATE_EXCEPT_START, item_weapon_ex_nostart),
        ]

        for mode in modes:
            with self.subTest(mode[0]):
                _wconf.weapon_mode = mode[1]
                itemsetup.setup_items(_wconf)
