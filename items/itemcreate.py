from __future__ import annotations
import math
import typing
from collections.abc import Iterable
from random import Random
from BaseClasses import Item, ItemClassification, LocationProgressType
from ..auxiliary import count_in_list
from ..names import ItemNames, LocationNames
from ..enums import WeaponMode, ItemGroups, ChaliceMode, CurseMode
from ..wconf import WorldConfig
from ..locations import locationdefs as ldef
from .itembase import CupheadItem, ItemData, get_filler_item_name, weighted_item_choice
from . import weapons, itemdefs as idef
if typing.TYPE_CHECKING:
    from .. import CupheadWorld

def create_item(name: str, player: int, force_classification: ItemClassification | None = None) -> Item:
    return create_item_ext(name, player, idef.items_all, force_classification)

def create_active_item(name: str, world: CupheadWorld, force_classification: ItemClassification | None = None) -> Item:
    return create_item_ext(name, world.player, world.active_items, force_classification)

def create_item_ext(
        name: str,
        player: int,
        item_defs: dict[str, ItemData],
        force_classification: ItemClassification | None = None
    ) -> Item:
    data = item_defs[name]

    if force_classification:
        classification = force_classification
    else:
        classification = data.item_type

    #print("Item: "+name+", "+str(classification))

    new_item = CupheadItem(name, classification, data.id, player)

    return new_item

def create_filler_item(world: CupheadWorld) -> Item:
    return create_active_item(get_filler_item_name(world), world)

def create_filler_items(world: CupheadWorld, filler_count: int) -> list[Item]:
    #print(f"Filler count: {filler_count}")
    rand = world.random
    _itempool: list[Item] = []
    if filler_count > 0:
        trap_count = math.ceil(world.wconfig.traps / 100 * filler_count)
        #print(f"Trap count: {trap_count}")
        if trap_count>0:
            _itempool += create_traps(world, trap_count, world.wconfig, rand)
            filler_count -= trap_count

        #print(f"Total count so far: {len(_itempool)}")
        #print(f"Filler count: {filler_count}")
        #print(len(world.multiworld.precollected_items[world.player]))
        _itempool += [create_filler_item(world) for _ in range(filler_count)]

    #print(f"Total count: {len(_itempool)}")
    return _itempool

def create_traps(world: CupheadWorld, trap_count: int, wconf: WorldConfig, rand: Random) -> list[Item]:
    active_trap_weights = wconf.trap_item_weights

    if not active_trap_weights:
        return []

    res: list[Item] = []

    for _ in range(trap_count):
        res.append(create_active_item(weighted_item_choice(active_trap_weights, rand), world))

    return res

def create_pool_items(world: CupheadWorld, items: list[str], precollected: list[str]) -> list[Item]:
    _itempool: list[Item] = []
    for itemname in items:
        if itemname in world.active_items.keys():
            item = world.active_items[itemname]
            qty = item.quantity - count_in_list(itemname, precollected)
            #if qty<0:
            #    print(f"WARNING: \"{items}\" has quantity of {str(qty)}!")
            if item.id and qty>0:
                _itempool += [create_active_item(itemname, world, item.item_type) for _ in range(qty)]
    return _itempool

def create_locked_item(
        world: CupheadWorld,
        name: str,
        location: str,
        force_classification: ItemClassification | None = None
    ):
    #print(f"Create locked item: '{name}' at '{location}'")
    world.multiworld.get_location(location, world.player) \
        .place_locked_item(create_active_item(name, world, force_classification))
def create_locked_items_at(
        world: CupheadWorld,
        name: str,
        locations: Iterable[str],
        force_classification: ItemClassification | None = None
    ):
    for loc in locations:
        if loc in world.active_locations.keys():
            create_locked_item(world, name, loc, force_classification)
        elif world.settings.is_debug_bit_on(1):
            print(f"Skipped {name} for {loc}")

def create_dlc_locked_items(world: CupheadWorld):
    create_locked_item(world, ItemNames.item_event_mausoleum, LocationNames.loc_event_mausoleum)
    create_locked_item(world, ItemNames.item_event_dlc_boataccess, LocationNames.loc_event_dlc_boatarrival)
    if world.wconfig.dlc_chalice == ChaliceMode.VANILLA:
        create_locked_item(world, ItemNames.item_charm_dlc_cookie, LocationNames.loc_event_dlc_cookie)
    if LocationNames.loc_event_dlc_goal_saltbaker in world.active_locations:
        if not world.wconfig.is_goal_used(LocationNames.loc_event_dlc_goal_saltbaker):
            print("WARNING: Saltbaker Goal location created even if it shouldn't")
        create_locked_item(world, ItemNames.item_event_goal_dlc_saltbakerko, LocationNames.loc_event_dlc_goal_saltbaker)
    create_locked_items_at(world, ItemNames.item_event_dlc_boss_chaliced, ldef.locations_dlc_event_boss_chaliced)
    create_locked_items_at(
        world,
        ItemNames.item_event_dlc_boss_chaliced,
        ldef.locations_dlc_event_boss_final_chaliced
    )

def create_locked_items(world: CupheadWorld):
    # Locked Items
    for i in range(1,6):
        _loc = LocationNames.loc_event_isle1_secret_prereq+" "+str(i)
        create_locked_item(world, ItemNames.item_event_isle1_secret_prereq, _loc)
    if world.wconfig.ginger_quest:
        create_locked_item(world, ItemNames.item_event_isle2_shortcut, LocationNames.loc_event_isle2_shortcut)
    if world.wconfig.fourmel_quest:
        create_locked_item(world, ItemNames.item_event_quest_4mel_4th, LocationNames.loc_event_quest_4mel_4th)
    if world.wconfig.music_quest:
        create_locked_item(world, ItemNames.item_event_ludwig, LocationNames.loc_event_quest_ludwig)
        #create_locked_item(world, ItemNames.item_event_wolfgang, LocationNames.loc_event_quest_wolfgang)
    if world.wconfig.silverworth_quest:
        create_locked_items_at(world, ItemNames.item_event_agrade, ldef.locations_event_agrade)
        create_locked_items_at(world, ItemNames.item_event_agrade, ldef.location_level_boss_final_event_agrade)
    if world.wconfig.pacifist_quest:
        create_locked_items_at(world, ItemNames.item_event_pacifist, ldef.location_level_rungun_event_pacifist)
    if LocationNames.loc_event_goal_devil in world.active_locations:
        if not world.wconfig.is_goal_used(LocationNames.loc_event_goal_devil):
            print("WARNING: Devil Goal location created even if it shouldn't")
        create_locked_item(world, ItemNames.item_event_goal_devilko, LocationNames.loc_event_goal_devil)

    if world.use_dlc:
        create_dlc_locked_items(world)

def create_special_items(world: CupheadWorld, precollected: list[str]) -> list[Item]:
    wconf = world.wconfig
    items: list[Item] = []

    for _ in range(world.wconfig.maxhealth_upgrades):
        items.append(create_active_item(ItemNames.item_healthupgrade, world))
    if wconf.use_dlc:
        if wconf.dlc_chalice == ChaliceMode.RANDOMIZED and ItemNames.item_charm_dlc_cookie not in precollected:
            items.append(create_active_item(ItemNames.item_charm_dlc_cookie, world))
        if (wconf.dlc_curse_mode == CurseMode.VANILLA or wconf.dlc_curse_mode == CurseMode.REVERSE and \
            ItemNames.item_charm_dlc_broken_relic not in precollected):
                items.append(create_active_item(ItemNames.item_charm_dlc_broken_relic, world))

    return items

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

def create_start_weapons(world: CupheadWorld) -> set[str]:
    wconf = world.wconfig
    weapon_dict = weapons.get_weapon_dict(world.wconfig)
    res: set[str] = set()

    weapon = weapon_dict[wconf.start_weapon]

    create_locked_item(world, weapon, LocationNames.loc_event_start_weapon, ItemClassification.progression)
    res.add(weapon)
    if LocationNames.loc_event_start_weapon_ex in world.active_locations:
        if wconf.weapon_mode == WeaponMode.PROGRESSIVE_EXCEPT_START:
            weapon_ex = weapons.weapon_p_dict[wconf.start_weapon]
        elif wconf.weapon_mode == WeaponMode.EX_SEPARATE_EXCEPT_START:
            weapon_ex = weapons.weapon_ex_dict[wconf.start_weapon]
        else:
            weapon_ex = ""
        create_locked_item(world, weapon_ex, LocationNames.loc_event_start_weapon_ex, ItemClassification.progression)
        res.add(weapon_ex)
    return res

def setup_weapon_pool(world: CupheadWorld, precollected_item_names: list[str]) -> list[str]:
    _weapons: list[str] = []
    _weapon_dict = weapons.get_weapon_dict(world.wconfig)

    _start_weapons = create_start_weapons(world)

    _no_set = {*precollected_item_names, *_start_weapons}

    _weapons = [x for x in set(_weapon_dict.values()) if x not in _no_set]

    if (world.wconfig.weapon_mode & WeaponMode.EX_SEPARATE) > 0:
        _weapons.extend([x for x in set(idef.item_weapon_ex.keys()) if x not in _no_set])
        if world.use_dlc:
            _weapons.extend([x for x in set(idef.item_dlc_weapon_ex.keys()) if x not in _no_set])

    return _weapons

def setup_ability_pool(world: CupheadWorld, precollected_item_names: list[str]) -> list[str]:
    _precollected = precollected_item_names
    abilities = list(idef.item_abilities.keys())
    # FIXME: Is this needed? If they are not active, they won't be added anyways
    if world.wconfig.dlc_chalice_items_separate & ItemGroups.ABILITIES:
        abilities.extend(idef.item_dlc_chalice_abilities.keys())
    else:
        abilities.append(ItemNames.item_ability_dlc_cdoublejump)
    # FIXME: Is checking precollected needed? (it is probably done elsewhere)
    return abilities

def create_coins(world: CupheadWorld, location_count: int, precollected_item_names: list[str],
                 coin_items: tuple[str, str, str]) -> list[Item]:
    res: list[Item] = []
    # Coins
    # TODO: Start inventory from pool vs start inventory. Allow for extra coins depending on shop.
    coin_amounts = world.wconfig.coin_amounts
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

    res += [create_active_item(coin_items[0], world) for _ in range(total_coins[0])]
    res += [create_active_item(coin_items[1], world) for _ in range(total_coins[1])]
    res += [create_active_item(coin_items[2], world) for _ in range(total_coins[2])]

    return res

def create_items(world: CupheadWorld) -> None:
    itempool: list[Item] = []

    precollected_item_names = [x.name for x in world.multiworld.precollected_items[world.player]]

    create_locked_items(world)

    # Setup Weapons including start weapons
    weapons = setup_weapon_pool(world, precollected_item_names)

    #total_locations = len([x.name for x in world.multiworld.get_locations(world.player) if not x.is_event])
    unfilled_locations = [x for x in world.multiworld.get_unfilled_locations(world.player)]
    unfilled_location_count = len(unfilled_locations)
    #print(total_locations)
    #print(unfilled_locations)
    # This can fail if someone uses plando
    # if total_locations != unfilled_locations:
    #     print("ERROR: unfilled locations mismatch total non-event locations")

    #print(weapons)

    # Item names for coins
    coin_items = (ItemNames.item_coin, ItemNames.item_coin2, ItemNames.item_coin3)

    essential_items = (
        [y for y in idef.item_essential.keys() if y not in coin_items] + \
            (list(idef.item_dlc_essential.keys()) if world.use_dlc else [])
    )
    charms = list(idef.item_charms.keys()) + (list(idef.item_dlc_charms.keys()) if world.use_dlc else [])
    supers = list(idef.item_super.keys())

    if world.use_dlc and world.wconfig.dlc_chalice_items_separate:
        essential_items += list(idef.item_dlc_chalice_essential.keys())
        #supers += list(items.item_dlc_chalice_super) # TODO: Investigate adding this later

    # Add the grouped fill items
    itempool += create_pool_items(world, essential_items, precollected_item_names)
    itempool += create_pool_items(world, weapons, precollected_item_names)
    itempool += create_pool_items(world, charms, precollected_item_names)
    itempool += create_pool_items(world, supers, precollected_item_names)
    if world.wconfig.randomize_abilities:
        abilities = setup_ability_pool(world, precollected_item_names)
        itempool += create_pool_items(world, abilities, precollected_item_names)

    # Add special Items
    itempool += create_special_items(world, precollected_item_names)

    excluded_location_count = len(
        [x for x in unfilled_locations if x.progress_type == LocationProgressType.EXCLUDED]
    )
    minimum_filler = max(world.wconfig.minimum_filler, excluded_location_count)

    # Add Coins
    leftover_locations = unfilled_location_count - len(itempool) - minimum_filler

    itempool += create_coins(world, leftover_locations, precollected_item_names, coin_items)

    leftover_locations = unfilled_location_count - len(itempool)
    if (leftover_locations<0):
        print("Error: There are more items than locations!")

    # Filler Items and Traps
    filler_count = leftover_locations
    if filler_count>0:
        itempool += create_filler_items(world, filler_count)

    #print("itempool size: "+str(len(itempool)))
    world.multiworld.itempool += itempool
