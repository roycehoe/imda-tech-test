```Mermaid
classDiagram
    class WashingMachine {
        -State state
        -WashingMachineStatistics statistics
        -WashingMachineBalance balance
        +run() void
        +change_state(State) void
    }
    class State {
        <<interface>>
        +handle_input(WashingMachine) void
    }
    class WashingMachineBalance {
        -float balance
        +topup_balance(float) void
        +reset_balance(float) void
        +__str__() string
    }
    class WashingMachineStatistics {
        -int total_time_switched_on_minutes
        -float money_earned
        +reset() void
        +add_total_time_switched_on_minutes(int) void
        +add_money_earned(float) void
        +__str__() string
    }
    class StartMenuState {
        +handle_input(WashingMachine) void
    }
    class MaintenanceMenuState {
        +handle_input(WashingMachine) void
    }
    class WashSettingsMenuState {
        +handle_input(WashingMachine) void
    }
    class InsertCoinMenuState {
        +handle_input(WashingMachine) void
    }
    class SelectWashMenuState {
        +handle_input(WashingMachine) void
        -_handle_payment(WashingMachine, SelectWashOutcome, float) void
        -_handle_wash_clothes(WashingMachine, int) void
    }

    State <|-- StartMenuState
    State <|-- MaintenanceMenuState
    State <|-- WashSettingsMenuState
    State <|-- InsertCoinMenuState
    State <|-- SelectWashMenuState

    WashingMachine *-- State : current state
    WashingMachine *-- WashingMachineStatistics : statistics
    WashingMachine *-- WashingMachineBalance : balance
```
