from typing import TYPE_CHECKING
import sys

from src.constants import Settings
from src.controller import Controller
from src.storage2 import Storage
from src.view import TUI


if TYPE_CHECKING:
    from src.habit import HabitAnalysis

"""
 NOTE: Some of the Classes are getting crowded with methods.
If they grew more, ideally they would be put into separate modules,
and/or separate classes.
As the assignment was to be mainly OOP (except for the Analytics part),
the choice was made to have a simpler Class structure,
at the cost of being more visually crowded, 
rather than branch out to multiple modules.

If the save-files don't exist, they get re-generated.
(i.e. they are safe to be deleted in order to start over)

2022-05-01 is a Sunday, and 1st of the month
-> after marking and advancing tonight, the monthly streak increments
-> the next day, after marking and advancing, the weekly streak increments

"""

def initialize_ui() -> TUI:
    """MAIN: sets up all the necessary instances for the TUI,
    and then returns the TUI"""
    settings: Settings = Settings()
    filename: str = settings.FILENAME
    storage: Storage = Storage()
    habitlist: HabitAnalysis = storage.HL_load(filename)
    controller: Controller = Controller(habitlist, storage)
    tui: TUI = TUI(controller)
    return tui

def main() -> None:
    """MAIN: main function. Runs the UI"""
    ui: TUI = initialize_ui()
    ui.interact()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Runtime exception: {e}")
        sys.exit(1)