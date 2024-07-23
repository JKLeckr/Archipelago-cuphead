from __future__ import annotations
import typing
from BaseClasses import MultiWorld, Region
from .regiondefs import DefType, RegionData, Rule, get_regions
from .levels import LevelData
from .locations import CupheadLocation
#from . import debug
if typing.TYPE_CHECKING:
    from . import CupheadWorld

def level_map(world: CupheadWorld, level: str) -> LevelData:
    levels = world.active_levels
    level_shuffle_map = world.level_shuffle_map
    if level not in levels:
        return LevelData(None, [])
    if level in level_shuffle_map:
        return levels[level_shuffle_map[level]]
    else:
        return levels[level]

def create_region(world: CupheadWorld, regc: RegionData):
    multiworld = world.multiworld
    locations = world.active_locations
    player = world.player
    region = Region(regc.name, player, multiworld, None)
    if regc.region_type == DefType.LEVEL:
        _locations = list(level_map(world, regc.name).locations)
        #print(regc.name+"[B] :")
        #debug.print_list(_locations)
        if regc.locations:
            _locations += regc.locations
    else:
        _locations = regc.locations
    #print(regc.name+"[A] :")
    #debug.print_list(_locations)
    if _locations:
        for loc_name in _locations:
            if not loc_name: # If entry is None
                print("WARNING: For \""+regc.name+"\": location is None!")
            elif loc_name in locations: # If entry exits in active locations
                loc_id = locations[loc_name].id
                event = locations[loc_name].event if loc_id else True
                progress_type = locations[loc_name].progress_type
                location = CupheadLocation(player, loc_name, loc_id, region, event, progress_type, True) # TODO: Update show_in_spoilers later
                region.locations.append(location)
            else:
                 print("WARNING: For \""+regc.name+"\": location \""+loc_name+"\" does not exist.")
    multiworld.regions.append(region)

def get_rule_def(a: Rule, b: Rule = None) -> Rule:
    if b:
        return lambda s, p: a(s, p) and b(s, p)
    else:
        return a

def connect_region_targets(world: CupheadWorld, regc: RegionData):
    multiworld = world.multiworld
    player = world.player
    for target in regc.connect_to:
        if target:
            if target.depends(world):
                if regc.region_type == DefType.LEVEL:
                    _ruleb = target.rule
                    _rulea = level_map(world, regc.name).rule
                else:
                    _ruleb = None
                    _rulea = target.rule
                _rule = get_rule_def(_rulea, _ruleb)
                src = multiworld.get_region(regc.name, player)
                tgt = multiworld.get_region(target.name, player)
                name = regc.name + " -> " + target.name
                #print("Connecting "+name)
                src.connect(tgt, name, (lambda state, player=player, rule=_rule: rule(state, player)) if _rule else None)
            #else:
            #    print("Skipping Target "+target.name) # if debug
        else:
            print("WARNING: For \""+regc.name+"\": a target is None!")

def create_regions(world: CupheadWorld) -> None:
    compile_regions = get_regions(world)
    #debug.print_list(list_regions_names(compile_regions))

    # Create Regions
    for regc in compile_regions:
        if regc:
            if regc.depends(world):
                create_region(world, regc)
            #else: # if debug
            #    print("Skipping Region "+regc.name)
        else:
            print("WARNING: For \"compile_regions\": region \"is None!\"")

    # Connect Region Targets
    freemove_isles = world.wsettings.freemove_isles
    for regc in compile_regions:
        if regc and regc.connect_to:
            if not freemove_isles or (regc.flags & 1)==1: # If flags contains LV_IGNORE_FREEMOVE
                connect_region_targets(world, regc)

def list_regions_names(regions: list[Region]) -> list[str]:
    return [x.name for x in regions if x]
def list_multiworld_regions_names(multiworld: MultiWorld) -> list[str]:
    return list_regions_names(multiworld.regions)
