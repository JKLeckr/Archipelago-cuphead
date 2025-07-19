from __future__ import annotations
from BaseClasses import ItemClassification
from ..names import ItemNames
from ..enums import ItemGroups, WeaponMode, GradeCheckMode, ChaliceCheckMode
from ..wconf import WorldConfig
from .itembase import ItemData
from . import weapons, itemdefs as idef

def add_item(items_ref: dict[str, ItemData], item: str):
    items_ref[item] = idef.items_all[item]

def change_item_type(items_ref: dict[str, ItemData], item: str, item_type: ItemClassification):
    items_ref[item] = items_ref[item].with_item_type(item_type)

def change_item_quantity(items_ref: dict[str, ItemData], item: str, quantity: int):
    items_ref[item] = items_ref[item].with_quantity(quantity)

def setup_dlc_items(items_ref: dict[str, ItemData], wconf: WorldConfig):
    items_ref.update(idef.items_dlc)
    if wconf.dlc_chalice>0:
        add_item(items_ref, ItemNames.item_charm_dlc_cookie)
        if wconf.dlc_boss_chalice_checks or wconf.dlc_cactusgirl_quest:
            change_item_type(items_ref, ItemNames.item_charm_dlc_cookie, ItemClassification.progression)
    if wconf.is_dlc_chalice_items_separate(ItemGroups.ESSENTIAL):
        items_ref.update(idef.item_dlc_chalice_essential)
    if wconf.is_dlc_chalice_items_separate(ItemGroups.SUPER):
        items_ref.update(idef.item_dlc_chalice_super)
    if (
        (wconf.weapon_mode & (WeaponMode.PROGRESSIVE | WeaponMode.EX_SEPARATE)) > 0 and
        wconf.is_dlc_chalice_items_separate(ItemGroups.WEAPON_EX)
    ):
        change_item_quantity(items_ref, ItemNames.item_dlc_cplane_ex, 1)

def setup_abilities(items_ref: dict[str, ItemData], wconf: WorldConfig):
    items_ref.update(idef.item_abilities)
    if wconf.use_dlc:
        if wconf.is_dlc_chalice_items_separate(ItemGroups.ABILITIES):
            items_ref.update(idef.item_dlc_chalice_abilities)
        else:
            add_item(items_ref, ItemNames.item_ability_dlc_cdoublejump)
    change_item_type(items_ref, ItemNames.item_charm_psugar, ItemClassification.progression)
    if wconf.boss_secret_checks:
        change_item_type(items_ref, ItemNames.item_ability_plane_shrink, ItemClassification.progression)

def setup_weapon_gate(items_ref: dict[str, ItemData], wconf: WorldConfig):
    weapon_keys = {
        **idef.item_weapons,
        **idef.item_dlc_weapons,
    }
    for w in weapon_keys:
        if w in items_ref.keys():
            change_item_type(items_ref, w, ItemClassification.progression)

def setup_weapons(items_ref: dict[str, ItemData], wconf: WorldConfig):
    _weapon_dict = weapons.get_weapon_dict(wconf, wconf.use_dlc)
    _grade_checks_required = (
        wconf.boss_grade_checks != GradeCheckMode.DISABLED or
        wconf.rungun_grade_checks != GradeCheckMode.DISABLED or
        (wconf.dlc_boss_chalice_checks & ChaliceCheckMode.GRADE_REQUIRED) > 0
    )
    for weapon in _weapon_dict.values():
        items_ref[weapon] = idef.items_all[weapon]
    if (wconf.weapon_mode & WeaponMode.PROGRESSIVE) > 0:
        if _grade_checks_required:
            [
                change_item_type(items_ref, x, ItemClassification.progression)
                for i,x in _weapon_dict.items() if i in weapons.weapon_p_dict.keys()
            ]
    if (wconf.weapon_mode & WeaponMode.EX_SEPARATE) > 0:
        items_ref.update({x: idef.items_all[x] for i,x in weapons.weapon_ex_dict.items() if i in _weapon_dict.keys()})
        if _grade_checks_required:
            [
                change_item_type(items_ref, x, ItemClassification.progression)
                for i,x in weapons.weapon_ex_dict.items() if i in _weapon_dict.keys()
            ]
    if (wconf.weapon_mode & (WeaponMode.PROGRESSIVE | WeaponMode.EX_SEPARATE)) > 0:
        change_item_quantity(items_ref, ItemNames.item_plane_ex, 1)
        if _grade_checks_required:
            [change_item_type(items_ref, x, ItemClassification.progression) for x in idef.item_super]

def setup_items(wconf: WorldConfig) -> dict[str, ItemData]:
    items: dict[str, ItemData] = {**idef.items_base}
    setup_weapons(items, wconf)
    if wconf.use_dlc:
        setup_dlc_items(items, wconf)
    if wconf.weapon_gate:
        setup_weapon_gate(items, wconf)
    if wconf.randomize_abilities:
        setup_abilities(items, wconf)
    if wconf.randomize_abilities_aim:
        items.update(idef.item_abilities_aim)
        if wconf.use_dlc and wconf.is_dlc_chalice_items_separate(ItemGroups.AIM_ABILITIES):
            items.update(idef.item_dlc_chalice_abilities_aim)
    if wconf.traps>0:
        items.update(idef.item_trap)
    return items
