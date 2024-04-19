from enum import Enum, auto


class StartMenu(Enum):
    USE_MACHINE = auto()
    VIEW_MANTENANCE_MENU = auto()
    EXIT = auto()


class MachineMenu(Enum):
    INSERT_COINS = auto()
    SELECT_WASH = auto()
    GO_BACK = auto()


class InsertCoinsMenu(Enum):
    INSERT_TEN_CENTS = auto()
    INSERT_TWENTY_CENTS = auto()
    INSERT_FIFTY_CENTS = auto()
    GO_BACK = auto()


class SelectWashMenu(Enum):
    QUICK_WASH = auto()
    MILD_WASH = auto()
    MEDIUM_WASH = auto()
    HEAVY_WASH = auto()
    GO_BACK = auto()


class PostWashMenu(Enum):
    USE_MACHINE = auto()
    EXIT = auto()


class MaintenanceMenu(Enum):
    DISPLAY_STATISTICS = auto()
    RESET_STATISTICS = auto()
    GO_BACK = auto()


START_MENU_DISPLAY = """
-------------------------------------
Impossibly Mighty Detergent Activator
-------------------------------------

Hello there! Thanks for choosing IMDA for your washing needs.
How may we assist you today?

[1] Start
[2] Exit"""

EXIT_DISPLAY = """Goodbye"""
MACHINE_MENU_DISPLAY = """
Please select one of the following options:

[1] Insert coins
[2] Select wash

Otherwise, press [0] to go back"""

INSERT_COINS_MENU_DISPLAY = """
Please choose one of the following coins to insert:

[1] 10c
[2] 20c
[3] 50c

Otherwise, press [0] to go back"""

SELECT_WASH_MENU_DISPLAY = """
Please select one of the following washes:


[1] Quick Wash: 10 mins - $2.00
[2] Mild Wash: 30 mins - $2.50
[3] Medium Wash: 45 mins - $4.20
[4] Heavy Wash: 1 hour - $6.00

Otherwise, press [0] to go back"""

INSUFFICIENT_FUNDS_DISPLAY = """Sorry, it seems you have insufficient funds to do that.

Please select a cheaper wash. Otherwise, try topping up your wallet"""

START_WASH_DISPLAY = """
Door locked. Wash starting...
"""

END_WASH_DISPLAY = """
Wash finished! The door is now unlocked. Please don't forget to take your clothes!
"""

MAINTANENCE_MENU = """
(Admin) What would you like to do?

[1] Display statistics
[2] Reset statistics

Otherwise, press [0] to go back"""
