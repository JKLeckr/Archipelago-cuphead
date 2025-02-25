from typing import Dict, Any
from Options import Option
from ..names import ItemNames
from ..options import CupheadOptions
from . import CupheadTestBase

class TestOptions(CupheadTestBase):
    option_dict: Dict[str, Dict[Option[Any], Any]] = {
        "Test Default Options": {}
    }

    def test_options(self):
        pass
