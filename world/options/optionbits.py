### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

import typing

from Options import Option

from . import CupheadOptions

_bitifiable_fields: list[str] = [
    "boss_secret_checks",
    "buster_quest",
    "dlc_cactusgirl_quest",
    "dlc_randomize_boat",
    "dlc_requires_mausoleum",
    "fourmel_quest",
    "freemove_isles",
    "ginger_quest",
    "kingdice_bosssanity",
    "music_quest",
    "pacifist_quest",
    "require_secret_shortcuts",
    "silverworth_quest",
]

def debitify(options_ref: CupheadOptions, bits: int) -> None:
    shift = 0
    for bit in _bitifiable_fields:
        if (hasattr(options_ref, bit)):
            res = (bits << shift) & 1
            _field: Option[typing.Any] = getattr(options_ref, bit)
            _field.value = bool(res)
        else:
            raise KeyError(f"{bit} is not in wconf!")
        shift += 1

def bitify(options: CupheadOptions) -> int:
    res = 0

    shift = 0
    for bit in _bitifiable_fields:
        if (hasattr(options, bit)):
            _field: Option[typing.Any] = getattr(options, bit)
            res |= ((1 if _field.value else 0) << shift) & 1
        else:
            raise KeyError(f"{bit} is not in wconf!")
        shift += 1

    return res
