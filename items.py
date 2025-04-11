from __future__ import annotations
from typing import NamedTuple, Optional
from BaseClasses import ItemClassification
from .names import ItemNames
from .wsettings import WorldSettings, ItemGroups, WeaponExMode
from . import itembase

class ItemData(NamedTuple):
    id: Optional[int]
    item_type: ItemClassification = ItemClassification.filler
    quantity: int = 1 # Set to 0 to skip automatic placement (Useful if placing manually)
    event: bool = False
    category: str | None = None

    def with_item_type(self, type: ItemClassification) -> ItemData:
        return ItemData(self.id, type, self.quantity, self.event, self.category)
    def with_quantity(self, quantity: int) -> ItemData:
        return ItemData(self.id, self.item_type, quantity, self.event, self.category)

base_id = 12905168
base_dlc_id = 12909264

def id(i: int): return base_id+i
def dlc_id(i: int): return base_dlc_id+i

# Items
# Next ids: 61, 23
item_generic: dict[str, ItemData] = {
    ItemNames.item_level_generic: ItemData(id(0), ItemClassification.filler, 0),
}
item_filler: dict[str, ItemData] = {
    ItemNames.item_level_extrahealth: ItemData(id(1), ItemClassification.filler, 0),
    ItemNames.item_level_superrecharge: ItemData(id(2), ItemClassification.filler, 0),
    ItemNames.item_level_fastfire: ItemData(id(3), ItemClassification.filler, 0),
    #ItemNames.item_level_4: ItemData(id(4), ItemClassification.filler, 0),
}

item_essential: dict[str, ItemData] = {
    ItemNames.item_coin: ItemData(id(5), ItemClassification.progression_skip_balancing, 0),
    ItemNames.item_coin2: ItemData(id(6), ItemClassification.progression_skip_balancing, 0),
    ItemNames.item_coin3: ItemData(id(7), ItemClassification.progression_skip_balancing, 0),
    ItemNames.item_contract: ItemData(id(8), ItemClassification.progression_skip_balancing, 17),
    ItemNames.item_plane_gun: ItemData(id(9), ItemClassification.progression),
    ItemNames.item_plane_ex: ItemData(id(10), ItemClassification.progression, 0),
    ItemNames.item_plane_bombs: ItemData(id(11), ItemClassification.progression),
    ItemNames.item_healthupgrade: ItemData(id(12), ItemClassification.useful, 0)
}
item_dlc_essential: dict[str, ItemData] = {
    ItemNames.item_dlc_boat: ItemData(dlc_id(0), ItemClassification.progression),
    ItemNames.item_dlc_ingredient: ItemData(dlc_id(1), ItemClassification.progression_skip_balancing, 5),
}
item_dlc_chalice_essential: dict[str, ItemData] = {
    ItemNames.item_dlc_cplane_gun: ItemData(dlc_id(2), ItemClassification.progression),
    ItemNames.item_dlc_cplane_ex: ItemData(dlc_id(3), ItemClassification.progression, 0),
    ItemNames.item_dlc_cplane_bombs: ItemData(dlc_id(4), ItemClassification.progression),
}

item_weapons: dict[str, ItemData] = {
    ItemNames.item_weapon_peashooter: ItemData(id(13), ItemClassification.useful),
    ItemNames.item_weapon_spread: ItemData(id(15), ItemClassification.useful),
    ItemNames.item_weapon_chaser: ItemData(id(17), ItemClassification.useful),
    ItemNames.item_weapon_lobber: ItemData(id(19), ItemClassification.useful),
    ItemNames.item_weapon_charge: ItemData(id(21), ItemClassification.useful),
    ItemNames.item_weapon_roundabout: ItemData(id(23), ItemClassification.useful),
}
item_dlc_weapons: dict[str, ItemData] = {
    ItemNames.item_weapon_dlc_crackshot: ItemData(dlc_id(5), ItemClassification.useful),
    ItemNames.item_weapon_dlc_converge: ItemData(dlc_id(7), ItemClassification.useful),
    ItemNames.item_weapon_dlc_twistup: ItemData(dlc_id(9), ItemClassification.useful),
}

item_p_weapons: dict[str, ItemData] = {
    ItemNames.item_p_weapon_peashooter: ItemData(id(14), ItemClassification.useful, 2),
    ItemNames.item_p_weapon_spread: ItemData(id(16), ItemClassification.useful, 2),
    ItemNames.item_p_weapon_chaser: ItemData(id(18), ItemClassification.useful, 2),
    ItemNames.item_p_weapon_lobber: ItemData(id(20), ItemClassification.useful, 2),
    ItemNames.item_p_weapon_charge: ItemData(id(22), ItemClassification.useful, 2),
    ItemNames.item_p_weapon_roundabout: ItemData(id(24), ItemClassification.useful, 2),
}
item_dlc_p_weapons: dict[str, ItemData] = {
    ItemNames.item_p_weapon_dlc_crackshot: ItemData(dlc_id(6), ItemClassification.useful, 2),
    ItemNames.item_p_weapon_dlc_converge: ItemData(dlc_id(8), ItemClassification.useful, 2),
    ItemNames.item_p_weapon_dlc_twistup: ItemData(dlc_id(10), ItemClassification.useful, 2),
}

item_charms: dict[str, ItemData] = {
    ItemNames.item_charm_heart: ItemData(id(25), ItemClassification.useful),
    ItemNames.item_charm_smokebomb: ItemData(id(26), ItemClassification.useful),
    ItemNames.item_charm_psugar: ItemData(id(27), ItemClassification.useful),
    ItemNames.item_charm_coffee: ItemData(id(28), ItemClassification.useful),
    ItemNames.item_charm_twinheart: ItemData(id(29), ItemClassification.useful),
    ItemNames.item_charm_whetstone: ItemData(id(30), ItemClassification.useful),
}
item_dlc_charms: dict[str, ItemData] = {
    ItemNames.item_charm_dlc_heartring: ItemData(dlc_id(11), ItemClassification.useful),
    ItemNames.item_charm_dlc_broken_relic: ItemData(dlc_id(12), ItemClassification.useful, 0), # Sequence will not be in logic  # noqa: E501
}

item_super: dict[str, ItemData] = {
    ItemNames.item_super_i: ItemData(id(31), ItemClassification.useful),
    ItemNames.item_super_ii: ItemData(id(32), ItemClassification.useful),
    ItemNames.item_super_iii: ItemData(id(33), ItemClassification.useful),
    ItemNames.item_plane_super: ItemData(id(34), ItemClassification.useful),
}
item_dlc_chalice_super: dict[str, ItemData] = {
    ItemNames.item_super_dlc_c_i: ItemData(dlc_id(13), ItemClassification.useful),
    ItemNames.item_super_dlc_c_ii: ItemData(dlc_id(14), ItemClassification.useful),
    ItemNames.item_super_dlc_c_iii: ItemData(dlc_id(15), ItemClassification.useful),
    ItemNames.item_dlc_cplane_super: ItemData(dlc_id(16), ItemClassification.useful),
}

item_abilities: dict[str, ItemData] = {
    ItemNames.item_ability_duck: ItemData(id(35), ItemClassification.progression),
    ItemNames.item_ability_dash: ItemData(id(36), ItemClassification.progression),
    ItemNames.item_ability_parry: ItemData(id(37), ItemClassification.progression),
    ItemNames.item_ability_plane_parry: ItemData(id(38), ItemClassification.progression),
    ItemNames.item_ability_plane_shrink: ItemData(id(39), ItemClassification.useful),
}
item_dlc_chalice_abilities: dict[str, ItemData] = {
    ItemNames.item_ability_dlc_cduck: ItemData(dlc_id(17), ItemClassification.progression),
    ItemNames.item_ability_dlc_p_cdash: ItemData(dlc_id(18), ItemClassification.progression, 2),
    ItemNames.item_ability_dlc_cdoublejump: ItemData(dlc_id(19), ItemClassification.progression),
    ItemNames.item_ability_dlc_cplane_parry: ItemData(dlc_id(20), ItemClassification.progression),
    ItemNames.item_ability_dlc_cplane_shrink: ItemData(dlc_id(21), ItemClassification.useful),
}
item_abilities_aim: dict[str, ItemData] = {
    ItemNames.item_ability_aim_left: ItemData(id(40), ItemClassification.progression),
    ItemNames.item_ability_aim_right: ItemData(id(41), ItemClassification.progression),
    ItemNames.item_ability_aim_up: ItemData(id(42), ItemClassification.progression),
    ItemNames.item_ability_aim_down: ItemData(id(43), ItemClassification.progression),
    ItemNames.item_ability_aim_upleft: ItemData(id(44), ItemClassification.progression),
    ItemNames.item_ability_aim_upright: ItemData(id(45), ItemClassification.progression),
    ItemNames.item_ability_aim_downleft: ItemData(id(46), ItemClassification.progression),
    ItemNames.item_ability_aim_downright: ItemData(id(47), ItemClassification.progression),
}
item_dlc_chalice_abilities_aim: dict[str, ItemData] = {
    ItemNames.item_ability_dlc_c_aim_left: ItemData(id(48), ItemClassification.progression),
    ItemNames.item_ability_dlc_c_aim_right: ItemData(id(49), ItemClassification.progression),
    ItemNames.item_ability_dlc_c_aim_up: ItemData(id(50), ItemClassification.progression),
    ItemNames.item_ability_dlc_c_aim_down: ItemData(id(51), ItemClassification.progression),
    ItemNames.item_ability_dlc_c_aim_upleft: ItemData(id(52), ItemClassification.progression),
    ItemNames.item_ability_dlc_c_aim_upright: ItemData(id(53), ItemClassification.progression),
    ItemNames.item_ability_dlc_c_aim_downleft: ItemData(id(54), ItemClassification.progression),
    ItemNames.item_ability_dlc_c_aim_downright: ItemData(id(55), ItemClassification.progression),
}

item_trap: dict[str, ItemData] = {
    ItemNames.item_level_trap_fingerjam: ItemData(id(56), ItemClassification.trap, 0),
    ItemNames.item_level_trap_slowfire: ItemData(id(57), ItemClassification.trap, 0),
    ItemNames.item_level_trap_superdrain: ItemData(id(58), ItemClassification.trap, 0),
    ItemNames.item_level_trap_loadout: ItemData(id(59), ItemClassification.trap, 0),
    ItemNames.item_level_trap_screen: ItemData(id(60), ItemClassification.trap, 0),
}

item_special: dict[str, ItemData] = {
    ItemNames.item_event_boss_defeated: ItemData(None, ItemClassification.progression_skip_balancing, 0),
    ItemNames.item_event_isle1_secret_prereq: ItemData(None, ItemClassification.progression_skip_balancing, 0),
    ItemNames.item_event_isle2_shortcut: ItemData(None, ItemClassification.progression, 0),
    ItemNames.item_event_quest_4mel_4th: ItemData(None, ItemClassification.progression, 0),
    ItemNames.item_event_agrade: ItemData(None, ItemClassification.progression_skip_balancing, 0),
    ItemNames.item_event_pacifist: ItemData(None, ItemClassification.progression_skip_balancing, 0),
    ItemNames.item_event_ludwig: ItemData(None, ItemClassification.progression, 0),
    ItemNames.item_event_wolfgang: ItemData(None, ItemClassification.progression, 0),
    #ItemNames.item_event_music: ItemData(None, ItemClassification.progression, 0),
}
item_dlc_special: dict[str, ItemData] = {
    ItemNames.item_charm_dlc_cookie: ItemData(dlc_id(22), ItemClassification.useful, 0),
    ItemNames.item_event_mausoleum: ItemData(None, ItemClassification.progression, 0),
    ItemNames.item_event_dlc_boataccess: ItemData(None, ItemClassification.progression, 0),
    ItemNames.item_event_dlc_start: ItemData(None, ItemClassification.progression, 0),
    ItemNames.item_event_dlc_boss_chaliced: ItemData(None, ItemClassification.progression_skip_balancing, 0),
}

item_goal: dict[str, ItemData] = {
    ItemNames.item_event_goal_devilko: ItemData(None, ItemClassification.progression, 0),
}
item_dlc_goal: dict[str, ItemData] = {
    ItemNames.item_event_goal_dlc_saltbakerko: ItemData(None, ItemClassification.progression, 0),
}

items_base: dict[str, ItemData] = {
    **item_generic,
    **item_filler,
    **item_essential,
    **item_charms,
    **item_super,
    **item_special,
    **item_goal
}
items_dlc: dict[str, ItemData] = {
    **item_dlc_essential,
    **item_dlc_charms,
    **item_dlc_special,
    **item_dlc_goal,
}

items_all: dict[str, ItemData] = {
    **items_base,
    **items_dlc,
    **item_weapons,
    **item_dlc_weapons,
    **item_p_weapons,
    **item_dlc_p_weapons,
    **item_dlc_chalice_essential,
    **item_dlc_chalice_super,
    **item_abilities,
    **item_dlc_chalice_abilities,
    #**item_abilities_aim,
    #**item_dlc_chalice_abilities_aim,
    **item_trap,
}

def get_item_groups() -> dict[str, set[str]]:
    n_item_groups: dict[str, set[str]] = {
        "Weapon": {*item_weapons.keys(), *item_p_weapons.keys(), *item_dlc_weapons.keys(), *item_dlc_p_weapons.keys()},
        "Charm": {*item_charms.keys(), *item_dlc_charms.keys(), ItemNames.item_charm_dlc_cookie},
        "Super": {*item_super.keys(), *item_dlc_chalice_super.keys()},
        "Ability": {
            *item_abilities.keys(),
            #*item_abilities_aim.keys(),
            *item_dlc_chalice_abilities.keys(),
            #*item_dlc_chalice_abilities_aim.keys()
        },
    }
    return n_item_groups

def add_item(items_ref: dict[str, ItemData], item: str):
    items_ref[item] = items_all[item]

def change_item_type(items_ref: dict[str, ItemData], item: str, item_type: ItemClassification):
    items_ref[item] = items_ref[item].with_item_type(item_type)

def change_item_quantity(items_ref: dict[str, ItemData], item: str, quantity: int):
    items_ref[item] = items_ref[item].with_quantity(quantity)

def setup_dlc_items(items_ref: dict[str, ItemData], settings: WorldSettings):
    items_ref.update(items_dlc)
    if settings.dlc_chalice>0:
        add_item(items_ref, ItemNames.item_charm_dlc_cookie)
        if settings.dlc_boss_chalice_checks or settings.dlc_cactusgirl_quest:
            change_item_type(items_ref, ItemNames.item_charm_dlc_cookie, ItemClassification.progression)
    if settings.is_dlc_chalice_items_separate(ItemGroups.ESSENTIAL):
        items_ref.update(item_dlc_chalice_essential)
    if settings.is_dlc_chalice_items_separate(ItemGroups.SUPER):
        items_ref.update(item_dlc_chalice_super)
    if settings.randomize_weapon_ex:
        change_item_quantity(items_ref, ItemNames.item_plane_ex, 1)

def setup_abilities(items_ref: dict[str, ItemData], settings: WorldSettings):
    items_ref.update(item_abilities)
    if settings.use_dlc and settings.is_dlc_chalice_items_separate(ItemGroups.ABILITIES):
        items_ref.update(item_dlc_chalice_abilities)
    change_item_type(items_ref, ItemNames.item_charm_psugar, ItemClassification.progression)
    if settings.boss_secret_checks:
        change_item_type(items_ref, ItemNames.item_ability_plane_shrink, ItemClassification.progression)

def setup_weapon_gate(items_ref: dict[str, ItemData], settings: WorldSettings):
    weapon_keys = {
        **item_weapons,
        **item_dlc_weapons,
    }
    for w in weapon_keys:
        if w in items_ref.keys():
            change_item_type(items_ref, w, ItemClassification.progression)

def setup_weapons(items_ref: dict[str, ItemData], settings: WorldSettings):
    _weapon_dict = itembase.get_weapon_dict(settings, settings.use_dlc)
    for weapon in _weapon_dict.values():
        items_ref[weapon] = items_all[weapon]
    if settings.randomize_weapon_ex > 0:
        change_item_quantity(items_ref, ItemNames.item_plane_ex, 1)
    if settings.randomize_weapon_ex == WeaponExMode.RANDOMIZED:
        _start_weapon = _weapon_dict[settings.start_weapon]
        change_item_quantity(items_ref, _start_weapon, 1)

def setup_items(settings: WorldSettings) -> dict[str, ItemData]:
    items: dict[str, ItemData] = {**items_base}
    setup_weapons(items, settings)
    if settings.use_dlc:
        setup_dlc_items(items, settings)
    if settings.weapon_gate:
        setup_weapon_gate(items, settings)
    if settings.randomize_abilities:
        setup_abilities(items, settings)
    if settings.randomize_abilities_aim:
        items.update(item_abilities_aim)
        if settings.use_dlc and settings.is_dlc_chalice_items_separate(ItemGroups.AIM_ABILITIES):
            items.update(item_dlc_chalice_abilities_aim)
    if settings.traps>0:
        items.update(item_trap)
    return items

name_to_id = {name: data.id for name, data in items_all.items() if data.id}
