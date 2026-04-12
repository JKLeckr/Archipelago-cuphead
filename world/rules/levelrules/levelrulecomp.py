### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from typing import TYPE_CHECKING

from rule_builder.rules import Rule, True_

from . import levelrulebase as lrb
from .levelruledefs import levelrules

if TYPE_CHECKING:
    from .... import CupheadWorld
    from ...options import CupheadOptions


class LevelRuleComp:
    _world: "CupheadWorld"
    _options: "CupheadOptions"

    def _debug_on(self) -> bool:
        return self._world.settings.is_debug_bit_on(128)

    def _compile_location_rule(
        self,
        level: lrb.LevelDef,
        loc: lrb.LocationDef,
    ) -> Rule["CupheadWorld"] | None:
        if level.base is None:
            return loc.rule
        if loc.rule is None:
            return level.base

        match loc.inherit:
            case lrb.InheritMode.AND:
                return level.base & loc.rule
            case lrb.InheritMode.OR:
                return level.base | loc.rule
            case lrb.InheritMode.NONE:
                return loc.rule

    def _compile_level_loc(
        self,
        rlname: str,
        ldef: lrb.LevelDef,
        locname: str,
        loc: lrb.LocationDef,
    ) -> None:
        if locname in self._world.active_locations:
            _rule = self._compile_location_rule(ldef, loc)
            if _rule is None:
                _rule = True_()
            self._world.rulereg.add_loc_rule(locname, _rule)
            if locname == ldef.exit_location:
                self._world.rulereg.add_region_exit_rule(rlname, _rule)
        else:
            if self._debug_on():
                print(f"Skipping rules for location '{locname}'")
            if locname == ldef.exit_location:
                raise ValueError(
                    f"level '{rlname}' exit_location '{ldef.exit_location}' is an inactive location."
                )

    def compile_levelrules(self) -> None:
        active_levels = self._world.active_levels

        for lname, ldef in levelrules.levels.items():
            if self._debug_on():
                print(lname)

            if lname in active_levels:
                if ldef.exit_location and ldef.exit_location not in ldef.locations:
                    raise ValueError(f"'{lname}'.exit_location: '{ldef.exit_location}' is unknown.")

                _rule = ldef.access
                self._world.rulereg.add_region_rule(lname, _rule if _rule is not None else True_())

                for locname, loc in ldef.locations.items():
                    self._compile_level_loc(lname, ldef, locname, loc)
            elif self._debug_on():
                print(f"Skipping rules for level '{lname}'")

    def __init__(self, world: "CupheadWorld"):
        self._world = world
        self._options = world.options
