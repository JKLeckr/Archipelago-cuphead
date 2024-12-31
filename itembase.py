from __future__ import annotations
import math
import typing
from typing import Optional
from random import Random
from BaseClasses import Item, ItemClassification
from .auxiliary import count_in_list
from .items import CupheadItem
from .names import ItemNames, LocationNames
from .settings import WorldSettings
from . import items, locations
if typing.TYPE_CHECKING:
    from . import CupheadWorld

def create_item(name: str, player: int, force_classification: Optional[ItemClassification] = None) -> Item:
    data = items.items_all[name]

    if force_classification:
        classification = force_classification
    else:
        classification = data.type

    #print("Item: "+name+", "+str(classification))

    new_item = CupheadItem(name, classification, data.id, player)

    return new_item

def weighted_item_choice(item_weights: list[tuple[str, int]], rand: Random) -> str:
    if len(item_weights)<1:
        raise ValueError("item_weights must not be empty!")

    active_items, active_weights = zip(*item_weights)

    total_weight = sum(active_weights)

    choice = rand.randint(1, total_weight)

    culmu_sum = 0
    for i, weight in enumerate(active_weights):
        culmu_sum += weight
        if choice <= culmu_sum:
            return active_items[i]
    return active_items[-1]

def get_filler_item_name(world: CupheadWorld) -> str:
    return weighted_item_choice(world.filler_item_weights, world.random)

def create_filler_items(world: CupheadWorld, filler_count: int) -> list[Item]:
    #print(f"Filler count: {filler_count}")
    rand = world.random
    _itempool: list[Item] = []
    if filler_count > 0:
        trap_count = math.ceil(world.wsettings.traps / 100 * filler_count)
        #print(f"Trap count: {trap_count}")
        if trap_count>0:
            _itempool += create_traps(trap_count, world.player, world.wsettings, rand)
            filler_count -= trap_count

        #print(f"Total count so far: {len(_itempool)}")
        #print(f"Filler count: {filler_count}")
        #print(len(world.multiworld.precollected_items[world.player]))
        _itempool += [create_item(get_filler_item_name(world), world.player) for _ in range(filler_count)]

    #print(f"Total count: {len(_itempool)}")
    return _itempool

def create_traps(trap_count: int, player:int, settings: WorldSettings, rand: Random) -> list[Item]:
    trap_items = list(items.item_trap.keys())
    trap_item_weights = settings.trap_weights

    active_trap_weights = [(trap, weight) for trap, weight in zip(trap_items, trap_item_weights) if weight > 0]

    if not active_trap_weights:
        return []

    res: list[Item] = []

    for _ in range(trap_count):
        res.append(create_item(weighted_item_choice(active_trap_weights, rand), player))

    return res

def create_pool_items(world: CupheadWorld, items: list[str], precollected: list[str]) -> list[Item]:
    _itempool: list[Item] = []
    for itemname in items:
        item = world.active_items[itemname]
        qty = item.quantity - count_in_list(item, precollected)
        if qty<0:
            print(f"WARNING: \"{items}\" has quantity of {str(qty)}!")
        if item.id and qty>0:
            _itempool += [create_item(itemname, world.player, item.type) for _ in range(qty)]
    return _itempool

def create_locked_item(world: CupheadWorld, name: str, location: str, force_classification: Optional[ItemClassification] = None) -> None:
    world.multiworld.get_location(location, world.player).place_locked_item(create_item(name, world.player, force_classification))
def create_locked_items(world: CupheadWorld, name: str, locations:  dict[str, locations.LocationData],
                        force_classification: Optional[ItemClassification] = None) -> None:
    for loc in locations:
        if loc in world.active_locations:
            create_locked_item(world, name, loc, force_classification)

def setup_locked_items(world: CupheadWorld):
    # Locked Items
    for i in range(1,6):
        _loc = LocationNames.loc_event_isle1_secret_prereq+" "+str(i)
        create_locked_item(world, ItemNames.item_event_isle1_secret_prereq, _loc)
    if world.wsettings.ginger_quest:
        create_locked_item(world, ItemNames.item_event_isle2_shortcut, LocationNames.loc_event_isle2_shortcut)
    if world.wsettings.fourmel_quest:
        create_locked_item(world, ItemNames.item_event_quest_4mel_4th, LocationNames.loc_event_quest_4mel_4th)
    if world.wsettings.music_quest:
        create_locked_item(world, ItemNames.item_event_ludwig, LocationNames.loc_event_quest_ludwig)
        #create_locked_item(world, ItemNames.item_event_wolfgang, LocationNames.loc_event_quest_wolfgang)
    if world.wsettings.agrade_quest:
        create_locked_items(world, ItemNames.item_event_agrade, locations.locations_event_agrade)
    if world.wsettings.pacifist_quest:
        create_locked_items(world, ItemNames.item_event_pacifist, locations.location_level_rungun_event_pacifist)
    create_locked_item(world, ItemNames.item_event_goal_devilko, LocationNames.loc_event_goal_devil)

    if world.use_dlc:
        create_locked_item(world, ItemNames.item_event_dlc_boataccess, LocationNames.loc_event_dlc_boatarrival)
        #create_locked_item(world, ItemNames.item_charm_dlc_broken_relic, LocationNames.loc_level_dlc_graveyard)
        create_locked_item(world, ItemNames.item_event_goal_dlc_saltbakerko, LocationNames.loc_event_dlc_goal_saltbaker)
        create_locked_items(world, ItemNames.item_event_agrade, locations.locations_dlc_event_agrade)
        create_locked_items(world, ItemNames.item_event_dlc_boss_chaliced, locations.locations_dlc_event_boss_chaliced)

def compress_coins(coin_amounts: tuple[int, int, int], location_count: int) -> tuple[int, int, int]:
    total_single_coins, total_double_coins, total_triple_coins = coin_amounts
    def _total_coins():
        return total_single_coins + total_double_coins + total_triple_coins
    while _total_coins() >= location_count:
        if total_single_coins >= 2 and _total_coins():
            total_single_coins -= 2
            total_double_coins += 1
        elif total_single_coins >= 3:
            total_single_coins -= 3
            total_triple_coins += 1
        elif total_double_coins >= 1 and total_single_coins >= 1:
            total_single_coins -= 1
            total_double_coins -= 1
            total_triple_coins += 1
        elif total_double_coins >= 3:
            total_double_coins -= 3
            total_triple_coins += 2
        elif total_single_coins >= 2:
            total_single_coins -= 2
            total_double_coins += 1
        else:
            print("Error: Cannot resolve coins!")
            break
    return (total_single_coins, total_double_coins, total_triple_coins)

def create_coins(world: CupheadWorld, location_count: int, precollected_item_names: list[str],
                 coin_items: tuple[str, str, str]) -> list[Item]:
    res: list[Item] = []
    # Coins
    coin_amounts = world.wsettings.coin_amounts ## TODO: Start inventory from pool vs start inventory. Allow for extra coins depending on shop
    total_single_coins = coin_amounts[0]
    total_double_coins = coin_amounts[1]
    total_triple_coins = coin_amounts[2]
    total_coins = world.total_coins

    # Starter Coins
    start_coins = 0
    for item in precollected_item_names:
        if item == coin_items[0]:
            start_coins += 1
        elif item == coin_items[1]:
            start_coins += 2
        elif item == coin_items[2]:
            start_coins += 3

    total_coins -= start_coins

    start_3coins = min(start_coins // 3, total_triple_coins)
    start_coins -= start_3coins * 3
    start_2coins = min(start_coins // 2, total_double_coins)
    start_coins -= start_2coins * 2

    total_triple_coins = max(total_triple_coins - start_3coins, 0)
    total_double_coins = max(total_double_coins - start_2coins, 0)
    total_single_coins = max(total_single_coins - start_coins, 0)

    total_coins = compress_coins((total_single_coins, total_double_coins, total_triple_coins), location_count)

    res += [create_item(coin_items[0], world.player) for _ in range(total_coins[0])]
    res += [create_item(coin_items[1], world.player) for _ in range(total_coins[1])]
    res += [create_item(coin_items[2], world.player) for _ in range(total_coins[2])]

    return res

def create_items(world: CupheadWorld) -> None:
    itempool: list[Item] = []

    precollected_item_names = [x.name for x in world.multiworld.precollected_items[world.player]]

    setup_locked_items(world)

    # total_locations = len([x.name for x in world.multiworld.get_locations(world.player) if not x.event])
    unfilled_locations = len([x.name for x in world.multiworld.get_unfilled_locations(world.player)])
    #print(total_locations)
    #print(unfilled_locations)
    # This can fail if someone uses plando
    # if total_locations != unfilled_locations:
    #     print("ERROR: unfilled locations mismatch total non-event locations")

    # Starter weapon
    weapon_dict: dict[int,str] = {
        0: ItemNames.item_weapon_peashooter,
        1: ItemNames.item_weapon_spread,
        2: ItemNames.item_weapon_chaser,
        3: ItemNames.item_weapon_lobber,
        4: ItemNames.item_weapon_charge,
        5: ItemNames.item_weapon_roundabout,
        6: ItemNames.item_weapon_dlc_crackshot,
        7: ItemNames.item_weapon_dlc_converge,
        8: ItemNames.item_weapon_dlc_twistup,
    }
    weapons = [x for x in set(items.item_weapons.keys()) if x not in precollected_item_names]
    if world.use_dlc:
        weapons.extend([x for x in set(items.item_dlc_weapons.keys()) if x not in precollected_item_names])
    start_weapon_index = world.start_weapon
    start_weapon = weapon_dict[start_weapon_index]
    if start_weapon in weapons:
        weapons.remove(start_weapon)

    # Item names for coins
    coin_items = (ItemNames.item_coin, ItemNames.item_coin2, ItemNames.item_coin3)

    essential_items = [y for y in items.item_essential.keys() if y not in coin_items] + (list(items.item_essential.keys()) if world.use_dlc else [])
    charms = list(items.item_charms.keys()) + (list(items.item_dlc_charms.keys()) if world.use_dlc else [])
    abilities = list(items.item_abilities.keys())

    # Add the other non-filler items before the coins
    itempool += create_pool_items(world, essential_items, precollected_item_names)
    itempool += create_pool_items(world, weapons, precollected_item_names)
    itempool += create_pool_items(world, charms, precollected_item_names)
    itempool += create_pool_items(world, list(items.item_super.keys()), precollected_item_names)
    if world.wsettings.randomize_abilities:
        itempool += create_pool_items(world, abilities, precollected_item_names)

    # Add Coins
    leftover_locations = unfilled_locations - len(itempool) - world.wsettings.minimum_filler

    itempool += create_coins(world, leftover_locations, precollected_item_names, coin_items)

    leftover_locations = unfilled_locations - len(itempool)
    if (leftover_locations<0):
        print("Error: There are more items than locations!")

    # Filler Items and Traps
    filler_count = leftover_locations
    if filler_count>0:
        itempool += create_filler_items(world, filler_count)

    #print("itempool size: "+str(len(itempool)))
    world.multiworld.itempool += itempool
