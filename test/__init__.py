### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from test.bases import WorldTestBase

from .. import CupheadWorld


class CupheadTestBase(WorldTestBase):
    game = CupheadWorld.GAME_NAME
