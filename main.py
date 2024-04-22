from models import WashingMachineStateInterface
from state import StartMenuState, WashingMachineBalance, WashingMachineStatistics


class WashingMachine:
    def __init__(
        self,
        state: WashingMachineStateInterface,
        statistics: WashingMachineStatistics,
        balance: WashingMachineBalance,
        is_door_locked: bool = False,
    ):

        self.state = state
        self.statistics = statistics
        self.balance = balance
        self.is_door_locked = is_door_locked

    def run(self) -> None:
        while self.state is not None:
            self.state.handle_input(self)

    def change_state(self, new_state: WashingMachineStateInterface) -> None:
        self.state = new_state

    def change_door_locked_status(self, new_door_locked_status: bool) -> None:
        self.is_door_locked = new_door_locked_status


washing_machine = WashingMachine(
    StartMenuState(), WashingMachineStatistics(), WashingMachineBalance()
)
washing_machine.run()
