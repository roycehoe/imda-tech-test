from controller import (
    StartMenuController,
    WashingMachine,
    WashingMachineBalance,
    WashingMachineStatistics,
)

washing_machine = WashingMachine(WashingMachineStatistics(), WashingMachineBalance())
controller = StartMenuController(washing_machine)
washing_machine.change_controller(controller)
washing_machine.run()
