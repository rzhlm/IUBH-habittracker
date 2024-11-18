#from src.analysis import X
from src.constants import Settings
from src.controller import Controller
from src.habit import Habit, HabitList
from src.storage2 import Storage
from src.view import View, TUI

def initialize_ui() -> TUI:
    settings: Settings = Settings()
    filename: str = settings.FILENAME
    storage: Storage = Storage()
    habitlist: HabitList = storage.load(filename)
    controller: Controller = Controller(habitlist, storage)
    
    tui = TUI(controller)
    return tui

def main() -> None:
    ui = initialize_ui()
    ui.interact()

if __name__ == "__main__":
    main()