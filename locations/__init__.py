from __future__ import annotations
from BaseClasses import Location, Region, LocationProgressType
from . import locationsetup

class CupheadLocation(Location):
    game: str = "Cuphead"
    def __init__(
            self,
            player: int,
            name: str = '',
            id: int | None = None,
            parent: Region | None = None,
            event: bool = False,
            progress_type: LocationProgressType = LocationProgressType.DEFAULT,
            show_in_spoiler: bool = True
        ):
        super().__init__(player, name, id, parent)
        self.event = event
        self.progress_type = progress_type
        self.show_in_spoiler = show_in_spoiler

setup_locations = locationsetup.setup_locations
