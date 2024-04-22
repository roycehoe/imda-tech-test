from controller import (
    StartMenuController,
    WashingMachineBalance,
    WashingMachineInterface,
    WashingMachineStatistics,
)

washing_machine = WashingMachineInterface(
    WashingMachineStatistics(), WashingMachineBalance()
)
controller = StartMenuController(washing_machine)
washing_machine.change_controller(controller)
washing_machine.run()
