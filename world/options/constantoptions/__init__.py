### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from ..protocols import NamedOption
from .constantoptionsbase import NonUserNumericOption

## Option classes that are used internally and are constant value.
## They can never be set by the user. If set by the user, it will be
## ignored.

class BusterQuest(NonUserNumericOption, NamedOption):
    """
    -NOT SUPPORTED OPTION-
    """
    name = "buster_quest"
    default = 1
