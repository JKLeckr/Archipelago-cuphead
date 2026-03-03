### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from BaseClasses import ItemClassification

from ..enums import ChaliceCheckMode, ChaliceMode, GameMode, GradeCheckMode, ItemGroups, WeaponMode
from ..names import itemnames
from ..options import CupheadOptions
from . import itemdefs as idef
from . import weapons
from .itembase import ItemData


def add_item(items_ref: dict[str, ItemData], item: str):
    items_ref[item] = idef.items_all[item]

def change_item_type(items_ref: dict[str, ItemData], item: str, item_type: ItemClassification):
    items_ref[item] = items_ref[item].with_item_type(item_type)

def change_item_quantity(items_ref: dict[str, ItemData], item: str, quantity: int):
    items_ref[item] = items_ref[item].with_quantity(quantity)

def setup_dlc_items(items_ref: dict[str, ItemData], options: CupheadOptions):
    items_ref.update(idef.items_dlc)
    if options.dlc_chalice.evalue == ChaliceMode.VANILLA or options.dlc_chalice.evalue == ChaliceMode.RANDOMIZED:
        add_item(items_ref, itemnames.item_charm_dlc_cookie)
        if (
            options.dlc_boss_chalice_checks.value or
            options.dlc_cactusgirl_quest.value or
            (options.mode.evalue & GameMode.DLC_NO_ISLE4) == 0
        ):
            change_item_type(items_ref, itemnames.item_charm_dlc_cookie, ItemClassification.progression)
    if options.is_dlc_chalice_items_separate(ItemGroups.ESSENTIAL):
        items_ref.update(idef.item_dlc_chalice_essential)
    if options.is_dlc_chalice_items_separate(ItemGroups.SUPER):
        items_ref.update(idef.item_dlc_chalice_super)
    if (
        (options.weapon_mode.evalue & (WeaponMode.PROGRESSIVE | WeaponMode.EX_SEPARATE)) > 0 and
        options.is_dlc_chalice_items_separate(ItemGroups.WEAPON_EX)
    ):
        change_item_quantity(items_ref, itemnames.item_dlc_cplane_ex, 1)

def setup_abilities(items_ref: dict[str, ItemData], options: CupheadOptions):
    items_ref.update(idef.item_abilities)
    if options.use_dlc.value:
        if options.is_dlc_chalice_items_separate(ItemGroups.ABILITIES):
            items_ref.update(idef.item_dlc_chalice_abilities)
        else:
            add_item(items_ref, itemnames.item_ability_dlc_cdoublejump)
    change_item_type(items_ref, itemnames.item_charm_psugar, ItemClassification.progression)
    if options.boss_secret_checks.value:
        change_item_type(items_ref, itemnames.item_ability_plane_shrink, ItemClassification.progression)

def setup_weapon_gate(items_ref: dict[str, ItemData], options: CupheadOptions):
    weapon_keys = {
        **idef.item_weapons,
        **idef.item_dlc_weapons,
    }
    for w in weapon_keys:
        if w in items_ref.keys():
            change_item_type(items_ref, w, ItemClassification.progression)

def setup_weapons(items_ref: dict[str, ItemData], options: CupheadOptions):
    _weapon_dict = weapons.get_weapon_dict(options, options.use_dlc.bvalue)
    silverworth_quest = getattr(getattr(options, "silverworth_quest", None), "bvalue", False)
    _grade_checks_required = (
        options.boss_grade_checks.evalue != GradeCheckMode.DISABLED or
        options.rungun_grade_checks.evalue != GradeCheckMode.DISABLED or
        (options.dlc_boss_chalice_checks.evalue & ChaliceCheckMode.GRADE_REQUIRED) > 0 or
        silverworth_quest
    )
    for weapon in _weapon_dict.values():
        items_ref[weapon] = idef.items_all[weapon]
    if (options.weapon_mode.evalue & WeaponMode.PROGRESSIVE) > 0:
        if _grade_checks_required:
            [
                change_item_type(items_ref, x, ItemClassification.progression)
                for i,x in _weapon_dict.items() if i in weapons.weapon_p_dict.keys()
            ]
    if (options.weapon_mode.evalue & WeaponMode.EX_SEPARATE) > 0:
        items_ref.update({x: idef.items_all[x] for i,x in weapons.weapon_ex_dict.items() if i in _weapon_dict.keys()})
        if _grade_checks_required:
            [
                change_item_type(items_ref, x, ItemClassification.progression)
                for i,x in weapons.weapon_ex_dict.items() if i in _weapon_dict.keys()
            ]
    if (options.weapon_mode.evalue & (WeaponMode.PROGRESSIVE | WeaponMode.EX_SEPARATE)) > 0:
        change_item_quantity(items_ref, itemnames.item_plane_ex, 1)
        if _grade_checks_required:
            [change_item_type(items_ref, x, ItemClassification.progression) for x in idef.item_super]

def setup_items(options: CupheadOptions) -> dict[str, ItemData]:
    items: dict[str, ItemData] = {**idef.items_base}
    setup_weapons(items, options)
    if options.use_dlc.bvalue:
        setup_dlc_items(items, options)
    if options.weapon_gate.bvalue:
        setup_weapon_gate(items, options)
    if options.randomize_abilities.bvalue:
        setup_abilities(items, options)
    if options.randomize_abilities_aim.bvalue:
        items.update(idef.item_abilities_aim)
        if options.use_dlc.bvalue and options.is_dlc_chalice_items_separate(ItemGroups.AIM_ABILITIES):
            items.update(idef.item_dlc_chalice_abilities_aim)
    if options.traps.value > 0:
        items.update(idef.item_trap)
    return items
