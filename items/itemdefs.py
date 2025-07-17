from __future__ import annotations
from BaseClasses import ItemClassification
from ..names import ItemNames
from .itembase import ItemData

base_id = 12905168
base_dlc_id = 12909264

def iid(i: int): return base_id+i
def dlc_iid(i: int): return base_dlc_id+i

# Items
# Next ids: 67, 26
item_generic: dict[str, ItemData] = {
    ItemNames.item_level_generic: ItemData(iid(0), ItemClassification.filler, 0),
}
item_filler: dict[str, ItemData] = {
    ItemNames.item_level_extrahealth: ItemData(iid(1), ItemClassification.filler, 0),
    ItemNames.item_level_supercharge: ItemData(iid(2), ItemClassification.filler, 0),
    ItemNames.item_level_fastfire: ItemData(iid(3), ItemClassification.filler, 0),
    #ItemNames.item_level_4: ItemData(iid(4), ItemClassification.filler, 0),
}

item_essential: dict[str, ItemData] = {
    ItemNames.item_coin: ItemData(iid(5), ItemClassification.progression_skip_balancing, 0),
    ItemNames.item_coin2: ItemData(iid(6), ItemClassification.progression_skip_balancing, 0),
    ItemNames.item_coin3: ItemData(iid(7), ItemClassification.progression_skip_balancing, 0),
    ItemNames.item_contract: ItemData(iid(8), ItemClassification.progression_skip_balancing, 17),
    ItemNames.item_plane_gun: ItemData(iid(9), ItemClassification.progression),
    ItemNames.item_plane_ex: ItemData(iid(10), ItemClassification.progression, 0),
    ItemNames.item_plane_bombs: ItemData(iid(11), ItemClassification.progression),
    ItemNames.item_healthupgrade: ItemData(iid(12), ItemClassification.useful, 0)
}
item_dlc_essential: dict[str, ItemData] = {
    ItemNames.item_dlc_boat: ItemData(dlc_iid(0), ItemClassification.progression),
    ItemNames.item_dlc_ingredient: ItemData(dlc_iid(1), ItemClassification.progression_skip_balancing, 5),
}
item_dlc_chalice_essential: dict[str, ItemData] = {
    ItemNames.item_dlc_cplane_gun: ItemData(dlc_iid(2), ItemClassification.progression),
    ItemNames.item_dlc_cplane_ex: ItemData(dlc_iid(3), ItemClassification.progression, 0),
    ItemNames.item_dlc_cplane_bombs: ItemData(dlc_iid(4), ItemClassification.progression),
}

item_weapons: dict[str, ItemData] = {
    ItemNames.item_weapon_peashooter: ItemData(iid(13), ItemClassification.useful),
    ItemNames.item_weapon_spread: ItemData(iid(16), ItemClassification.useful),
    ItemNames.item_weapon_chaser: ItemData(iid(19), ItemClassification.useful),
    ItemNames.item_weapon_lobber: ItemData(iid(22), ItemClassification.useful),
    ItemNames.item_weapon_charge: ItemData(iid(25), ItemClassification.useful),
    ItemNames.item_weapon_roundabout: ItemData(iid(28), ItemClassification.useful),
}
item_dlc_weapons: dict[str, ItemData] = {
    ItemNames.item_weapon_dlc_crackshot: ItemData(dlc_iid(5), ItemClassification.useful),
    ItemNames.item_weapon_dlc_converge: ItemData(dlc_iid(8), ItemClassification.useful),
    ItemNames.item_weapon_dlc_twistup: ItemData(dlc_iid(11), ItemClassification.useful),
}
item_all_weapons: dict[str, ItemData] = {**item_weapons, **item_dlc_weapons}

item_weapon_ex: dict[str, ItemData] = {
    ItemNames.item_weapon_peashooter_ex: ItemData(iid(14), ItemClassification.useful),
    ItemNames.item_weapon_spread_ex: ItemData(iid(17), ItemClassification.useful),
    ItemNames.item_weapon_chaser_ex: ItemData(iid(20), ItemClassification.useful),
    ItemNames.item_weapon_lobber_ex: ItemData(iid(23), ItemClassification.useful),
    ItemNames.item_weapon_charge_ex: ItemData(iid(26), ItemClassification.useful),
    ItemNames.item_weapon_roundabout_ex: ItemData(iid(29), ItemClassification.useful),
}
item_dlc_weapon_ex: dict[str, ItemData] = {
    ItemNames.item_weapon_dlc_crackshot_ex: ItemData(dlc_iid(6), ItemClassification.useful),
    ItemNames.item_weapon_dlc_converge_ex: ItemData(dlc_iid(9), ItemClassification.useful),
    ItemNames.item_weapon_dlc_twistup_ex: ItemData(dlc_iid(12), ItemClassification.useful),
}
item_all_weapon_ex: dict[str, ItemData] = {**item_weapon_ex, **item_dlc_weapon_ex}

item_p_weapons: dict[str, ItemData] = {
    ItemNames.item_p_weapon_peashooter: ItemData(iid(15), ItemClassification.useful, 2),
    ItemNames.item_p_weapon_spread: ItemData(iid(18), ItemClassification.useful, 2),
    ItemNames.item_p_weapon_chaser: ItemData(iid(21), ItemClassification.useful, 2),
    ItemNames.item_p_weapon_lobber: ItemData(iid(24), ItemClassification.useful, 2),
    ItemNames.item_p_weapon_charge: ItemData(iid(27), ItemClassification.useful, 2),
    ItemNames.item_p_weapon_roundabout: ItemData(iid(30), ItemClassification.useful, 2),
}
item_dlc_p_weapons: dict[str, ItemData] = {
    ItemNames.item_p_weapon_dlc_crackshot: ItemData(dlc_iid(7), ItemClassification.useful, 2),
    ItemNames.item_p_weapon_dlc_converge: ItemData(dlc_iid(10), ItemClassification.useful, 2),
    ItemNames.item_p_weapon_dlc_twistup: ItemData(dlc_iid(13), ItemClassification.useful, 2),
}
item_all_p_weapons: dict[str, ItemData] = {**item_p_weapons, **item_dlc_p_weapons}

item_charms: dict[str, ItemData] = {
    ItemNames.item_charm_heart: ItemData(iid(31), ItemClassification.useful),
    ItemNames.item_charm_smokebomb: ItemData(iid(32), ItemClassification.useful),
    ItemNames.item_charm_psugar: ItemData(iid(33), ItemClassification.useful),
    ItemNames.item_charm_coffee: ItemData(iid(34), ItemClassification.useful),
    ItemNames.item_charm_twinheart: ItemData(iid(35), ItemClassification.useful),
    ItemNames.item_charm_whetstone: ItemData(iid(36), ItemClassification.useful),
}
item_dlc_charms: dict[str, ItemData] = {
    ItemNames.item_charm_dlc_heartring: ItemData(dlc_iid(14), ItemClassification.useful),
    ItemNames.item_charm_dlc_broken_relic: ItemData(dlc_iid(15), ItemClassification.useful, 0), # Sequence will not be in logic  # noqa: E501
}
item_all_charms: dict[str, ItemData] = {**item_charms, **item_dlc_charms}

item_super: dict[str, ItemData] = {
    ItemNames.item_super_i: ItemData(iid(37), ItemClassification.useful),
    ItemNames.item_super_ii: ItemData(iid(38), ItemClassification.useful),
    ItemNames.item_super_iii: ItemData(iid(39), ItemClassification.useful),
    ItemNames.item_plane_super: ItemData(iid(40), ItemClassification.useful),
}
item_dlc_chalice_super: dict[str, ItemData] = {
    ItemNames.item_super_dlc_c_i: ItemData(dlc_iid(16), ItemClassification.useful),
    ItemNames.item_super_dlc_c_ii: ItemData(dlc_iid(17), ItemClassification.useful),
    ItemNames.item_super_dlc_c_iii: ItemData(dlc_iid(18), ItemClassification.useful),
    ItemNames.item_dlc_cplane_super: ItemData(dlc_iid(19), ItemClassification.useful),
}

item_abilities: dict[str, ItemData] = {
    ItemNames.item_ability_duck: ItemData(iid(41), ItemClassification.progression),
    ItemNames.item_ability_dash: ItemData(iid(42), ItemClassification.progression),
    ItemNames.item_ability_parry: ItemData(iid(43), ItemClassification.progression),
    ItemNames.item_ability_plane_parry: ItemData(iid(44), ItemClassification.progression),
    ItemNames.item_ability_plane_shrink: ItemData(iid(45), ItemClassification.useful),
}
item_dlc_chalice_abilities: dict[str, ItemData] = {
    ItemNames.item_ability_dlc_cduck: ItemData(dlc_iid(20), ItemClassification.progression),
    ItemNames.item_ability_dlc_p_cdash: ItemData(dlc_iid(21), ItemClassification.progression, 2),
    ItemNames.item_ability_dlc_cdoublejump: ItemData(dlc_iid(22), ItemClassification.progression),
    ItemNames.item_ability_dlc_cplane_parry: ItemData(dlc_iid(23), ItemClassification.progression),
    ItemNames.item_ability_dlc_cplane_shrink: ItemData(dlc_iid(24), ItemClassification.useful),
}
item_abilities_aim: dict[str, ItemData] = {
    ItemNames.item_ability_aim_left: ItemData(iid(46), ItemClassification.progression),
    ItemNames.item_ability_aim_right: ItemData(iid(47), ItemClassification.progression),
    ItemNames.item_ability_aim_up: ItemData(iid(48), ItemClassification.progression),
    ItemNames.item_ability_aim_down: ItemData(iid(49), ItemClassification.progression),
    ItemNames.item_ability_aim_upleft: ItemData(iid(50), ItemClassification.progression),
    ItemNames.item_ability_aim_upright: ItemData(iid(51), ItemClassification.progression),
    ItemNames.item_ability_aim_downleft: ItemData(iid(52), ItemClassification.progression),
    ItemNames.item_ability_aim_downright: ItemData(iid(53), ItemClassification.progression),
}
item_dlc_chalice_abilities_aim: dict[str, ItemData] = {
    ItemNames.item_ability_dlc_c_aim_left: ItemData(iid(54), ItemClassification.progression),
    ItemNames.item_ability_dlc_c_aim_right: ItemData(iid(55), ItemClassification.progression),
    ItemNames.item_ability_dlc_c_aim_up: ItemData(iid(56), ItemClassification.progression),
    ItemNames.item_ability_dlc_c_aim_down: ItemData(iid(57), ItemClassification.progression),
    ItemNames.item_ability_dlc_c_aim_upleft: ItemData(iid(58), ItemClassification.progression),
    ItemNames.item_ability_dlc_c_aim_upright: ItemData(iid(59), ItemClassification.progression),
    ItemNames.item_ability_dlc_c_aim_downleft: ItemData(iid(60), ItemClassification.progression),
    ItemNames.item_ability_dlc_c_aim_downright: ItemData(iid(61), ItemClassification.progression),
}

item_trap: dict[str, ItemData] = {
    ItemNames.item_level_trap_fingerjam: ItemData(iid(62), ItemClassification.trap, 0),
    ItemNames.item_level_trap_slowfire: ItemData(iid(63), ItemClassification.trap, 0),
    ItemNames.item_level_trap_superdrain: ItemData(iid(64), ItemClassification.trap, 0),
    ItemNames.item_level_trap_loadout: ItemData(iid(65), ItemClassification.trap, 0),
    ItemNames.item_level_trap_screen: ItemData(iid(66), ItemClassification.trap, 0),
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
    ItemNames.item_charm_dlc_cookie: ItemData(dlc_iid(25), ItemClassification.useful, 0),
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
    **item_weapon_ex,
    **item_dlc_weapon_ex,
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

name_to_id = {name: data.id for name, data in items_all.items() if data.id}
