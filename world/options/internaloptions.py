### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from Options import FreeText, NumericOption, Option, Visibility

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


class CoinAmounts(Option[tuple[int, int, int]], NamedOption):
    """
    Internal. Set during generation.
    Amount of each type of coin
    """
    name = "coin_amounts"
    visibility = Visibility.none
    default = (0, 0, 0)


class ContractRequirementsIsle2(NumericOption, NamedOption):
    """
    Internal. Set during generation.
    Amount of contracts needed to access Inkwell Isle II
    """
    name = "contract_requirements_isle2"
    visibility = Visibility.none


class ContractRequirementsIsle3(NumericOption, NamedOption):
    """
    Internal. Set during generation.
    Amount of contracts needed to access Inkwell Isle III
    """
    name = "contract_requirements_isle3"
    visibility = Visibility.none
