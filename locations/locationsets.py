from ..names import LocationNames

s_plane_locations_lv: set[str] = {
    LocationNames.loc_level_boss_plane_blimp,
    LocationNames.loc_level_boss_plane_genie,
    LocationNames.loc_level_boss_plane_bird,
    LocationNames.loc_level_boss_plane_mermaid,
    LocationNames.loc_level_boss_plane_robot,
    LocationNames.loc_level_dlc_boss_plane_cowboy
}
s_plane_locations_topgrade: set[str] = {
    LocationNames.loc_level_boss_plane_blimp_topgrade,
    LocationNames.loc_level_boss_plane_genie_topgrade,
    LocationNames.loc_level_boss_plane_bird_topgrade,
    LocationNames.loc_level_boss_plane_mermaid_topgrade,
    LocationNames.loc_level_boss_plane_robot_topgrade,
    LocationNames.loc_level_dlc_boss_plane_cowboy_topgrade
}
s_plane_locations_event_agrade: set[str] = {
    LocationNames.loc_level_boss_plane_blimp_event_agrade,
    LocationNames.loc_level_boss_plane_genie_event_agrade,
    LocationNames.loc_level_boss_plane_bird_event_agrade,
    LocationNames.loc_level_boss_plane_mermaid_event_agrade,
    LocationNames.loc_level_boss_plane_robot_event_agrade,
}
s_plane_locations_dlc_chaliced: set[str] = {
    LocationNames.loc_level_boss_plane_blimp_dlc_chaliced,
    LocationNames.loc_level_boss_plane_genie_dlc_chaliced,
    LocationNames.loc_level_boss_plane_bird_dlc_chaliced,
    LocationNames.loc_level_boss_plane_mermaid_dlc_chaliced,
    LocationNames.loc_level_boss_plane_robot_dlc_chaliced,
    LocationNames.loc_level_dlc_boss_plane_cowboy_dlc_chaliced
}
s_plane_locations_dlc_event_chaliced: set[str] = {
    LocationNames.loc_level_boss_plane_blimp_event_dlc_chaliced,
    LocationNames.loc_level_boss_plane_genie_event_dlc_chaliced,
    LocationNames.loc_level_boss_plane_bird_event_dlc_chaliced,
    LocationNames.loc_level_boss_plane_mermaid_event_dlc_chaliced,
    LocationNames.loc_level_boss_plane_robot_event_dlc_chaliced,
    LocationNames.loc_level_dlc_boss_plane_cowboy_event_dlc_chaliced,
}

s_plane_locations: set[str] = {
    *s_plane_locations_lv,
    *s_plane_locations_topgrade,
    *s_plane_locations_event_agrade,
    *s_plane_locations_dlc_chaliced,
    *s_plane_locations_dlc_event_chaliced,
}
