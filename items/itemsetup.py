from __future__ import annotations
from BaseClasses import ItemClassification
from ..names import ItemNames
from ..enums import ItemGroups
from ..wsettings import WorldSettings
from .itembase import ItemData
from . import weapons, itemdefs as idef

def add_item(items_ref: dict[str, ItemData], item: str):
    items_ref[item] = idef.items_all[item]

def change_item_type(items_ref: dict[str, ItemData], item: str, item_type: ItemClassification):
    items_ref[item] = items_ref[item].with_item_type(item_type)

def change_item_quantity(items_ref: dict[str, ItemData], item: str, quantity: int):
    items_ref[item] = items_ref[item].with_quantity(quantity)

def setup_dlc_items(items_ref: dict[str, ItemData], settings: WorldSettings):
    items_ref.update(idef.items_dlc)
    if settings.dlc_chalice>0:
        add_item(items_ref, ItemNames.item_charm_dlc_cookie)
        if settings.dlc_boss_chalice_checks or settings.dlc_cactusgirl_quest:
            change_item_type(items_ref, ItemNames.item_charm_dlc_cookie, ItemClassification.progression)
    if settings.is_dlc_chalice_items_separate(ItemGroups.ESSENTIAL):
        items_ref.update(idef.item_dlc_chalice_essential)
    if settings.is_dlc_chalice_items_separate(ItemGroups.SUPER):
        items_ref.update(idef.item_dlc_chalice_super)
    if settings.randomize_weapon_ex:
        change_item_quantity(items_ref, ItemNames.item_plane_ex, 1)

def setup_abilities(items_ref: dict[str, ItemData], settings: WorldSettings):
    items_ref.update(idef.item_abilities)
    if settings.use_dlc and settings.is_dlc_chalice_items_separate(ItemGroups.ABILITIES):
        items_ref.update(idef.item_dlc_chalice_abilities)
    change_item_type(items_ref, ItemNames.item_charm_psugar, ItemClassification.progression)
    if settings.boss_secret_checks:
        change_item_type(items_ref, ItemNames.item_ability_plane_shrink, ItemClassification.progression)

def setup_weapon_gate(items_ref: dict[str, ItemData], settings: WorldSettings):
    weapon_keys = {
        **idef.item_weapons,
        **idef.item_dlc_weapons,
    }
    for w in weapon_keys:
        if w in items_ref.keys():
            change_item_type(items_ref, w, ItemClassification.progression)

def setup_weapons(items_ref: dict[str, ItemData], settings: WorldSettings):
    for weapon in weapons.get_weapon_dict(settings, settings.use_dlc).values():
        items_ref[weapon] = idef.items_all[weapon]
    if settings.randomize_weapon_ex:
        change_item_quantity(items_ref, ItemNames.item_plane_ex, 1)

def setup_items(settings: WorldSettings) -> dict[str, ItemData]:
    items: dict[str, ItemData] = {**idef.items_base}
    setup_weapons(items, settings)
    if settings.use_dlc:
        setup_dlc_items(items, settings)
    if settings.weapon_gate:
        setup_weapon_gate(items, settings)
    if settings.randomize_abilities:
        setup_abilities(items, settings)
    if settings.randomize_abilities_aim:
        items.update(idef.item_abilities_aim)
        if settings.use_dlc and settings.is_dlc_chalice_items_separate(ItemGroups.AIM_ABILITIES):
            items.update(idef.item_dlc_chalice_abilities_aim)
    if settings.traps>0:
        items.update(idef.item_trap)
    return items
