import time
from enum import Enum
from typing import TypeVar

from display import get_washing_job_progress_display
from enums import SelectWashOutcome

T = TypeVar("T", bound=Enum)


def simulate_washing_progress(wash_time: int) -> None:
    for time_left in range(1, wash_time + 1):
        time.sleep(0.1)
        display = get_washing_job_progress_display(
            time_left / wash_time, wash_time - time_left
        )
        print(display)


def get_wash_outcome(balance: float, wash_price: float) -> SelectWashOutcome:
    if balance == wash_price:
        return SelectWashOutcome.BALANCE_EQUALS_TO_WASH_PRICE
    if balance > wash_price:
        return SelectWashOutcome.BALANCE_MORE_THAN_WASH_PRICE
    return SelectWashOutcome.BALANCE_LESS_THAN_WASH_PRICE


def get_refund_amount(balance: float, wash_price: float) -> float:
    return balance - wash_price
