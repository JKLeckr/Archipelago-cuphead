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
        "dlc_chalice": "disabled",
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
