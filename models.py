from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class WashingMachineBalanceInterface(ABC):
    balance: float

    @abstractmethod
    def topup_balance(self, money: float):
        pass

    @abstractmethod
    def reduce_balance(self, money: float):
        pass

    def __str__(self):
        pass


@dataclass
class WashingMachineStatisticsInterface(ABC):
    total_time_switched_on_minutes: int
    money_earned: float

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def add_total_time_switched_on_minutes(self, additional_time: int):
        pass

    @abstractmethod
    def add_money_earned(self, additional_money_earned: float):
        pass

    def __str__(self):
        pass


class WashingMachineStateInterface(ABC):
    def handle_input(self, context):
        raise NotImplementedError


class WashingMachineInterface(ABC):
    def __init__(
        self,
        state: WashingMachineStateInterface,
        statistics: WashingMachineStatisticsInterface,
        balance: WashingMachineBalanceInterface,
        is_door_locked=False,
    ):
        self.state = state
        self.statistics = statistics
        self.balance = balance
        self.is_door_locked = is_door_locked

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def change_state(self, new_state):
        pass

    @abstractmethod
    def change_door_locked_status(self, new_door_locked_status: bool):
        pass
