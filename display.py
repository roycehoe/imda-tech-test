PROMPT_INPUT = "Input: "
EXIT_DISPLAY = """
============Shutting Down============
Goodbye"""
INSUFFICIENT_FUNDS_DISPLAY = """=========Insufficient Funds==========
Sorry, it seems you have insufficient funds to do that.

Please select a cheaper wash. Otherwise, try topping up your wallet"""

START_WASH_DISPLAY = """
=============Door Locked=============
===========Start of wash============="""

TOPUP_SUCCESS_DISPLAY = """
==========Topup Successful==========="""

END_WASH_DISPLAY = """
============Door Unlocked============
============End of wash==============

Wash finished! The door is now unlocked. 
Please don't forget to take your clothes!"""


STATISTICS_RESET_SUCCESS_DISPLAY = """
========Resetting Statistics=========
======Statistics Reset Complete======"""

INVALID_SELECTION_DISPLAY = """
==========Invalid Option=============
You have selected an invalid option. Please try again."""

MENU_START_DISPLAY = """
+++++++++++++++++++++++++++++++++++++
Impossibly Mighty Detergent Activator
+++++++++++++++++++++++++++++++++++++

-------------------------------------
--------------Welcome----------------
-------------------------------------

Hello there! Thanks for choosing IMDA for your washing needs.
How may we assist you today?

[1] Start
[2] Mantenance
[3] Exit
"""
MENU_WASH_SETTINGS_DISPLAY = """
-------------------------------------
-----------Wash Settings-------------
-------------------------------------

Please select one of the following options:

[1] Insert coins
[2] Select wash

Otherwise, press [0] to go back"""
MENU_INSERT_COIN_DISPLAY = """
-------------------------------------
------------Insert Coins-------------
-------------------------------------

Please choose one of the following coins to insert:

[1] 10c
[2] 20c
[3] 50c
[4] $1

Otherwise, press [0] to go back"""
MENU_MAINTENANCE_DISPLAY = """
-------------------------------------
------------Maintenance--------------
-------------------------------------

What would you like to do?

[1] Display statistics
[2] Reset statistics

Otherwise, press [0] to go back"""


def get_refund_excess_display(excess_amount: float) -> str:
    return f"""
========Calculating change===========
Clonk clonk. ${excess_amount} refunded"""


def get_washing_job_progress_display(
    progress_percentage: float, remaining_time_minutes: int
) -> str:
    return f"""....................................
Current progress: {progress_percentage * 100:.0f}%
Remaining time: {remaining_time_minutes} mins
...................................."""


def get_menu_select_wash_display(current_balance: float) -> str:
    return f"""
-------------------------------------
------------Select Wash--------------
-------------------------------------
      
-------------------------------------
Current balance: {current_balance:.2f}
-------------------------------------

Please select one of the following washes:

[1] Quick Wash: 10 mins - $2.00
[2] Mild Wash: 30 mins - $2.50
[3] Medium Wash: 45 mins - $4.20
[4] Heavy Wash: 1 hour - $6.00

Otherwise, press [0] to go back"""
