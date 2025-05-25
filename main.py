from typing import TYPE_CHECKING
#from src.analysis import X
from src.constants import Settings
from src.controller import Controller
from src.storage2 import Storage
from src.view import TUI
import sys

if TYPE_CHECKING:
    from src.habit import HabitAnalysis

def initialize_ui() -> TUI:
    settings: Settings = Settings()
    filename: str = settings.FILENAME
    storage: Storage = Storage()
    habitlist: HabitAnalysis = storage.HL_load(filename)
    controller: Controller = Controller(habitlist, storage)
    tui: TUI = TUI(controller)
    return tui

def main() -> None:
    ui: TUI = initialize_ui()
    ui.interact()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Runtime exception: {e}")
        sys.exit(1)