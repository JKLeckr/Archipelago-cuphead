from __future__ import annotations
from typing import NamedTuple, Optional
from BaseClasses import Item, ItemClassification
from .names import ItemNames
from .settings import WorldSettings

class CupheadItem(Item):
    game: str = "Cuphead"

class ItemData(NamedTuple):
    id: Optional[int]
    type: ItemClassification = ItemClassification.filler
    quantity: int = 1 # Set to 0 to skip automatic placement (Useful if placing manually)
    event: bool = False
    catefory: str = None

base_id = 0xc4ead0
base_dlc_id = 0xc4fad0

def id(i: int): return base_id+i
def dlc_id(i: int): return base_dlc_id+i

# Items
# Next ids: 42, 8
item_generic = {
    ItemNames.item_level_generic: ItemData(id(0), ItemClassification.filler, 0),
}
item_filler = {
    ItemNames.item_level_extrahealth: ItemData(id(1), ItemClassification.filler, 0),
    ItemNames.item_level_superrecharge: ItemData(id(2), ItemClassification.filler, 0),
}

item_essential = {
    ItemNames.item_coin: ItemData(id(3), ItemClassification.progression_skip_balancing, 0),
    ItemNames.item_coin2: ItemData(id(4), ItemClassification.progression_skip_balancing, 0),
    ItemNames.item_coin3: ItemData(id(5), ItemClassification.progression_skip_balancing, 0),
    ItemNames.item_plane_gun: ItemData(id(6), ItemClassification.progression),
    ItemNames.item_plane_bombs: ItemData(id(7), ItemClassification.progression),
    ItemNames.item_plane_super: ItemData(id(8), ItemClassification.useful),
    ItemNames.item_contract: ItemData(id(9), ItemClassification.progression_skip_balancing, 17),
}
item_dlc_essential = {
    ItemNames.item_dlc_boat: ItemData(dlc_id(0), ItemClassification.progression, 5),
    ItemNames.item_dlc_ingredient: ItemData(dlc_id(1), ItemClassification.progression_skip_balancing, 5),
}

item_weapons = {
    ItemNames.item_weapon_peashooter: ItemData(id(10), ItemClassification.useful,1),
    ItemNames.item_weapon_spread: ItemData(id(11), ItemClassification.useful,1),
    ItemNames.item_weapon_chaser: ItemData(id(12), ItemClassification.useful,1),
    ItemNames.item_weapon_lobber: ItemData(id(13), ItemClassification.useful,1),
    ItemNames.item_weapon_charge: ItemData(id(14), ItemClassification.useful,1),
    ItemNames.item_weapon_roundabout: ItemData(id(15), ItemClassification.useful,1),
}
item_dlc_weapons = {
    ItemNames.item_weapon_dlc_crackshot: ItemData(dlc_id(2), ItemClassification.useful),
    ItemNames.item_weapon_dlc_converge: ItemData(dlc_id(3), ItemClassification.useful),
    ItemNames.item_weapon_dlc_twistup: ItemData(dlc_id(4), ItemClassification.useful),
}

item_charms = {
    ItemNames.item_charm_heart: ItemData(id(16), ItemClassification.useful),
    ItemNames.item_charm_smokebomb: ItemData(id(17), ItemClassification.useful),
    ItemNames.item_charm_psugar: ItemData(id(18), ItemClassification.useful),
    ItemNames.item_charm_coffee: ItemData(id(19), ItemClassification.useful),
    ItemNames.item_charm_twinheart: ItemData(id(20), ItemClassification.useful),
    ItemNames.item_charm_whetstone: ItemData(id(21), ItemClassification.useful),
}
item_dlc_charms = {
    #ItemNames.item_charm_dlc_cookie: ItemData(dlc_id(5), ItemClassification.useful, 0),
    ItemNames.item_charm_dlc_heartring: ItemData(dlc_id(6), ItemClassification.useful),
    ItemNames.item_charm_dlc_broken_relic: ItemData(dlc_id(7), ItemClassification.useful, 1), # Sequence will not be in logic
}

item_shop = {
    #ItemNames.item_weapon: ItemData(None, ItemClassification.progression, 0),
    #ItemNames.item_charm: ItemData(None, ItemClassification.useful, 0),
}
item_dlc_shop = {
    #ItemNames.item_dlc_weapon: ItemData(None, ItemClassification.progression, 0),
    #ItemNames.item_dlc_charm: ItemData(None, ItemClassification.useful, 0),
}

item_super = {
    ItemNames.item_super_i: ItemData(id(22), ItemClassification.useful),
    ItemNames.item_super_ii: ItemData(id(23), ItemClassification.useful,0),
    ItemNames.item_super_iii: ItemData(id(24), ItemClassification.useful,0),
}

item_abilities = {
    ItemNames.item_ability_duck: ItemData(id(25), ItemClassification.progression),
    ItemNames.item_ability_dash: ItemData(id(26), ItemClassification.progression),
    ItemNames.item_ability_parry: ItemData(id(27), ItemClassification.progression),
    ItemNames.item_ability_plane_shrink: ItemData(id(28), ItemClassification.useful),
    ItemNames.item_ability_plane_parry: ItemData(id(29), ItemClassification.useful),
}
item_abilities_aim = {
    ItemNames.item_ability_aim_left: ItemData(id(30), ItemClassification.progression),
    ItemNames.item_ability_aim_right: ItemData(id(31), ItemClassification.progression),
    ItemNames.item_ability_aim_up: ItemData(id(32), ItemClassification.progression),
    ItemNames.item_ability_aim_down: ItemData(id(33), ItemClassification.progression),
    ItemNames.item_ability_aim_upleft: ItemData(id(34), ItemClassification.progression),
    ItemNames.item_ability_aim_upright: ItemData(id(35), ItemClassification.progression),
    ItemNames.item_ability_aim_downleft: ItemData(id(36), ItemClassification.progression),
    ItemNames.item_ability_aim_downright: ItemData(id(37), ItemClassification.progression),
}

item_trap = {
    #ItemNames.item_level_trap_fingerjam: ItemData(id(38), ItemClassification.trap, 0),
    #ItemNames.item_level_trap_slowfire: ItemData(id(39), ItemClassification.trap, 0),
    ItemNames.item_level_trap_superdrain: ItemData(id(40), ItemClassification.trap, 0),
    ItemNames.item_level_trap_reversal: ItemData(id(41), ItemClassification.trap, 0)
}
item_trap_special = {
    ItemNames.item_level_trap_envirotrap: ItemData(id(42), ItemClassification.trap, 0),
}

item_special = {
    ItemNames.item_event_boss_defeated: ItemData(None, ItemClassification.progression_skip_balancing, 0),
    ItemNames.item_event_isle1_secret_prereq: ItemData(None, ItemClassification.progression_skip_balancing, 0),
    ItemNames.item_event_isle2_shortcut: ItemData(None, ItemClassification.progression, 0),
    ItemNames.item_event_quest_4mel_4th: ItemData(None, ItemClassification.progression, 0),
    ItemNames.item_event_agrade: ItemData(None, ItemClassification.progression_skip_balancing, 0),
    ItemNames.item_event_pacifist: ItemData(None, ItemClassification.progression_skip_balancing, 0),
    ItemNames.item_event_ludwig: ItemData(None, ItemClassification.progression, 0),
    ItemNames.item_event_wolfgang: ItemData(None, ItemClassification.progression, 0),
    #ItemNames.item_event_music: ItemData(None, ItemClassification.progression, 0),
    ItemNames.item_event_dlc_boss_chaliced: ItemData(None, ItemClassification.progression_skip_balancing, 0),
}
item_dlc_special = {
    #ItemNames.item_event_dlc_boataccess: ItemData(None, ItemClassification.progression, 0),
    ItemNames.item_event_dlc_start: ItemData(None, ItemClassification.progression, 0),
}

item_goal = {ItemNames.item_event_goal_devilko: ItemData(None, ItemClassification.progression, 0),}
item_dlc_goal = {ItemNames.item_event_goal_dlc_saltbakerko: ItemData(None, ItemClassification.progression, 0),}

items_base = {
    #**item_generic,
    **item_filler,
    **item_essential,
    **item_weapons,
    **item_charms,
    **item_shop,
    **item_super,
    **item_special,
    **item_goal
}
items_dlc = {
    **item_dlc_essential,
    **item_dlc_weapons,
    **item_dlc_charms,
    **item_dlc_shop,
    **item_dlc_special,
    **item_dlc_goal,
}

items_all = {
    **items_base,
    **items_dlc,
    **item_abilities,
    **item_trap,
    **item_trap_special
}

def setup_items(settings: WorldSettings):
    items: dict[str,ItemData] = {**items_base}
    if settings.use_dlc:
        items.update(items_dlc)
        if settings.dlc_boss_chalice_checks or settings.dlc_cactusgirl_quest:
            items[ItemNames.item_charm_dlc_cookie].type = ItemClassification.progression
    if settings.weapon_gate:
        weapon_keys = {
            **item_weapons,
            **item_dlc_weapons,
        }
        for w in weapon_keys:
            if w in items.keys():
                items[w].type = ItemClassification.progression
    if settings.randomize_abilities:
        items.update(item_abilities)
    if settings.traps>0:
        items.update(item_trap)
        if settings.envirotraps:
            items.update(item_trap_special[ItemNames.item_level_trap_envirotrap])
    return items

name_to_id = {name: data.id for name, data in items_all.items() if data.id}
