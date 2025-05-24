# lots of trouble with imports, 
# (temporarily) solved by '.env' file with PYTHONPATH hardcoded
# some kind of venv-related problem

from __future__ import annotations
from src.habit import Habit
from typing import TYPE_CHECKING
from src.constants import Settings

if TYPE_CHECKING:
    from src.storage2 import Storage
    from src.habit import Period, HabitAnalysis


class Controller:
    def __init__(self, habitlist: HabitAnalysis,
                  storage: Storage):
        self.habitlist: HabitAnalysis = habitlist
        self.storage : Storage = storage
        self.current_date = self.storage.date_load()
        #print(f"STARTup: DATE: {self.current_date.split("\n")}/end")
        #import os
        #os.system('pause')

    def do_save_date(self, date: str) -> None:
        """CONTROLLER: saves the date (passes to STORAGE)"""
        self.current_date = date
        self.storage.date_save(self.current_date)

    def do_advance_date(self, newdate: str):
        """CONTROLLER: advances the manual date"""
        pass

    def do_qm(self):
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
        """CONTROLLER: returns a list of all habits"""
        return self.habitlist.return_all() or []

    def do_showlist_tracked(self) -> list[Habit]:
        """CONTROLLER: returns a list of tracked habits"""
        return self.habitlist.return_tracked() or []
    
    def do_showlist_period(self, period: Period) -> list[Habit]:
        """CONTROLLER: returns all habits with same periodicity"""
        return self.habitlist.return_same_period(period) or []

    def do_add(self, period: Period, description: str) -> None:
        """CONTROLLER: adds a new habit to Habitlist"""
        # id, start-date, period, track, streak, last-done, desc
        id: int = self.habitlist.get_len() + 1
        new_habit: Habit = Habit(
            id = id,
            description = description,
            creation_data = self.current_date,
            period = period,
            isTracked = True,
            streak = 0,
            last_complete = ""
        )
        self.habitlist.add_habit(new_habit)

    def do_delete(self, period: Period) -> bool:
        """CONTROLLER: removes a habit from Habitlist"""
        return False
        pass

    def do_edit(self, habit: Habit):
        """CONTROLLER: edits a habit"""
        #print("1. Inside Edit (Controller)")
        pass

    def do_help(self) -> str:
        """CONTROLLER: help instructions"""
        print("1. Inside Help (Controller)")
        return ""
    
    def do_quit(self):
        """CONTROLLER: exit logic"""
        print("entering QUIT LOGIC")
        settings: Settings = Settings()
        self.storage.date_save(self.current_date)
        self.storage.HL_save(self.habitlist, settings.FILENAME)


if __name__ == '__main__':
    print("This module is for import, not for running as main")
    # for testing & dev purposes
# if the below is removed, remove the respective test-savefiles as well
"""     st = Storage()
    hl: HabitList = st.load("controller.sav")
    c = Controller(hl, st)

    tui = TUI(c)
    tui.interact() """
