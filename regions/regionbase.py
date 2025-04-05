from __future__ import annotations
from typing_extensions import override
from enum import IntEnum, IntFlag
from ..rules.rulebase import RegionRule
from .dep import Dep
from . import dep

class DefType(IntEnum):
    SIMPLE = 0
    LEVEL = 1
    WORLD = 2
class DefFlags(IntFlag):
    NONE = 0
    TGT_IGNORE_FREEMOVE = 1
    DICE_PALACE = 3

class Target:
    name: str
    rule: RegionRule | None
    depends: Dep
    tgt_type: DefType
    def __init__(
            self,
            name: str,
            rule: RegionRule | None = None,
            depends: Dep | None = None,
            tgt_type: DefType = DefType.SIMPLE
        ):
        self.name = name
        self.rule = rule
        self.depends = depends if depends else dep.dep_none
        self.tgt_type = tgt_type
    @override
    def __str__(self) -> str:
        return self.name
class LevelTarget(Target):
    def __init__(self, name: str, add_rule: RegionRule | None = None, depends: Dep | None = None):
        super().__init__(name, add_rule, depends, DefType.LEVEL)
class RegionData:
    name: str
    locations: list[str] | None
    connect_to: list[Target] | None
    depends: Dep
    region_type: DefType
    flags: DefFlags
    def __init__(
            self,
            name: str,
            locations: list[str] | None = None,
            connect_to: list[Target] | None = None,
            depends: Dep | None = None,
            region_type: DefType = DefType.SIMPLE,
            flags: DefFlags = DefFlags.NONE):
        self.name = name
        self.locations = locations
        self.connect_to = connect_to
        self.depends = depends if depends else dep.dep_none
        self.region_type = region_type
        self.flags = flags
    @override
    def __str__(self) -> str:
        return self.name
class LevelRegionData(RegionData):
    def __init__(
            self,
            name: str,
            add_locations: list[str] | None = None,
            connect_to: list[Target] | None = None,
            depends: Dep | None = None,
            flags: DefFlags = DefFlags.NONE):
        super().__init__(name, add_locations, connect_to, depends, DefType.LEVEL, flags)
class WorldRegionData(RegionData):
    def __init__(
            self,
            name: str,
            add_locations: list[str] | None = None,
            connect_to: list[Target] | None = None,
            depends: Dep | None = None,
            flags: DefFlags = DefFlags.TGT_IGNORE_FREEMOVE):
        super().__init__(name, add_locations, connect_to, depends, DefType.WORLD, flags)
