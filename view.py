from dataclasses import dataclass

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
    STATISTICS_RESET_SUCCESS_DISPLAY,
    TOPUP_SUCCESS_DISPLAY,
)
from models import WashingMachineInterface


@dataclass
class InsertCoinMenuView:
    state: WashingMachineInterface
    menu = MENU_INSERT_COIN_DISPLAY
    topup_success = TOPUP_SUCCESS_DISPLAY
    invalid_selection = INVALID_SELECTION_DISPLAY
    prompt_input = PROMPT_INPUT

    def __post_init__(self):
        self.balance = self.state.balance


@dataclass
class StartMenuView:
    menu = MENU_START_DISPLAY
    invalid_selection = INVALID_SELECTION_DISPLAY
    prompt_input = PROMPT_INPUT
    exit = EXIT_DISPLAY


@dataclass
class MaintenanceMenuView:
    state: WashingMachineInterface

    menu = MENU_MAINTENANCE_DISPLAY
    invalid_selection = INVALID_SELECTION_DISPLAY
    prompt_input = PROMPT_INPUT
    statistics_reset_success = STATISTICS_RESET_SUCCESS_DISPLAY
    statistics = None

    def __post_init__(self):
        self.statistics = self.state.statistics


@dataclass
class WashSettingsMenuView:
    menu = MENU_WASH_SETTINGS_DISPLAY
    invalid_selection = INVALID_SELECTION_DISPLAY
    prompt_input = PROMPT_INPUT


@dataclass
class SelectWashMenuView:
    state: WashingMachineInterface
    invalid_selection = INVALID_SELECTION_DISPLAY
    prompt_input = PROMPT_INPUT
    insufficient_funds = INSUFFICIENT_FUNDS_DISPLAY
    start_wash = START_WASH_DISPLAY
    end_wash = END_WASH_DISPLAY
    menu = None

    def __post_init__(self):
        self.menu = self.get_menu_display(self.state.balance.balance)

    def get_refund_amount_display(self, refund_amount: float) -> str:
        return f"""
========Calculating change===========
Clonk clonk. ${refund_amount} refunded"""

    def get_menu_display(self, current_balance: float) -> str:
        return f"""
    -------------------------------------
    ------------Select Wash--------------
    -------------------------------------
        
    -------------------------------------
    Current balance: {current_balance:.2f}
    -------------------------------------

    Please select one of the following washes:

    [1] Quick Wash: 10 mins - $2.00
    [2] Mild Wash: 30 mins - $2.50
    [3] Medium Wash: 45 mins - $4.20
    [4] Heavy Wash: 1 hour - $6.00

    Otherwise, press [0] to go back"""
