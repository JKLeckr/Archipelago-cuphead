from typing import NamedTuple, Optional
from BaseClasses import Location, LocationProgressType
from .names import LocationNames
from .settings import WorldSettings, GradeCheckMode

class CupheadLocation(Location):
    game: str = "Cuphead"
    def __init__(self, player: int, name: str = '', id: int = None, parent=None, event: bool = False, progress_type: LocationProgressType = LocationProgressType.DEFAULT, show_in_spoiler: bool = True):
        super().__init__(player, name, id, parent)
        self.event = event
        self.progress_type = progress_type
        self.show_in_spoiler = show_in_spoiler

class LocationData(NamedTuple):
    id: Optional[int]
    progress_type: LocationProgressType = LocationProgressType.DEFAULT
    event: bool = False
    category: str = None

base_id = 0xc4ead0
base_dlc_id = 0xc4fad0

def id(i: int): return base_id+i
def dlc_id(i: int): return base_dlc_id+i

# Locations
# Next ids: 129, 56
# Level Locations
location_level_tutorial = {
    LocationNames.loc_level_tutorial: LocationData(id(0)),
    LocationNames.loc_level_tutorial_coin: LocationData(id(1)),
    #LocationNames.loc_level_plane_tutorial: LocationData(id(2)),
}
location_level_dlc_tutorial = {
    LocationNames.loc_level_dlc_tutorial: LocationData(dlc_id(0)),
    LocationNames.loc_level_dlc_tutorial_coin: LocationData(dlc_id(1)),
}

location_level_boss = {
    LocationNames.loc_level_boss_veggies: LocationData(id(3)),
    LocationNames.loc_level_boss_slime: LocationData(id(5)),
    LocationNames.loc_level_boss_frogs: LocationData(id(7)),
    LocationNames.loc_level_boss_flower: LocationData(id(9)),
    LocationNames.loc_level_boss_baroness: LocationData(id(11)),
    LocationNames.loc_level_boss_clown: LocationData(id(13)),
    LocationNames.loc_level_boss_dragon: LocationData(id(15)),
    LocationNames.loc_level_boss_bee: LocationData(id(17)),
    LocationNames.loc_level_boss_pirate: LocationData(id(19)),
    LocationNames.loc_level_boss_mouse: LocationData(id(21)),
    LocationNames.loc_level_boss_sallystageplay: LocationData(id(23)),
    LocationNames.loc_level_boss_train: LocationData(id(25)),
    LocationNames.loc_level_boss_kingdice: LocationData(id(27)),

    LocationNames.loc_level_boss_plane_blimp: LocationData(id(29)),
    LocationNames.loc_level_boss_plane_genie: LocationData(id(31)),
    LocationNames.loc_level_boss_plane_bird: LocationData(id(33)),
    LocationNames.loc_level_boss_plane_mermaid: LocationData(id(35)),
    LocationNames.loc_level_boss_plane_robot: LocationData(id(37)),
}
location_level_boss_final = {
    LocationNames.loc_level_boss_devil: LocationData(id(39)),
}
location_level_boss_topgrade = {
    LocationNames.loc_level_boss_veggies_topgrade: LocationData(id(4)),
    LocationNames.loc_level_boss_slime_topgrade: LocationData(id(6)),
    LocationNames.loc_level_boss_frogs_topgrade: LocationData(id(8)),
    LocationNames.loc_level_boss_flower_topgrade: LocationData(id(10)),
    LocationNames.loc_level_boss_baroness_topgrade: LocationData(id(12)),
    LocationNames.loc_level_boss_clown_topgrade: LocationData(id(14)),
    LocationNames.loc_level_boss_dragon_topgrade: LocationData(id(16)),
    LocationNames.loc_level_boss_bee_topgrade: LocationData(id(18)),
    LocationNames.loc_level_boss_pirate_topgrade: LocationData(id(20)),
    LocationNames.loc_level_boss_mouse_topgrade: LocationData(id(22)),
    LocationNames.loc_level_boss_sallystageplay_topgrade: LocationData(id(24)),
    LocationNames.loc_level_boss_train_topgrade: LocationData(id(26)),
    LocationNames.loc_level_boss_kingdice_topgrade: LocationData(id(28)),

    LocationNames.loc_level_boss_plane_blimp_topgrade: LocationData(id(30)),
    LocationNames.loc_level_boss_plane_genie_topgrade: LocationData(id(32)),
    LocationNames.loc_level_boss_plane_bird_topgrade: LocationData(id(34)),
    LocationNames.loc_level_boss_plane_mermaid_topgrade: LocationData(id(36)),
    LocationNames.loc_level_boss_plane_robot_topgrade: LocationData(id(38)),
}
location_level_boss_dlc_chaliced = {
    LocationNames.loc_level_boss_veggies_dlc_chaliced: LocationData(dlc_id(2)),
    LocationNames.loc_level_boss_slime_dlc_chaliced: LocationData(dlc_id(3)),
    LocationNames.loc_level_boss_frogs_dlc_chaliced: LocationData(dlc_id(4)),
    LocationNames.loc_level_boss_flower_dlc_chaliced: LocationData(dlc_id(5)),
    LocationNames.loc_level_boss_baroness_dlc_chaliced: LocationData(dlc_id(6)),
    LocationNames.loc_level_boss_clown_dlc_chaliced: LocationData(dlc_id(7)),
    LocationNames.loc_level_boss_dragon_dlc_chaliced: LocationData(dlc_id(8)),
    LocationNames.loc_level_boss_bee_dlc_chaliced: LocationData(dlc_id(9)),
    LocationNames.loc_level_boss_pirate_dlc_chaliced: LocationData(dlc_id(10)),
    LocationNames.loc_level_boss_mouse_dlc_chaliced: LocationData(dlc_id(11)),
    LocationNames.loc_level_boss_sallystageplay_dlc_chaliced: LocationData(dlc_id(12)),
    LocationNames.loc_level_boss_train_dlc_chaliced: LocationData(dlc_id(13)),
    LocationNames.loc_level_boss_kingdice_dlc_chaliced: LocationData(dlc_id(14)),
    LocationNames.loc_level_boss_plane_blimp_dlc_chaliced: LocationData(dlc_id(15)),
    LocationNames.loc_level_boss_plane_genie_dlc_chaliced: LocationData(dlc_id(16)),
    LocationNames.loc_level_boss_plane_bird_dlc_chaliced: LocationData(dlc_id(17)),
    LocationNames.loc_level_boss_plane_mermaid_dlc_chaliced: LocationData(dlc_id(18)),
    LocationNames.loc_level_boss_plane_robot_dlc_chaliced: LocationData(dlc_id(19)),
}
location_level_boss_event_agrade = {
    LocationNames.loc_level_boss_veggies_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_slime_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_frogs_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_flower_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_baroness_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_clown_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_dragon_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_bee_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_pirate_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_mouse_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_sallystageplay_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_train_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_kingdice_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_plane_blimp_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_plane_genie_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_plane_bird_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_plane_mermaid_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_plane_robot_event_agrade: LocationData(None),
}
location_level_boss_event_dlc_chaliced = {
    LocationNames.loc_level_boss_veggies_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_slime_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_frogs_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_flower_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_baroness_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_clown_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_dragon_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_bee_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_pirate_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_mouse_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_sallystageplay_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_train_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_kingdice_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_plane_blimp_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_plane_genie_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_plane_bird_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_plane_mermaid_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_plane_robot_event_dlc_chaliced: LocationData(None),
}
location_level_boss_final_topgrade = {
    LocationNames.loc_level_boss_devil_topgrade: LocationData(id(40))
}
location_level_boss_final_dlc_chaliced = {
    LocationNames.loc_level_boss_devil_dlc_chaliced: LocationData(dlc_id(20))
}
location_level_boss_final_event_agrade = {
    LocationNames.loc_level_boss_devil_event_agrade: LocationData(None)
}
location_level_boss_final_event_dlc_chaliced = {
    LocationNames.loc_level_boss_devil_event_dlc_chaliced: LocationData(None)
}
location_level_dlc_boss = {
    LocationNames.loc_level_dlc_boss_oldman: LocationData(dlc_id(21)),
    LocationNames.loc_level_dlc_boss_rumrunners: LocationData(dlc_id(24)),
    LocationNames.loc_level_dlc_boss_snowcult: LocationData(dlc_id(27)),
    LocationNames.loc_level_dlc_boss_airplane: LocationData(dlc_id(30)),

    LocationNames.loc_level_dlc_boss_plane_cowboy: LocationData(dlc_id(33)),
}
location_level_dlc_boss_final = {
    LocationNames.loc_level_dlc_boss_saltbaker: LocationData(dlc_id(36)),
}
location_level_dlc_boss_topgrade = {
    LocationNames.loc_level_dlc_boss_oldman_topgrade: LocationData(dlc_id(22)),
    LocationNames.loc_level_dlc_boss_rumrunners_topgrade: LocationData(dlc_id(25)),
    LocationNames.loc_level_dlc_boss_snowcult_topgrade: LocationData(dlc_id(28)),
    LocationNames.loc_level_dlc_boss_airplane_topgrade: LocationData(dlc_id(31)),

    LocationNames.loc_level_dlc_boss_plane_cowboy_topgrade: LocationData(dlc_id(34)),
}
location_level_dlc_boss_dlc_chaliced = {
    LocationNames.loc_level_dlc_boss_oldman_dlc_chaliced: LocationData(dlc_id(23)),
    LocationNames.loc_level_dlc_boss_rumrunners_dlc_chaliced: LocationData(dlc_id(26)),
    LocationNames.loc_level_dlc_boss_snowcult_dlc_chaliced: LocationData(dlc_id(29)),
    LocationNames.loc_level_dlc_boss_airplane_dlc_chaliced: LocationData(dlc_id(32)),
    LocationNames.loc_level_dlc_boss_plane_cowboy_dlc_chaliced: LocationData(dlc_id(35)),
}
location_level_dlc_boss_event_agrade = {
    LocationNames.loc_level_dlc_boss_oldman_event_agrade: LocationData(None),
    LocationNames.loc_level_dlc_boss_rumrunners_event_agrade: LocationData(None),
    LocationNames.loc_level_dlc_boss_snowcult_event_agrade: LocationData(None),
    LocationNames.loc_level_dlc_boss_airplane_event_agrade: LocationData(None),
    LocationNames.loc_level_dlc_boss_plane_cowboy_event_agrade: LocationData(None),
}
location_level_dlc_boss_event_dlc_chaliced = {
    LocationNames.loc_level_dlc_boss_oldman_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_dlc_boss_rumrunners_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_dlc_boss_snowcult_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_dlc_boss_airplane_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_dlc_boss_plane_cowboy_event_dlc_chaliced: LocationData(None),
}
location_level_dlc_boss_final_topgrade = {
    LocationNames.loc_level_dlc_boss_saltbaker_topgrade: LocationData(dlc_id(37)),
}
location_level_dlc_boss_final_dlc_chaliced= {
    LocationNames.loc_level_dlc_boss_saltbaker_dlc_chaliced: LocationData(dlc_id(38)),
}
location_level_dlc_boss_final_event_agrade = {
    LocationNames.loc_level_dlc_boss_saltbaker_event_agrade: LocationData(None),
}
location_level_dlc_boss_final_event_dlc_chaliced = {
    LocationNames.loc_level_dlc_boss_saltbaker_event_dlc_chaliced: LocationData(None),
}

location_level_dicepalace = {
    LocationNames.loc_level_dicepalace_boss1: LocationData(id(41)),
    LocationNames.loc_level_dicepalace_boss2: LocationData(id(42)),
    LocationNames.loc_level_dicepalace_boss3: LocationData(id(43)),
    LocationNames.loc_level_dicepalace_boss4: LocationData(id(44)),
    LocationNames.loc_level_dicepalace_boss5: LocationData(id(45)),
    LocationNames.loc_level_dicepalace_boss6: LocationData(id(46)),
    LocationNames.loc_level_dicepalace_boss7: LocationData(id(47)),
    LocationNames.loc_level_dicepalace_boss8: LocationData(id(48)),
    LocationNames.loc_level_dicepalace_boss9: LocationData(id(49)),
}

location_level_rungun = {
    LocationNames.loc_level_rungun_forest: LocationData(id(50)),
    LocationNames.loc_level_rungun_forest_coin1: LocationData(id(53)),
    LocationNames.loc_level_rungun_forest_coin2: LocationData(id(54)),
    LocationNames.loc_level_rungun_forest_coin3: LocationData(id(55)),
    LocationNames.loc_level_rungun_forest_coin4: LocationData(id(56)),
    LocationNames.loc_level_rungun_forest_coin5: LocationData(id(57)),

    LocationNames.loc_level_rungun_tree: LocationData(id(58)),
    LocationNames.loc_level_rungun_tree_coin1: LocationData(id(61)),
    LocationNames.loc_level_rungun_tree_coin2: LocationData(id(62)),
    LocationNames.loc_level_rungun_tree_coin3: LocationData(id(63)),
    LocationNames.loc_level_rungun_tree_coin4: LocationData(id(64)),
    LocationNames.loc_level_rungun_tree_coin5: LocationData(id(65)),

    LocationNames.loc_level_rungun_circus: LocationData(id(66)),
    LocationNames.loc_level_rungun_circus_coin1: LocationData(id(69)),
    LocationNames.loc_level_rungun_circus_coin2: LocationData(id(70)),
    LocationNames.loc_level_rungun_circus_coin3: LocationData(id(71)),
    LocationNames.loc_level_rungun_circus_coin4: LocationData(id(72)),
    LocationNames.loc_level_rungun_circus_coin5: LocationData(id(73)),

    LocationNames.loc_level_rungun_funhouse: LocationData(id(74)),
    LocationNames.loc_level_rungun_funhouse_coin1: LocationData(id(77)),
    LocationNames.loc_level_rungun_funhouse_coin2: LocationData(id(78)),
    LocationNames.loc_level_rungun_funhouse_coin3: LocationData(id(79)),
    LocationNames.loc_level_rungun_funhouse_coin4: LocationData(id(80)),
    LocationNames.loc_level_rungun_funhouse_coin5: LocationData(id(81)),

    LocationNames.loc_level_rungun_harbour: LocationData(id(82)),
    LocationNames.loc_level_rungun_harbour_coin1: LocationData(id(85)),
    LocationNames.loc_level_rungun_harbour_coin2: LocationData(id(86)),
    LocationNames.loc_level_rungun_harbour_coin3: LocationData(id(87)),
    LocationNames.loc_level_rungun_harbour_coin4: LocationData(id(88)),
    LocationNames.loc_level_rungun_harbour_coin5: LocationData(id(89)),

    LocationNames.loc_level_rungun_mountain: LocationData(id(90)),
    LocationNames.loc_level_rungun_mountain_coin1: LocationData(id(93)),
    LocationNames.loc_level_rungun_mountain_coin2: LocationData(id(94)),
    LocationNames.loc_level_rungun_mountain_coin3: LocationData(id(95)),
    LocationNames.loc_level_rungun_mountain_coin4: LocationData(id(96)),
    LocationNames.loc_level_rungun_mountain_coin5: LocationData(id(97)),
}
location_level_rungun_agrade = {
    LocationNames.loc_level_rungun_forest_agrade: LocationData(id(51)),
    LocationNames.loc_level_rungun_tree_agrade: LocationData(id(59)),
    LocationNames.loc_level_rungun_circus_agrade: LocationData(id(67)),
    LocationNames.loc_level_rungun_funhouse_agrade: LocationData(id(75)),
    LocationNames.loc_level_rungun_harbour_agrade: LocationData(id(83)),
    LocationNames.loc_level_rungun_mountain_agrade: LocationData(id(91)),
}
location_level_rungun_pacifist = {
    LocationNames.loc_level_rungun_forest_pacifist: LocationData(id(52)),
    LocationNames.loc_level_rungun_tree_pacifist: LocationData(id(60)),
    LocationNames.loc_level_rungun_circus_pacifist: LocationData(id(68)),
    LocationNames.loc_level_rungun_funhouse_pacifist: LocationData(id(76)),
    LocationNames.loc_level_rungun_harbour_pacifist: LocationData(id(84)),
    LocationNames.loc_level_rungun_mountain_pacifist: LocationData(id(92)),
}
location_level_rungun_event_agrade = {
    LocationNames.loc_level_rungun_forest_event_agrade: LocationData(None),
    LocationNames.loc_level_rungun_tree_event_agrade: LocationData(None),
    LocationNames.loc_level_rungun_circus_event_agrade: LocationData(None),
    LocationNames.loc_level_rungun_funhouse_event_agrade: LocationData(None),
    LocationNames.loc_level_rungun_harbour_event_agrade: LocationData(None),
    LocationNames.loc_level_rungun_mountain_event_agrade: LocationData(None),
}
location_level_rungun_event_pacifist = {
    LocationNames.loc_level_rungun_forest_event_pacifist: LocationData(None),
    LocationNames.loc_level_rungun_tree_event_pacifist: LocationData(None),
    LocationNames.loc_level_rungun_circus_event_pacifist: LocationData(None),
    LocationNames.loc_level_rungun_funhouse_event_pacifist: LocationData(None),
    LocationNames.loc_level_rungun_harbour_event_pacifist: LocationData(None),
    LocationNames.loc_level_rungun_mountain_event_pacifist: LocationData(None),
}

location_level_mausoleum = {
    LocationNames.loc_level_mausoleum_i: LocationData(id(98)),
    LocationNames.loc_level_mausoleum_ii: LocationData(id(99)),
    LocationNames.loc_level_mausoleum_iii: LocationData(id(100)),
}

location_level_dlc_chesscastle = {
    LocationNames.loc_level_dlc_chesscastle_run: LocationData(dlc_id(39)),
    LocationNames.loc_level_dlc_chesscastle_pawn: LocationData(dlc_id(40)),
    LocationNames.loc_level_dlc_chesscastle_knight: LocationData(dlc_id(41)),
    LocationNames.loc_level_dlc_chesscastle_bishop: LocationData(dlc_id(42)),
    LocationNames.loc_level_dlc_chesscastle_rook: LocationData(dlc_id(43)),
    LocationNames.loc_level_dlc_chesscastle_queen: LocationData(dlc_id(44)),
}

location_level_dlc_special = {
    LocationNames.loc_level_dlc_graveyard: LocationData(dlc_id(45)),
}

# Shop Locations
location_shop = {
    LocationNames.loc_shop_weapon1: LocationData(id(101)),
    LocationNames.loc_shop_weapon2: LocationData(id(102)),
    LocationNames.loc_shop_weapon3: LocationData(id(103)),
    LocationNames.loc_shop_weapon4: LocationData(id(104)),
    LocationNames.loc_shop_weapon5: LocationData(id(105)),
    LocationNames.loc_shop_charm1: LocationData(id(106)),
    LocationNames.loc_shop_charm2: LocationData(id(107)),
    LocationNames.loc_shop_charm3: LocationData(id(108)),
    LocationNames.loc_shop_charm4: LocationData(id(109)),
    LocationNames.loc_shop_charm5: LocationData(id(110)),
    LocationNames.loc_shop_charm6: LocationData(id(111)),
}
location_shop_event = {
    LocationNames.loc_shop_weapon1_bought: LocationData(None, category="weapon"),
    LocationNames.loc_shop_weapon2_bought: LocationData(None, category="weapon"),
    LocationNames.loc_shop_weapon3_bought: LocationData(None, category="weapon"),
    LocationNames.loc_shop_weapon4_bought: LocationData(None, category="weapon"),
    LocationNames.loc_shop_weapon5_bought: LocationData(None, category="weapon"),
    LocationNames.loc_shop_charm1_bought: LocationData(None, category="charm"),
    LocationNames.loc_shop_charm2_bought: LocationData(None, category="charm"),
    LocationNames.loc_shop_charm3_bought: LocationData(None, category="charm"),
    LocationNames.loc_shop_charm4_bought: LocationData(None, category="charm"),
    LocationNames.loc_shop_charm5_bought: LocationData(None, category="charm"),
    LocationNames.loc_shop_charm6_bought: LocationData(None, category="charm"),
}
location_shop_dlc = {
    LocationNames.loc_shop_dlc_weapon6: LocationData(dlc_id(46)),
    LocationNames.loc_shop_dlc_weapon7: LocationData(dlc_id(47)),
    LocationNames.loc_shop_dlc_weapon8: LocationData(dlc_id(48)),
    LocationNames.loc_shop_dlc_charm7: LocationData(dlc_id(49)),
    LocationNames.loc_shop_dlc_charm8: LocationData(dlc_id(50)),
}
location_shop_dlc_event = {
    LocationNames.loc_shop_dlc_weapon6_bought: LocationData(None, category="dlc_weapon"),
    LocationNames.loc_shop_dlc_weapon7_bought: LocationData(None, category="dlc_weapon"),
    LocationNames.loc_shop_dlc_weapon8_bought: LocationData(None, category="dlc_weapon"),
    LocationNames.loc_shop_dlc_charm7_bought: LocationData(None, category="dlc_charm"),
    LocationNames.loc_shop_dlc_charm8_bought: LocationData(None, category="dlc_charm"),
}

# World Locations
location_world = {
    LocationNames.loc_npc_mac: LocationData(id(112)),
    LocationNames.loc_npc_canteen: LocationData(id(113)),
    LocationNames.loc_coin_isle1_secret: LocationData(id(114)),
    LocationNames.loc_coin_isle2_secret: LocationData(id(115)),
    LocationNames.loc_coin_isle3_secret: LocationData(id(116)),
    LocationNames.loc_coin_isleh_secret: LocationData(id(117)),
}
location_world_event = {
    LocationNames.loc_event_isle1_secret_prereq1: LocationData(None),
    LocationNames.loc_event_isle1_secret_prereq2: LocationData(None),
    LocationNames.loc_event_isle1_secret_prereq3: LocationData(None),
    LocationNames.loc_event_isle1_secret_prereq4: LocationData(None),
    LocationNames.loc_event_isle1_secret_prereq5: LocationData(None),
}
location_world_quest = {
    LocationNames.loc_quest_4parries: LocationData(id(118)),
    LocationNames.loc_quest_ginger: LocationData(id(119)),
    LocationNames.loc_quest_4mel: LocationData(id(120)),
    LocationNames.loc_quest_lucien: LocationData(id(121)),
    LocationNames.loc_quest_pacifist: LocationData(id(122)),
    LocationNames.loc_quest_15agrades: LocationData(id(123)),
    LocationNames.loc_quest_ludwig: LocationData(id(124)),
    LocationNames.loc_quest_wolfgang: LocationData(id(125)),
}
location_dlc_world = {
    #LocationNames.loc_dlc_cookie: LocationData(dlc_id(51)),
    LocationNames.loc_dlc_npc_newscat: LocationData(dlc_id(52)),
    LocationNames.loc_dlc_coin_isle4_secret: LocationData(dlc_id(53)),
    #LocationNames.loc_event_dlc_curse_complete: LocationData(dlc_id(54)),
}
location_dlc_world_event = {
    LocationNames.loc_event_dlc_boatarrival: LocationData(None),
}
location_dlc_world_quest = {
    LocationNames.loc_dlc_quest_cactusgirl: LocationData(dlc_id(55)),
}

location_level_boss_secret = {
    LocationNames.loc_level_boss_veggies_secret: LocationData(id(126)),
    LocationNames.loc_level_boss_plane_genie_secret: LocationData(id(127)),
    LocationNames.loc_level_boss_sallystageplay_secret: LocationData(id(128)),
}

# Special Locations
location_special = {
    #LocationNames.loc_event_firstweapon: LocationData(None),
    LocationNames.loc_event_isle2_shortcut: LocationData(None),
    LocationNames.loc_event_quest_4mel_4th: LocationData(None),
    LocationNames.loc_event_music: LocationData(None),
}
location_dlc_special = {
    LocationNames.loc_event_dlc_start: LocationData(None),
}

# Goal Locations
location_goal = {
    LocationNames.loc_event_goal_devil: LocationData(None),
}
location_dlc_goal = {
    LocationNames.loc_event_dlc_goal_saltbaker: LocationData(None),
}

locations_base = {
    **location_level_tutorial,
    **location_level_boss,
    #**location_level_boss_final,
    **location_level_rungun,
    **location_level_mausoleum,
    **location_shop,
    #**location_shop_event,
    **location_world,
    **location_world_event,
}
locations_topgrade = {
    **location_level_boss_topgrade,
    ##**location_level_boss_final_topgrade,
    **location_level_rungun_agrade,
    **location_level_rungun_pacifist,
}
locations_event_agrade = {
    **location_level_boss_event_agrade,
    #**location_level_boss_final_event_agrade,
    **location_level_rungun_event_agrade,
}
locations_dlc = {
    **location_level_dlc_tutorial,
    **location_level_dlc_boss,
    #**location_level_dlc_boss_final,
    **location_level_dlc_chesscastle,
    **location_level_dlc_special,
    **location_shop_dlc,
    #**location_shop_dlc_event,
    **location_dlc_world,
    **location_dlc_world_event,
}
locations_dlc_boss_chaliced = {
    **location_level_boss_dlc_chaliced,
    #**location_level_boss_final_dlc_chaliced,
    **location_level_dlc_boss_dlc_chaliced,
    #**location_level_dlc_boss_final_dlc_chaliced,
}
locations_dlc_topgrade = {
    **location_level_dlc_boss_topgrade,
    #**location_level_dlc_boss_final_topgrade,
}
locations_dlc_event_agrade = {
    **location_level_dlc_boss_event_agrade,
    #**location_level_dlc_boss_final_event_agrade,
}
locations_dlc_event_boss_chaliced = {
    **location_level_boss_event_dlc_chaliced,
    #**location_level_boss_final_event_dlc_chaliced,
    **location_level_dlc_boss_event_dlc_chaliced,
    #**location_level_dlc_boss_final_event_dlc_chaliced,
}

locations_all = {
    **locations_base,
    **locations_topgrade,
    **locations_event_agrade,
    **location_level_rungun_event_pacifist,
    **location_world_quest,
    **location_special,
    **location_goal,
    **locations_dlc,
    **locations_dlc_topgrade,
    **locations_dlc_boss_chaliced,
    **locations_dlc_event_agrade,
    **locations_dlc_event_boss_chaliced,
    **location_dlc_world_quest,
    **location_dlc_special,
    **location_dlc_goal,
    **location_level_dicepalace,
}

def setup_locations(settings: WorldSettings):
    use_dlc = settings.use_dlc
    locations: dict[str,LocationData] = {**locations_base}
    boss_grade_checks = settings.get_boss_grade_checks()
    rungun_grade_checks = settings.get_rungun_grade_checks()
    if boss_grade_checks>0:
        locations.update(location_level_boss_topgrade)
        if use_dlc:
            locations.update(location_level_boss_final_topgrade)
    if rungun_grade_checks>0:
        if rungun_grade_checks==GradeCheckMode.a_grade or rungun_grade_checks==GradeCheckMode.aplus_grade:
            locations.update(location_level_rungun_agrade)
        elif rungun_grade_checks==GradeCheckMode.pacifist:
            locations.update(location_level_rungun_pacifist)
    if settings.boss_secret_checks:
        locations.update(location_level_boss_secret)

    # Switches
    def _add_location(name: str, location_dict: dict[str,LocationData]) -> None:
        locations[name] = location_dict[name]
    if settings.fourparries_quest:
        _add_location(LocationNames.loc_quest_4parries,location_world_quest)
    if settings.ginger_quest:
        _add_location(LocationNames.loc_quest_ginger,location_world_quest)
        _add_location(LocationNames.loc_event_isle2_shortcut,location_special)
    if settings.fourmel_quest:
        _add_location(LocationNames.loc_quest_4mel,location_world_quest)
        _add_location(LocationNames.loc_event_quest_4mel_4th,location_special)
    if settings.lucien_quest:
        _add_location(LocationNames.loc_quest_lucien,location_world_quest)
    if settings.ludwig_quest:
        _add_location(LocationNames.loc_quest_ludwig,location_world_quest)
    if settings.wolfgang_quest:
        _add_location(LocationNames.loc_quest_wolfgang,location_world_quest)
        _add_location(LocationNames.loc_event_music,location_special)
    if settings.agrade_quest:
        locations.update({**locations_event_agrade})
        _add_location(LocationNames.loc_quest_15agrades,location_world_quest)
    if settings.pacifist_quest:
        locations.update({**location_level_rungun_event_pacifist})
        _add_location(LocationNames.loc_quest_pacifist,location_world_quest)
    locations.update({**location_goal})

    if use_dlc:
        locations.update({**locations_dlc, **(locations_dlc_event_agrade if settings.agrade_quest else {})})
        if boss_grade_checks>0:
            locations.update({**location_level_dlc_boss_topgrade})
        if settings.dlc_boss_chalice_checks:
            locations.update({**locations_dlc_boss_chaliced})
        if settings.dlc_cactusgirl_quest:
            locations.update({**locations_dlc_event_boss_chaliced})
            _add_location(LocationNames.loc_dlc_quest_cactusgirl,location_dlc_world_quest)
        locations.update({**location_dlc_goal})
    return locations

name_to_id = {name: data.id for name, data in locations_all.items() if data.id}
