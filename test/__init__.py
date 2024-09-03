from test.bases import WorldTestBase
from .. import CupheadWorld

class CupheadTestBase(WorldTestBase):
    game = "Cuphead"
    world: CupheadWorld
