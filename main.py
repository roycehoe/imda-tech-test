from dataclasses import dataclass
from enum import Enum, auto

from display import (
    EXIT_DISPLAY,
    INVALID_SELECTION_DISPLAY,
    PROMPT_INPUT,
    START_MENU_DISPLAY,
)

DEFAULT_WALLET_BALANCE = 0.00


class InvalidMenuSelectionError(Exception):
    pass


class StartMenuSelection(Enum):
    GO_TO_USE_MACHINE_MENU = auto()
    GO_TO_MANTENANCE_MENU = auto()
    EXIT = auto()


class UseMachineMenuSelection(Enum):
    INSERT_COINS = auto()
    SELECT_WASH = auto()
    GO_BACK = auto()


class InsertCoinsMenuSelection(Enum):
    INSERT_TEN_CENTS = auto()
    INSERT_TWENTY_CENTS = auto()
    INSERT_FIFTY_CENTS = auto()
    INSERT_ONE_DOLLAR = auto()
    GO_BACK = auto()


class SelectWashMenuSelection(Enum):
    QUICK_WASH = auto()
    MILD_WASH = auto()
    MEDIUM_WASH = auto()
    HEAVY_WASH = auto()
    GO_BACK = auto()


class MaintenanceMenuSelection(Enum):
    DISPLAY_STATISTICS = auto()
    RESET_STATISTICS = auto()
    GO_BACK = auto()


def get_start_menu_selection() -> StartMenuSelection:
    start_menu_selection = input(PROMPT_INPUT)
    if start_menu_selection == "1":
        return StartMenuSelection.GO_TO_USE_MACHINE_MENU
    if start_menu_selection == "2":
        return StartMenuSelection.GO_TO_MANTENANCE_MENU
    if start_menu_selection == "3":
        return StartMenuSelection.EXIT
    raise InvalidMenuSelectionError


def get_start_menu_input() -> StartMenuSelection:
    while True:
        try:
            print(START_MENU_DISPLAY)
            start_menu_selection = get_start_menu_selection()
            return start_menu_selection
        except InvalidMenuSelectionError:
            print(INVALID_SELECTION_DISPLAY)


while True:
    start_menu_input = get_start_menu_input()
    if start_menu_input == StartMenuSelection.EXIT:
        print(EXIT_DISPLAY)
        exit()
