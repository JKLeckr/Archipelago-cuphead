from __future__ import annotations
import typing
from BaseClasses import MultiWorld, Region, LocationProgressType
from .regiondefs import define_regions
from .levels import LevelData
from .locations import CupheadLocation
if typing.TYPE_CHECKING:
    from . import CupheadWorld

def level_map(world: CupheadWorld, level: str) -> LevelData:
    levels = world.active_levels
    level_shuffle_map = world.level_shuffle_map
    if level not in levels:
        return LevelData(None,[])
    if level in level_shuffle_map:
        return levels[level_shuffle_map[level]]
    else:
        return levels[level]

def create_regions(world: CupheadWorld) -> None:
    player = world.player
    multiworld = world.multiworld
    locations = world.active_locations

    compile_regions = define_regions(world)

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
                        print("WARNING: For \""+regc.name+"\": location \""+loc_name+"\" does not exist.")
            multiworld.regions.append(region)

    # Connect Region Targets
    for regc in compile_regions:
        if regc and regc.connect_to:
            for target in regc.connect_to:
                if target:
                    src = multiworld.get_region(regc.name, player)
                    tgt = multiworld.get_region(target.name, player)
                    name = regc.name + " -> " + target.name
                    #print("Connecting "+name)
                    src.connect(tgt, name, target.rule)

def list_regions_names(regions: list[Region]) -> list[str]:
    return [x.name for x in regions if x]
def list_multiworld_regions_names(multiworld: MultiWorld) -> list[str]:
    return list_regions_names(multiworld.regions)
