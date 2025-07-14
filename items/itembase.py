from __future__ import annotations
import typing
from typing import NamedTuple
from random import Random
from BaseClasses import Item, ItemClassification
if typing.TYPE_CHECKING:
    from .. import CupheadWorld

class CupheadItem(Item):
    game: str = "Cuphead"

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

def weighted_item_choice(item_weights: list[tuple[str, int]], rand: Random) -> str:
    if len(item_weights)<1:
        raise ValueError("item_weights must not be empty!")

    active_items, active_weights = zip(*item_weights, strict=True)

    total_weight = sum(active_weights)

    if total_weight <= 0:
        raise ValueError("Total weight must be greater than 0!")

    choice = rand.randint(1, total_weight)

    culum_sum = 0
    for i, weight in enumerate(active_weights):
        culum_sum += weight
        if choice <= culum_sum:
            return active_items[i]
    raise ValueError("Failed to choose an item from weighted_item_choice!")

def get_filler_item_name(world: CupheadWorld) -> str:
    return weighted_item_choice(world.wconfig.filler_item_weights, world.random)
