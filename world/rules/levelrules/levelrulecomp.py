### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing

from rule_builder.rules import And as RBAnd
from rule_builder.rules import Or as RBOr
from rule_builder.rules import Rule, True_

from ...names import namemap
from . import levelrulebase as lrb
from .levelruledefs import levelrules

if typing.TYPE_CHECKING:
    from .... import CupheadWorld
    from ...options import CupheadOptions


class LevelRuleComp:
    _world: CupheadWorld
    _options: CupheadOptions

    def _debug_on(self) -> bool:
        return self._world.settings.is_debug_bit_on(128)

    def _eval_rule_list(self, rule_list: lrb.RuleList | None) -> Rule:
        if not rule_list:
            return True_()
        return lrb.compile_rule_list(rule_list, self._options, True)

    def _compile_location_rule(self, level: lrb.LevelDef, loc: lrb.LocationDef) -> Rule:
        loc_rule = self._eval_rule_list(loc)
        if not level.base:
            return loc_rule

        base_rule = self._eval_rule_list(level.base)
        match loc.inherit:
            case lrb.InheritMode.AND:
                return RBAnd(base_rule, loc_rule)
            case lrb.InheritMode.OR:
                return RBOr(base_rule, loc_rule)
            case lrb.InheritMode.NONE:
                return loc_rule

    def _compile_level_loc(self, rlname: str, ldef: lrb.LevelDef, locname: str, loc: lrb.LocationDef) -> None:
        rlocname = namemap.get_location_name(locname)
        if rlocname in self._world.active_locations:
            _rule = self._compile_location_rule(ldef, loc)
            self._world.rulereg.add_loc_rule(rlocname, _rule)
            if locname == ldef.exit_location:
                self._world.rulereg.add_region_exit_rule(rlname, _rule)
        else:
            if self._debug_on():
                print(f"Skipping rules for location '{locname}'")
            if locname == ldef.exit_location:
                raise Warning(
                    f"level '{rlname}' exit_location '{ldef.exit_location}' is skipped because location is inactive."
                )

    def compile_levelrules(self) -> None:
        active_levels = self._world.active_levels

        for lname, ldef in levelrules.levels.items():
            if self._debug_on():
                print(lname)

            rlname = namemap.get_region_name(lname)
            if rlname in active_levels:
                if ldef.exit_location and ldef.exit_location not in ldef.locations:
                    raise ValueError(f"'{lname}'.exit_location: '{ldef.exit_location}' is unknown.")

                if not ldef.access:
                    self._world.rulereg.add_region_rule(rlname, self._eval_rule_list(ldef.access))

                for locname, loc in ldef.locations.items():
                    self._compile_level_loc(rlname, ldef, locname, loc)
            elif self._debug_on():
                print(f"Skipping rules for level '{lname}'")

    def __init__(self, world: CupheadWorld):
        self._world = world
        self._options = world.options
