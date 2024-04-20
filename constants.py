from dataclasses import dataclass
from typing import Final

from enums import (
    InsertCoinOptions,
    MaintenanceOptions,
    SelectWashOptions,
    StartMenuOptions,
    WashSettingsOptions,
)


@dataclass
class WashingTypeData:
    time: int
    price: float


@dataclass
class WashingTypes:
    QUICK_WASH: Final = WashingTypeData(10, 2.00)
    MILD_WASH: Final = WashingTypeData(10, 2.00)
    MEDIUM_WASH: Final = WashingTypeData(10, 2.00)
    HEAVY_WASH: Final = WashingTypeData(10, 2.00)


DEFAULT_WASHING_TYPES = WashingTypes()

USER_INPUT_TO_START_OPTIONS_MAPPING = {
    "1": StartMenuOptions.WASH_SETTINGS,
    "2": StartMenuOptions.MANTENANCE,
    "3": StartMenuOptions.EXIT,
}

USER_INPUT_TO_MAINTENANCE_OPTIONS_MAPPING = {
    "1": MaintenanceOptions.DISPLAY_STATISTICS,
    "2": MaintenanceOptions.RESET_STATISTICS,
    "0": MaintenanceOptions.GO_BACK,
}

USER_INPUT_TO_WASH_SETTINGS_OPTIONS_MAPPING = {
    "1": WashSettingsOptions.INSERT_COINS,
    "2": WashSettingsOptions.SELECT_WASH,
    "0": WashSettingsOptions.GO_BACK,
}

USER_INPUT_TO_INSERT_COIN_OPTIONS_MAPPING = {
    "1": InsertCoinOptions.INSERT_TEN_CENTS,
    "2": InsertCoinOptions.INSERT_TWENTY_CENTS,
    "3": InsertCoinOptions.INSERT_FIFTY_CENTS,
    "4": InsertCoinOptions.INSERT_ONE_DOLLAR,
    "0": InsertCoinOptions.GO_BACK,
}

USER_INPUT_TO_SELECT_WASH_OPTIONS_MAPPING = {
    "1": SelectWashOptions.QUICK_WASH,
    "2": SelectWashOptions.MILD_WASH,
    "3": SelectWashOptions.MEDIUM_WASH,
    "4": SelectWashOptions.HEAVY_WASH,
    "0": SelectWashOptions.GO_BACK,
}

INSERT_COIN_OPTIONS_TO_COIN_VALUE_MAPPING = {
    InsertCoinOptions.INSERT_TEN_CENTS: 0.10,
    InsertCoinOptions.INSERT_TWENTY_CENTS: 0.20,
    InsertCoinOptions.INSERT_FIFTY_CENTS: 0.50,
    InsertCoinOptions.INSERT_ONE_DOLLAR: 1.00,
}
