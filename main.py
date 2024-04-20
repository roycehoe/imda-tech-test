import time
from abc import ABC
from dataclasses import dataclass
from typing import Final

from constants import (
    DEFAULT_WASHING_TYPES,
    INSERT_COIN_OPTIONS_TO_COIN_VALUE_MAPPING,
    USER_INPUT_TO_INSERT_COIN_OPTIONS_MAPPING,
    USER_INPUT_TO_SELECT_WASH_OPTIONS_MAPPING,
    USER_INPUT_TO_START_OPTIONS_MAPPING,
    USER_INPUT_TO_WASH_SETTINGS_OPTIONS_MAPPING,
)
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
    WashingMachineBalance,
    WashingMachineStatistics,
    show_refund_excess_message,
    show_statistics,
    show_washing_job_progress,
)
from enums import (
    InsertCoinOptions,
    MaintenanceOptions,
    SelectWashOptions,
    SelectWashOutcome,
    StartMenuOptions,
    WashSettingsOptions,
)


class InvalidMenuSelectionError(Exception):
    pass


class InvalidCoinValueError(Exception):
    pass


def get_start_menu_options(
    user_selection: str,
    user_input_mapping: dict[
        str, StartMenuOptions
    ] = USER_INPUT_TO_START_OPTIONS_MAPPING,
) -> StartMenuOptions:
    if user_selected_option := user_input_mapping.get(user_selection):
        return user_selected_option
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


def get_maintenance_menu_options(
    user_selection: str, user_input_mapping=USER_INPUT_TO_MAINTENANCE_OPTIONS_MAPPING
) -> MaintenanceOptions:
    if user_selected_option := user_input_mapping.get(user_selection):
        return user_selected_option
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


def get_wash_settings_options(
    user_selection: str, user_input_mapping=USER_INPUT_TO_WASH_SETTINGS_OPTIONS_MAPPING
) -> WashSettingsOptions:
    if user_selected_option := user_input_mapping.get(user_selection):
        return user_selected_option
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


def get_insert_coin_options(
    user_selection: str, user_input_mapping=USER_INPUT_TO_INSERT_COIN_OPTIONS_MAPPING
) -> InsertCoinOptions:
    if user_selected_option := user_input_mapping.get(user_selection):
        return user_selected_option
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


def get_select_wash_options(
    user_selection: str, user_input_mapping=USER_INPUT_TO_SELECT_WASH_OPTIONS_MAPPING
) -> SelectWashOptions:
    if user_selected_option := user_input_mapping.get(user_selection):
        return user_selected_option
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
    washing_machine_state: WashingMachineBalance,
    insert_coin_input: InsertCoinOptions,
    coin_value_mapping=INSERT_COIN_OPTIONS_TO_COIN_VALUE_MAPPING,
) -> None:
    if coin_value := coin_value_mapping.get(insert_coin_input):
        return washing_machine_state.topup_balance(coin_value)
    raise InvalidCoinValueError


def get_select_wash_outcome(balance: float, wash_price: float) -> SelectWashOutcome:
    if balance == wash_price:
        return SelectWashOutcome.BALANCE_EQUALS_TO_WASH_PRICE
    if balance > wash_price:
        return SelectWashOutcome.BALANCE_MORE_THAN_WASH_PRICE
    return SelectWashOutcome.BALANCE_LESS_THAN_WASH_PRICE


def get_wash_price(selected_wash: SelectWashOptions) -> float:
    if selected_wash == SelectWashOptions.QUICK_WASH:
        return DEFAULT_WASHING_TYPES.QUICK_WASH.price
    if selected_wash == SelectWashOptions.MILD_WASH:
        return DEFAULT_WASHING_TYPES.MILD_WASH.price
    if selected_wash == SelectWashOptions.MEDIUM_WASH:
        return DEFAULT_WASHING_TYPES.MEDIUM_WASH.price
    return DEFAULT_WASHING_TYPES.HEAVY_WASH.price


def get_wash_time(selected_wash: SelectWashOptions) -> int:
    if selected_wash == SelectWashOptions.QUICK_WASH:
        return DEFAULT_WASHING_TYPES.QUICK_WASH.time
    if selected_wash == SelectWashOptions.MILD_WASH:
        return DEFAULT_WASHING_TYPES.MILD_WASH.time
    if selected_wash == SelectWashOptions.MEDIUM_WASH:
        return DEFAULT_WASHING_TYPES.MEDIUM_WASH.time
    return DEFAULT_WASHING_TYPES.HEAVY_WASH.time


def get_refund_amount(balance: float, wash_price: float) -> float:
    return balance - wash_price


def show_mock_continuous_washing_job_progress(wash_time: int) -> None:
    for time_left in range(1, wash_time + 1):
        time.sleep(0.1)
        show_washing_job_progress(time_left / wash_time, wash_time - time_left)


class State(ABC):
    def handle_input(self, context):
        raise NotImplementedError


class WashingMachine:
    def __init__(
        self,
        state: State,
        statistics: WashingMachineStatistics,
        balance: WashingMachineBalance,
    ):

        self.state = state
        self.statistics = statistics
        self.balance = balance

    def run(self) -> None:
        while self.state is not None:
            self.state.handle_input(self)

    def change_state(self, new_state: State) -> None:
        self.state = new_state


class SelectWashMenuState(State):
    def handle_input(self, washing_machine: WashingMachine):
        while True:
            selected_wash_input = get_select_wash_input()
            if selected_wash_input == SelectWashOptions.GO_BACK:
                washing_machine.change_state(WashSettingsMenuState())
                break

            wash_price = get_wash_price(selected_wash_input)
            wash_time = get_wash_time(selected_wash_input)
            select_wash_outcome = get_select_wash_outcome(
                washing_machine.balance.balance, wash_price
            )
            if select_wash_outcome == SelectWashOutcome.BALANCE_LESS_THAN_WASH_PRICE:
                print(INSUFFICIENT_FUNDS_DISPLAY)
                return

            self._handle_payment(washing_machine, select_wash_outcome, wash_price)
            self._handle_wash_clothes(washing_machine, wash_time)

    def _handle_payment(
        self,
        washing_machine: WashingMachine,
        outcome: SelectWashOutcome,
        wash_price: float,
    ):
        if outcome == SelectWashOutcome.BALANCE_MORE_THAN_WASH_PRICE:
            refund_amount = get_refund_amount(
                washing_machine.balance.balance, wash_price
            )
            show_refund_excess_message(refund_amount)

        washing_machine.balance.reset_balance(wash_price)
        washing_machine.statistics.add_money_earned(wash_price)

    def _handle_wash_clothes(
        self,
        washing_machine: WashingMachine,
        wash_time: int,
    ):
        washing_machine.statistics.add_total_time_switched_on_minutes(wash_time)

        print(START_WASH_DISPLAY)
        show_mock_continuous_washing_job_progress(wash_time)
        print(END_WASH_DISPLAY)

        washing_machine.change_state(StartMenuState())


class InsertCoinMenuState(State):
    def handle_input(self, washing_machine: WashingMachine):
        while True:
            insert_coin_input = get_insert_coin_input()
            if insert_coin_input == InsertCoinOptions.GO_BACK:
                washing_machine.change_state(WashSettingsMenuState())
                break

            topup_washing_machine(washing_machine.balance, insert_coin_input)
            print(washing_machine.balance)


class WashSettingsMenuState(State):
    def handle_input(self, washing_machine: WashingMachine):
        machine_menu_input = get_wash_settings_input()
        if machine_menu_input == WashSettingsOptions.INSERT_COINS:
            washing_machine.change_state(InsertCoinMenuState())

        if machine_menu_input == WashSettingsOptions.SELECT_WASH:
            washing_machine.change_state(SelectWashMenuState())

        if machine_menu_input == WashSettingsOptions.GO_BACK:
            washing_machine.change_state(StartMenuState())


class MaintenanceMenuState(State):
    def handle_input(self, washing_machine: WashingMachine):
        while True:
            maintenance_menu_input = get_maintenance_menu_input()
            if maintenance_menu_input == MaintenanceOptions.DISPLAY_STATISTICS:
                show_statistics(washing_machine.statistics)
            if maintenance_menu_input == MaintenanceOptions.RESET_STATISTICS:
                washing_machine.statistics.reset()
                print(STATISTICS_RESET_DISPLAY)
            if maintenance_menu_input == MaintenanceOptions.GO_BACK:
                washing_machine.change_state(StartMenuState())
                break


class StartMenuState(State):
    def handle_input(self, washing_machine: WashingMachine):
        start_menu_input = get_start_menu_input()
        if start_menu_input == StartMenuOptions.EXIT:
            print(EXIT_DISPLAY)
            exit()

        if start_menu_input == StartMenuOptions.MANTENANCE:
            washing_machine.change_state(MaintenanceMenuState())

        if start_menu_input == StartMenuOptions.WASH_SETTINGS:
            washing_machine.change_state(WashSettingsMenuState())


washing_machine = WashingMachine(
    StartMenuState(), WashingMachineStatistics(), WashingMachineBalance()
)
washing_machine.run()
