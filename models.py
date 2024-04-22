from dataclasses import dataclass

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
from enums import (
    InsertCoinOptions,
    MaintenanceOptions,
    SelectWashOptions,
    StartMenuOptions,
    WashSettingsOptions,
)
from exceptions import InvalidCoinValueError, InvalidMenuSelectionError
from base import (
    WashingMachineInterface,
)
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
