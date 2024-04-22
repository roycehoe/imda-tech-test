from abc import ABC, abstractmethod
from dataclasses import dataclass

from state import WashingMachineBalance, WashingMachineStatistics


class State(ABC):
    def handle_input(self, context):
        raise NotImplementedError


class WashingMachineInterface(ABC):
    def __init__(
        self,
        state: State,
        statistics: WashingMachineStatistics,
        balance: WashingMachineBalance,
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
