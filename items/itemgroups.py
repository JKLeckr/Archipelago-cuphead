from ..names import ItemNames
#from .weapons import weapon_dict, weapon_p_dict
from . import itemdefs as idefs

item_groups: dict[str, set[str]] = {
    "Weapon": {
        *idefs.item_weapons.keys(),
        *idefs.item_p_weapons.keys(),
        *idefs.item_dlc_weapons.keys(),
        *idefs.item_dlc_p_weapons.keys()
    },
    "Charm": {
        *idefs.item_charms.keys(),
        *idefs.item_dlc_charms.keys(),
        ItemNames.item_charm_dlc_cookie
    },
    "Super": {
        *idefs.item_super.keys(),
        *idefs.item_dlc_chalice_super.keys()
    },
    "Ability": {
        *idefs.item_abilities.keys(),
        #*idefs.item_abilities_aim.keys(),
        *idefs.item_dlc_chalice_abilities.keys(),
        #*idefs.item_dlc_chalice_abilities_aim.keys()
    },
}

# TODO: Make aliases a thing, but avoid the conflicts
#for i in range(len(weapon_dict)):
#    item_groups[weapon_dict[i]] = {weapon_p_dict[i]}
