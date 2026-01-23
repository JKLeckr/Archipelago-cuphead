### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing

from worlds.generic.Rules import forbid_item, forbid_items_for_player, set_rule

from ..enums import GameMode, ItemGroups
from ..items import itemdefs as idef
from ..locations import locationdefs as ld
from ..names import itemnames, locationnames, regionnames
from . import levelrules
from . import rulebase as rb

if typing.TYPE_CHECKING:
    from ... import CupheadWorld

def set_rules(world: CupheadWorld):
    w = world
    wconfig = w.wconfig
    use_dlc = w.use_dlc
    contract_reqs = wconfig.contract_requirements

    rb.set_region_rules(w, regionnames.world_inkwell_2, rb.rule_has(w, itemnames.item_contract, contract_reqs[0]))
    rb.set_region_rules(w, regionnames.world_inkwell_3, rb.rule_has(w, itemnames.item_contract, contract_reqs[1]))

    set_shop_rules(w)

    set_level_rules(w)

    rb.set_item_rule(w, locationnames.loc_coin_isle1_secret, itemnames.item_event_isle1_secret_prereq, 5)

    set_quest_rules(w)

    if use_dlc:
        set_dlc_rules(w)

    set_goal(w)

def set_dlc_rules(world: CupheadWorld):
    w = world
    wconfig = w.wconfig
    ingredient_reqs = wconfig.dlc_ingredient_requirements
    set_dlc_boat_rules(w)
    rb.set_region_rules(
        w,
        regionnames.level_dlc_boss_saltbaker,
        rb.rule_has(w, itemnames.item_dlc_ingredient, ingredient_reqs)
    )

def set_dlc_boat_rules(world: CupheadWorld):
    w = world
    wconfig = w.wconfig
    randomize_boat = wconfig.dlc_randomize_boat
    require_mausoleum = wconfig.dlc_requires_mausoleum
    if require_mausoleum:
        rb.add_region_rule(w, regionnames.reg_dlc_boat, rb.rule_has(w, itemnames.item_event_mausoleum))
    if randomize_boat:
        rb.add_region_rule(w, regionnames.reg_dlc_boat, rb.rule_has(w, itemnames.item_dlc_boat))

def set_quest_rules(world: CupheadWorld):
    w = world
    wconfig = w.wconfig
    if wconfig.fourmel_quest:
        rb.set_item_rule(w, locationnames.loc_quest_4mel, itemnames.item_event_quest_4mel_4th)
    if wconfig.ginger_quest:
        rb.set_item_rule(w, locationnames.loc_quest_ginger, itemnames.item_event_isle2_shortcut)
    if wconfig.buster_quest and wconfig.randomize_abilities:
        rb.set_item_rule(w, locationnames.loc_quest_buster, itemnames.item_ability_parry)
        if wconfig.is_dlc_chalice_items_separate(ItemGroups.ABILITIES):
            rb.add_loc_rule(w, locationnames.loc_quest_buster, rb.rule_has_all(w, {
                itemnames.item_ability_dlc_cdash,
                itemnames.item_ability_dlc_cparry,
            }), False)
    if wconfig.silverworth_quest:
        rb.set_item_rule(w, locationnames.loc_quest_silverworth, itemnames.item_event_agrade, 15)
    if wconfig.pacifist_quest:
        rb.set_item_rule(w, locationnames.loc_quest_pacifist, itemnames.item_event_pacifist, 6)
    if wconfig.music_quest:
        rb.set_item_rule(w, locationnames.loc_quest_music, itemnames.item_event_ludwig)

def set_level_rules(world: CupheadWorld):
    w = world
    levelrules.set_levelrules(w)

def set_shop_rules(world: CupheadWorld):
    w = world
    player = w.player
    use_dlc = w.use_dlc
    total_coins = w.total_coins
    shop_map = w.shop.shop_map

    shop_items = {**ld.location_shop, **(ld.location_shop_dlc if use_dlc else {})}
    coins = (itemnames.item_coin, itemnames.item_coin2, itemnames.item_coin3)

    # Prevent certain items from appearing in the shop
    for shop_item in shop_items.keys():
        _loc = rb.get_location(w, shop_item)
        # Prevent putting money in the shop
        [forbid_item(_loc, x, player) for x in coins]
        # Prevent putting local filler items in the shop
        forbid_items_for_player(_loc, set(idef.item_filler.keys()), player)

    # Set coin requirements for the shops
    shop_costs: list[int] = [0, 0, 0, 0]

    for i in range(len(shop_map)):
        shop_costs[i] = (shop_map[i][0]*4) + (shop_map[i][1]*3)

    total_cost = shop_costs[0] + shop_costs[1] + shop_costs[2] + (shop_costs[3] if use_dlc else 0)

    if total_cost > total_coins:
        raise Exception(f"Error: Total cost is {total_cost}, but there are {total_coins} coins!")

    for i in range(4 if use_dlc else 3):
        set_shop_cost_rule(w, i, shop_costs)

def set_shop_cost_rule(world: CupheadWorld, shop_index: int, shop_costs: list[int]):
    player = world.player
    cost = 0
    for i in range(shop_index+1):
        cost += shop_costs[i]
    region = rb.get_region(world, regionnames.shop_sets[shop_index])
    for entrance in region.entrances:
        set_rule(entrance, lambda state: state.has(itemnames.item_coin, player, cost))

def set_goal(world: CupheadWorld):
    w = world
    wconfig = w.wconfig
    w.multiworld.completion_condition[w.player] = (
        rb.rule_has(w, itemnames.item_contract, wconfig.contract_goal_requirements)
    ) if wconfig.mode == GameMode.COLLECT_CONTRACTS else (
        rb.rule_can_reach_all_regions(
            w, regionnames.shop_sets if wconfig.use_dlc else regionnames.base_shop_sets
        )
    ) if wconfig.mode == GameMode.BUY_OUT_SHOP else (
        rb.rule_has(w, itemnames.item_event_goal_dlc_saltbakerko)
    ) if wconfig.mode == GameMode.DLC_BEAT_SALTBAKER or wconfig.mode == GameMode.DLC_BEAT_SALTBAKER_ISLE4_ONLY else (
        rb.rule_has_all(w, {itemnames.item_event_goal_devilko, itemnames.item_event_goal_dlc_saltbakerko})
    ) if wconfig.mode == GameMode.DLC_BEAT_BOTH else (
        rb.rule_has(w, itemnames.item_dlc_ingredient, wconfig.dlc_ingredient_goal_requirements)
    ) if wconfig.mode == GameMode.DLC_COLLECT_INGREDIENTS else (
        rb.rule_and(
            rb.rule_has(w, itemnames.item_contract, wconfig.contract_goal_requirements),
            rb.rule_has(w, itemnames.item_dlc_ingredient, wconfig.dlc_ingredient_goal_requirements)
        )
    ) if wconfig.mode == GameMode.DLC_COLLECT_BOTH else (
        rb.rule_has(w, itemnames.item_event_goal_devilko)
    )
