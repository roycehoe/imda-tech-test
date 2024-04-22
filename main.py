from controller import (
    StartMenuController,
    WashingMachine,
    WashingMachineBalance,
    WashingMachineStatistics,
)


def init_washing_machine() -> WashingMachine:
    washing_machine = WashingMachine(
        WashingMachineStatistics(), WashingMachineBalance()
    )
    washing_machine.change_controller(StartMenuController(washing_machine))
    return washing_machine


washing_machine = init_washing_machine()
washing_machine.run()
