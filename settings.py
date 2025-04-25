from __future__ import annotations
from typing import Union # type: ignore
import settings

class CupheadSettings(settings.Group):
    class StrictGoalOptions(settings.Bool):
        """
        Make goal options strict.
        That means certain option combinations are enforced.
        One example is contract_goal_requirements must be greater than or equal to contract_requirements.
        """

    class LogOptionOverrides(settings.Bool):
        """Log options that are overridden from incompatible combinations to console."""

    class WriteOverridesToSpoiler(settings.Bool):
        """Write options that are overridden from incompatible combinations to spoiler."""

    class Verbose(settings.Bool):
        """Log extra information to the console."""

    class Debug:
        """Debug mode."""

    strict_goal_options: Union[StrictGoalOptions, bool] = True # type: ignore
    log_option_overrides: Union[LogOptionOverrides, bool] = True # type: ignore
    write_overrides_to_spoiler: Union[WriteOverridesToSpoiler, bool] = True # type: ignore
    verbose: Union[LogOptionOverrides, bool] = False # type: ignore
    debug: Union[Debug, int] = 0 # type: ignore
