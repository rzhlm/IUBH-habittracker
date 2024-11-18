# lots of trouble with imports, 
# (temporarily) solved by '.env' file with PYTHONPATH hardcoded
# some kind of venv-related problem

from src.habit import Habit, HabitList
from src.storage2 import Storage
# can't run directly, must run: python -m src.controller
#from habit import Habit, HabitList
#from storage2 import Storage
from src.view import View, TUI
from typing import List


class Controller:
    def __init__(self, habitlist: HabitList = None,
                  storage: Storage = None):
        self.habitlist: HabitList = habitlist
        self.storage : Storage = storage
        pass

    def do_qm(self):
        print("1.inside QM (Controller)")
        pass
    def do_analysis(self):
        print("1.inside Analysis (Controller)")
        pass
    def do_showlist(self) -> None | List[Habit]:
        print("1.Inside showlist(Controller)")
        return self.habitlist.return_all()
        #self.habitlist.return_tracked
        pass
    def do_add(self):
        print("1.Inside add (Controller)")
        pass
    def do_edit(self):
        print("1. Inside Edit (Controller)")
        pass
    def do_quit(self):
        print("1.Inside Quit (controller)")
        pass

if __name__ == '__main__':
    pass
    # for testing & dev purposes
"""     st = Storage()
    hl: HabitList = st.load("controller.sav")
    c = Controller(hl, st)

    tui = TUI(c)
    tui.interact() """
