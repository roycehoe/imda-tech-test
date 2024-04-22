from dataclasses import dataclass
from typing import Any

from constants import (
    INSERT_COIN_OPTIONS_TO_COIN_VALUE_MAPPING,
    USER_INPUT_TO_INSERT_COIN_OPTIONS_MAPPING,
    USER_INPUT_TO_START_OPTIONS_MAPPING,
)
from display import (
    INVALID_SELECTION_DISPLAY,
    MENU_INSERT_COIN_DISPLAY,
    MENU_START_DISPLAY,
    PROMPT_INPUT,
    TOPUP_SUCCESS_DISPLAY,
)
from enums import InsertCoinOptions
from exceptions import InvalidMenuSelectionError
from state import WashingMachineBalance, WashingMachineStatistics, WashSettingsMenuState


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
    view = None

    def __post_init__(self):
        self.view = InsertCoinMenuView(self.state)

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
        raise Exception


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
                self.model.change_machine_state(WashSettingsMenuState())
                break

            topup_value = self.model.get_coin_value(parsed_user_input)
            self.model.topup_washing_machine(topup_value)

            print(self.view.topup_success)
            print(self.view.balance)


# @dataclass
# class StartMenuView:
#     menu = MENU_START_DISPLAY
#     invalid_selection = INVALID_SELECTION_DISPLAY
#     prompt_input = PROMPT_INPUT

# @dataclass
# class StartMenuModel:
#     menu = MENU_START_DISPLAY
#     invalid_selection = INVALID_SELECTION_DISPLAY
#     prompt_input = PROMPT_INPUT


washing_machine = WashingMachine(WashingMachineStatistics(), WashingMachineBalance())
controller = InsertCoinMenuController(washing_machine)
washing_machine.change_controller(controller)
washing_machine.run()
