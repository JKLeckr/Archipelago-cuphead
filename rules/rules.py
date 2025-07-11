from __future__ import annotations
import typing
from BaseClasses import Location, Region, Entrance
from worlds.generic.Rules import set_rule, add_rule, forbid_item, forbid_items_for_player
from . import rulebase as rb
from ..levels import levelrules, levellocrules
from ..items import weapons, itemdefs as idef
from ..locations import locationdefs as ld
from ..names import ItemNames, LocationNames
from .rulebase import Rule
from ..enums import GameMode, WeaponMode, ItemGroups
if typing.TYPE_CHECKING:
    from .. import CupheadWorld

def get_entrance(world: CupheadWorld, exit: str, entrance: str) -> Entrance:
    return world.multiworld.get_entrance(exit+" -> "+entrance, world.player)
def get_location(world: CupheadWorld, location: str) -> Location:
    return world.multiworld.get_location(location, world.player)
def get_region(world: CupheadWorld, region: str) -> Region:
    return world.multiworld.get_region(region, world.player)
def set_item_rule(world: CupheadWorld, loc: str, item: str, count: int = 1) -> None:
    set_loc_rule(world, loc, rb.rule_has(world, item, count))
def add_item_rule(world: CupheadWorld, loc: str, item: str, count: int = 1, combine_and: bool = True) -> None:
    add_loc_rule(world, loc, rb.rule_has(world, item, count), combine_and)
def set_loc_rule(world: CupheadWorld, loc: str, rule: Rule) -> None:
    set_rule(get_location(world, loc), rule)
def add_loc_rule(world: CupheadWorld, loc: str, rule: Rule, combine_and: bool = True) -> None:
    add_rule(get_location(world, loc), rule, "and" if combine_and else "or")
def set_region_rules(world: CupheadWorld, region_name: str, rule: Rule):
    region = get_region(world, region_name)
    for entrance in region.entrances:
        set_rule(entrance, rule)
def add_region_rules(world: CupheadWorld, region_name: str, rule: Rule, combine_and: bool = True):
    region = get_region(world, region_name)
    for entrance in region.entrances:
        add_rule(entrance, rule, "and" if combine_and else "or")

def set_rules(world: CupheadWorld):
    w = world
    settings = w.wconfig
    use_dlc = w.use_dlc
    contract_reqs = settings.contract_requirements

    set_region_rules(w, LocationNames.world_inkwell_2, rb.rule_has(w, ItemNames.item_contract, contract_reqs[0]))
    set_region_rules(w, LocationNames.world_inkwell_3, rb.rule_has(w, ItemNames.item_contract, contract_reqs[1]))
    set_region_rules(w, LocationNames.level_boss_kingdice,
                     rb.rule_and(
                         rb.rule_has(w, ItemNames.item_contract, contract_reqs[2]),
                         rb.region_rule_to_rule(levelrules.level_rule_kingdice(settings), w.player)
                     ))
    set_shop_rules(w)

    set_level_rules(w)

    set_item_rule(w, LocationNames.loc_coin_isle1_secret, ItemNames.item_event_isle1_secret_prereq, 5)

    set_quest_rules(w)

    if use_dlc:
        set_dlc_rules(w)

    set_goal(w)

def set_dlc_rules(world: CupheadWorld):
    w = world
    settings = w.wconfig
    ingredient_reqs = settings.dlc_ingredient_requirements
    set_dlc_boat_rules(w)
    set_region_rules(
        w,
        LocationNames.level_dlc_boss_saltbaker,
        rb.rule_has(w, ItemNames.item_dlc_ingredient, ingredient_reqs)
    )
    if settings.dlc_boss_chalice_checks:
        for _loc in ld.locations_dlc_boss_chaliced.keys():
            set_item_rule(w, _loc, ItemNames.item_charm_dlc_cookie)
    if settings.dlc_cactusgirl_quest:
        for _loc in ld.locations_dlc_event_boss_chaliced.keys():
            set_item_rule(w, _loc, ItemNames.item_charm_dlc_cookie)
        num_chaliced_events = len(ld.locations_dlc_event_boss_chaliced.keys())
        set_loc_rule(
            w,
            LocationNames.loc_dlc_quest_cactusgirl,
            rb.rule_has(w, ItemNames.item_event_dlc_boss_chaliced, num_chaliced_events)
        )

def set_dlc_boat_rules(world: CupheadWorld):
    w = world
    settings = w.wconfig
    randomize_boat = settings.dlc_randomize_boat
    require_mausoleum = settings.dlc_requires_mausoleum
    if require_mausoleum:
        add_region_rules(w, LocationNames.reg_dlc_boat, rb.rule_has(w, ItemNames.item_event_mausoleum))
    if randomize_boat:
        add_region_rules(w, LocationNames.reg_dlc_boat, rb.rule_has(w, ItemNames.item_dlc_boat))

def set_quest_rules(world: CupheadWorld):
    w = world
    settings = w.wconfig
    if settings.fourmel_quest:
        set_item_rule(w, LocationNames.loc_quest_4mel, ItemNames.item_event_quest_4mel_4th)
    if settings.ginger_quest:
        set_item_rule(w, LocationNames.loc_quest_ginger, ItemNames.item_event_isle2_shortcut)
    if settings.buster_quest and settings.randomize_abilities:
        set_item_rule(w, LocationNames.loc_quest_buster, ItemNames.item_ability_parry)
        if settings.is_dlc_chalice_items_separate(ItemGroups.ABILITIES):
            add_loc_rule(w, LocationNames.loc_quest_buster, rb.rule_has_all(w, {
                ItemNames.item_ability_dlc_cdash,
                ItemNames.item_ability_dlc_cparry,
            }), False)
    if settings.silverworth_quest:
        set_item_rule(w, LocationNames.loc_quest_silverworth, ItemNames.item_event_agrade, 15)
    if settings.pacifist_quest:
        set_item_rule(w, LocationNames.loc_quest_pacifist, ItemNames.item_event_pacifist, 6)
    if settings.music_quest:
        set_item_rule(w, LocationNames.loc_quest_music, ItemNames.item_event_ludwig)

def get_weapon_ex_rules(world: CupheadWorld) -> Rule:
    w = world
    res: Rule = rb.rule_none()
    for i in range(len(weapons.weapon_dict)):
        rule = rb.rule_has(
            w,
            weapons.weapon_p_dict[i],
            2
        )
        if i == 0:
            res = rule
        else:
            res = rb.rule_or(res, rule)
    return res

def add_level_grade_rule(world: CupheadWorld, loc: str):
    w = world
    if loc in ld.s_plane_locations:
        add_item_rule(w, loc, ItemNames.item_ability_plane_parry)
        if w.wconfig.weapon_mode == WeaponMode.PROGRESSIVE:
            add_loc_rule(w, loc, rb.rule_has_any(w, {
                ItemNames.item_plane_ex,
                ItemNames.item_plane_super,
                ItemNames.item_dlc_cplane_ex,
                ItemNames.item_dlc_cplane_super,
            }), False)
    else:
        add_item_rule(w, loc, ItemNames.item_ability_parry)
        if w.wconfig.weapon_mode == WeaponMode.PROGRESSIVE:
            add_loc_rule(w, loc, rb.rule_or(rb.rule_has(w, "Super"), get_weapon_ex_rules(w)), False)
        # TODO: Chalice?

def set_level_loc_rules(world: CupheadWorld):
    w = world
    loc_rules = levellocrules.level_loc_rules
    for _loc_rule in loc_rules:
        for loc, rule in _loc_rule.loc_rules.items():
            if loc in w.active_locations:
                set_loc_rule(w, loc, rb.region_rule_to_rule(rule(w.wconfig), w.player))
            elif world.settings.verbose:
                print(f"[set_level_loc_rules] Skipping {loc}")

def set_level_boss_grade_rules(world: CupheadWorld):
    w = world
    boss_grade_checks = w.wconfig.boss_grade_checks
    if boss_grade_checks > 0:
        for _loc in ld.location_level_boss_topgrade:
            if (
                _loc != LocationNames.loc_level_boss_kingdice_topgrade and
                _loc not in levellocrules.level_loc_rule_locs
                ):
                add_level_grade_rule(w, _loc)
        if w.wconfig.silverworth_quest:
            for _loc in ld.location_level_boss_event_agrade:
                if (
                    _loc != LocationNames.loc_level_boss_kingdice_event_agrade and
                    _loc not in levellocrules.level_loc_rule_locs
                    ):
                    add_level_grade_rule(w, _loc)
        if w.wconfig.use_dlc:
            for _loc in ld.location_level_dlc_boss_topgrade:
                if _loc not in levellocrules.level_loc_rule_locs:
                    add_level_grade_rule(w, _loc)

def set_level_rules(world: CupheadWorld):
    w = world
    #rungun_grade_checks = w.wsettings.rungun_grade_checks
    boss_secret_checks = w.wconfig.boss_secret_checks
    set_level_loc_rules(w)
    # TODO: Eventually phase this over to the level_loc_rules
    if w.wconfig.randomize_abilities:
        set_level_boss_grade_rules(w)
        if boss_secret_checks:
            add_item_rule(w, LocationNames.loc_level_boss_plane_genie_secret, ItemNames.item_ability_plane_shrink)
            add_item_rule(w, LocationNames.loc_level_boss_sallystageplay_secret, ItemNames.item_ability_parry)

def set_shop_rules(world: CupheadWorld):
    w = world
    player = w.player
    use_dlc = w.use_dlc
    total_coins = w.total_coins
    shop_map = w.shop.shop_map

    shop_items = {**ld.location_shop, **(ld.location_shop_dlc if use_dlc else {})}
    coins = (ItemNames.item_coin, ItemNames.item_coin2, ItemNames.item_coin3)

    # Prevent certain items from appearing in the shop
    for shop_item in shop_items.keys():
        _loc = get_location(w, shop_item)
        # Prevent putting money in the shop
        [forbid_item(_loc, x, player) for x in coins]
        # Prevent putting local filler items in the shop
        forbid_items_for_player(_loc, {x for x in idef.item_filler.keys()}, player)

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
    region = get_region(world, LocationNames.shop_sets[shop_index])
    for entrance in region.entrances:
        set_rule(entrance, lambda state: state.has(ItemNames.item_coin, player, cost))

def set_goal(world: CupheadWorld):
    w = world
    settings = w.wconfig
    w.multiworld.completion_condition[w.player] = (
        rb.rule_has(w, ItemNames.item_contract, settings.contract_goal_requirements)
    ) if settings.mode == GameMode.COLLECT_CONTRACTS else (
        rb.rule_can_reach_all_regions(
            w, LocationNames.shop_sets if settings.use_dlc else LocationNames.base_shop_sets
        )
    ) if settings.mode == GameMode.BUY_OUT_SHOP else (
        rb.rule_has(w, ItemNames.item_event_goal_dlc_saltbakerko)
    ) if settings.mode == GameMode.DLC_BEAT_SALTBAKER or settings.mode == GameMode.DLC_BEAT_SALTBAKER_ISLE4_ONLY else (
        rb.rule_has_all(w, {ItemNames.item_event_goal_devilko, ItemNames.item_event_goal_dlc_saltbakerko})
    ) if settings.mode == GameMode.DLC_BEAT_BOTH else (
        rb.rule_has(w, ItemNames.item_dlc_ingredient, settings.dlc_ingredient_goal_requirements)
    ) if settings.mode == GameMode.DLC_COLLECT_INGREDIENTS else (
        rb.rule_and(
            rb.rule_has(w, ItemNames.item_contract, settings.contract_goal_requirements),
            rb.rule_has(w, ItemNames.item_dlc_ingredient, settings.dlc_ingredient_goal_requirements)
        )
    ) if settings.mode == GameMode.DLC_COLLECT_BOTH else (
        rb.rule_has(w, ItemNames.item_event_goal_devilko)
    )
