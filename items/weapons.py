from ..names import ItemNames
from ..enums import WeaponExMode
from ..wsettings import WorldSettings

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
def get_weapon_dict(settings: WorldSettings, dlc_weapons: bool = True) -> dict[int,str]:
    orig_weapon_dict: dict[int,str] = weapon_p_dict if settings.randomize_weapon_ex>0 else weapon_dict
    nweapon_dict: dict[int,str] = {k:v for k,v in orig_weapon_dict.items() if k<6 or dlc_weapons}
    if settings.randomize_abilities == WeaponExMode.ALL_BUT_START:
        start_weapon = settings.start_weapon
        nweapon_dict[start_weapon] = weapon_dict[start_weapon]
    return nweapon_dict
