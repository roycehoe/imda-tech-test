import time
from enum import Enum
from typing import TypeVar

from constants import DEFAULT_WASHING_TYPES, INSERT_COIN_OPTIONS_TO_COIN_VALUE_MAPPING
from display import (
    INVALID_SELECTION_DISPLAY,
    PROMPT_INPUT,
    get_washing_job_progress_display,
)
from enums import InsertCoinOptions, SelectWashOptions, SelectWashOutcome
from exceptions import InvalidCoinValueError, InvalidMenuSelectionError
from models import WashingMachineBalance

T = TypeVar("T", bound=Enum)


def get_menu_option(option_str: str, options_mapping: dict[str, T]) -> T:
    if selected_option := options_mapping.get(option_str):
        return selected_option
    raise InvalidMenuSelectionError


def get_user_menu_input(
    display_message: str,
    options_mapping: dict[str, T],
    prompt_message: str = PROMPT_INPUT,
) -> T:
    while True:
        try:
            print(display_message)
            user_input = input(prompt_message)
            return get_menu_option(user_input, options_mapping)
        except InvalidMenuSelectionError:
            print(INVALID_SELECTION_DISPLAY)


def topup_washing_machine(
    washing_machine_balance: WashingMachineBalance,
    insert_coin_input: InsertCoinOptions,
    coin_value_mapping: dict[
        InsertCoinOptions, float
    ] = INSERT_COIN_OPTIONS_TO_COIN_VALUE_MAPPING,
) -> None:
    if coin_value := coin_value_mapping.get(insert_coin_input):
        return washing_machine_balance.topup_balance(coin_value)
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


def simulate_washing_progress(wash_time: int) -> None:
    for time_left in range(1, wash_time + 1):
        time.sleep(0.1)
        display = get_washing_job_progress_display(
            time_left / wash_time, wash_time - time_left
        )
        print(display)
