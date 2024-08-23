from __future__ import annotations
import math
import typing
from random import Random
from BaseClasses import Item, ItemClassification
from .names import ItemNames, LocationNames
from .auxiliary import count_in_list
from .items import CupheadItem
from . import items, locations
if typing.TYPE_CHECKING:
    from . import CupheadWorld

def create_item(name: str, player: int, force_classification: ItemClassification = None) -> Item:
    data = items.items_all[name]

    if force_classification:
            classification = force_classification
    else:
        classification = data.type

    new_item = CupheadItem(name, classification, data.id, player)

    return new_item

def get_filler_item_name(random: Random):
    return random.choice(tuple(items.item_filler.keys()))

def create_pool_items(world: CupheadWorld, items: list[str], precollected: list[str]) -> list[CupheadItem]:
    _itempool = []
    for item in items:
        qty = world.active_items[item].quantity - count_in_list(item, precollected)
        if qty<0:
            print("WARNING: \""+item+"\" has quantity of "+str(qty)+"!")
        if world.active_items[item].id and qty>0:
            _itempool += [create_item(item, world.player) for _ in range(qty)]
    return _itempool
def create_filler_items(world: CupheadWorld, filler_count: int) -> list[Item]:
    rand = world.random
    _itempool: list[Item] = []
    if filler_count > 0:
        trap_count = math.ceil(world.wsettings.traps / filler_count * 100)
        if world.wsettings.traps>0:
            trap_items = set(items.item_trap.keys())
            if world.wsettings.envirotraps:
                trap_items.add(ItemNames.item_level_trap_envirotrap)
            _itempool += [create_item(rand.choice(trap_items), world.player) for _ in range(trap_count)]
            filler_count -= trap_count

        #print(len(world.multiworld.precollected_items[world.player]))
        _itempool += [create_item(get_filler_item_name(rand), world.player) for _ in range(filler_count)]

    return _itempool

def create_locked_item(world: CupheadWorld, name: str, location: str, force_classification: ItemClassification = None) -> None:
    world.multiworld.get_location(location, world.player).place_locked_item(create_item(name, world.player, force_classification))
def create_locked_items(world: CupheadWorld, name: str, locations: set[str], force_classification: ItemClassification = None) -> None:
    for loc in locations:
        if loc in world.active_locations:
            create_locked_item(world, name, loc, force_classification)

def create_items(world: CupheadWorld) -> None:
    itempool: list[CupheadItem] = []

    #TODO: Handle start_inventory

    #starter_items.append(world.create_item(ItemNames.item_charm_heart))
    #print(len(starter_items))
    precollected_item_names = [x.name for x in world.multiworld.precollected_items[world.player]]
    def append_starter_items(item: Item):
        world.multiworld.push_precollected(item)
        precollected_item_names.append(item.name)

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

    total_locations = len([x.name for x in world.multiworld.get_locations(world.player) if not x.event])
    unfilled_locations = len([x.name for x in world.multiworld.get_unfilled_locations(world.player)])
    #print(total_locations)
    #print(unfilled_locations)
    if total_locations != unfilled_locations:
        print("ERROR: unfilled locations mismatch total non-event locations")

    # Shop Items
    #shop_events = {**Locations.location_shop_event, **(Locations.location_shop_dlc_event if world.use_dlc else {})}
    #for shop_event in shop_events.keys():
    #    if shop_events[shop_event].category == "weapon":
    #        create_locked_item(world, ItemNames.item_weapon,shop_event)
    #    if shop_events[shop_event].category == "charm":
    #        create_locked_item(world, ItemNames.item_charm,shop_event)
    #    if shop_events[shop_event].category == "dlc_weapon":
    #        create_locked_item(world, ItemNames.item_dlc_weapon,shop_event)
    #    if shop_events[shop_event].category == "dlc_charm":
    #        create_locked_item(world, ItemNames.item_dlc_charm,shop_event)

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
    weapons = {x for x in set(items.item_weapons.keys()) if x not in precollected_item_names}
    start_weapon_index = world.start_weapon
    if world.use_dlc:
        weapons.update({x for x in set(items.item_dlc_weapons.keys()) if x not in precollected_item_names})
    start_weapon = weapon_dict[start_weapon_index]
    if start_weapon in weapons:
        weapons.remove(start_weapon)

    # Item names for coins
    coin_items = (ItemNames.item_coin, ItemNames.item_coin2, ItemNames.item_coin3)

    essential_items = [y for y in items.item_essential.keys() if y not in coin_items] + (list(items.item_essential.keys()) if world.use_dlc else [])
    charms = list(items.item_charms.keys()) + (list(items.item_dlc_charms.keys()) if world.use_dlc else [])

    # Add the other non-filler items before the coins
    itempool += create_pool_items(world, essential_items, precollected_item_names)
    itempool += create_pool_items(world, weapons, precollected_item_names)
    itempool += create_pool_items(world, charms, precollected_item_names)
    itempool += create_pool_items(world, items.item_super.keys(), precollected_item_names)
    if world.wsettings.randomize_abilities:
        itempool += create_pool_items(items.item_abilities.keys(), precollected_item_names)

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

    leftover_locations = total_locations - len(itempool) - world.wsettings.filler_item_buffer

    start_3coins = min(start_coins // 3, total_triple_coins)
    start_coins -= start_3coins * 3
    start_2coins = min(start_coins // 2, total_double_coins)
    start_coins -= start_2coins * 2

    total_triple_coins = max(total_triple_coins - start_3coins, 0)
    total_double_coins = max(total_double_coins - start_2coins, 0)
    total_single_coins = max(total_single_coins - start_coins, 0)

    while (total_single_coins + total_double_coins + total_triple_coins) >= leftover_locations:
        if total_single_coins >= 3:
            total_single_coins -= 3
            total_triple_coins += 1
        elif total_double_coins >= 1 and total_single_coins >= 1:
            total_single_coins -= 1
            total_double_coins -= 1
            total_triple_coins += 1
        elif total_double_coins >= 3:
            total_double_coins -= 3
            total_triple_coins += 2
        else:
            print("Error: Cannot resolve coins!")
            break

    # Add Coins
    itempool += [create_item(coin_items[0], world.player) for _ in range(total_single_coins)]
    itempool += [create_item(coin_items[1], world.player) for _ in range(total_double_coins)]
    itempool += [create_item(coin_items[2], world.player) for _ in range(total_triple_coins)]

    leftover_locations = total_locations - len(itempool)
    if (leftover_locations<0):
        print("Error: There are more items than locations!")

    # Filler Items and Traps
    filler_count = leftover_locations
    if filler_count>0:
        itempool += create_filler_items(world, filler_count)

    #print("itempool size: "+str(len(itempool)))
    world.multiworld.itempool += itempool
