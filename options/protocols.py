from typing import Protocol

class CupheadOption(Protocol):
    name: str
    @property
    def current_key(self) -> str:
        return ""

class CupheadNumericOption(CupheadOption, Protocol):
    value: int

class CupheadOptionSet(CupheadOption, Protocol):
    value: set[str]
