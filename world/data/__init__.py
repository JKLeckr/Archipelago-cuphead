### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from enum import IntEnum
from importlib import resources
from typing import Any, Literal, NamedTuple

import orjson

if not __package__:
    raise ImportError("Package is None")

data_files = resources.files(__package__)

_loaded_data: dict[str, str | bytes] = {}

class DataType(IntEnum):
    BIN = 0
    STR = 1
    JSON = 2

class DataEntry(NamedTuple):
    file_ext: str
    data_type: DataType

data_reg: dict[str, DataEntry] = {
    "levelruledefs": DataEntry("json", DataType.JSON),
    "levelrulepresets": DataEntry("json", DataType.JSON)
}
DataName = Literal["levelruledefs", "levelrulepresets"]

def load_data(dataname: DataName) -> None:
    if dataname not in data_reg:
        raise KeyError(f"'{dataname}' is not in the data registry")
    if dataname in _loaded_data:
        raise ResourceWarning(f"'{dataname}' is already loaded. Reloading.")
    data_entry = data_reg[dataname]
    datafilename = dataname + (f".{data_entry.file_ext}" if data_entry.file_ext else "")
    try:
        with data_files.joinpath(datafilename).open("rb") as file:
            data = file.read()
        if data_entry.data_type == DataType.STR:
            data = data.decode("utf-8")
        elif data_entry.data_type == DataType.JSON:
            data = orjson.loads(data)
        _loaded_data[dataname] = data
    except OSError as e:
        raise OSError(f"Could not load resource '{dataname}': {e}") from e

def unload_data(dataname: DataName) -> None:
    if dataname not in data_reg:
        raise KeyError(f"'{dataname}' is not in the data registry")
    if dataname not in _loaded_data:
        raise ResourceWarning(f"'{dataname}' is not loaded.")
    del _loaded_data[dataname]

def get_data(dataname: DataName) -> str | bytes:
    if dataname not in data_reg:
        raise KeyError(f"'{dataname}' is not loaded")
    return _loaded_data[dataname]

def get_bytes_data(dataname: DataName) -> bytes:
    _data = get_data(dataname)
    if _data is bytes:
        return _data
    raise ValueError(f"{dataname} is not a valid binary data type")

def get_str_data(dataname: DataName) -> str:
    _data = get_data(dataname)
    if _data is str:
        return _data
    raise ValueError(f"{dataname} is not a valid binary data type")

def get_json_data(dataname: DataName) -> Any:
    _data = get_data(dataname)
    if data_reg[dataname].data_type != DataType.JSON:
        raise ValueError(f"{dataname} is not a valid json data type")
    return _data
