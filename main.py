from dataclasses import dataclass
from enum import Enum, auto

from display import (
    EXIT_DISPLAY,
    INSERT_COIN_MENU_DISPLAY,
    INVALID_SELECTION_DISPLAY,
    MACHINE_MENU_DISPLAY,
    MAINTENANCE_MENU,
    PROMPT_INPUT,
    START_MENU_DISPLAY,
    STATISTICS_RESET_DISPLAY,
    WashingMachineState,
    WashingMachineStatistics,
    show_statistics,
)

DEFAULT_WALLET_BALANCE = 0.00


class InvalidMenuSelectionError(Exception):
    pass


class StartMenuSelection(Enum):
    GO_TO_USE_MACHINE_MENU = auto()
    GO_TO_MANTENANCE_MENU = auto()
    EXIT = auto()


class MachineMenuSelection(Enum):
    INSERT_COINS = auto()
    SELECT_WASH = auto()
    GO_BACK = auto()


class InsertCoinMenuSelection(Enum):
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


def get_maintenance_menu_selection() -> MaintenanceMenuSelection:
    maintenance_menu_selection = input(PROMPT_INPUT)
    if maintenance_menu_selection == "1":
        return MaintenanceMenuSelection.DISPLAY_STATISTICS
    if maintenance_menu_selection == "2":
        return MaintenanceMenuSelection.RESET_STATISTICS
    if maintenance_menu_selection == "0":
        return MaintenanceMenuSelection.GO_BACK
    raise InvalidMenuSelectionError


def get_maintenance_menu_input() -> MaintenanceMenuSelection:
    while True:
        try:
            print(MAINTENANCE_MENU)
            maintenance_menu_selection = get_maintenance_menu_selection()
            return maintenance_menu_selection
        except InvalidMenuSelectionError:
            print(INVALID_SELECTION_DISPLAY)


def get_machine_menu_selection() -> MachineMenuSelection:
    machine_menu_selection = input(PROMPT_INPUT)
    if machine_menu_selection == "1":
        return MachineMenuSelection.INSERT_COINS
    if machine_menu_selection == "2":
        return MachineMenuSelection.SELECT_WASH
    if machine_menu_selection == "3":
        return MachineMenuSelection.GO_BACK
    raise InvalidMenuSelectionError


def get_machine_menu_input() -> MachineMenuSelection:
    while True:
        try:
            print(MACHINE_MENU_DISPLAY)
            machine_menu_selection = get_machine_menu_selection()
            return machine_menu_selection
        except InvalidMenuSelectionError:
            print(INVALID_SELECTION_DISPLAY)


def get_insert_coin_selection() -> InsertCoinMenuSelection:
    insert_coin_selection = input(PROMPT_INPUT)
    if insert_coin_selection == "1":
        return InsertCoinMenuSelection.INSERT_TEN_CENTS
    if insert_coin_selection == "2":
        return InsertCoinMenuSelection.INSERT_TWENTY_CENTS
    if insert_coin_selection == "3":
        return InsertCoinMenuSelection.INSERT_FIFTY_CENTS
    if insert_coin_selection == "4":
        return InsertCoinMenuSelection.INSERT_ONE_DOLLAR
    if insert_coin_selection == "0":
        return InsertCoinMenuSelection.GO_BACK
    raise InvalidMenuSelectionError


def get_insert_coin_input() -> InsertCoinMenuSelection:
    while True:
        try:
            print(INSERT_COIN_MENU_DISPLAY)
            insert_coin_selection = get_insert_coin_selection()
            return insert_coin_selection
        except InvalidMenuSelectionError:
            print(INVALID_SELECTION_DISPLAY)


def topup_washing_machine(
    washing_machine_state: WashingMachineState,
    insert_coin_input: InsertCoinMenuSelection,
) -> None:
    if insert_coin_input == InsertCoinMenuSelection.INSERT_TEN_CENTS:
        return washing_machine_state.topup_balance(0.1)
    if insert_coin_input == InsertCoinMenuSelection.INSERT_TWENTY_CENTS:
        return washing_machine_state.topup_balance(0.2)
    if insert_coin_input == InsertCoinMenuSelection.INSERT_FIFTY_CENTS:
        return washing_machine_state.topup_balance(0.5)
    if insert_coin_input == InsertCoinMenuSelection.INSERT_ONE_DOLLAR:
        return washing_machine_state.topup_balance(1.0)


washing_machine_statistics = WashingMachineStatistics()
washing_machine_state = WashingMachineState()

while True:
    start_menu_input = get_start_menu_input()
    if start_menu_input == StartMenuSelection.EXIT:
        print(EXIT_DISPLAY)
        exit()

    if start_menu_input == StartMenuSelection.GO_TO_MANTENANCE_MENU:
        while True:
            maintenance_menu_input = get_maintenance_menu_input()
            if maintenance_menu_input == MaintenanceMenuSelection.DISPLAY_STATISTICS:
                show_statistics(washing_machine_statistics)
            if maintenance_menu_input == MaintenanceMenuSelection.RESET_STATISTICS:
                washing_machine_statistics.reset()
                print(STATISTICS_RESET_DISPLAY)
            if maintenance_menu_input == MaintenanceMenuSelection.GO_BACK:
                break

    if start_menu_input == StartMenuSelection.GO_TO_USE_MACHINE_MENU:
        while True:
            machine_menu_input = get_machine_menu_input()
            if machine_menu_input == MachineMenuSelection.INSERT_COINS:
                while True:
                    insert_coin_input = get_insert_coin_input()
                    if insert_coin_input == InsertCoinMenuSelection.GO_BACK:
                        break
                    topup_washing_machine(washing_machine_state, insert_coin_input)
                    print(washing_machine_state)

            if machine_menu_input == MachineMenuSelection.SELECT_WASH:
                ...
            if machine_menu_input == MachineMenuSelection.GO_BACK:
                break
