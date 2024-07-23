from BaseClasses import MultiWorld, Location
from worlds.generic.Rules import set_rule, forbid_item
from .Locations import location_shop, location_shop_dlc, locations_dlc_boss_chaliced, locations_dlc_event_boss_chaliced
from .names import ItemNames, LocationNames
from .Settings import WorldSettings

class RuleData:
    multiworld: MultiWorld
    player: int
    use_dlc: bool
    total_coins: int
    def __init__(self, multiworld: MultiWorld, player: int, settings: WorldSettings, total_coins: int):
        self.multiworld = multiworld
        self.player = player
        self.use_dlc = settings.use_dlc
        self.total_coins = total_coins
    def get_entrance(self, exit: str, entrance: str) -> Location:
        return self.multiworld.get_entrance(exit+" -> "+entrance, self.player)
    def get_location(self, location: str) -> Location:
        return self.multiworld.get_location(location, self.player)

def set_rules(multiworld: MultiWorld, player: int, settings: WorldSettings, total_coins: int):
    rdata = RuleData(multiworld, player, settings, total_coins)
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
    set_rule(rdata.get_entrance(LocationNames.world_inkwell_1, LocationNames.level_shop), lambda state: state.has(ItemNames.item_coin, player, total_coins))
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
        lambda state: state.has_all({ItemNames.item_goal_devilko, ItemNames.item_goal_dlc_saltbakerko}, player)
    ) if use_dlc else (
        lambda state: state.has(ItemNames.item_goal_devilko, player)
    )

def set_shop_rules(rdata: RuleData):
    player = rdata.player
    use_dlc = rdata.use_dlc

    shop_items = {**location_shop, **(location_shop_dlc if use_dlc else {})}
    coins = (ItemNames.item_coin, ItemNames.item_coin2, ItemNames.item_coin3)

     # Prevent putting money in the shop
    for shop_item in shop_items.keys():
        [forbid_item(rdata.get_location(shop_item), x, player) for x in coins]

    # Set Rules for items to be bought
    #item_costs: dict[str,tuple[int,int]] = {
    #    LocationNames.loc_shop_weapon1: (4, 18), # Format: (cost, group total requirement in world progression)
    #    LocationNames.loc_shop_weapon2: (4, 18),
    #    LocationNames.loc_shop_weapon3: (4, 18),
    #    LocationNames.loc_shop_weapon4: (4, 36 if use_dlc else 32),
    #    LocationNames.loc_shop_weapon5: (4, 36 if use_dlc else 32),

    #    LocationNames.loc_shop_dlc_weapon6: (4, 36),
    #    LocationNames.loc_shop_dlc_weapon7: (4, 52),
    #    LocationNames.loc_shop_dlc_weapon8: (4, 52),

    #    LocationNames.loc_shop_charm1: (3, 18),
    #    LocationNames.loc_shop_charm2: (3, 18),
    #    LocationNames.loc_shop_charm3: (3, 36 if use_dlc else 32),
    #    LocationNames.loc_shop_charm4: (3, 36 if use_dlc else 32),
    #    LocationNames.loc_shop_charm5: (5, 52 if use_dlc else 40),
    #    LocationNames.loc_shop_charm6: (3, 52 if use_dlc else 40),

    #    LocationNames.loc_shop_dlc_charm7: (3, 56),
    #    LocationNames.loc_shop_dlc_charm8: (1, 56),
    #}

    #for item in shop_items.keys():
    #    set_rule(multiworld.get_entrance(LocationNames.level_shop+" -> "+item, player), lambda state,item=item: state.has(ItemNames.item_coin, player, item_costs[item][1]))

# TODO: Add rules for the shop items (complicated)
