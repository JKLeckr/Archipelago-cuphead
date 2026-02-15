### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from ..protocols import NamedOption
from .constantoptionsbase import ConstNumericOption

## Option classes that are used internally and are constant value.
## They can never be set by the user. If set by the user, it will be
## ignored.

class BusterQuest(ConstNumericOption, NamedOption):
    """
    -NOT SUPPORTED OPTION-
    """
    name = "buster_quest"
    value = 1


class DlcRandomizeBoat(ConstNumericOption, NamedOption):
    """
    -NOT SUPPORTED OPTION-
    """
    name = "randomize_boat"
    value = 1


class DlcRequiresMausoleum(ConstNumericOption, NamedOption):
    """
    -NOT SUPPORTED OPTION-
    """
    name = "dlc_requires_mausoleum"
    value = 1
