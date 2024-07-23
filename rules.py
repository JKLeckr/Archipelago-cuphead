from BaseClasses import MultiWorld, Location
from worlds.generic.Rules import set_rule, forbid_item
from .locations import location_shop, location_shop_dlc, locations_dlc_boss_chaliced, locations_dlc_event_boss_chaliced
from .names import ItemNames, LocationNames
from .settings import WorldSettings

class RuleData:
    multiworld: MultiWorld
    player: int
    use_dlc: bool
    total_coins: int
    def __init__(self, multiworld: MultiWorld, player: int, settings: WorldSettings, total_coins: int, shop_map: list[tuple[int]]):
        self.multiworld = multiworld
        self.player = player
        self.use_dlc = settings.use_dlc
        self.total_coins = total_coins
        self.shop_map = shop_map
    def get_entrance(self, exit: str, entrance: str) -> Location:
        return self.multiworld.get_entrance(exit+" -> "+entrance, self.player)
    def get_location(self, location: str) -> Location:
        return self.multiworld.get_location(location, self.player)

def set_rules(multiworld: MultiWorld, player: int, settings: WorldSettings, total_coins: int, shop_map: list[tuple[int]]):
    rdata = RuleData(multiworld, player, settings, total_coins, shop_map)
    use_dlc = rdata.use_dlc

    set_rule(rdata.get_location(LocationNames.loc_coin_isle1_secret), lambda state: state.has(ItemNames.item_event_isle1_secret_prereq, player, 5))
    if settings.fourmel_quest:
        set_rule(rdata.get_location(LocationNames.loc_quest_4mel), lambda state: state.has(ItemNames.item_event_quest_4mel_4th, player))
    if settings.ginger_quest:
        set_rule(rdata.get_location(LocationNames.loc_quest_ginger), lambda state: state.has(ItemNames.item_event_isle2_shortcut, player))
    if settings.agrade_quest:
        set_rule(rdata.get_location(LocationNames.loc_quest_15agrades), lambda state: state.has(ItemNames.item_event_agrade, player, 15))
    if settings.pacifist_quest:
        set_rule(rdata.get_location(LocationNames.loc_quest_pacifist), lambda state: state.has(ItemNames.item_event_pacifist, player, 6))
    if settings.wolfgang_quest:
        set_rule(rdata.get_location(LocationNames.loc_quest_wolfgang), lambda state: state.has(ItemNames.item_event_music, player))
    set_shop_rules(rdata) # This will be fully implemented later. There is currently flaws in the logic right now.

    if use_dlc:
        if settings.dlc_boss_chalice_checks:
            for _loc in locations_dlc_boss_chaliced.keys():
                set_rule(rdata.get_location(_loc), lambda state:
                         state.has(ItemNames.item_charm_dlc_cookie, player))
        if settings.dlc_cactusgirl_quest:
            for _loc in locations_dlc_event_boss_chaliced.keys():
                set_rule(rdata.get_location(_loc), lambda state:
                         state.has(ItemNames.item_charm_dlc_cookie, player))
            set_rule(rdata.get_location(LocationNames.loc_dlc_quest_cactusgirl),
                     lambda state: state.has_all(set(locations_dlc_event_boss_chaliced.keys()), player))

    multiworld.completion_condition[player] = (
        lambda state: state.has_all({ItemNames.item_event_goal_devilko, ItemNames.item_event_goal_dlc_saltbakerko}, player)
    ) if use_dlc else (
        lambda state: state.has(ItemNames.item_event_goal_devilko, player)
    )

def set_shop_rules(rdata: RuleData):
    player = rdata.player
    use_dlc = rdata.use_dlc
    total_coins = rdata.total_coins
    shop_map = rdata.shop_map

    shop_items = {**location_shop, **(location_shop_dlc if use_dlc else {})}
    coins = (ItemNames.item_coin, ItemNames.item_coin2, ItemNames.item_coin3)

    # Prevent putting money in the shop
    for shop_item in shop_items.keys():
        [forbid_item(rdata.get_location(shop_item), x, player) for x in coins]

    # Set coin requirements for the shops
    shop_costs: list[int] = [0, 0, 0, 0]

    for i in range(len(shop_map)):
        shop_costs[i] = (shop_map[i][0]*4) + (shop_map[i][1]*3)

    total_cost = shop_costs[0] + shop_costs[1] + shop_costs[2] + (shop_costs[3] if use_dlc else 0)

    if total_cost > total_coins:
        raise Exception(f"Error: Total cost is {total_cost}, but there are {total_coins} coins!")
        # TODO: Add a resolution if this occurs

    for i in range(4 if use_dlc else 3):
        set_shop_cost_rule(rdata, i, player, shop_costs)

def set_shop_cost_rule(rdata: RuleData, shop_index: int, player: int, shop_costs: list[int]):
    cost = 0
    for i in range(shop_index+1):
        cost += shop_costs[i]
    location = LocationNames.world_inkwell + LocationNames._nums_[shop_index]
    set_rule(rdata.get_entrance(location, LocationNames.level_shops[shop_index]), lambda state: state.has(ItemNames.item_coin, player, cost))
