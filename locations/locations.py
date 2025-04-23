from __future__ import annotations
from BaseClasses import Location, Region, LocationProgressType
from .locationbase import LocationData
from ..enums import GameMode, GradeCheckMode, ChessCastleMode
from ..names import LocationNames
from ..wsettings import WorldSettings
from . import locationdefs as ld

class CupheadLocation(Location):
    game: str = "Cuphead"
    def __init__(
            self,
            player: int,
            name: str = '',
            id: int | None = None,
            parent: Region | None = None,
            event: bool = False,
            progress_type: LocationProgressType = LocationProgressType.DEFAULT,
            show_in_spoiler: bool = True
        ):
        super().__init__(player, name, id, parent)
        self.event = event
        self.progress_type = progress_type
        self.show_in_spoiler = show_in_spoiler

def add_location(locations_ref: dict[str,LocationData], loc_name: str):
    locations_ref[loc_name] = ld.locations_all[loc_name]

def exclude_location(locations_ref: dict[str,LocationData], loc_name: str):
    locations_ref[loc_name] = locations_ref[loc_name].with_progress_type(LocationProgressType.EXCLUDED)

def setup_grade_check_locations(locations_ref: dict[str,LocationData], settings: WorldSettings):
    boss_grade_checks = settings.boss_grade_checks
    rungun_grade_checks = settings.rungun_grade_checks
    if boss_grade_checks>0:
        locations_ref.update(ld.location_level_boss_topgrade)
        if settings.mode != GameMode.BEAT_DEVIL:
            locations_ref.update(ld.location_level_boss_final_topgrade)
    if rungun_grade_checks>0:
        if rungun_grade_checks>=1 and rungun_grade_checks<=3:
            locations_ref.update(ld.location_level_rungun_agrade)
        elif rungun_grade_checks==GradeCheckMode.PACIFIST:
            locations_ref.update(ld.location_level_rungun_pacifist)
    if settings.boss_secret_checks:
        locations_ref.update(ld.location_level_boss_secret)

def setup_quest_locations(locations_ref: dict[str,LocationData], settings: WorldSettings):
    def _add_location(name: str):
        add_location(locations_ref, name)
    if settings.fourparries_quest:
        _add_location(LocationNames.loc_quest_4parries)
    if settings.ginger_quest:
        _add_location(LocationNames.loc_quest_ginger)
        _add_location(LocationNames.loc_event_isle2_shortcut)
    if settings.fourmel_quest:
        _add_location(LocationNames.loc_quest_4mel)
        _add_location(LocationNames.loc_event_quest_4mel_4th)
    if settings.lucien_quest:
        _add_location(LocationNames.loc_quest_lucien)
    if settings.music_quest:
        _add_location(LocationNames.loc_quest_music)
        _add_location(LocationNames.loc_event_quest_ludwig)
        _add_location(LocationNames.loc_event_quest_wolfgang)
    if settings.silverworth_quest:
        locations_ref.update(ld.locations_event_agrade)
        if settings.mode == GameMode.BEAT_DEVIL:
            locations_ref.update(ld.location_level_boss_final_event_agrade)
        _add_location(LocationNames.loc_quest_silverworth)
    if settings.pacifist_quest:
        locations_ref.update(ld.location_level_rungun_event_pacifist)
        _add_location(LocationNames.loc_quest_pacifist)

def setup_boss_final_locations(
        locations_ref: dict[str,LocationData],
        settings: WorldSettings,
        base_final: dict[str,LocationData],
        dlc_final: dict[str,LocationData],
    ):
    if settings.mode != GameMode.BEAT_DEVIL:
        locations_ref.update(base_final)
    if settings.use_dlc and settings.mode != GameMode.DLC_BEAT_SALTBAKER:
        locations_ref.update(dlc_final)

def setup_dlc_chalice_locations(locations_ref: dict[str,LocationData], settings: WorldSettings):
    locations_ref.update(ld.location_level_dlc_tutorial)
    add_location(locations_ref, LocationNames.loc_dlc_cookie)
    if settings.dlc_boss_chalice_checks:
        locations_ref.update(ld.locations_dlc_boss_chaliced)
        if settings.mode != GameMode.DLC_BEAT_SALTBAKER:
            locations_ref.update(ld.location_level_boss_final_dlc_chaliced)
        if settings.mode != GameMode.DLC_BEAT_SALTBAKER:
            locations_ref.update(ld.location_level_dlc_boss_final_dlc_chaliced)
    if settings.dlc_rungun_chalice_checks:
        locations_ref.update(ld.location_level_rungun_dlc_chaliced)
    if settings.dlc_kingdice_chalice_checks:
        locations_ref.update(ld.location_level_dicepalace_dlc_chaliced)
    if settings.dlc_chess_chalice_checks:
        locations_ref.update(ld.location_level_dlc_chesscastle_dlc_chaliced)
    if settings.dlc_cactusgirl_quest:
        locations_ref.update(ld.locations_dlc_event_boss_chaliced)
        setup_boss_final_locations(
            locations_ref,
            settings,
            ld.location_level_boss_final_event_dlc_chaliced,
            ld.location_level_dlc_boss_final_event_dlc_chaliced,
        )
        add_location(locations_ref, LocationNames.loc_dlc_quest_cactusgirl)

def setup_dlc_locations(locations_ref: dict[str,LocationData], settings: WorldSettings):
    locations_ref.update(ld.locations_dlc)
    if settings.boss_grade_checks>0:
        locations_ref.update(ld.location_level_dlc_boss_topgrade)
        if settings.mode != GameMode.DLC_BEAT_SALTBAKER:
            locations_ref.update(ld.location_level_dlc_boss_final_topgrade)
    if settings.dlc_requires_mausoleum:
        add_location(locations_ref, LocationNames.loc_event_mausoleum)
    if settings.dlc_chalice > 0:
        setup_dlc_chalice_locations(locations_ref, settings)
    if settings.dlc_kingsleap != ChessCastleMode.INCLUDE_ALL:
        for loc in ld.location_level_dlc_chesscastle.keys():
            if (
                (
                    settings.dlc_kingsleap == ChessCastleMode.EXCLUDE_GAUNTLET and
                    loc == LocationNames.level_dlc_chesscastle_run
                ) or (
                    settings.dlc_kingsleap == ChessCastleMode.GAUNTLET_ONLY and
                    loc != LocationNames.level_dlc_chesscastle_run
                ) or settings.dlc_kingsleap == ChessCastleMode.EXCLUDE
            ):
                exclude_location(locations_ref, loc)

def setup_locations(settings: WorldSettings):
    use_dlc = settings.use_dlc
    locations: dict[str,LocationData] = {**ld.locations_base}

    setup_grade_check_locations(locations, settings)

    setup_quest_locations(locations, settings)

    if use_dlc:
        setup_dlc_locations(locations, settings)

    if settings.is_goal_used(LocationNames.loc_event_goal_devil):
        locations.update(ld.location_goal)
    if use_dlc and settings.is_goal_used(LocationNames.loc_event_dlc_goal_saltbaker):
        locations.update(ld.location_dlc_goal)

    setup_boss_final_locations(
        locations,
        settings,
        ld.location_level_boss_final,
        ld.location_level_dlc_boss_final
    )

    return locations
