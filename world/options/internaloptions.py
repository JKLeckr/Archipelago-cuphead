### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from Options import FreeText, NumericOption, Visibility

from .protocols import NamedOption

## Internally set Option classes. These options are set internally by the APWorld
## and can never be set by the user. If set by the user, it will be overwritten
## internally.

class Version(FreeText, NamedOption):
    """
    Internal. Set during generation.
    The version of the APWorld
    """
    name = "version"
    display_name = "APWorld Version"
    visibility = Visibility.spoiler
    default = "MISSINGVER"

class Coin1Amount(NumericOption, NamedOption):
    """
    Internal. Set during generation.
    Amount of 1 coins
    """
    name = "coin1_amount"
    visibility = Visibility.none

class Coin2Amount(NumericOption, NamedOption):
    """
    Internal. Set during generation.
    Amount of 2 coins
    """
    name = "coin2_amount"
    visibility = Visibility.none

class Coin3Amount(NumericOption, NamedOption):
    """
    Internal. Set during generation.
    Amount of 3 coins
    """
    name = "coin3_amount"
    visibility = Visibility.none
