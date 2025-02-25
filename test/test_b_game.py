from ..names import ItemNames
from . import CupheadTestBase

class TestDefault(CupheadTestBase):
    def test_default(self):
        self.world_setup()
        self.assertBeatable(False)
        contracts = self.get_items_by_name(ItemNames.item_contract)
        self.collect(contracts)
        self.collect_by_name(ItemNames.item_plane_gun)
        self.assertBeatable(True)
