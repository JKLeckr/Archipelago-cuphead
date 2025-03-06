#from ..names import ItemNames
from . import CupheadTestBase

class TestGame(CupheadTestBase):
    def test_default(self):
        test = TestGame()
        #test.assertBeatable(False)
        #contracts = test.get_items_by_name(ItemNames.item_contract)
        #test.collect(contracts)
        #test.collect_by_name(ItemNames.item_plane_gun)
        #test.collect_by_name(ItemNames.item_plane_bombs)
        test.test_all_state_can_reach_everything()
        #test.assertBeatable(True)
        #FIXME: Fix later

    def test_dlc(self):
        test = TestGame()
        test.options = {
            "use_dlc": True,
            "mode": "dlc_beat_both",
        }
        test.world_setup()
        test.test_all_state_can_reach_everything()
        #FIXME: Same as test_default
