from dataclasses import dataclass
from typing import Any

from constants import (
    DEFAULT_WASH_DATA,
    INSERT_COIN_OPTIONS_TO_COIN_VALUE_MAPPING,
    USER_INPUT_TO_INSERT_COIN_OPTIONS_MAPPING,
    USER_INPUT_TO_MAINTENANCE_OPTIONS_MAPPING,
    USER_INPUT_TO_SELECT_WASH_OPTIONS_MAPPING,
    USER_INPUT_TO_START_OPTIONS_MAPPING,
    USER_INPUT_TO_WASH_SETTINGS_OPTIONS_MAPPING,
    WashingTypeData,
)
from display import (
    END_WASH_DISPLAY,
    EXIT_DISPLAY,
    INSUFFICIENT_FUNDS_DISPLAY,
    INVALID_SELECTION_DISPLAY,
    MENU_INSERT_COIN_DISPLAY,
    MENU_MAINTENANCE_DISPLAY,
    MENU_START_DISPLAY,
    MENU_WASH_SETTINGS_DISPLAY,
    PROMPT_INPUT,
    START_WASH_DISPLAY,
    TOPUP_SUCCESS_DISPLAY,
    get_menu_select_wash_display,
)
from enums import (
    InsertCoinOptions,
    MaintenanceOptions,
    SelectWashOptions,
    SelectWashOutcome,
    StartMenuOptions,
    WashSettingsOptions,
)
from exceptions import InvalidCoinValueError, InvalidMenuSelectionError
from state import WashingMachineBalance, WashingMachineStatistics, WashSettingsMenuState
from utils import simulate_washing_progress


@dataclass
class WashingMachine:
    statistics: WashingMachineStatistics
    balance: WashingMachineBalance

    controller = None
    is_door_locked: bool = False

    def run(self) -> None:
        while self.controller is not None:
            self.controller.run()

    def change_controller(self, new_controller) -> None:
        self.controller = new_controller

    def change_door_locked_status(self, new_door_locked_status: bool) -> None:
        self.is_door_locked = new_door_locked_status


@dataclass
class InsertCoinMenuModel:
    state: WashingMachine

    input_mapping = USER_INPUT_TO_INSERT_COIN_OPTIONS_MAPPING
    coin_value_mapping = INSERT_COIN_OPTIONS_TO_COIN_VALUE_MAPPING

    def topup_washing_machine(self, topup_amount: float) -> None:
        self.state.balance.topup_balance(topup_amount)

    def change_machine_state(self, new_state):
        self.state.change_controller(new_state)

    def parse_user_input(self, user_input: str) -> InsertCoinOptions:
        if selected_option := self.input_mapping.get(user_input):
            return selected_option
        raise InvalidMenuSelectionError

    def get_coin_value(self, insert_coin_option: InsertCoinOptions) -> float:
        if coin_value := self.coin_value_mapping.get(insert_coin_option):
            return coin_value
        raise InvalidCoinValueError


@dataclass
class InsertCoinMenuView:
    state: WashingMachine
    menu = MENU_INSERT_COIN_DISPLAY
    topup_success = TOPUP_SUCCESS_DISPLAY
    invalid_selection = INVALID_SELECTION_DISPLAY
    prompt_input = PROMPT_INPUT

    def __post_init__(self):
        self.balance = self.state.balance


@dataclass
class InsertCoinMenuController:
    state: WashingMachine

    def __post_init__(self):
        self.model = InsertCoinMenuModel(state=self.state)
        self.view = InsertCoinMenuView(self.state)

    def run(self):
        self.handle_user_input()

    def handle_user_input(self):
        while True:
            print(self.view.menu)
            user_input = input(self.view.prompt_input)
            parsed_user_input = self.model.parse_user_input(user_input)

            if parsed_user_input == InsertCoinOptions.GO_BACK:
                self.model.change_machine_state(WashSettingsMenuController(self.state))
                break

            topup_value = self.model.get_coin_value(parsed_user_input)
            self.model.topup_washing_machine(topup_value)

            print(self.view.topup_success)
            print(self.view.balance)


@dataclass
class StartMenuModel:
    state: WashingMachine

    input_mapping = USER_INPUT_TO_START_OPTIONS_MAPPING

    def change_machine_state(self, new_state):
        self.state.change_controller(new_state)

    def parse_user_input(self, user_input: str) -> StartMenuOptions:
        if selected_option := self.input_mapping.get(user_input):
            return selected_option
        raise InvalidMenuSelectionError


@dataclass
class StartMenuView:
    menu = MENU_START_DISPLAY
    invalid_selection = INVALID_SELECTION_DISPLAY
    prompt_input = PROMPT_INPUT
    exit = EXIT_DISPLAY


@dataclass
class StartMenuController:
    state: WashingMachine
    view = StartMenuView()

    def __post_init__(self):
        self.model = StartMenuModel(state=self.state)

    def run(self):
        self.handle_user_input()

    def handle_user_input(self):
        while True:
            print(self.view.menu)
            user_input = input(self.view.prompt_input)
            parsed_user_input = self.model.parse_user_input(user_input)

            if parsed_user_input == StartMenuOptions.EXIT:
                print(self.view.exit)
                exit()

            if parsed_user_input == StartMenuOptions.MANTENANCE:
                self.state.change_controller(MaintenanceMenuController(self.state))

            if parsed_user_input == StartMenuOptions.WASH_SETTINGS:
                self.state.change_controller(WashSettingsMenuController(self.state))
                break


@dataclass
class MaintenanceMenuModel:
    state: WashingMachine
    input_mapping = USER_INPUT_TO_MAINTENANCE_OPTIONS_MAPPING

    def change_machine_state(self, new_state):
        self.state.change_controller(new_state)

    def parse_user_input(self, user_input: str) -> MaintenanceOptions:
        if selected_option := self.input_mapping.get(user_input):
            return selected_option
        raise InvalidMenuSelectionError

    def reset_statistics(self):
        self.state.statistics.reset()


@dataclass
class MaintenanceMenuView:
    state: WashingMachine

    menu = MENU_MAINTENANCE_DISPLAY
    invalid_selection = INVALID_SELECTION_DISPLAY
    prompt_input = PROMPT_INPUT
    statistics = None

    def __post_init__(self):
        self.statistics = self.state.statistics


@dataclass
class MaintenanceMenuController:
    state: WashingMachine

    def __post_init__(self):
        self.model = MaintenanceMenuModel(state=self.state)
        self.view = MaintenanceMenuView(state=self.state)

    def run(self):
        self.handle_user_input()

    def handle_user_input(self):
        while True:
            print(self.view.menu)
            user_input = input(self.view.prompt_input)
            parsed_user_input = self.model.parse_user_input(user_input)

            if parsed_user_input == MaintenanceOptions.GO_BACK:
                self.state.change_controller(StartMenuController(self.state))
                break

            if parsed_user_input == MaintenanceOptions.DISPLAY_STATISTICS:
                print(self.view.statistics)

            if parsed_user_input == MaintenanceOptions.RESET_STATISTICS:
                self.model.reset_statistics()


@dataclass
class WashSettingsMenuModel:
    state: WashingMachine
    input_mapping = USER_INPUT_TO_WASH_SETTINGS_OPTIONS_MAPPING

    def change_machine_controller(self, new_controller):
        self.state.change_controller(new_controller)

    def parse_user_input(self, user_input: str) -> WashSettingsOptions:
        if selected_option := self.input_mapping.get(user_input):
            return selected_option
        raise InvalidMenuSelectionError


@dataclass
class WashSettingsMenuView:
    menu = MENU_WASH_SETTINGS_DISPLAY
    invalid_selection = INVALID_SELECTION_DISPLAY
    prompt_input = PROMPT_INPUT


@dataclass
class WashSettingsMenuController:
    state: WashingMachine
    view = WashSettingsMenuView()

    def __post_init__(self):
        self.model = MaintenanceMenuModel(state=self.state)

    def run(self):
        self.handle_user_input()

    def handle_user_input(self):
        while True:
            print(self.view.menu)
            user_input = input(self.view.prompt_input)
            parsed_user_input = self.model.parse_user_input(user_input)

            if parsed_user_input == WashSettingsOptions.INSERT_COINS:
                self.model.change_machine_state(InsertCoinMenuController(self.state))

            # if parsed_user_input == WashSettingsOptions.SELECT_WASH:
            #     washing_machine.change_state(SelectWashMenuState())

            if parsed_user_input == WashSettingsOptions.GO_BACK:
                self.model.change_machine_state(StartMenuController(self.state))


@dataclass
class SelectWashMenuModel:
    state: WashingMachine
    input_mapping = USER_INPUT_TO_SELECT_WASH_OPTIONS_MAPPING
    wash_data = DEFAULT_WASH_DATA

    def change_machine_controller(self, new_controller):
        self.state.change_controller(new_controller)

    def parse_user_input(self, user_input: str) -> SelectWashOptions:
        if selected_option := self.input_mapping.get(user_input):
            return selected_option
        raise InvalidMenuSelectionError

    def get_wash_data(self, selected_wash: SelectWashOptions) -> WashingTypeData:
        if selected_wash == SelectWashOptions.QUICK_WASH:
            return self.wash_data.QUICK_WASH
        if selected_wash == SelectWashOptions.MILD_WASH:
            return self.wash_data.MILD_WASH
        if selected_wash == SelectWashOptions.MEDIUM_WASH:
            return self.wash_data.MEDIUM_WASH
        return self.wash_data.HEAVY_WASH

    def get_wash_outcome(self, balance: float, wash_price: float) -> SelectWashOutcome:
        if balance == wash_price:
            return SelectWashOutcome.BALANCE_EQUALS_TO_WASH_PRICE
        if balance > wash_price:
            return SelectWashOutcome.BALANCE_MORE_THAN_WASH_PRICE
        return SelectWashOutcome.BALANCE_LESS_THAN_WASH_PRICE

    def get_refund_amount(self, balance: float, wash_price: float) -> float:
        return balance - wash_price

    def reduce_washing_machine_balance(self, wash_price: float) -> None:
        self.state.balance.reduce_balance(wash_price)

    def increase_washing_machine_money_earned(
        self, additional_money_earned: float
    ) -> None:
        self.state.statistics.add_money_earned(additional_money_earned)

    def add_washing_machine_total_time_switched_on_minutes(
        self, additional_time_switched_on: int
    ) -> None:
        self.state.statistics.add_total_time_switched_on_minutes(
            additional_time_switched_on
        )

    def change_washing_machine_door_lock_status(self, new_status: bool) -> None:
        self.state.change_door_locked_status(new_status)


@dataclass
class SelectWashMenuView:
    state: WashingMachine
    invalid_selection = INVALID_SELECTION_DISPLAY
    prompt_input = PROMPT_INPUT
    insufficient_funds = INSUFFICIENT_FUNDS_DISPLAY
    start_wash = START_WASH_DISPLAY
    end_wash = END_WASH_DISPLAY
    menu = None

    def __post_init__(self):
        self.menu = get_menu_select_wash_display(self.state.balance.balance)

    def get_refund_amount_display(self, refund_amount: float) -> str:
        return f"""
========Calculating change===========
Clonk clonk. ${refund_amount} refunded"""


# def handle_input(self, washing_machine: WashingMachineInterface):
#     while True:

#         selected_wash_input = get_user_menu_input(
#             get_menu_select_wash_display(washing_machine.balance.balance),
#             USER_INPUT_TO_SELECT_WASH_OPTIONS_MAPPING,
#         )
#         if selected_wash_input == SelectWashOptions.GO_BACK:
#             washing_machine.change_state(WashSettingsMenuState())
#             break

#         wash_price = get_wash_price(selected_wash_input)
#         wash_time = get_wash_time(selected_wash_input)
#         select_wash_outcome = get_select_wash_outcome(
#             washing_machine.balance.balance, wash_price
#         )
#         if select_wash_outcome == SelectWashOutcome.BALANCE_LESS_THAN_WASH_PRICE:
#             print(INSUFFICIENT_FUNDS_DISPLAY)
#             return

#         self._handle_payment(washing_machine, select_wash_outcome, wash_price)
#         self._handle_wash_clothes(washing_machine, wash_time)
#         washing_machine.change_state(StartMenuState())
#         break

# def _handle_payment(
#     self,
#     washing_machine: WashingMachineInterface,
#     outcome: SelectWashOutcome,
#     wash_price: float,
# ):
#     if outcome == SelectWashOutcome.BALANCE_MORE_THAN_WASH_PRICE:
#         refund_amount = get_refund_amount(
#             washing_machine.balance.balance, wash_price
#         )
#         refund_amount_display = get_refund_excess_display(refund_amount)
#         print(refund_amount_display)

#     washing_machine.balance.reset_balance(wash_price)
#     washing_machine.statistics.add_money_earned(wash_price)

# def _handle_wash_clothes(
#     self,
#     washing_machine: WashingMachineInterface,
#     wash_time: int,
# ):
#     washing_machine.statistics.add_total_time_switched_on_minutes(wash_time)

#     washing_machine.change_door_locked_status(True)
#     print(START_WASH_DISPLAY)
#     simulate_washing_progress(wash_time)
#     washing_machine.change_door_locked_status(False)
#     print(END_WASH_DISPLAY)


@dataclass
class SelectWashMenuController:
    state: WashingMachine

    def __post_init__(self):
        self.model = SelectWashMenuModel(state=self.state)
        self.view = SelectWashMenuView(state=self.state)

    def run(self):
        self.handle_user_input()

    def handle_user_input(self):
        while True:
            print(self.view.menu)
            user_input = input(self.view.prompt_input)
            parsed_user_input = self.model.parse_user_input(user_input)

            wash_data = self.model.get_wash_data(parsed_user_input)
            wash_outcome = self.model.get_wash_outcome(
                self.state.balance.balance, wash_data.price
            )
            if wash_outcome == SelectWashOutcome.BALANCE_LESS_THAN_WASH_PRICE:
                print(self.view.insufficient_funds)
                return

            if wash_outcome == SelectWashOutcome.BALANCE_MORE_THAN_WASH_PRICE:
                refund_amount = self.model.get_refund_amount(
                    self.state.balance.balance, wash_data.price
                )
                print(self.view.get_refund_amount_display(refund_amount))
            self.model.reduce_washing_machine_balance(wash_data.price)
            self.model.increase_washing_machine_money_earned(wash_data.price)
            self.model.add_washing_machine_total_time_switched_on_minutes(
                wash_data.time
            )
            print(self.view.start_wash)
            self.model.change_washing_machine_door_lock_status(True)
            simulate_washing_progress(wash_data.time)  # To put this in class
            self.model.change_washing_machine_door_lock_status(False)
            print(self.view.end_wash)
            self.model.change_machine_controller(StartMenuController(self.state))


washing_machine = WashingMachine(WashingMachineStatistics(), WashingMachineBalance())
controller = StartMenuController(washing_machine)
washing_machine.change_controller(controller)
washing_machine.run()
