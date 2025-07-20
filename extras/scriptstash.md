## ScriptStash
A place for discarded code that might be useful in the future

```python

shop_item_weapons = [
        LocationNames.loc_shop_weapon1,
        LocationNames.loc_shop_weapon2,
        LocationNames.loc_shop_weapon3,
        LocationNames.loc_shop_weapon4,
        LocationNames.loc_shop_weapon5,
]
shop_item_dlc_weapons = [
        LocationNames.loc_shop_dlc_weapon6,
        LocationNames.loc_shop_dlc_weapon7,
        LocationNames.loc_shop_dlc_weapon8,
]
shop_item_charms = [
        LocationNames.loc_shop_charm1,
        LocationNames.loc_shop_charm2,
        LocationNames.loc_shop_charm3,
        LocationNames.loc_shop_charm4,
        LocationNames.loc_shop_charm5,
        LocationNames.loc_shop_charm6,
]
shop_item_dlc_charms = [
        LocationNames.loc_shop_dlc_charm7,
        LocationNames.loc_shop_dlc_charm8,
]
shop_items_list = shop_item_weapons + shop_item_charms + ((shop_item_dlc_weapons + shop_item_dlc_charms) if using_dlc else [])

# Weapon Gate Logic
def create_weapontiers(multiworld: MultiWorld, player: int, starting_weapons: list[str] = None) -> dict[int,list[str]]:
    use_dlc = multiworld.game_content[player] == "delicious_last_course"
    rand = multiworld.random
    tiers = 3
    res: dict[int,list[str]] = {}
    start_weapons = starting_weapons if starting_weapons else []
    weapons = []
    [weapons.append(x) for x in items.item_weapons.keys() if (x not in start_weapons)]
    if use_dlc:
        [weapons.append(x) for x in items.item_dlc_weapons.keys() if (x not in start_weapons)]
    res.update({0: start_weapons})
    rand.shuffle(weapons)
    weapons_per_tier = -(len(weapons)//-tiers)
    for i in range(tiers):
        res.update({i+1: weapons[(i*weapons_per_tier):min((i+1)*weapons_per_tier,len(weapons))]})
    return res

def create_weapongates(multiworld: MultiWorld, player: int, weapon_tiers: dict[int,list[str]], levels: dict[str,LevelData]) -> dict[str,(str,str)]:
    use_dlc = multiworld.game_content[player] == "delicious_last_course"
    rand = multiworld.random
    res: dict[str,tuple(str,str)] = {}
    weapons = list(items.item_weapons.keys())
    used_weapons = []
    if use_dlc:
        weapons.append(items.item_dlc_weapons.keys())
    for level in levels.keys:
        weapon_pool = []
        if levels[level].is_starter:
            weapon_pool = weapon_tiers[0]
        elif levels[level].world_location == LocationNames.world_inkwell_1:
            weapon_pool = weapon_tiers[0] + weapon_tiers[1]
        elif levels[level].world_location == LocationNames.world_inkwell_2:
            weapon_pool = weapon_tiers[0] + weapon_tiers[1] + weapon_tiers[2]
        elif levels[level].world_location == LocationNames.world_inkwell_3:
            weapon_pool = weapons
        else:
            weapon_pool = weapons

        if not (all(x in used_weapons for x in weapon_pool)):
            weapon_pool = [x for x in weapon_pool if x not in used_weapons]
        res.update({level: tuple(rand.choices(weapon_pool, k=2))})

    return res

    # Overrides for Levels (to automatically account for level shuffling)
    class LevelTarget(Target):
        def __new__(cls, name: str, add_rule: Optional[Callable] = None) -> Target:
            _rule = _level_map(name).rule
            _add_rule = add_rule if add_rule else lambda state: True
            return super().__new__(cls, name, (lambda state: _rule(state,player) and _add_rule(state)) if _rule else None)
    class LevelRegionData(RegionData):
        def __init__(self, name: str, add_locations: list[str] = None, connect_to: list[Target] = None, ignore_freemove_islands: bool = False) -> None:
            _locations = list(_level_map(name).locations)
            if add_locations:
                _locations += add_locations
            super().__init__(name, _locations, connect_to if not freemove_isles or ignore_freemove_islands else None)

class MysteryLevelItems(Toggle):
    """
    Replace all filler items and traps with presents.
    Presents hold a random filler item or trap (if enabled).
    For those who like uncertainty.
    """
    display_name = "Mystery Filler Items"

```

```python
class TestLogicBase(CupheadTestBase):
    def setup_initial_items(self):
        _world: CupheadWorld = cast(CupheadWorld, self.world)
        wconfig = _world.wconfig

        self.assertTrue(self.can_reach_location(LocationNames.loc_event_start_weapon))

        weapon_progressive = (wconfig.weapon_mode & WeaponMode.PROGRESSIVE) > 0

        _start_weapon = self.get_item_by_name(
            weapons.weapon_p_dict[wconfig.start_weapon] if weapon_progressive else
            weapons.weapon_dict[wconfig.start_weapon]
        )

        _start_locations = tuple(self.multiworld.get_region("Start", self.player).locations)

        start_weapon_loc = self.multiworld.get_location(LocationNames.loc_event_start_weapon, self.player)
        self.assertIn(start_weapon_loc, _start_locations)
        self.multiworld.state.collect(_start_weapon, location=start_weapon_loc)

        if (wconfig.weapon_mode & WeaponMode.EXCEPT_START) > 0:
            self.assertTrue(self.can_reach_location(LocationNames.loc_event_start_weapon_ex))
            _start_weapon_ex = self.get_item_by_name(
                weapons.weapon_p_dict[wconfig.start_weapon] if weapon_progressive else
                weapons.weapon_ex_dict[wconfig.start_weapon]
            )
            start_weapon_ex_loc = self.multiworld.get_location(LocationNames.loc_event_start_weapon_ex, self.player)
            self.assertIn(start_weapon_ex_loc, _start_locations)
            self.multiworld.state.collect(_start_weapon_ex, location=start_weapon_ex_loc)

class TestLogicInit(TestLogicBase):
    def test_start_weapon(self):
        _options: dict[str, Any] = {
            "use_dlc": True,
            "start_weapon": "peashooter",
        }
        test = TestLogicBase()
        test.options = _options
        test.world_setup()
        test.assertBeatable(False)

        #test.setup_initial_items()

        test.assertEqual(test.count(ItemNames.item_weapon_peashooter), 1)

    def test_start_p_weapon(self):
        _options: dict[str, Any] = {
            "use_dlc": True,
            "start_weapon": "spread",
            "weapon_mode": "progressive",
        }
        test = TestLogicBase()
        test.options = _options
        test.world_setup()
        test.assertBeatable(False)

        #test.setup_initial_items()

        test.assertEqual(test.count(ItemNames.item_p_weapon_spread), 1)

    def test_start_p_weapon_except_start(self):
        _options: dict[str, Any] = {
            "use_dlc": True,
            "start_weapon": "dlc_crackshot",
            "weapon_mode": "progressive_except_start",
        }
        test = TestLogicBase()
        test.options = _options
        test.world_setup()
        test.assertBeatable(False)

        #test.setup_initial_items()

        test.assertEqual(test.count(ItemNames.item_p_weapon_dlc_crackshot), 2)

    def test_start_weapon_ex(self):
        _options: dict[str, Any] = {
            "use_dlc": True,
            "start_weapon": "dlc_twistup",
            "weapon_mode": "ex_separate",
        }
        test = TestLogicBase()
        test.options = _options
        test.world_setup()
        test.assertBeatable(False)

        #test.setup_initial_items()

        test.assertEqual(test.count(ItemNames.item_weapon_dlc_twistup), 1)

    def test_start_weapon_ex_except_start(self):
        _options: dict[str, Any] = {
            "use_dlc": True,
            "start_weapon": "lobber",
            "weapon_mode": "ex_separate_except_start",
        }
        test = TestLogicBase()
        test.options = _options
        test.world_setup()
        test.assertBeatable(False)

        test.setup_initial_items()

        test.assertEqual(test.count(ItemNames.item_weapon_lobber), 1)
        test.assertEqual(test.count(ItemNames.item_weapon_lobber_ex), 1)
```
