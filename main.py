import time
from abc import ABC
from dataclasses import dataclass
from enum import Enum, auto

from display import (
    END_WASH_DISPLAY,
    EXIT_DISPLAY,
    INSERT_COIN_MENU_DISPLAY,
    INSUFFICIENT_FUNDS_DISPLAY,
    INVALID_SELECTION_DISPLAY,
    MACHINE_MENU_DISPLAY,
    MAINTENANCE_MENU,
    PROMPT_INPUT,
    SELECT_WASH_MENU_DISPLAY,
    START_MENU_DISPLAY,
    START_WASH_DISPLAY,
    STATISTICS_RESET_DISPLAY,
    WashingMachineState,
    WashingMachineStatistics,
    show_refund_excess_message,
    show_statistics,
    show_washing_job_progress,
)

DEFAULT_WALLET_BALANCE = 0.00

WASHING_TYPES = {
    "Quick Wash": {"time": 10, "price": 2.00},
    "Mild Wash": {"time": 30, "price": 2.5},
    "Medium Wash": {"time": 45, "price": 4.20},
    "Heavy Wash": {"time": 60, "price": 6.00},
}


@dataclass
class WashPrices:
    QUICK = 2.00
    MILD = 2.50
    MEDIUM = 4.20
    HEAVY = 6.00


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


class SelectWashOutcome(Enum):
    BALANCE_MORE_THAN_WASH_PRICE = auto()
    BALANCE_EQUALS_TO_WASH_PRICE = auto()
    BALANCE_LESS_THAN_WASH_PRICE = auto()


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


def get_select_wash_selection() -> SelectWashMenuSelection:
    select_wash_selection = input(PROMPT_INPUT)
    if select_wash_selection == "1":
        return SelectWashMenuSelection.QUICK_WASH
    if select_wash_selection == "2":
        return SelectWashMenuSelection.MILD_WASH
    if select_wash_selection == "3":
        return SelectWashMenuSelection.MEDIUM_WASH
    if select_wash_selection == "4":
        return SelectWashMenuSelection.HEAVY_WASH
    if select_wash_selection == "0":
        return SelectWashMenuSelection.GO_BACK
    raise InvalidMenuSelectionError


def get_select_wash_input() -> SelectWashMenuSelection:
    while True:
        try:
            print(SELECT_WASH_MENU_DISPLAY)
            select_wash_selection = get_select_wash_selection()
            return select_wash_selection
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


def get_select_wash_outcome(balance: float, wash_price: float) -> SelectWashOutcome:
    if balance == wash_price:
        return SelectWashOutcome.BALANCE_EQUALS_TO_WASH_PRICE
    if balance > wash_price:
        return SelectWashOutcome.BALANCE_MORE_THAN_WASH_PRICE
    return SelectWashOutcome.BALANCE_LESS_THAN_WASH_PRICE


def get_wash_price(selected_wash: SelectWashMenuSelection) -> float:
    if selected_wash == SelectWashMenuSelection.QUICK_WASH:
        return WASHING_TYPES["Quick Wash"]["price"]
    if selected_wash == SelectWashMenuSelection.MILD_WASH:
        return WASHING_TYPES["Mild Wash"]["price"]
    if selected_wash == SelectWashMenuSelection.MEDIUM_WASH:
        return WASHING_TYPES["Medium Wash"]["price"]
    return WASHING_TYPES["Heavy Wash"]["price"]


def get_wash_time(selected_wash: SelectWashMenuSelection) -> int:
    if selected_wash == SelectWashMenuSelection.QUICK_WASH:
        return WASHING_TYPES["Quick Wash"]["time"]
    if selected_wash == SelectWashMenuSelection.MILD_WASH:
        return WASHING_TYPES["Mild Wash"]["time"]
    if selected_wash == SelectWashMenuSelection.MEDIUM_WASH:
        return WASHING_TYPES["Medium Wash"]["time"]
    return WASHING_TYPES["Heavy Wash"]["time"]


def get_refund_amount(balance: float, wash_price: float) -> float:
    return balance - wash_price


def handle_maintenance_menu(
    washing_machine_statistics: WashingMachineStatistics,
) -> None:
    while True:
        maintenance_menu_input = get_maintenance_menu_input()
        if maintenance_menu_input == MaintenanceMenuSelection.DISPLAY_STATISTICS:
            show_statistics(washing_machine_statistics)
        if maintenance_menu_input == MaintenanceMenuSelection.RESET_STATISTICS:
            washing_machine_statistics.reset()
            print(STATISTICS_RESET_DISPLAY)
        if maintenance_menu_input == MaintenanceMenuSelection.GO_BACK:
            break


def handle_insert_coins_menu(washing_machine_state: WashingMachineState) -> None:
    while True:
        insert_coin_input = get_insert_coin_input()
        if insert_coin_input == InsertCoinMenuSelection.GO_BACK:
            break
        topup_washing_machine(washing_machine_state, insert_coin_input)
        print(washing_machine_state)


def show_mock_continuous_washing_job_progress(wash_time: int) -> None:
    for i in range(1, wash_time + 1):
        time.sleep(0.1)
        show_washing_job_progress(i / wash_time, wash_time - i)


def handle_select_wash_menu(
    washing_machine_state: WashingMachineState,
    washing_machine_statistics: WashingMachineStatistics,
) -> None:
    while True:
        select_wash_input = get_select_wash_input()
        if select_wash_input == SelectWashMenuSelection.GO_BACK:
            break

        wash_price = get_wash_price(select_wash_input)
        select_wash_outcome = get_select_wash_outcome(
            washing_machine_state.balance, wash_price
        )
        if select_wash_outcome == SelectWashOutcome.BALANCE_LESS_THAN_WASH_PRICE:
            print(INSUFFICIENT_FUNDS_DISPLAY)
        if select_wash_outcome == SelectWashOutcome.BALANCE_MORE_THAN_WASH_PRICE:
            refund_amount = get_refund_amount(washing_machine_state.balance, wash_price)
            show_refund_excess_message(refund_amount)
        if (
            select_wash_outcome == SelectWashOutcome.BALANCE_MORE_THAN_WASH_PRICE
            or select_wash_outcome == SelectWashOutcome.BALANCE_EQUALS_TO_WASH_PRICE
        ):
            washing_machine_state.reset_balance(wash_price)
            wash_time = get_wash_time(select_wash_input)
            washing_machine_statistics.add_money_earned(wash_price)
            washing_machine_statistics.add_total_time_switched_on_minutes(wash_time)
            print(START_WASH_DISPLAY)
            show_mock_continuous_washing_job_progress(wash_time)
            print(END_WASH_DISPLAY)
            break


class State(ABC):
    def handle_input(self, context):
        raise NotImplementedError


class WashingMachine:
    def __init__(
        self,
        state: State,
        statistics: WashingMachineStatistics,
        machine_state: WashingMachineState,
    ):
        self.state = state
        self.washing_machine_statistics = statistics
        self.washing_machine_state = machine_state

    def run(self):
        while self.state is not None:
            self.state.handle_input(self)


class SelectWashMenuState(State):
    def handle_input(self, context: WashingMachine):
        while True:
            select_wash_input = get_select_wash_input()
            if select_wash_input == SelectWashMenuSelection.GO_BACK:
                context.state = UseMachineMenuState()
                break

            wash_price = get_wash_price(select_wash_input)
            select_wash_outcome = get_select_wash_outcome(
                context.washing_machine_state.balance, wash_price
            )
            if select_wash_outcome == SelectWashOutcome.BALANCE_LESS_THAN_WASH_PRICE:
                print(INSUFFICIENT_FUNDS_DISPLAY)
            if select_wash_outcome == SelectWashOutcome.BALANCE_MORE_THAN_WASH_PRICE:
                refund_amount = get_refund_amount(
                    washing_machine_state.balance, wash_price
                )
                show_refund_excess_message(refund_amount)
            if (
                select_wash_outcome == SelectWashOutcome.BALANCE_MORE_THAN_WASH_PRICE
                or select_wash_outcome == SelectWashOutcome.BALANCE_EQUALS_TO_WASH_PRICE
            ):
                washing_machine_state.reset_balance(wash_price)
                wash_time = get_wash_time(select_wash_input)
                washing_machine_statistics.add_money_earned(wash_price)
                washing_machine_statistics.add_total_time_switched_on_minutes(wash_time)
                print(START_WASH_DISPLAY)
                show_mock_continuous_washing_job_progress(wash_time)
                print(END_WASH_DISPLAY)
                context.state = StartMenuState()
                break


class InsertCoinMenuState(State):
    def handle_input(self, context: WashingMachine):
        while True:
            insert_coin_input = get_insert_coin_input()
            if insert_coin_input == InsertCoinMenuSelection.GO_BACK:
                context.state = UseMachineMenuState()
                break

            topup_washing_machine(context.washing_machine_state, insert_coin_input)
            print(washing_machine_state)


class UseMachineMenuState(State):
    def handle_input(self, context: WashingMachine):
        machine_menu_input = get_machine_menu_input()
        if machine_menu_input == MachineMenuSelection.INSERT_COINS:
            handle_insert_coins_menu(washing_machine_state)

        if machine_menu_input == MachineMenuSelection.SELECT_WASH:
            context.state = SelectWashMenuState()

        if machine_menu_input == MachineMenuSelection.GO_BACK:
            context.state = StartMenuState()


class MaintenanceMenuState(State):
    def handle_input(self, context: WashingMachine):
        while True:
            maintenance_menu_input = get_maintenance_menu_input()
            if maintenance_menu_input == MaintenanceMenuSelection.DISPLAY_STATISTICS:
                show_statistics(context.washing_machine_statistics)
            if maintenance_menu_input == MaintenanceMenuSelection.RESET_STATISTICS:
                context.washing_machine_statistics.reset()
                print(STATISTICS_RESET_DISPLAY)
            if maintenance_menu_input == MaintenanceMenuSelection.GO_BACK:
                context.state = StartMenuState()
                break


class StartMenuState(State):
    def handle_input(self, context: WashingMachine):
        start_menu_input = get_start_menu_input()
        if start_menu_input == StartMenuSelection.EXIT:
            print(EXIT_DISPLAY)
            exit()

        if start_menu_input == StartMenuSelection.GO_TO_MANTENANCE_MENU:
            context.state = MaintenanceMenuState()

        if start_menu_input == StartMenuSelection.GO_TO_USE_MACHINE_MENU:
            context.state = UseMachineMenuState()


washing_machine_statistics = WashingMachineStatistics()
washing_machine_state = WashingMachineState()

initial_state = StartMenuState()
washing_machine = WashingMachine(
    initial_state, washing_machine_statistics, washing_machine_state
)
washing_machine.run()
