from __future__ import annotations
from typing import Union # type: ignore
import settings

class CupheadSettings(settings.Group):
    class Debug(int):
        """Debug mode."""

    debug: Union[Debug, int] = 0 # type: ignore

    def is_debug_bit_on(self, bit: int):
        return (int(self.debug) & bit) == bit
