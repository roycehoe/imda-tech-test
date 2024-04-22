import time
from enum import Enum
from typing import TypeVar

from display import (
    get_washing_job_progress_display,
)

T = TypeVar("T", bound=Enum)



def simulate_washing_progress(wash_time: int) -> None:
    for time_left in range(1, wash_time + 1):
        time.sleep(0.1)
        display = get_washing_job_progress_display(
            time_left / wash_time, wash_time - time_left
        )
        print(display)
