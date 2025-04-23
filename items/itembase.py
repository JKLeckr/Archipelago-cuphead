from __future__ import annotations
from typing import NamedTuple
from BaseClasses import ItemClassification

class ItemData(NamedTuple):
    id: int | None
    item_type: ItemClassification = ItemClassification.filler
    quantity: int = 1 # Set to 0 to skip automatic placement (Useful if placing manually)
    event: bool = False
    category: str | None = None

    def with_item_type(self, type: ItemClassification) -> ItemData:
        return ItemData(self.id, type, self.quantity, self.event, self.category)
    def with_quantity(self, quantity: int) -> ItemData:
        return ItemData(self.id, self.item_type, quantity, self.event, self.category)
