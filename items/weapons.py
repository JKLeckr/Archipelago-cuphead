from ..names import ItemNames
from ..enums import WeaponMode
from ..wconf import WorldConfig

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
weapon_ex_dict: dict[int,str] = {
    0: ItemNames.item_weapon_peashooter_ex,
    1: ItemNames.item_weapon_spread_ex,
    2: ItemNames.item_weapon_chaser_ex,
    3: ItemNames.item_weapon_lobber_ex,
    4: ItemNames.item_weapon_charge_ex,
    5: ItemNames.item_weapon_roundabout_ex,
    6: ItemNames.item_weapon_dlc_crackshot_ex,
    7: ItemNames.item_weapon_dlc_converge_ex,
    8: ItemNames.item_weapon_dlc_twistup_ex,
}
weapon_p_dict: dict[int,str] = {
    0: ItemNames.item_p_weapon_peashooter,
    1: ItemNames.item_p_weapon_spread,
    2: ItemNames.item_p_weapon_chaser,
    3: ItemNames.item_p_weapon_lobber,
    4: ItemNames.item_p_weapon_charge,
    5: ItemNames.item_p_weapon_roundabout,
    6: ItemNames.item_p_weapon_dlc_crackshot,
    7: ItemNames.item_p_weapon_dlc_converge,
    8: ItemNames.item_p_weapon_dlc_twistup,
}
weapon_to_index: dict[str, int] = {y:x for x,y in weapon_dict.items()}

def get_weapon_dict(wconf: WorldConfig, dlc_weapons: bool = True) -> dict[int,str]:
    orig_weapon_dict: dict[int,str] = weapon_p_dict if (wconf.weapon_mode & WeaponMode.PROGRESSIVE) > 0 else weapon_dict
    nweapon_dict: dict[int,str] = {k:v for k,v in orig_weapon_dict.items() if k<6 or dlc_weapons}
    return nweapon_dict
