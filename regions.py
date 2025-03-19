from __future__ import annotations
import typing
from typing import Optional, Collection
from BaseClasses import MultiWorld, Region
from .regiondefs import DefType, RegionData, RegionRule, get_regions
from .levels import get_level, get_mapped_level_name, level_dicepalace_boss
from .locations import CupheadLocation
if typing.TYPE_CHECKING:
    from . import CupheadWorld

def get_region_locations(world: CupheadWorld, region: Region, regc: RegionData) -> list[str]:
    locations: list[str] = []

    if regc.region_type == DefType.LEVEL:
        _level_name = get_mapped_level_name(world, regc.name)
        region.name = _level_name
        _level = get_level(world, _level_name, False)
        locations = _level.locations
        if regc.locations:
            locations = locations + regc.locations
        if (regc.flags & 2)>0 and world.wsettings.kingdice_bosssanity:
            for ldata in level_dicepalace_boss.values():
                locations = locations + ldata.locations
    elif regc.locations:
        locations = regc.locations

    return locations

def create_region(world: CupheadWorld, regc: RegionData, locset: Optional[set[str]] = None):
    multiworld = world.multiworld
    locations = world.active_locations
    player = world.player
    region = Region(regc.name, player, multiworld, None)
    #print(f"Region: {regc.name}, {regc.region_type}")
    region_locations = get_region_locations(world, region, regc)

    for loc_name in region_locations:
        if not loc_name: # If entry is None
            print(f"WARNING: For \"{regc.name}\": location is None!")
        elif loc_name in locations: # If entry exits in active locations
            loc_id = locations[loc_name].id
            event = locations[loc_name].event if loc_id else True
            progress_type = locations[loc_name].progress_type
            location = CupheadLocation(player, loc_name, loc_id, region, event, progress_type, True) # TODO: Update show_in_spoilers later  # noqa: E501
            if locset:
                if loc_name not in locset:
                    locset.add(loc_name)
                else:
                    print(f"WARNING: \"{loc_name}\" already was registered!")
            region.locations.append(location)
        elif world.settings.verbose:
            print(f"Skipping location \"{loc_name}\" for \"{regc.name}\" as it does not exist for this configuration.")

    multiworld.regions.append(region)

def get_rule_def(a: RegionRule, b: Optional[RegionRule] = None) -> RegionRule:
    if b:
        return lambda s, p: a(s, p) and b(s, p)
    else:
        return a

def connect_region_targets(world: CupheadWorld, regc: RegionData, locset: Optional[set[str]] = None):
    if not regc.connect_to:
        raise ValueError(f"For {regc.name}: connect_to cannot be None!")
    multiworld = world.multiworld
    player = world.player
    wsettings = world.wsettings
    for target in regc.connect_to:
        if target:
            if target.depends(wsettings):
                if target.tgt_type == DefType.LEVEL:
                    _ruleb = target.rule
                    _level = get_level(world, target.name)
                    _rulea = _level.rule(wsettings)
                else:
                    _ruleb = None
                    _rulea = target.rule
                _rule = get_rule_def(_rulea, _ruleb) if _rulea else None
                src = multiworld.get_region(regc.name, player)
                tgt = multiworld.get_region(target.name, player)
                name = regc.name + " -> " + target.name
                if locset:
                    for loc in tgt.locations:
                        if loc.name not in locset:
                            locset.add(loc.name)
                src.connect(tgt, name, (lambda state, plyr=player, rule=_rule: rule(state, plyr)) if _rule else None)
                #print(f"{name} | {regc.region_type} | {target.tgt_type} | Rule: {_rule}")
            elif world.settings.verbose:
                print("Skipping Target "+target.name)
        else:
            print(f"WARNING: For \"{regc.name}\": a target is None!")

def create_regions(world: CupheadWorld) -> None:
    compile_regions = get_regions(world)
    #debug.print_list(list_regions_names(compile_regions))

    # Create Regions
    for regc in compile_regions:
        if regc:
            if regc.depends(world.wsettings):
                create_region(world, regc)
            elif world.settings.verbose:
                print("Skipping Region "+regc.name)
        else:
            print(f"WARNING: For \"{compile_regions}\": region is None!")

    # Connect Region Targets
    freemove_isles = world.wsettings.freemove_isles
    for regc in compile_regions:
        if regc and regc.depends(world.wsettings) and regc.connect_to:
            if not freemove_isles or (regc.flags & 1)>0: # If flags contains LV_IGNORE_FREEMOVE
                connect_region_targets(world, regc)

def list_regions_names(regions: Collection[Region]) -> list[str]:
    return [x.name for x in regions if x]
def list_multiworld_regions_names(multiworld: MultiWorld) -> list[str]:
    return list_regions_names(multiworld.get_regions(None))
