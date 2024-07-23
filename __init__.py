import math
from typing import TextIO, Dict, Any
from BaseClasses import Item, Tutorial, CollectionState, ItemClassification
from Utils import visualize_regions
from worlds.AutoWorld import World, WebWorld
from .names import ItemNames, LocationNames
from .auxiliary import count_in_list
from .options import CupheadOptions
from .settings import WorldSettings
from .items import CupheadItem, ItemData
from .locations import LocationData
from .levels import LevelData
from . import debug, items, levels, locations, regions, rules

class CupheadWebWorld(WebWorld):
    theme = "grass"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Cuphead Archipelago randomizer on your machine",
        "English",
        "setup_en.md",
        "setup/en",
        ["JKLeckr"]
    )
    tutorials = [setup_en]
    bug_report_page = "https://gitlab.com/JKLeckr/CupheadArchipelagoMod/-/issues"

class CupheadWorld(World):
    """
    A classic run and gun action game heavily focused on boss battles
    """
    game: str = "Cuphead"
    web = CupheadWebWorld()
    options_dataclass = CupheadOptions
    options: CupheadOptions
    version = 0
    required_client_version = (0, 4, 2)

    item_name_to_id = items.name_to_id
    location_name_to_id = locations.name_to_id

    item_names = set(items.items_all.keys())
    location_names = set(locations.locations_all.keys())

    wsettings: WorldSettings = None

    def generate_early(self) -> None:
        # Settings (See Settings.py)
        self.wsettings = WorldSettings(self.options)

        self.topology_present = not self.wsettings.freemove_isles

        self.use_dlc = self.wsettings.use_dlc
        self.start_weapon = self.wsettings.start_weapon
        self.level_shuffle = self.wsettings.level_shuffle

        coin_amounts = self.get_coin_amounts()
        self.total_coins = coin_amounts[0] + (coin_amounts[1]*2) + (coin_amounts[2]*3)

        self.resolve_precollected_items()

        self.active_items: dict[str,ItemData] = items.setup_items(self.wsettings)
        self.active_locations: dict[str,LocationData] = locations.setup_locations(self.wsettings)
        #Tests.test_duplicates(self.active_locations)
        self.active_levels: dict[str,LevelData] = levels.setup_levels(self.wsettings,self.active_locations)
        self.level_shuffle_map: dict[str,str] = {}
        if self.level_shuffle:
            self.level_shuffle_map: dict[str,str] = levels.setup_level_shuffle_map(self.random, self.wsettings)

        # Group Items
        self.item_name_groups = {}
        for item in self.active_items.keys():
            if item in items.item_weapons or (self.use_dlc and item in items.item_dlc_weapons):
                self.item_name_groups.update({"weapons": item})
            if item in items.item_charms or (self.use_dlc and item in items.item_dlc_charms):
                self.item_name_groups.update({"charms": item})
            if item in items.item_super:
                self.item_name_groups.update({"super": item})
            if item in items.item_abilities or item in items.item_abilities_aim:
                self.item_name_groups.update({"abilities": item})

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = {
            "version": self.version,
            "levels": list(self.active_levels.keys()),
            "level_shuffle_map": self.level_shuffle_map,
            **self.options.as_dict("use_dlc", "expert_mode", "freemove_isles")
        }
        return slot_data

    def create_regions(self) -> None:
        regions.create_regions(self.multiworld, self.player, self.active_locations, self.active_levels, self.level_shuffle_map, self.wsettings)
        #print(self.multiworld.get_locations(self.player))
        #print(regions.list_multiworld_regions_names(self.multiworld))
        #print(self.multiworld.get_region(LocationNames.level_mausoleum_ii, self.player).locations)

    def create_item(self, name: str, force_classification: ItemClassification = None) -> Item:
        data = items.items_all[name]

        if force_classification:
            classification = force_classification
        else:
            classification = data.type

        new_item = CupheadItem(name, classification, data.id, self.player)

        return new_item

    def create_locked_item(self, name: str, location: str, force_classification: ItemClassification = None) -> None:
        self.multiworld.get_location(location, self.player).place_locked_item(self.create_item(name, force_classification))
    def create_locked_items(self, name: str, locations: set[str], force_classification: ItemClassification = None) -> None:
        for loc in locations:
            if loc in self.active_locations:
                self.create_locked_item(name, loc, force_classification)

    def create_items(self) -> None:
        rand = self.random
        itempool: list[CupheadItem] = []

        #TODO: Handle start_inventory correctly

        starter_items = self.multiworld.precollected_items[self.player]
        #starter_items.append(self.create_item(ItemNames.item_charm_heart))
        #print(len(starter_items))
        starter_items_names = [x.name for x in starter_items]
        def append_starter_items(item: Item):
            starter_items.append(item)
            starter_items_names.append(item.name)

        # Locked Items
        for i in range(1,6):
            _loc = LocationNames.loc_event_isle1_secret_prereq+" "+str(i)
            self.create_locked_item(ItemNames.item_event_isle1_secret_prereq, _loc)
        if self.wsettings.ginger_quest:
            self.create_locked_item(ItemNames.item_event_isle2_shortcut, LocationNames.loc_event_isle2_shortcut)
        if self.wsettings.fourmel_quest:
            self.create_locked_item(ItemNames.item_event_quest_4mel_4th, LocationNames.loc_event_quest_4mel_4th)
        if self.wsettings.wolfgang_quest:
            self.create_locked_item(ItemNames.item_event_music, LocationNames.loc_event_music)
        if self.wsettings.agrade_quest:
            self.create_locked_items(ItemNames.item_event_agrade, locations.locations_event_agrade)
        if self.wsettings.pacifist_quest:
            self.create_locked_items(ItemNames.item_event_pacifist, locations.location_level_rungun_event_pacifist)
        self.create_locked_item(ItemNames.item_event_goal_devilko, LocationNames.loc_event_goal_devil)

        if self.use_dlc:
            self.create_locked_item(ItemNames.item_event_dlc_boataccess, LocationNames.loc_event_dlc_boatarrival)
            #self.create_locked_item(ItemNames.item_charm_dlc_broken_relic, LocationNames.loc_level_dlc_graveyard)
            self.create_locked_item(ItemNames.item_event_goal_dlc_saltbakerko, LocationNames.loc_event_dlc_goal_saltbaker)
            self.create_locked_items(ItemNames.item_event_agrade, locations.locations_dlc_event_agrade)
            self.create_locked_items(ItemNames.item_event_dlc_boss_chaliced, locations.locations_dlc_event_boss_chaliced)

        total_locations = len([x.name for x in self.multiworld.get_locations(self.player) if not x.event])
        unfilled_locations = len([x.name for x in self.multiworld.get_unfilled_locations(self.player)])
        #print(total_locations)
        #print(unfilled_locations)
        if total_locations != unfilled_locations:
            print("ERROR: unfilled locations mismatch total non-event locations")

        # Shop Items
        #shop_events = {**Locations.location_shop_event, **(Locations.location_shop_dlc_event if self.use_dlc else {})}
        #for shop_event in shop_events.keys():
        #    if shop_events[shop_event].category == "weapon":
        #        self.create_locked_item(ItemNames.item_weapon,shop_event)
        #    if shop_events[shop_event].category == "charm":
        #        self.create_locked_item(ItemNames.item_charm,shop_event)
        #    if shop_events[shop_event].category == "dlc_weapon":
        #        self.create_locked_item(ItemNames.item_dlc_weapon,shop_event)
        #    if shop_events[shop_event].category == "dlc_charm":
        #        self.create_locked_item(ItemNames.item_dlc_charm,shop_event)

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
        weapons = {x for x in set(items.item_weapons.keys()) if x not in starter_items_names}
        start_weapon_index = self.start_weapon
        if self.use_dlc:
            weapons.update(items.item_dlc_weapons.keys())
        elif start_weapon_index>5:
            start_weapon_index = rand.randint(0,5)
        start_weapon = weapon_dict[start_weapon_index]
        if start_weapon not in starter_items_names:
            append_starter_items(self.create_item(start_weapon))
            weapons.remove(start_weapon)

        # Item names for coins
        coin_items = (ItemNames.item_coin, ItemNames.item_coin2, ItemNames.item_coin3)

        essential_items = [y for y in items.item_essential.keys() if y not in coin_items] + (list(items.item_essential.keys()) if self.use_dlc else [])
        charms = list(items.item_charms.keys()) + (list(items.item_dlc_charms.keys()) if self.use_dlc else [])

        # Add the other non-filler items before the coins
        def _fill_pool(items: list[str]) -> list[CupheadItem]:
            _itempool = []
            for item in items:
                qty = self.active_items[item].quantity - count_in_list(item, starter_items_names)
                if qty<0:
                    print("WARNING: \""+item+"\" has quantity of "+str(qty)+"!")
                if self.active_items[item].id and qty>0:
                    _itempool += [self.create_item(item) for _ in range(qty)]
            return _itempool
        itempool += _fill_pool(essential_items)
        itempool += _fill_pool(weapons)
        itempool += _fill_pool(charms)
        itempool += _fill_pool(items.item_super.keys())
        if self.wsettings.randomize_abilities:
            itempool += _fill_pool(items.item_abilities.keys())

        # Coins
        coin_amounts = self.get_coin_amounts()
        total_single_coins = coin_amounts[0]
        total_double_coins = coin_amounts[1]
        total_triple_coins = coin_amounts[2]
        total_coins = self.total_coins

        # Starter Coins
        start_coins = 0
        for item in starter_items_names:
            if item == coin_items[0]:
                start_coins += 1
            elif item == coin_items[1]:
                start_coins += 2
            elif item == coin_items[2]:
                start_coins += 3

        total_coins -= start_coins

        leftover_locations = total_locations - len(itempool) - self.wsettings.filler_item_buffer

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
        itempool += [self.create_item(coin_items[0]) for _ in range(total_single_coins)]
        itempool += [self.create_item(coin_items[1]) for _ in range(total_double_coins)]
        itempool += [self.create_item(coin_items[2]) for _ in range(total_triple_coins)]

        leftover_locations = total_locations - len(itempool)
        if (leftover_locations<0):
            print("Error: There are more items than locations!")

        # Filler Items and Traps
        filler_count = leftover_locations

        if self.wsettings.traps>0:
            trap_count = math.ceil(self.traps / filler_count * 100)
            itempool += [self.create_item(rand.choice(tuple(items.item_trap.keys()))) for _ in range(trap_count)]
            filler_count -= trap_count

        #print(len(self.multiworld.precollected_items[self.player]))

        itempool += [self.create_item(self.get_filler_item_name()) for _ in range(filler_count)]

        #print("itempool size: "+str(len(itempool)))
        self.multiworld.itempool += itempool

    def get_coin_amounts(self) -> tuple[int]:
        total_single_coins = 40 if self.use_dlc else 37
        total_double_coins = 5 if self.use_dlc else 0
        total_triple_coins = 2 if self.use_dlc else 1

        return (total_single_coins, total_double_coins, total_triple_coins)

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if self.level_shuffle and len(self.level_shuffle_map)>0:
            spoiler_handle.write("\n\nLevel Shuffle Map:\n")
            spoiler_handle.write('\n'.join([(x[0] + '->' + x[1]) for x in self.level_shuffle_map.items()]) + '\n\n')

    def collect(self, state: CollectionState, item: Item) -> bool:
        if item.name in {ItemNames.item_coin2, ItemNames.item_coin3}:
            amount = 3 if item.name == ItemNames.item_coin3 else 2
            state.prog_items[self.player][ItemNames.item_coin] += amount
            return True
        else:
            return super().collect(state, item)

    def get_filler_item_name(self) -> str:
        return self.random.choice(tuple(items.item_filler.keys()))

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        if self.level_shuffle:
            hint_dict: Dict[int, str] = {}
            for level in self.level_shuffle_map.items():
                if level in self.active_locations.keys():
                    for location in self.active_levels[level].locations:
                        hint_dict.update({location.id: (" ->> " + self.level_shuffle_map[level] + " at " + level)})
            hint_data.update({self.player: hint_dict})

    def resolve_precollected_items(self) -> None:
        starter_items = self.multiworld.precollected_items[self.player]
        starter_items_names = [x.name for x in starter_items]
        # Convert coin bundles into single coins
        for item in starter_items_names:
            if item in (ItemNames.item_coin2, ItemNames.item_coin3):
                index = starter_items_names.index(item)
                count = 2 if item == ItemNames.item_coin2 else 3
                starter_items.pop(index)
                starter_items_names.pop(index)
                for _ in range(count):
                    starter_items.insert(index, self.create_item(ItemNames.item_coin))
                    starter_items_names.insert(index, ItemNames.item_coin)

    def set_rules(self) -> None:
        rules.set_rules(self.multiworld, self.player, self.wsettings, self.total_coins)
        #visualize_regions(self.multiworld.get_region("Menu", self.player), "./output/regionmap.puml")
