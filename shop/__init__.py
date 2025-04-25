from __future__ import annotations
from typing import NamedTuple
from ..names import LocationNames
from ..wconf import WorldConfig

shop_weapons = [
    LocationNames.loc_shop_weapon1,
    LocationNames.loc_shop_weapon2,
    LocationNames.loc_shop_weapon3,
    LocationNames.loc_shop_weapon4,
    LocationNames.loc_shop_weapon5,
    LocationNames.loc_shop_dlc_weapon6,
    LocationNames.loc_shop_dlc_weapon7,
    LocationNames.loc_shop_dlc_weapon8
]
shop_charms = [
    LocationNames.loc_shop_charm1,
    LocationNames.loc_shop_charm2,
    LocationNames.loc_shop_charm3,
    LocationNames.loc_shop_charm4,
    LocationNames.loc_shop_charm5,
    LocationNames.loc_shop_charm6,
    LocationNames.loc_shop_dlc_charm7,
    LocationNames.loc_shop_dlc_charm8
]

class ShopData(NamedTuple):
    shop_map: list[tuple[int, int]]
    shop_locations: dict[str,list[str]]

# Shop Map (shop_index(weapons, charms)) # TODO: Maybe shuffle the amounts later
def get_shop_map(wconf: WorldConfig) -> list[tuple[int, int]]:
        return [(2,2), (2,2), (1,2), (3,2)] if not wconf.use_dlc else [(2,2), (2,2), (2,2), (2,2)]

def setup_shop_data(wconf: WorldConfig) -> ShopData:
    shop_map: list[tuple[int, int]] = get_shop_map(wconf)
    shop_locations: dict[str,list[str]] = {}

    weapon_index = 0
    charm_index = 0
    for i in range(4):
        shop_region: list[str] = []
        if (i == 3):
            shop_region += shop_weapons[weapon_index:]+shop_charms[charm_index:]
        else:
            wcount = min(shop_map[i][0], len(shop_weapons)-weapon_index)
            ccount = min(shop_map[i][1], len(shop_charms)-charm_index)
            shop_region += shop_weapons[weapon_index:(weapon_index+wcount)]
            shop_region += shop_charms[charm_index:(charm_index+ccount)]
            weapon_index+=wcount
            charm_index+=ccount
        shop_locations[LocationNames.shop_sets[i]] = shop_region

    return ShopData(shop_map, shop_locations)
