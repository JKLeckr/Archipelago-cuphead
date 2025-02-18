from ..names import ItemNames
from . import CupheadTestBase

class TestDefault(CupheadTestBase):
    def test_default(self):
        self.assertBeatable(False)
        contracts = self.get_items_by_name(ItemNames.item_contract)
        self.collect(contracts)
        self.assertBeatable(True)
