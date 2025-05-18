from enum import IntEnum, IntFlag

class GameMode(IntEnum):
    BEAT_DEVIL = 0
    COLLECT_CONTRACTS = 1
    BUY_OUT_SHOP = 2
    DLC_BEAT_SALTBAKER = 3
    DLC_BEAT_BOTH = 4
    DLC_COLLECT_INGREDIENTS = 5
    DLC_COLLECT_BOTH = 6
    DLC_BEAT_DEVIL_NO_ISLE4 = 7
    DLC_BEAT_SALTBAKER_ISLE4_ONLY = 8
class WeaponMode(IntEnum):
    NORMAL = 0
    PROGRESSIVE = 1
    PROGRESSIVE_EXCEPT_START = 5
    EX_SEPARATE = 2
    EX_SEPARATE_EXCEPT_START = 6
class LevelShuffleMode(IntEnum):
    DISABLED = 0
    ENABLED = 1
    PLANE_SEPARATE = 2
class GradeCheckMode(IntEnum):
    DISABLED = 0
    A_MINUS_GRADE = 1
    A_GRADE = 2
    A_PLUS_GRADE = 3
    S_GRADE = 4
    PACIFIST = 5
class ChaliceMode(IntEnum):
    DISABLED = 0
    START = 1
    VANILLA = 2
    RANDOMIZED = 3
    CHALICE_ONLY = 4
class ChessCastleMode(IntEnum):
    EXCLUDE = 0
    EXCLUDE_GAUNTLET = 1
    GAUNTLET_ONLY = 2
    INCLUDE_ALL = 3
class CurseMode(IntEnum):
    OFF = 0
    VANILLA = 1
    REVERSE = 2
    ALWAYS_ON = 3
    ALWAYS_ON_R = 4
    ALWAYS_ON_1 = 5
    ALWAYS_ON_2 = 6
    ALWAYS_ON_3 = 7
    ALWAYS_ON_4 = 8

class ItemGroups(IntFlag):
    NONE = 0
    ESSENTIAL = 1
    SUPER = 2
    CORE_ITEMS = 3
    WEAPON_BASIC = 4
    WEAPON_EX = 8
    ABILITIES = 32
    AIM_ABILITIES = 64
    ALL = 255
