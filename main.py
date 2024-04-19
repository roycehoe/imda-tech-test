from enum import Enum, auto


class StartMenu(Enum):
    USE_MACHINE = auto()
    EXIT = auto()


class MachineMenu(Enum):
    INSERT_COINS = auto()
    SELECT_WASH = auto()


class InsertCoinsMenu(Enum):
    INSERT_TEN_CENTS = auto()
    INSERT_TWENTY_CENTS = auto()
    INSERT_FIFTY_CENTS = auto()
    GO_BACK = auto()


class SelectWashMenu(Enum):
    QUICK_WASH = auto()
    MILD_WASH = auto()
    MEDIUM_WASH = auto()
    HEAVY_WASH = auto()


class PostWashMenu(Enum):
    DISPLAY_STATISTICS = auto()
    RESET_STATISTICS = auto()
    USE_MACHINE = auto()
    EXIT = auto()
