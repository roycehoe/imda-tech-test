from dataclasses import dataclass

from constants import DEFAULT_MONEY_EARNED, DEFAULT_TOTAL_TIME_SWITCHED_ON_MINUTES


@dataclass
class WashingMachineBalance:
    balance: float = 0.00

    def topup_balance(self, money: float):
        self.balance += money

    def reset_balance(self, money: float):
        self.balance -= money

    def __str__(self):
        return f"""-------------------------------------
Current balance: ${self.balance:.2f}
-------------------------------------"""


@dataclass
class WashingMachineStatistics:
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
