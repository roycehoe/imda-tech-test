import time
from abc import ABC

from display import (
    END_WASH_DISPLAY,
    EXIT_DISPLAY,
    INSERT_COIN_MENU_DISPLAY,
    INSUFFICIENT_FUNDS_DISPLAY,
    INVALID_SELECTION_DISPLAY,
    MACHINE_MENU_DISPLAY,
    MAINTENANCE_MENU,
    PROMPT_INPUT,
    SELECT_WASH_MENU_DISPLAY,
    START_MENU_DISPLAY,
    START_WASH_DISPLAY,
    STATISTICS_RESET_DISPLAY,
    WashingMachineBalance,
    WashingMachineStatistics,
    show_refund_excess_message,
    show_statistics,
    show_washing_job_progress,
)
from enums import (
    InsertCoinOptions,
    MaintenanceOptions,
    SelectWashOptions,
    SelectWashOutcome,
    StartMenuOptions,
    WashSettingsOptions,
)

START_MENU_MAPPING = {
    "1": StartMenuOptions.WASH_SETTINGS,
    "2": StartMenuOptions.MANTENANCE,
    "3": StartMenuOptions.EXIT,
}

MAINTENANCE_MENU_MAPPING = {
    "1": MaintenanceOptions.DISPLAY_STATISTICS,
    "2": MaintenanceOptions.RESET_STATISTICS,
    "0": MaintenanceOptions.GO_BACK,
}

WASH_SETTINGS_MENU_MAPPING = {
    "1": WashSettingsOptions.INSERT_COINS,
    "2": WashSettingsOptions.SELECT_WASH,
    "3": WashSettingsOptions.GO_BACK,
}

INSERT_COIN_MENU_MAPPING = {
    "1": InsertCoinOptions.INSERT_TEN_CENTS,
    "2": InsertCoinOptions.INSERT_TWENTY_CENTS,
    "3": InsertCoinOptions.INSERT_FIFTY_CENTS,
    "4": InsertCoinOptions.INSERT_ONE_DOLLAR,
    "0": InsertCoinOptions.GO_BACK,
}

SELECT_WASH_MENU_MAPPING = {
    "1": SelectWashOptions.QUICK_WASH,
    "2": SelectWashOptions.MILD_WASH,
    "3": SelectWashOptions.MEDIUM_WASH,
    "4": SelectWashOptions.HEAVY_WASH,
    "0": SelectWashOptions.GO_BACK,
}


class InvalidMenuSelectionError(Exception):
    pass


def get_start_menu_options(
    user_selection: str,
    start_menu_mapping: dict[str, StartMenuOptions] = START_MENU_MAPPING,
) -> StartMenuOptions:
    if user_selected_option := start_menu_mapping.get(user_selection):
        return user_selected_option
    raise InvalidMenuSelectionError


def get_start_menu_input() -> StartMenuOptions:
    while True:
        try:
            print(START_MENU_DISPLAY)
            user_input = input(PROMPT_INPUT)
            start_menu_selection = get_start_menu_options(user_input)
            return start_menu_selection
        except InvalidMenuSelectionError:
            print(INVALID_SELECTION_DISPLAY)


def get_maintenance_menu_options(
    user_selection: str, maintenance_menu_mapping=MAINTENANCE_MENU_MAPPING
) -> MaintenanceOptions:
    if user_selected_option := maintenance_menu_mapping.get(user_selection):
        return user_selected_option
    raise InvalidMenuSelectionError


def get_maintenance_menu_input() -> MaintenanceOptions:
    while True:
        try:
            print(MAINTENANCE_MENU)
            user_selection = input(PROMPT_INPUT)
            maintenance_menu_selection = get_maintenance_menu_options(user_selection)
            return maintenance_menu_selection
        except InvalidMenuSelectionError:
            print(INVALID_SELECTION_DISPLAY)


def get_wash_settings_options(
    user_selection: str, wash_settings_menu_mapping=WASH_SETTINGS_MENU_MAPPING
) -> WashSettingsOptions:
    if user_selected_option := wash_settings_menu_mapping.get(user_selection):
        return user_selected_option
    raise InvalidMenuSelectionError


def get_wash_settings_input() -> WashSettingsOptions:
    while True:
        try:
            print(MACHINE_MENU_DISPLAY)
            user_selection = input(PROMPT_INPUT)
            machine_menu_selection = get_wash_settings_options(user_selection)
            return machine_menu_selection
        except InvalidMenuSelectionError:
            print(INVALID_SELECTION_DISPLAY)


def get_insert_coin_options(
    user_selection: str, insert_coin_menu_mapping=INSERT_COIN_MENU_MAPPING
) -> InsertCoinOptions:
    if user_selected_option := insert_coin_menu_mapping.get(user_selection):
        return user_selected_option
    raise InvalidMenuSelectionError


def get_insert_coin_input() -> InsertCoinOptions:
    while True:
        try:
            print(INSERT_COIN_MENU_DISPLAY)
            user_selection = input(PROMPT_INPUT)
            insert_coin_selection = get_insert_coin_options(user_selection)
            return insert_coin_selection
        except InvalidMenuSelectionError:
            print(INVALID_SELECTION_DISPLAY)


def get_select_wash_options(
    user_selection: str, select_wash_menu_mapping=SELECT_WASH_MENU_MAPPING
) -> SelectWashOptions:
    if user_selected_option := select_wash_menu_mapping.get(user_selection):
        return user_selected_option
    raise InvalidMenuSelectionError


def get_select_wash_input() -> SelectWashOptions:
    while True:
        try:
            print(SELECT_WASH_MENU_DISPLAY)
            user_selection = input(PROMPT_INPUT)
            select_wash_selection = get_select_wash_options(user_selection)
            return select_wash_selection
        except InvalidMenuSelectionError:
            print(INVALID_SELECTION_DISPLAY)


def topup_washing_machine(
    washing_machine_state: WashingMachineBalance,
    insert_coin_input: InsertCoinOptions,
) -> None:
    if insert_coin_input == InsertCoinOptions.INSERT_TEN_CENTS:
        return washing_machine_state.topup_balance(0.1)
    if insert_coin_input == InsertCoinOptions.INSERT_TWENTY_CENTS:
        return washing_machine_state.topup_balance(0.2)
    if insert_coin_input == InsertCoinOptions.INSERT_FIFTY_CENTS:
        return washing_machine_state.topup_balance(0.5)
    if insert_coin_input == InsertCoinOptions.INSERT_ONE_DOLLAR:
        return washing_machine_state.topup_balance(1.0)


def get_select_wash_outcome(balance: float, wash_price: float) -> SelectWashOutcome:
    if balance == wash_price:
        return SelectWashOutcome.BALANCE_EQUALS_TO_WASH_PRICE
    if balance > wash_price:
        return SelectWashOutcome.BALANCE_MORE_THAN_WASH_PRICE
    return SelectWashOutcome.BALANCE_LESS_THAN_WASH_PRICE


WASHING_TYPES = {
    "Quick Wash": {"time": 10, "price": 2.00},
    "Mild Wash": {"time": 30, "price": 2.5},
    "Medium Wash": {"time": 45, "price": 4.20},
    "Heavy Wash": {"time": 60, "price": 6.00},
}


def get_wash_price(selected_wash: SelectWashOptions) -> float:
    if selected_wash == SelectWashOptions.QUICK_WASH:
        return WASHING_TYPES["Quick Wash"]["price"]
    if selected_wash == SelectWashOptions.MILD_WASH:
        return WASHING_TYPES["Mild Wash"]["price"]
    if selected_wash == SelectWashOptions.MEDIUM_WASH:
        return WASHING_TYPES["Medium Wash"]["price"]
    return WASHING_TYPES["Heavy Wash"]["price"]


def get_wash_time(selected_wash: SelectWashOptions) -> int:
    if selected_wash == SelectWashOptions.QUICK_WASH:
        return WASHING_TYPES["Quick Wash"]["time"]
    if selected_wash == SelectWashOptions.MILD_WASH:
        return WASHING_TYPES["Mild Wash"]["time"]
    if selected_wash == SelectWashOptions.MEDIUM_WASH:
        return WASHING_TYPES["Medium Wash"]["time"]
    return WASHING_TYPES["Heavy Wash"]["time"]


def get_refund_amount(balance: float, wash_price: float) -> float:
    return balance - wash_price


def show_mock_continuous_washing_job_progress(wash_time: int) -> None:
    for i in range(1, wash_time + 1):
        time.sleep(0.1)
        show_washing_job_progress(i / wash_time, wash_time - i)


class State(ABC):
    def handle_input(self, context):
        raise NotImplementedError


class WashingMachine:
    def __init__(
        self,
        state: State,
        statistics: WashingMachineStatistics,
        balance: WashingMachineBalance,
    ):

        self.state = state
        self.statistics = statistics
        self.balance = balance

    def run(self) -> None:
        while self.state is not None:
            self.state.handle_input(self)

    def change_state(self, new_state: State) -> None:
        self.state = new_state


class SelectWashMenuState(State):
    def handle_input(self, washing_machine: WashingMachine):
        while True:
            select_wash_input = get_select_wash_input()
            if select_wash_input == SelectWashOptions.GO_BACK:
                washing_machine.change_state(WashSettingsMenuState())
                break

            wash_price = get_wash_price(select_wash_input)
            select_wash_outcome = get_select_wash_outcome(
                washing_machine.balance.balance, wash_price
            )

            if select_wash_outcome == SelectWashOutcome.BALANCE_LESS_THAN_WASH_PRICE:
                print(INSUFFICIENT_FUNDS_DISPLAY)

            if select_wash_outcome == SelectWashOutcome.BALANCE_MORE_THAN_WASH_PRICE:
                refund_amount = get_refund_amount(
                    washing_machine.balance.balance, wash_price
                )
                show_refund_excess_message(refund_amount)

            if (
                select_wash_outcome == SelectWashOutcome.BALANCE_MORE_THAN_WASH_PRICE
                or select_wash_outcome == SelectWashOutcome.BALANCE_EQUALS_TO_WASH_PRICE
            ):
                washing_machine.balance.reset_balance(wash_price)
                wash_time = get_wash_time(select_wash_input)
                washing_machine.statistics.add_money_earned(wash_price)
                washing_machine.statistics.add_total_time_switched_on_minutes(wash_time)
                print(START_WASH_DISPLAY)
                show_mock_continuous_washing_job_progress(wash_time)
                print(END_WASH_DISPLAY)
                washing_machine.change_state(StartMenuState())
                break


class InsertCoinMenuState(State):
    def handle_input(self, context: WashingMachine):
        while True:
            insert_coin_input = get_insert_coin_input()
            if insert_coin_input == InsertCoinOptions.GO_BACK:
                context.change_state(WashSettingsMenuState())
                break

            topup_washing_machine(context.balance, insert_coin_input)
            print(context.balance)


class WashSettingsMenuState(State):
    def handle_input(self, context: WashingMachine):
        machine_menu_input = get_wash_settings_input()
        if machine_menu_input == WashSettingsOptions.INSERT_COINS:
            context.change_state(InsertCoinMenuState())

        if machine_menu_input == WashSettingsOptions.SELECT_WASH:
            context.change_state(SelectWashMenuState())

        if machine_menu_input == WashSettingsOptions.GO_BACK:
            context.change_state(StartMenuState())


class MaintenanceMenuState(State):
    def handle_input(self, context: WashingMachine):
        while True:
            maintenance_menu_input = get_maintenance_menu_input()
            if maintenance_menu_input == MaintenanceOptions.DISPLAY_STATISTICS:
                show_statistics(context.statistics)
            if maintenance_menu_input == MaintenanceOptions.RESET_STATISTICS:
                context.statistics.reset()
                print(STATISTICS_RESET_DISPLAY)
            if maintenance_menu_input == MaintenanceOptions.GO_BACK:
                context.change_state(StartMenuState())
                break


class StartMenuState(State):
    def handle_input(self, context: WashingMachine):
        start_menu_input = get_start_menu_input()
        if start_menu_input == StartMenuOptions.EXIT:
            print(EXIT_DISPLAY)
            exit()

        if start_menu_input == StartMenuOptions.MANTENANCE:
            context.change_state(MaintenanceMenuState())

        if start_menu_input == StartMenuOptions.WASH_SETTINGS:
            context.change_state(WashSettingsMenuState())


washing_machine = WashingMachine(
    StartMenuState(), WashingMachineStatistics(), WashingMachineBalance()
)
washing_machine.run()
