import time
from abc import ABC
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


class InvalidMenuSelectionError(Exception):
    pass


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


def get_start_menu_options(user_selection: str) -> StartMenuOptions:
    if user_selection == "1":
        return StartMenuOptions.WASH_SETTINGS
    if user_selection == "2":
        return StartMenuOptions.MANTENANCE
    if user_selection == "3":
        return StartMenuOptions.EXIT
    raise InvalidMenuSelectionError


def get_start_menu_input() -> StartMenuOptions:
    while True:
        try:
            print(START_MENU_DISPLAY)
            user_input = input(PROMPT_INPUT)
            start_menu_selection = get_start_menu_options(user_input)
            return start_menu_selection
        except InvalidMenuSelectionError:
            print(INVALID_SELECTION_DISPLAY)


def get_maintenance_menu_options(user_selection: str) -> MaintenanceOptions:
    if user_selection == "1":
        return MaintenanceOptions.DISPLAY_STATISTICS
    if user_selection == "2":
        return MaintenanceOptions.RESET_STATISTICS
    if user_selection == "0":
        return MaintenanceOptions.GO_BACK
    raise InvalidMenuSelectionError


def get_maintenance_menu_input() -> MaintenanceOptions:
    while True:
        try:
            print(MAINTENANCE_MENU)
            user_selection = input(PROMPT_INPUT)
            maintenance_menu_selection = get_maintenance_menu_options(user_selection)
            return maintenance_menu_selection
        except InvalidMenuSelectionError:
            print(INVALID_SELECTION_DISPLAY)


def get_wash_settings_options(user_selection: str) -> WashSettingsOptions:
    if user_selection == "1":
        return WashSettingsOptions.INSERT_COINS
    if user_selection == "2":
        return WashSettingsOptions.SELECT_WASH
    if user_selection == "3":
        return WashSettingsOptions.GO_BACK
    raise InvalidMenuSelectionError


def get_wash_settings_input() -> WashSettingsOptions:
    while True:
        try:
            print(MACHINE_MENU_DISPLAY)
            user_selection = input(PROMPT_INPUT)
            machine_menu_selection = get_wash_settings_options(user_selection)
            return machine_menu_selection
        except InvalidMenuSelectionError:
            print(INVALID_SELECTION_DISPLAY)


def get_insert_coin_options(user_selection: str) -> InsertCoinOptions:
    if user_selection == "1":
        return InsertCoinOptions.INSERT_TEN_CENTS
    if user_selection == "2":
        return InsertCoinOptions.INSERT_TWENTY_CENTS
    if user_selection == "3":
        return InsertCoinOptions.INSERT_FIFTY_CENTS
    if user_selection == "4":
        return InsertCoinOptions.INSERT_ONE_DOLLAR
    if user_selection == "0":
        return InsertCoinOptions.GO_BACK
    raise InvalidMenuSelectionError


def get_insert_coin_input() -> InsertCoinOptions:
    while True:
        try:
            print(INSERT_COIN_MENU_DISPLAY)
            user_selection = input(PROMPT_INPUT)
            insert_coin_selection = get_insert_coin_options(user_selection)
            return insert_coin_selection
        except InvalidMenuSelectionError:
            print(INVALID_SELECTION_DISPLAY)


def get_select_wash_options(user_selection: str) -> SelectWashOptions:
    if user_selection == "1":
        return SelectWashOptions.QUICK_WASH
    if user_selection == "2":
        return SelectWashOptions.MILD_WASH
    if user_selection == "3":
        return SelectWashOptions.MEDIUM_WASH
    if user_selection == "4":
        return SelectWashOptions.HEAVY_WASH
    if user_selection == "0":
        return SelectWashOptions.GO_BACK
    raise InvalidMenuSelectionError


def get_select_wash_input() -> SelectWashOptions:
    while True:
        try:
            print(SELECT_WASH_MENU_DISPLAY)
            user_selection = input(PROMPT_INPUT)
            select_wash_selection = get_select_wash_options(user_selection)
            return select_wash_selection
        except InvalidMenuSelectionError:
            print(INVALID_SELECTION_DISPLAY)


def topup_washing_machine(
    washing_machine_state: WashingMachineState,
    insert_coin_input: InsertCoinOptions,
) -> None:
    if insert_coin_input == InsertCoinOptions.INSERT_TEN_CENTS:
        return washing_machine_state.topup_balance(0.1)
    if insert_coin_input == InsertCoinOptions.INSERT_TWENTY_CENTS:
        return washing_machine_state.topup_balance(0.2)
    if insert_coin_input == InsertCoinOptions.INSERT_FIFTY_CENTS:
        return washing_machine_state.topup_balance(0.5)
    if insert_coin_input == InsertCoinOptions.INSERT_ONE_DOLLAR:
        return washing_machine_state.topup_balance(1.0)


def get_select_wash_outcome(balance: float, wash_price: float) -> SelectWashOutcome:
    if balance == wash_price:
        return SelectWashOutcome.BALANCE_EQUALS_TO_WASH_PRICE
    if balance > wash_price:
        return SelectWashOutcome.BALANCE_MORE_THAN_WASH_PRICE
    return SelectWashOutcome.BALANCE_LESS_THAN_WASH_PRICE


def get_wash_price(selected_wash: SelectWashOptions) -> float:
    if selected_wash == SelectWashOptions.QUICK_WASH:
        return WASHING_TYPES["Quick Wash"]["price"]
    if selected_wash == SelectWashOptions.MILD_WASH:
        return WASHING_TYPES["Mild Wash"]["price"]
    if selected_wash == SelectWashOptions.MEDIUM_WASH:
        return WASHING_TYPES["Medium Wash"]["price"]
    return WASHING_TYPES["Heavy Wash"]["price"]


def get_wash_time(selected_wash: SelectWashOptions) -> int:
    if selected_wash == SelectWashOptions.QUICK_WASH:
        return WASHING_TYPES["Quick Wash"]["time"]
    if selected_wash == SelectWashOptions.MILD_WASH:
        return WASHING_TYPES["Mild Wash"]["time"]
    if selected_wash == SelectWashOptions.MEDIUM_WASH:
        return WASHING_TYPES["Medium Wash"]["time"]
    return WASHING_TYPES["Heavy Wash"]["time"]


def get_refund_amount(balance: float, wash_price: float) -> float:
    return balance - wash_price


def show_mock_continuous_washing_job_progress(wash_time: int) -> None:
    for i in range(1, wash_time + 1):
        time.sleep(0.1)
        show_washing_job_progress(i / wash_time, wash_time - i)


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
            if select_wash_input == SelectWashOptions.GO_BACK:
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
            if insert_coin_input == InsertCoinOptions.GO_BACK:
                context.state = UseMachineMenuState()
                break

            topup_washing_machine(context.washing_machine_state, insert_coin_input)
            print(washing_machine_state)


class UseMachineMenuState(State):
    def handle_input(self, context: WashingMachine):
        machine_menu_input = get_wash_settings_input()
        if machine_menu_input == WashSettingsOptions.INSERT_COINS:
            context.state = InsertCoinMenuState()

        if machine_menu_input == WashSettingsOptions.SELECT_WASH:
            context.state = SelectWashMenuState()

        if machine_menu_input == WashSettingsOptions.GO_BACK:
            context.state = StartMenuState()


class MaintenanceMenuState(State):
    def handle_input(self, context: WashingMachine):
        while True:
            maintenance_menu_input = get_maintenance_menu_input()
            if maintenance_menu_input == MaintenanceOptions.DISPLAY_STATISTICS:
                show_statistics(context.washing_machine_statistics)
            if maintenance_menu_input == MaintenanceOptions.RESET_STATISTICS:
                context.washing_machine_statistics.reset()
                print(STATISTICS_RESET_DISPLAY)
            if maintenance_menu_input == MaintenanceOptions.GO_BACK:
                context.state = StartMenuState()
                break


class StartMenuState(State):
    def handle_input(self, context: WashingMachine):
        start_menu_input = get_start_menu_input()
        if start_menu_input == StartMenuOptions.EXIT:
            print(EXIT_DISPLAY)
            exit()

        if start_menu_input == StartMenuOptions.MANTENANCE:
            context.state = MaintenanceMenuState()

        if start_menu_input == StartMenuOptions.WASH_SETTINGS:
            context.state = UseMachineMenuState()


washing_machine_statistics = WashingMachineStatistics()
washing_machine_state = WashingMachineState()

initial_state = StartMenuState()
washing_machine = WashingMachine(
    initial_state, washing_machine_statistics, washing_machine_state
)
washing_machine.run()
