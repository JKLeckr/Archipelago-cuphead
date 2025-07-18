from ..names import ItemNames, LocationNames
from . import CupheadTestBase

class TestGame(CupheadTestBase):
    def test_default(self):
        test = TestGame()
        test.world_setup()
        test.assertBeatable(False)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.assertFalse(test.can_reach_region(LocationNames.level_mausoleum_i))
        test.collect_by_name(ItemNames.item_ability_parry)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.assertTrue(test.can_reach_region(LocationNames.level_mausoleum_i))
        contracts = test.get_items_by_name(ItemNames.item_contract)
        test.collect(contracts)
        test.collect_by_name(ItemNames.item_plane_gun)
        test.collect_by_name(ItemNames.item_ability_dash)
        test.assertBeatable(True)

class TestGameDlc(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
    }

    def test_dlc(self):
        test = TestGameDlc()
        test.world_setup()
        test.assertBeatable(False)
        test.assertFalse(test.can_reach_region(LocationNames.world_dlc_inkwell_4))
        test.collect_by_name(ItemNames.item_dlc_boat)
        test.assertFalse(test.can_reach_region(LocationNames.world_dlc_inkwell_4))
        test.assertFalse(test.can_reach_region(LocationNames.level_mausoleum_i))
        test.collect_by_name(ItemNames.item_ability_parry)
        test.assertTrue(test.can_reach_region(LocationNames.level_mausoleum_i))
        test.assertTrue(test.can_reach_region(LocationNames.world_dlc_inkwell_4))
        contracts = test.get_items_by_name(ItemNames.item_contract)
        test.collect(contracts)
        ingredients = test.get_items_by_name(ItemNames.item_dlc_ingredient)
        test.collect(ingredients)
        test.collect_by_name(ItemNames.item_plane_gun)
        test.collect_by_name(ItemNames.item_ability_dash)
        test.assertBeatable(True)

class TestGameTopGrade(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
        "boss_grade_checks": "a_minus_grade",
        "rungun_grade_checks": "a_minus_grade"
    }

    def test_topgrade(self):
        test = TestGameTopGrade()
        test.world_setup()
        test.assertBeatable(False)

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect_by_name(ItemNames.item_ability_parry)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))
        test.collect_by_name(ItemNames.item_ability_dash)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))

class TestGameChaliced(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
        "dlc_chalice": "randomized",
        "freemove_isles": "true",
        "dlc_boss_chalice_checks": "enabled",
        "dlc_rungun_chalice_checks": "enabled"
    }

    def test_chaliced(self):
        test = TestGameChaliced()
        test.world_setup()
        test.assertBeatable(False)

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.collect_by_name(ItemNames.item_charm_dlc_cookie)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.remove_by_name(ItemNames.item_charm_dlc_cookie)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.collect_by_name(ItemNames.item_ability_dash)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.collect_by_name(ItemNames.item_charm_dlc_cookie)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))

class TestGameChalicedGradeRequired(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
        "dlc_chalice": "randomized",
        "freemove_isles": "true",
        "dlc_boss_chalice_checks": "grade_required",
        "dlc_rungun_chalice_checks": "grade_required"
    }

    def test_chaliced_grade_required(self):
        test = TestGameChalicedGradeRequired()
        test.world_setup()
        test.assertBeatable(False)

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.collect_by_name(ItemNames.item_charm_dlc_cookie)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.collect_by_name(ItemNames.item_ability_parry)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.collect_by_name(ItemNames.item_ability_dash)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.remove_by_name([ItemNames.item_charm_dlc_cookie, ItemNames.item_ability_dash])
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_dlc_chaliced))
        test.collect_by_name(ItemNames.item_ability_dash)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_dlc_chaliced))
        test.collect_by_name(ItemNames.item_charm_dlc_cookie)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest_dlc_chaliced))

class TestGameChalicedGradeRequiredSeparate(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
        "dlc_chalice": "randomized",
        "freemove_isles": "true",
        "dlc_boss_chalice_checks": "separate_grade_required",
        "dlc_rungun_chalice_checks": "separate_grade_required"
    }

    def test_chaliced_grade_required_separate(self):
        test = TestGameChalicedGradeRequiredSeparate()
        test.world_setup()
        test.assertBeatable(False)

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.collect_by_name(ItemNames.item_charm_dlc_cookie)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.collect_by_name(ItemNames.item_ability_parry)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.collect_by_name(ItemNames.item_ability_dash)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.remove_by_name([ItemNames.item_charm_dlc_cookie, ItemNames.item_ability_dash])
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_dlc_chaliced))
        test.collect_by_name(ItemNames.item_ability_dash)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_dlc_chaliced))
        test.collect_by_name(ItemNames.item_charm_dlc_cookie)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest_dlc_chaliced))

class TestGameWeaponProgression(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
        "dlc_chalice": "disabled",
        "start_weapon": "peashooter",
        "weapon_mode": "progressive",
        "freemove_isles": "true",
        "boss_grade_checks": "a_minus_grade",
        "rungun_grade_checks": "a_minus_grade"
    }

    def test_weapon_progression(self):
        test = TestGameWeaponProgression()
        test.world_setup()
        test.assertBeatable(False)

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect_by_name(ItemNames.item_ability_parry)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect_by_name(ItemNames.item_super_i)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.remove_by_name(ItemNames.item_super_i)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect_by_name(ItemNames.item_p_weapon_spread)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.remove_by_name(ItemNames.item_p_weapon_spread)
        test.collect_by_name(ItemNames.item_p_weapon_peashooter)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.remove_by_name(ItemNames.item_p_weapon_peashooter)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))
        test.collect_by_name([ItemNames.item_ability_parry, ItemNames.item_ability_dash])
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))
        test.collect_by_name(ItemNames.item_super_i)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))
        test.remove_by_name(ItemNames.item_super_i)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))
        test.collect_by_name(ItemNames.item_p_weapon_spread)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))
        test.remove_by_name(ItemNames.item_p_weapon_spread)
        test.collect_by_name(ItemNames.item_weapon_spread_ex)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))

        test.collect_by_name([ItemNames.item_plane_gun, ItemNames.item_ability_plane_parry])
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))
        test.collect_by_name(ItemNames.item_plane_ex)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))
        test.remove_by_name(ItemNames.item_plane_ex)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))
        test.collect_by_name(ItemNames.item_plane_super)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))

class TestGameWeaponEX(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
        "dlc_chalice": "disabled",
        "start_weapon": "peashooter",
        "weapon_mode": "ex_separate",
        "freemove_isles": "true",
        "boss_grade_checks": "a_minus_grade",
        "rungun_grade_checks": "a_minus_grade"
    }

    def test_weapon_ex(self):
        test = TestGameWeaponEX()
        test.world_setup()
        test.assertBeatable(False)

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect_by_name(ItemNames.item_ability_parry)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect_by_name(ItemNames.item_super_i)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.remove_by_name(ItemNames.item_super_i)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect_by_name(ItemNames.item_weapon_peashooter_ex)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.remove_by_name(ItemNames.item_weapon_peashooter_ex)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect_by_name(ItemNames.item_weapon_spread_ex)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.remove_by_name(ItemNames.item_weapon_spread_ex)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))
        test.collect_by_name([ItemNames.item_ability_parry, ItemNames.item_ability_dash])
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))
        test.collect_by_name(ItemNames.item_super_i)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))
        test.remove_by_name(ItemNames.item_super_i)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))
        test.collect_by_name(ItemNames.item_weapon_peashooter_ex)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))
        test.remove_by_name(ItemNames.item_weapon_peashooter_ex)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))
        test.collect_by_name(ItemNames.item_weapon_spread_ex)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))

        test.collect_by_name([ItemNames.item_plane_gun, ItemNames.item_ability_plane_parry])
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))
        test.collect_by_name(ItemNames.item_plane_ex)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))
        test.remove_by_name(ItemNames.item_plane_ex)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))
        test.collect_by_name(ItemNames.item_plane_super)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))

class TestGameWeaponEXExceptStart(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
        "dlc_chalice": "disabled",
        "start_weapon": "peashooter",
        "weapon_mode": "ex_separate_except_start",
        "freemove_isles": "true",
        "boss_grade_checks": "a_minus_grade",
        "rungun_grade_checks": "a_minus_grade"
    }

    def test_weapon_ex_except_start(self):
        test = TestGameWeaponEXExceptStart()
        test.world_setup()
        test.assertBeatable(False)

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect_by_name(ItemNames.item_ability_parry)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.remove_by_name(ItemNames.item_ability_parry)

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))
        test.collect_by_name([ItemNames.item_ability_parry, ItemNames.item_ability_dash])
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))

        test.collect_by_name([ItemNames.item_plane_gun, ItemNames.item_ability_plane_parry])
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))
        test.collect_by_name(ItemNames.item_plane_ex)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))
        test.remove_by_name(ItemNames.item_plane_ex)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))
        test.collect_by_name(ItemNames.item_plane_super)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))
