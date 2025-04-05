from __future__ import annotations
from typing import NamedTuple
from BaseClasses import LocationProgressType

class LocationData(NamedTuple):
    id: int | None
    progress_type: LocationProgressType = LocationProgressType.DEFAULT
    event: bool = False

    def with_progress_type(self, progress_type: LocationProgressType) -> LocationData:
        return LocationData(self.id, progress_type, self.event)
