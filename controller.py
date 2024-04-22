from dataclasses import dataclass

from constants import (
    DEFAULT_MONEY_EARNED,
    DEFAULT_TOTAL_TIME_SWITCHED_ON_MINUTES,
    DEFAULT_WASH_DATA,
    INSERT_COIN_OPTIONS_TO_COIN_VALUE_MAPPING,
    USER_INPUT_TO_INSERT_COIN_OPTIONS_MAPPING,
    USER_INPUT_TO_MAINTENANCE_OPTIONS_MAPPING,
    USER_INPUT_TO_SELECT_WASH_OPTIONS_MAPPING,
    USER_INPUT_TO_START_OPTIONS_MAPPING,
    USER_INPUT_TO_WASH_SETTINGS_OPTIONS_MAPPING,
    WashingTypeData,
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
from models import (
    WashingMachineBalanceInterface,
    WashingMachineController,
    WashingMachineInterface,
    WashingMachineStatisticsInterface,
)
from utils import get_refund_amount, get_wash_outcome, simulate_washing_progress
from view import (
    InsertCoinMenuView,
    MaintenanceMenuView,
    SelectWashMenuView,
    StartMenuView,
    WashSettingsMenuView,
)


@dataclass
class WashingMachineBalance(WashingMachineBalanceInterface):
    balance: float = 0.00

    def topup_balance(self, money: float):
        self.balance += money

    def reduce_balance(self, money: float):
        self.balance -= money

    def __str__(self):
        return f"""-------------------------------------
Current balance: ${self.balance:.2f}
-------------------------------------"""


@dataclass
class WashingMachineStatistics(WashingMachineStatisticsInterface):
    total_time_switched_on_minutes: int = DEFAULT_TOTAL_TIME_SWITCHED_ON_MINUTES
    money_earned: float = DEFAULT_MONEY_EARNED

    def reset(self):
        self.total_time_switched_on_minutes = DEFAULT_TOTAL_TIME_SWITCHED_ON_MINUTES
        self.money_earned = DEFAULT_MONEY_EARNED

    def add_total_time_switched_on_minutes(self, additional_time: int):
        self.total_time_switched_on_minutes += additional_time

    def add_money_earned(self, additional_money_earned: float):
        self.money_earned += additional_money_earned

    def __str__(self):
        return f"""
========Getting Statistics===========

------------------------------------------------------------------------
Total time switched on: {self.total_time_switched_on_minutes} minutes 
Balance: ${self.money_earned:.2f}
------------------------------------------------------------------------"""


@dataclass
class WashingMachine(WashingMachineInterface):
    statistics: WashingMachineStatistics
    balance: WashingMachineBalance

    controller: WashingMachineController = None
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
    state: WashingMachineInterface

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
class InsertCoinMenuController(WashingMachineController):
    state: WashingMachineInterface

    def __post_init__(self):
        self.model = InsertCoinMenuModel(state=self.state)
        self.view = InsertCoinMenuView(self.state)

    def run(self):
        self.handle_user_input()

    def handle_user_input(self):
        while True:
            try:
                print(self.view.menu)
                user_input = input(self.view.prompt_input)
                parsed_user_input = self.model.parse_user_input(user_input)

                if parsed_user_input == InsertCoinOptions.GO_BACK:
                    self.model.change_machine_state(
                        WashSettingsMenuController(self.state)
                    )
                    break

                topup_value = self.model.get_coin_value(parsed_user_input)
                self.model.topup_washing_machine(topup_value)

                print(self.view.topup_success)
                print(self.view.balance)
            except InvalidMenuSelectionError:
                print(self.view.invalid_selection)


@dataclass
class StartMenuModel:
    state: WashingMachineInterface

    input_mapping = USER_INPUT_TO_START_OPTIONS_MAPPING

    def change_machine_state(self, new_state):
        self.state.change_controller(new_state)

    def parse_user_input(self, user_input: str) -> StartMenuOptions:
        if selected_option := self.input_mapping.get(user_input):
            return selected_option
        raise InvalidMenuSelectionError


@dataclass
class StartMenuController(WashingMachineController):
    state: WashingMachineInterface
    view = StartMenuView()

    def __post_init__(self):
        self.model = StartMenuModel(state=self.state)

    def run(self):
        self.handle_user_input()

    def handle_user_input(self):
        while True:
            try:
                print(self.view.menu)
                user_input = input(self.view.prompt_input)
                parsed_user_input = self.model.parse_user_input(user_input)

                if parsed_user_input == StartMenuOptions.EXIT:
                    print(self.view.exit)
                    exit()

                if parsed_user_input == StartMenuOptions.MANTENANCE:
                    self.state.change_controller(MaintenanceMenuController(self.state))
                    break

                if parsed_user_input == StartMenuOptions.WASH_SETTINGS:
                    self.state.change_controller(WashSettingsMenuController(self.state))
                    break
            except InvalidMenuSelectionError:
                print(self.view.invalid_selection)


@dataclass
class MaintenanceMenuModel:
    state: WashingMachineInterface
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
class MaintenanceMenuController(WashingMachineController):
    state: WashingMachineInterface

    def __post_init__(self):
        self.model = MaintenanceMenuModel(state=self.state)
        self.view = MaintenanceMenuView(state=self.state)

    def run(self):
        self.handle_user_input()

    def handle_user_input(self):
        while True:
            try:
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
                    print(self.view.statistics_reset_success)
            except InvalidMenuSelectionError:
                print(self.view.invalid_selection)


@dataclass
class WashSettingsMenuModel:
    state: WashingMachineInterface
    input_mapping = USER_INPUT_TO_WASH_SETTINGS_OPTIONS_MAPPING

    def change_machine_state(self, new_controller):
        self.state.change_controller(new_controller)

    def parse_user_input(self, user_input: str) -> WashSettingsOptions:
        if selected_option := self.input_mapping.get(user_input):
            return selected_option
        raise InvalidMenuSelectionError


@dataclass
class WashSettingsMenuController(WashingMachineController):
    state: WashingMachineInterface
    view = WashSettingsMenuView()

    def __post_init__(self):
        self.model = WashSettingsMenuModel(state=self.state)

    def run(self):
        self.handle_user_input()

    def handle_user_input(self):
        while True:
            try:
                print(self.view.menu)
                user_input = input(self.view.prompt_input)
                parsed_user_input = self.model.parse_user_input(user_input)

                if parsed_user_input == WashSettingsOptions.INSERT_COINS:
                    self.state.change_controller(InsertCoinMenuController(self.state))
                    break

                if parsed_user_input == WashSettingsOptions.SELECT_WASH:
                    self.state.change_controller(SelectWashMenuController(self.state))
                    break

                if parsed_user_input == WashSettingsOptions.GO_BACK:
                    self.model.change_machine_state(StartMenuController(self.state))
                    break
            except InvalidMenuSelectionError:
                print(self.view.invalid_selection)


@dataclass
class SelectWashMenuModel:
    state: WashingMachineInterface
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
class SelectWashMenuController(WashingMachineController):
    state: WashingMachineInterface

    def __post_init__(self):
        self.model = SelectWashMenuModel(state=self.state)
        self.view = SelectWashMenuView(state=self.state)

    def run(self):
        self.handle_user_input()

    def handle_user_input(self):
        while True:
            try:
                print(self.view.menu)
                user_input = input(self.view.prompt_input)
                parsed_user_input = self.model.parse_user_input(user_input)

                if parsed_user_input == SelectWashOptions.GO_BACK:
                    self.model.change_machine_controller(
                        WashSettingsMenuController(self.state)
                    )

                wash_data = self.model.get_wash_data(parsed_user_input)
                wash_outcome = get_wash_outcome(
                    self.state.balance.balance, wash_data.price
                )
                if wash_outcome == SelectWashOutcome.BALANCE_LESS_THAN_WASH_PRICE:
                    print(self.view.insufficient_funds)
                    return

                if wash_outcome == SelectWashOutcome.BALANCE_MORE_THAN_WASH_PRICE:
                    refund_amount = get_refund_amount(
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
                break
            except InvalidMenuSelectionError:
                print(self.view.invalid_selection)


washing_machine = WashingMachine(WashingMachineStatistics(), WashingMachineBalance())
controller = StartMenuController(washing_machine)
washing_machine.change_controller(controller)
washing_machine.run()
