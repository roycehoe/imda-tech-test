from enum import Enum, auto


class StartMenuOptions(Enum):
    WASH_SETTINGS = auto()
    MANTENANCE = auto()
    EXIT = auto()


class WashSettingsOptions(Enum):
    INSERT_COINS = auto()
    SELECT_WASH = auto()
    GO_BACK = auto()


class InsertCoinOptions(Enum):
    INSERT_TEN_CENTS = auto()
    INSERT_TWENTY_CENTS = auto()
    INSERT_FIFTY_CENTS = auto()
    INSERT_ONE_DOLLAR = auto()
    GO_BACK = auto()


class SelectWashOptions(Enum):
    QUICK_WASH = auto()
    MILD_WASH = auto()
    MEDIUM_WASH = auto()
    HEAVY_WASH = auto()
    GO_BACK = auto()


class MaintenanceOptions(Enum):
    DISPLAY_STATISTICS = auto()
    RESET_STATISTICS = auto()
    GO_BACK = auto()


class SelectWashOutcome(Enum):
    BALANCE_MORE_THAN_WASH_PRICE = auto()
    BALANCE_EQUALS_TO_WASH_PRICE = auto()
    BALANCE_LESS_THAN_WASH_PRICE = auto()
