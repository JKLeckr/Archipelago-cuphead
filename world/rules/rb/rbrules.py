### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar

from typing_extensions import override

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from rule_builder.rules import Has, HasAny, Rule, WrapperRule

from ...consts import GAME_NAME as GAME
from ...items import weapons

if TYPE_CHECKING:
    from .... import CupheadWorld

@dataclass
class Preset(WrapperRule["CupheadWorld"], game=GAME):
    name: str
    filtered_resolution: bool = field(default=True, kw_only=True)
    _names_reg: ClassVar[set[str]] = set()

    def __post_init__(self) -> None:
        if self.name in self._names_reg:
            raise ValueError(f"Preset name '{self.name}' already exists!")
        super().__post_init__()
        self._names_reg.add(self.name)

    @override
    def _instantiate(self, world: "CupheadWorld") -> Rule.Resolved:
        _reg = world.rulereg.presets
        if rrule := _reg.get(self.name):
            return rrule
        rrule = self.Resolved(
            self.child.resolve(world),
            self.name,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )
        _reg.set(self.name, rrule)
        return rrule

    @override
    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.child}]"

    class Resolved(WrapperRule.Resolved):
        name: str

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            if state is None:
                return [{"type": "text", "text": str(self)}]
            msg: list[JSONMessagePart] = [
                {"type": "color", "color": "green" if self(state) else "salmon", "text": self.name},
                {"type": "color", "color": "white", "text": "["},
            ]
            msg.extend(self.child.explain_json(state))
            msg.append({"type": "color", "color": "white", "text": "]"})
            return msg

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            return f"{self.name}: {state is not None} ({self.child.explain_str(state)})"

        @override
        def __str__(self) -> str:
            return f"{self.name}[{self.child}]"

@dataclass
class HasAnyWeapon(Rule["CupheadWorld"], game=GAME):
    @override
    def _instantiate(self, world: "CupheadWorld") -> Rule.Resolved:
        return self.Resolved(
            tuple(weapons.weapon_dict.values()),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(HasAny.Resolved):
        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                item: {id(self)}
                for items in [self.item_names, weapons.weapon_p_dict.values()]
                for item in items
            }

@dataclass
class HasAnyWeaponEx(HasAnyWeapon, game=GAME):
    @override
    def _instantiate(self, world: "CupheadWorld") -> Rule.Resolved:
        _weapon_dict = weapons.weapon_ex_dict if world.options.weapon_mode > 0 else weapons.weapon_dict
        return self.Resolved(
            tuple(_weapon_dict.values()),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

@dataclass
class HasWeapon(Rule["CupheadWorld"], game=GAME):
    weapon_name: str

    @override
    def __post_init__(self) -> None:
        if self.weapon_name not in weapons.weapon_to_index.keys():
            raise KeyError(f"{self.weapon_name} not in weapon_dict")
        return super().__post_init__()

    @override
    def _instantiate(self, world: "CupheadWorld") -> Rule.Resolved:
        return self.Resolved(
            self.weapon_name,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(Has.Resolved):
        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                self.item_name: {id(self)},
                weapons.weapon_p_dict[weapons.weapon_to_index[self.item_name]]: {id(self)}
            }

@dataclass
class HasWeaponEx(HasWeapon, game=GAME):
    @override
    def __post_init__(self) -> None:
        if self.weapon_name not in weapons.weapon_to_index.keys():
            raise KeyError(f"{self.weapon_name} not in weapon_dict")
        return super().__post_init__()

    @override
    def _instantiate(self, world: "CupheadWorld") -> Rule.Resolved:
        if world.options.weapon_mode > 0:
            _weapon_name = weapons.weapon_ex_dict[weapons.weapon_to_index[self.weapon_name]]
        else:
            _weapon_name = self.weapon_name
        return self.Resolved(
            _weapon_name,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(HasWeapon.Resolved):
        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                self.item_name: {id(self)},
                weapons.weapon_p_dict[weapons.weapon_ex_to_index[self.item_name]]: {id(self)}
            }
