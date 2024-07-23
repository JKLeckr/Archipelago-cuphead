## ScriptStash: A place for discarded code that might be useful in the future

from __future__ import annotations
from BaseClasses import MultiWorld
from .names import ItemNames, LocationNames
from .levels import LevelData
from . import items

using_dlc = False

shop_item_weapons = [
        LocationNames.loc_shop_weapon1,
        LocationNames.loc_shop_weapon2,
        LocationNames.loc_shop_weapon3,
        LocationNames.loc_shop_weapon4,
        LocationNames.loc_shop_weapon5,
]
shop_item_dlc_weapons = [
        LocationNames.loc_shop_dlc_weapon6,
        LocationNames.loc_shop_dlc_weapon7,
        LocationNames.loc_shop_dlc_weapon8,
]
shop_item_charms = [
        LocationNames.loc_shop_charm1,
        LocationNames.loc_shop_charm2,
        LocationNames.loc_shop_charm3,
        LocationNames.loc_shop_charm4,
        LocationNames.loc_shop_charm5,
        LocationNames.loc_shop_charm6,
]
shop_item_dlc_charms = [
        LocationNames.loc_shop_dlc_charm7,
        LocationNames.loc_shop_dlc_charm8,
]
shop_items_list = shop_item_weapons + shop_item_charms + ((shop_item_dlc_weapons + shop_item_dlc_charms) if using_dlc else [])

# Weapon Gate Logic
def create_weapontiers(multiworld: MultiWorld, player: int, starting_weapons: list[str] = None) -> dict[int,list[str]]:
    use_dlc = multiworld.game_content[player] == "delicious_last_course"
    rand = multiworld.random
    tiers = 3
    res: dict[int,list[str]] = {}
    start_weapons = starting_weapons if starting_weapons else []
    weapons = []
    [weapons.append(x) for x in items.item_weapons.keys() if (x not in start_weapons)]
    if use_dlc:
        [weapons.append(x) for x in items.item_dlc_weapons.keys() if (x not in start_weapons)]
    res.update({0: start_weapons})
    rand.shuffle(weapons)
    weapons_per_tier = -(len(weapons)//-tiers)
    for i in range(tiers):
        res.update({i+1: weapons[(i*weapons_per_tier):min((i+1)*weapons_per_tier,len(weapons))]})
    return res

def create_weapongates(multiworld: MultiWorld, player: int, weapon_tiers: dict[int,list[str]], levels: dict[str,LevelData]) -> dict[str,(str,str)]:
    use_dlc = multiworld.game_content[player] == "delicious_last_course"
    rand = multiworld.random
    res: dict[str,tuple(str,str)] = {}
    weapons = list(items.item_weapons.keys())
    used_weapons = []
    if use_dlc:
        weapons.append(items.item_dlc_weapons.keys())
    for level in levels.keys:
        weapon_pool = []
        if levels[level].is_starter:
            weapon_pool = weapon_tiers[0]
        elif levels[level].world_location == LocationNames.world_inkwell_1:
            weapon_pool = weapon_tiers[0] + weapon_tiers[1]
        elif levels[level].world_location == LocationNames.world_inkwell_2:
            weapon_pool = weapon_tiers[0] + weapon_tiers[1] + weapon_tiers[2]
        elif levels[level].world_location == LocationNames.world_inkwell_3:
            weapon_pool = weapons
        else:
            weapon_pool = weapons

        if not (all(x in used_weapons for x in weapon_pool)):
            weapon_pool = [x for x in weapon_pool if x not in used_weapons]
        res.update({level: tuple(rand.choices(weapon_pool, k=2))})

    return res

