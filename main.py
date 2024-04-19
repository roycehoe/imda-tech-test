from dataclasses import dataclass
from enum import Enum, auto

DEFAULT_WALLET_BALANCE = 0.00


class StartMenu(Enum):
    GO_TO_USE_MACHINE_MENU = auto()
    GO_TO_MANTENANCE_MENU = auto()
    EXIT = auto()


class UseMachineMenu(Enum):
    INSERT_COINS = auto()
    SELECT_WASH = auto()
    GO_BACK = auto()


class InsertCoinsMenu(Enum):
    INSERT_TEN_CENTS = auto()
    INSERT_TWENTY_CENTS = auto()
    INSERT_FIFTY_CENTS = auto()
    INSERT_ONE_DOLLAR = auto()
    GO_BACK = auto()


class SelectWashMenu(Enum):
    QUICK_WASH = auto()
    MILD_WASH = auto()
    MEDIUM_WASH = auto()
    HEAVY_WASH = auto()
    GO_BACK = auto()


class PostWashMenu(Enum):
    GO_TO_USE_MACHINE_MENU = auto()
    EXIT = auto()


class MaintenanceMenu(Enum):
    DISPLAY_STATISTICS = auto()
    RESET_STATISTICS = auto()
    GO_BACK = auto()


START_MENU_DISPLAY = """
-------------------------------------
Impossibly Mighty Detergent Activator
-------------------------------------

Hello there! Thanks for choosing IMDA for your washing needs.
How may we assist you today?

[1] Start
[2] Exit"""

EXIT_DISPLAY = """Goodbye"""
USE_MACHINE_MENU_DISPLAY = """
Please select one of the following options:

[1] Insert coins
[2] Select wash

Otherwise, press [0] to go back"""

INSERT_COINS_MENU_DISPLAY = """
Please choose one of the following coins to insert:

[1] 10c
[2] 20c
[3] 50c
[4] $1

Otherwise, press [5] to go back"""

SELECT_WASH_MENU_DISPLAY = """
Please select one of the following washes:

[1] Quick Wash: 10 mins - $2.00
[2] Mild Wash: 30 mins - $2.50
[3] Medium Wash: 45 mins - $4.20
[4] Heavy Wash: 1 hour - $6.00

Otherwise, press [0] to go back"""

INSUFFICIENT_FUNDS_DISPLAY = """Sorry, it seems you have insufficient funds to do that.

Please select a cheaper wash. Otherwise, try topping up your wallet"""

START_WASH_DISPLAY = """
Door locked. Wash starting...
"""

END_WASH_DISPLAY = """
Wash finished! The door is now unlocked. Please don't forget to take your clothes!
"""

MAINTANENCE_MENU = """
(Admin) What would you like to do?

[1] Display statistics
[2] Reset statistics

Otherwise, press [0] to go back"""


STATISTICS_RESET_DISPLAY = """
All statistics has been reset
"""

INVALID_SELECTION_DISPLAY = """
You have selected an invalid option. Please try again
"""


@dataclass
class MachineStatistics:
    total_time_switched_on_hours: int = 0
    money_earned: float = 0.01

    def __str__(self):
        return f"""Total time switched on: {self.total_time_switched_on_hours} hours
Balance: ${self.money_earned:.2f}"""


def show_wallet_balance(balance: float) -> None:
    print(f"Current balance: ${balance}")


def show_statistics(machine_statistics: MachineStatistics) -> None:
    print(machine_statistics)


def show_insert_coin_success_message(coin_value: float) -> None:
    print(f"Ding! ${coin_value} successfully added to your wallet")


def show_refund_excess_message(excess_amount: float) -> None:
    print(f"Clonk clonk. ${excess_amount} refunded")


def show_washing_job_progress(
    progress_percentage: float, remaining_time_minutes: int
) -> None:
    print(
        f"""Current progress: {progress_percentage * 100:.0f}%
Remaining time: {remaining_time_minutes} mins"""
    )
