from ..names import ItemNames
from . import itemdefs as idefs

item_groups: dict[str, set[str]] = {
    ## Main Groups
    "Weapon": {
        *idefs.item_weapons.keys(),
        *idefs.item_p_weapons.keys(),
        *idefs.item_dlc_weapons.keys(),
        *idefs.item_dlc_p_weapons.keys()
    },
    "Weapon EX": {
        *idefs.item_weapon_ex.keys(),
        *idefs.item_dlc_weapon_ex.keys()
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

    ## Aliases
    ItemNames.item_plane_gun_a: {ItemNames.item_plane_gun},
    ItemNames.item_dlc_cplane_gun_a: {ItemNames.item_dlc_cplane_gun},
}
