from typing import Optional, Callable
from BaseClasses import MultiWorld, Region, Entrance, LocationProgressType
from .settings import WorldSettings
from .regiondefs import define_regions
from .locations import CupheadLocation, LocationData
from .levels import LevelData

def create_regions(multiworld: MultiWorld, player: int, locations: dict[str, LocationData], levels: dict[str, LevelData], level_shuffle_map: dict[str, str], settings: WorldSettings) -> None:
    compile_regions = define_regions(player, levels, level_shuffle_map, settings)

    # Create Regions
    for regc in compile_regions:
        if regc:
            region = Region(regc.name, player, multiworld, None)
            if regc.locations:
                for loc_name in regc.locations:
                    if not loc_name: # If entry is None
                        print("WARNING: For \""+regc.name+"\": location \"is None!\"")
                    elif loc_name in locations: # If entry exits in active locations
                        loc_id = locations[loc_name].id
                        event = locations[loc_name].event if loc_id else True
                        progress_type = locations[loc_name].progress_type #if not event else LocationProgressType.EXCLUDED
                        location = CupheadLocation(player, loc_name, loc_id, region, event, progress_type, True) # TODO: Update show_in_spoilers later
                        region.locations.append(location)
                    else:
                        print("NOTE: For \""+regc.name+"\": location \""+loc_name+"\" does not exist.")
            multiworld.regions.append(region)

    # Connect Regions
    def _connect_regions(source: str, target: str, rule: Optional[Callable] = None):
        src = multiworld.get_region(source, player)
        tgt = multiworld.get_region(target, player)
        name = source + " -> " + target
        #print("Connecting "+name)
        connection = Entrance(player, name, src)
        if rule:
            connection.access_rule = rule
        src.exits.append(connection)
        connection.connect(tgt)
    # Connect Region Targets
    for regc in compile_regions:
        if regc and regc.connect_to:
            for target in regc.connect_to:
                if target:
                    _connect_regions(regc.name, target.name, target.rule)

def list_regions_names(regions: list[Region]) -> list[str]:
    return [x.name for x in regions if x]
def list_multiworld_regions_names(multiworld: MultiWorld) -> list[str]:
    return list_regions_names(multiworld.regions)
