# lots of trouble with imports, 
# (temporarily) solved by '.env' file with PYTHONPATH hardcoded
# some kind of venv-related problem
from __future__ import annotations
from src.habit import Habit
from typing import TYPE_CHECKING

# can't run directly, must run: python -m src.controller
#from habit import Habit, HabitList
#from storage2 import Storage
#from src.view import View, TUI
#from typing import List

if TYPE_CHECKING:
    from src.storage2 import Storage
    from src.habit import Period, HabitList


class Controller:
    def __init__(self, habitlist: HabitList,
                  storage: Storage):
        self.habitlist: HabitList = habitlist
        self.storage : Storage = storage
        self.current_date = ""
        # TODO: add date loading
        pass

    def do_advance_date(self):
        pass

    def do_qm(self):
        """Mark habit as done"""
        # need to ID the habit, and toggle it
        # need to know which habits are active for today
        # freshly added habits should also be active for today

        print("1.inside QM (Controller)")
        # mark habit as done
        pass
    def do_analysis(self):
        print("1.inside Analysis (Controller)")
        pass
    def do_showlist(self) -> list[Habit]:
        #print("1.Inside showlist(Controller)")
        
        return self.habitlist.return_all() or []
        #self.habitlist.return_tracked
        pass

    def do_showlist_tracked(self) -> list[Habit]:
        return self.habitlist.return_tracked() or []
    
    def do_showlist_period(self, period: Period) -> list[Habit]:
        return self.habitlist.return_same_period(period) or []

    def do_add(self, period: Period, description: str):
        #print("1.Inside add (Controller)")
        # Habit:
        # id, start-date, period, track, streak, last-done, desc
        id: int = self.habitlist.get_len() + 1
        new_habit: Habit = Habit(
            id = id,
            description = description,
            creation_data=self.current_date,
            period = period,
            isTracked = True,
            streak=0,
            last_complete=""
        )
        self.habitlist.add_habit(new_habit)
        pass

    def do_edit(self):
        print("1. Inside Edit (Controller)")
        pass
    def do_help(self):
        print("1. Inside Help (Controller)")
    
    def do_quit(self):
        print("1.Inside Quit (controller)")
        pass

if __name__ == '__main__':
    pass
    # for testing & dev purposes
# if the below is removed, remove the respective test-savefiles as well
"""     st = Storage()
    hl: HabitList = st.load("controller.sav")
    c = Controller(hl, st)

    tui = TUI(c)
    tui.interact() """
