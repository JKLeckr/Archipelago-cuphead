from __future__ import annotations
from typing import NamedTuple
from enum import IntFlag
from BaseClasses import ItemClassification

class ItemGroups(IntFlag):
    NONE = 0
    ESSENTIAL = 1
    SUPER = 2
    CORE_ITEMS = 3
    ABILITIES = 4
    CORE_AND_ABILITIES = 7
    AIM_ABILITIES = 8
    CORE_AND_AIM = 11
    ABILITIES_AND_AIM = 12
    ALL = 255

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
