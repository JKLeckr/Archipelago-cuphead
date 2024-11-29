from __future__ import annotations
import typing
from BaseClasses import Location, Region, Entrance
from worlds.generic.Rules import set_rule, forbid_item, forbid_items_for_player
from .items import item_filler
from .levels import level_rule_kingdice
from .locations import s_plane_locations
from .names import ItemNames, LocationNames
from .rulebase import Rule, rule_and, rule_has, rule_has_all, rule_has_any, region_rule_to_rule, rule_can_reach_all_regions
from . import locations
if typing.TYPE_CHECKING:
    from . import CupheadWorld

def get_entrance(world: CupheadWorld, exit: str, entrance: str) -> Entrance:
    return world.multiworld.get_entrance(exit+" -> "+entrance, world.player)
def get_location(world: CupheadWorld, location: str) -> Location:
    return world.multiworld.get_location(location, world.player)
def get_region(world: CupheadWorld, region: str) -> Region:
    return world.multiworld.get_region(region, world.player)
def set_item_rule(world: CupheadWorld, loc: str, item: str, count: int = 1) -> None:
    set_loc_rule(world, loc, rule_has(world, item, count))
def set_loc_rule(world: CupheadWorld, loc: str, rule: Rule = None) -> None:
    set_rule(get_location(world, loc), rule)
def set_region_rules(world: CupheadWorld, region_name: str, rule: Rule):
    region = get_region(world, region_name)
    for entrance in region.entrances:
        set_rule(entrance, rule)
def add_region_rules(world: CupheadWorld, region_name: str, rule: Rule):
    region = get_region(world, region_name)
    for entrance in region.entrances:
        if entrance.access_rule:
            set_rule(entrance, rule)

def set_rules(world: CupheadWorld):
    w = world
    settings = w.wsettings
    use_dlc = w.use_dlc
    contract_reqs = settings.contract_requirements
    ingredient_reqs = settings.dlc_ingredient_requirements

    set_region_rules(w, LocationNames.world_inkwell_2, rule_has(w, ItemNames.item_contract, contract_reqs[0]))
    set_region_rules(w, LocationNames.world_inkwell_3, rule_has(w, ItemNames.item_contract, contract_reqs[1]))
    set_region_rules(w, LocationNames.level_boss_kingdice,
                     rule_and(
                         rule_has(w, ItemNames.item_contract, contract_reqs[2]),
                         region_rule_to_rule(level_rule_kingdice(settings), w.player)
                     ))
    set_shop_rules(w)

    set_level_rules(w)

    set_item_rule(w, LocationNames.loc_coin_isle1_secret, ItemNames.item_event_isle1_secret_prereq, 5)
    if settings.fourmel_quest:
        set_item_rule(w, LocationNames.loc_quest_4mel, ItemNames.item_event_quest_4mel_4th)
    if settings.ginger_quest:
        set_item_rule(w, LocationNames.loc_quest_ginger, ItemNames.item_event_isle2_shortcut)
    if settings.agrade_quest:
        set_item_rule(w, LocationNames.loc_quest_silverworth, ItemNames.item_event_agrade, 15)
    if settings.pacifist_quest:
        set_item_rule(w, LocationNames.loc_quest_pacifist, ItemNames.item_event_pacifist, 6)
    if settings.music_quest:
        set_item_rule(w, LocationNames.loc_quest_music, ItemNames.item_event_ludwig)

    if use_dlc:
        set_region_rules(w, LocationNames.level_dlc_boss_saltbaker, rule_has(w, ItemNames.item_dlc_ingredient, ingredient_reqs))
        if settings.dlc_boss_chalice_checks:
            for _loc in locations.locations_dlc_boss_chaliced.keys():
                set_item_rule(w, _loc, ItemNames.item_charm_dlc_cookie)
        if settings.dlc_cactusgirl_quest:
            for _loc in locations.locations_dlc_event_boss_chaliced.keys():
                set_item_rule(w, _loc, ItemNames.item_charm_dlc_cookie)
            chaliced_events = set(locations.locations_dlc_event_boss_chaliced.keys())
            set_loc_rule(w, LocationNames.loc_dlc_quest_cactusgirl, rule_has_all(w, chaliced_events))

    set_goal(w)

def set_level_parry_rule(world: CupheadWorld, loc: str):
    w = world
    if loc in s_plane_locations:
        set_item_rule(w, loc, ItemNames.item_ability_plane_parry)
    else:
        set_item_rule(w, loc, ItemNames.item_ability_parry)

def set_level_rules(world: CupheadWorld):
    w = world
    boss_grade_checks = w.wsettings.boss_grade_checks
    rungun_grade_checks = w.wsettings.rungun_grade_checks
    boss_secret_checks = w.wsettings.boss_secret_checks
    if w.wsettings.randomize_abilities:
        if boss_grade_checks > 0:
            for _loc in locations.location_level_boss_topgrade:
                if _loc != LocationNames.loc_level_boss_kingdice_topgrade:
                    set_level_parry_rule(w, _loc)
            if w.wsettings.use_dlc:
                for _loc in locations.location_level_dlc_boss_topgrade:
                    set_level_parry_rule(w, _loc)
        if rungun_grade_checks > 0 and rungun_grade_checks < 5:
            for _loc in locations.location_level_rungun_agrade:
                set_item_rule(w, _loc, ItemNames.item_ability_parry)
        if boss_secret_checks:
            set_item_rule(w, LocationNames.loc_level_boss_plane_genie_secret, ItemNames.item_ability_plane_shrink)
            set_item_rule(w, LocationNames.loc_level_boss_sallystageplay_secret, ItemNames.item_ability_parry)

def set_shop_rules(world: CupheadWorld):
    w = world
    player = w.player
    use_dlc = w.use_dlc
    total_coins = w.total_coins
    shop_map = w.shop_map

    shop_items = {**locations.location_shop, **(locations.location_shop_dlc if use_dlc else {})}
    coins = (ItemNames.item_coin, ItemNames.item_coin2, ItemNames.item_coin3)

    # Prevent certain items from appearing in the shop
    for shop_item in shop_items.keys():
        _loc = get_location(w, shop_item)
        # Prevent putting money in the shop
        [forbid_item(_loc, x, player) for x in coins]
        # Prevent putting local filler items in the shop
        forbid_items_for_player(_loc, {x for x in item_filler.keys()}, player)

    # Set coin requirements for the shops
    shop_costs: list[int] = [0, 0, 0, 0]

    for i in range(len(shop_map)):
        shop_costs[i] = (shop_map[i][0]*4) + (shop_map[i][1]*3)

    total_cost = shop_costs[0] + shop_costs[1] + shop_costs[2] + (shop_costs[3] if use_dlc else 0)

    if total_cost > total_coins:
        raise Exception(f"Error: Total cost is {total_cost}, but there are {total_coins} coins!")
        # TODO: Add a resolution if this occurs

    for i in range(4 if use_dlc else 3):
        set_shop_cost_rule(w, i, shop_costs)

def set_shop_cost_rule(world: CupheadWorld, shop_index: int, shop_costs: list[int]):
    player = world.player
    cost = 0
    for i in range(shop_index+1):
        cost += shop_costs[i]
    region = get_region(world, LocationNames.level_shops[shop_index])
    for entrance in region.entrances:
        set_rule(entrance, lambda state: state.has(ItemNames.item_coin, player, cost))

def set_goal(world: CupheadWorld):
    w = world
    settings = w.wsettings
    w.multiworld.completion_condition[w.player] = (
        rule_has(w, ItemNames.item_contract, settings.contract_goal_requirements)
    ) if settings.mode == 1 else (
        rule_can_reach_all_regions(w, LocationNames.level_shops if settings.use_dlc else LocationNames.level_base_shops)
    ) if settings.mode == 2 else (
        rule_has(w, ItemNames.item_event_goal_dlc_saltbakerko)
    ) if settings.mode == 3 else (
        rule_has_all(w, {ItemNames.item_event_goal_devilko, ItemNames.item_event_goal_dlc_saltbakerko})
    ) if settings.mode == 4 else (
        rule_has(w, ItemNames.item_dlc_ingredient, settings.dlc_ingredient_goal_requirements)
    ) if settings.mode == 5 else (
        rule_and(
            rule_has(w, ItemNames.item_contract, settings.contract_goal_requirements),
            rule_has(w, ItemNames.item_dlc_ingredient, settings.dlc_ingredient_goal_requirements)
        )
    ) if settings.mode == 6 else (
        rule_has(w, ItemNames.item_event_goal_devilko)
    )
