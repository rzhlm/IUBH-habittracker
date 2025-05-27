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
at the cost of being more visually crowded.

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