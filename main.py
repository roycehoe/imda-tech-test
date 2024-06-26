from constants import (
    USER_INPUT_TO_INSERT_COIN_OPTIONS_MAPPING,
    USER_INPUT_TO_MAINTENANCE_OPTIONS_MAPPING,
    USER_INPUT_TO_SELECT_WASH_OPTIONS_MAPPING,
    USER_INPUT_TO_START_OPTIONS_MAPPING,
    USER_INPUT_TO_WASH_SETTINGS_OPTIONS_MAPPING,
)
from display import (
    END_WASH_DISPLAY,
    EXIT_DISPLAY,
    INSUFFICIENT_FUNDS_DISPLAY,
    MENU_INSERT_COIN_DISPLAY,
    MENU_MAINTENANCE_DISPLAY,
    MENU_START_DISPLAY,
    MENU_WASH_SETTINGS_DISPLAY,
    START_WASH_DISPLAY,
    STATISTICS_RESET_DISPLAY,
    TOPUP_SUCCESS_DISPLAY,
    get_menu_select_wash_display,
    get_refund_excess_display,
)
from enums import (
    InsertCoinOptions,
    MaintenanceOptions,
    SelectWashOptions,
    SelectWashOutcome,
    StartMenuOptions,
    WashSettingsOptions,
)
from models import State, WashingMachineBalance, WashingMachineStatistics
from utils import (
    get_refund_amount,
    get_select_wash_outcome,
    get_user_menu_input,
    get_wash_price,
    get_wash_time,
    simulate_washing_progress,
    topup_washing_machine,
)


class WashingMachine:
    def __init__(
        self,
        state: State,
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

    def change_state(self, new_state: State) -> None:
        self.state = new_state

    def change_door_locked_status(self, new_door_locked_status: bool) -> None:
        self.is_door_locked = new_door_locked_status


class SelectWashMenuState(State):
    def handle_input(self, washing_machine: WashingMachine):
        while True:

            selected_wash_input = get_user_menu_input(
                get_menu_select_wash_display(washing_machine.balance.balance),
                USER_INPUT_TO_SELECT_WASH_OPTIONS_MAPPING,
            )
            if selected_wash_input == SelectWashOptions.GO_BACK:
                washing_machine.change_state(WashSettingsMenuState())
                break

            wash_price = get_wash_price(selected_wash_input)
            wash_time = get_wash_time(selected_wash_input)
            select_wash_outcome = get_select_wash_outcome(
                washing_machine.balance.balance, wash_price
            )
            if select_wash_outcome == SelectWashOutcome.BALANCE_LESS_THAN_WASH_PRICE:
                print(INSUFFICIENT_FUNDS_DISPLAY)
                return

            self._handle_payment(washing_machine, select_wash_outcome, wash_price)
            self._handle_wash_clothes(washing_machine, wash_time)
            washing_machine.change_state(StartMenuState())
            break

    def _handle_payment(
        self,
        washing_machine: WashingMachine,
        outcome: SelectWashOutcome,
        wash_price: float,
    ):
        if outcome == SelectWashOutcome.BALANCE_MORE_THAN_WASH_PRICE:
            refund_amount = get_refund_amount(
                washing_machine.balance.balance, wash_price
            )
            refund_amount_display = get_refund_excess_display(refund_amount)
            print(refund_amount_display)

        washing_machine.balance.reset_balance(wash_price)
        washing_machine.statistics.add_money_earned(wash_price)

    def _handle_wash_clothes(
        self,
        washing_machine: WashingMachine,
        wash_time: int,
    ):
        washing_machine.statistics.add_total_time_switched_on_minutes(wash_time)

        washing_machine.change_door_locked_status(True)
        print(START_WASH_DISPLAY)
        simulate_washing_progress(wash_time)
        washing_machine.change_door_locked_status(False)
        print(END_WASH_DISPLAY)


class InsertCoinMenuState(State):
    def handle_input(self, washing_machine: WashingMachine):
        while True:
            insert_coin_input = get_user_menu_input(
                MENU_INSERT_COIN_DISPLAY, USER_INPUT_TO_INSERT_COIN_OPTIONS_MAPPING
            )
            if insert_coin_input == InsertCoinOptions.GO_BACK:
                washing_machine.change_state(WashSettingsMenuState())
                break
            topup_washing_machine(washing_machine.balance, insert_coin_input)
            print(TOPUP_SUCCESS_DISPLAY)
            print(washing_machine.balance)


class WashSettingsMenuState(State):
    def handle_input(self, washing_machine: WashingMachine):
        wash_settings_input = get_user_menu_input(
            MENU_WASH_SETTINGS_DISPLAY, USER_INPUT_TO_WASH_SETTINGS_OPTIONS_MAPPING
        )
        if wash_settings_input == WashSettingsOptions.INSERT_COINS:
            washing_machine.change_state(InsertCoinMenuState())

        if wash_settings_input == WashSettingsOptions.SELECT_WASH:
            washing_machine.change_state(SelectWashMenuState())

        if wash_settings_input == WashSettingsOptions.GO_BACK:
            washing_machine.change_state(StartMenuState())


class MaintenanceMenuState(State):
    def handle_input(self, washing_machine: WashingMachine):
        while True:
            maintenance_menu_input = get_user_menu_input(
                MENU_MAINTENANCE_DISPLAY, USER_INPUT_TO_MAINTENANCE_OPTIONS_MAPPING
            )
            if maintenance_menu_input == MaintenanceOptions.DISPLAY_STATISTICS:
                print(washing_machine.statistics)
            if maintenance_menu_input == MaintenanceOptions.RESET_STATISTICS:
                washing_machine.statistics.reset()
                print(STATISTICS_RESET_DISPLAY)
            if maintenance_menu_input == MaintenanceOptions.GO_BACK:
                washing_machine.change_state(StartMenuState())
                break


class StartMenuState(State):
    def handle_input(self, washing_machine: WashingMachine):
        start_menu_input = get_user_menu_input(
            MENU_START_DISPLAY, USER_INPUT_TO_START_OPTIONS_MAPPING
        )
        if start_menu_input == StartMenuOptions.EXIT:
            print(EXIT_DISPLAY)
            exit()

        if start_menu_input == StartMenuOptions.MANTENANCE:
            washing_machine.change_state(MaintenanceMenuState())

        if start_menu_input == StartMenuOptions.WASH_SETTINGS:
            washing_machine.change_state(WashSettingsMenuState())


washing_machine = WashingMachine(
    StartMenuState(), WashingMachineStatistics(), WashingMachineBalance()
)
washing_machine.run()
