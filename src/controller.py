# lots of trouble with imports, 
# (temporarily) solved by '.env' file with PYTHONPATH hardcoded
# some kind of venv-related problem

from __future__ import annotations
from src.habit import Habit
from typing import TYPE_CHECKING
from src.constants import Settings
import datetime as dt
#from copy import deepcopy
from dataclasses import dataclass

if TYPE_CHECKING:
    from src.storage2 import Storage
    from src.habit import Period, HabitAnalysis


@dataclass
class DoneIndicator:
    id: int
    marked: bool
    done: bool


@dataclass
class DoneIndicatorList:
    today: dt.date
    data: list[DoneIndicator]


class Controller:
    def __init__(self, habitlist: HabitAnalysis,
                  storage: Storage):
        self.settings: Settings = Settings()
        self.habitlist: HabitAnalysis = habitlist
        self.storage : Storage = storage
        #self.current_date = self.storage.date_load()
        self.current_date: dt.date = self.load_date()
        self.ready_to_advance = False
        self.done_indicator = self.init_done_indicator_list()

    def init_done_indicator_list(self) -> DoneIndicatorList:
        #if self.done_indicator:
        #    del self.done_indicator

        di_temp: list[DoneIndicator] = [
            DoneIndicator(habit.id, marked = False, done = False)
            for habit
            in self.do_showlist_tracked()]
        return DoneIndicatorList(self.current_date, di_temp)

    def do_save_date(self) -> None:
        """CONTROLLER: saves the date (passes to STORAGE)"""
        #self.current_date = date
        strf = self.settings.DTSTRF
        date_str = self.current_date.strftime(strf)
        self.storage.date_save(date_str)

    def load_date(self) -> dt.date:
        strf = self.settings.DTSTRF
        loaded_date = self.storage.date_load()
        date_dt = dt.datetime.strptime(loaded_date, strf)
        return date_dt

    def dt_to_str(self, date: dt.date) -> str:
        format = self.settings.DTSTRF
        return date.strftime(format)

    def are_all_habits_marked(self) -> bool:
        if self.done_indicator.today == self.current_date:
            return all(di.marked for di in self.done_indicator.data)
        raise Exception("CONTROLLER: are_all_habits_marked: logic error")

    def is_ready_to_advance(self) -> bool:
        if self.done_indicator.today == self.current_date:
            if self.are_all_habits_marked():
                self.ready_to_advance = True
                return True
            return False
        raise Exception("CONTROLLER: is_ready_to_advance: logic error")

    def mark_habit_done(self, passed_habit: Habit) -> None:
        strf = self.settings.DTSTRF
        passed_habit.last_complete = self.current_date.strftime(strf)
        self.habitlist.update_habit(passed_habit)
        
        for di in self.done_indicator.data:
            if passed_habit.id == di.id:
                di.marked == True # type: ignore
                di.done == True # type: ignore
                break

    def mark_habit_not_done(self, habit: Habit) -> None:
        for di in self.done_indicator.data:
            if habit.id == di.id:
                di.marked == True # type: ignore
                break

    def can_advance_date(self) -> bool:
        return self.is_ready_to_advance()

    def do_advance_date(self) -> None:
        """CONTROLLER: advances the manual date"""
        if self.can_advance_date():
            pass
            # update streaks, for done

            # reset streaks, for not done

            # advance date

            # create new done_indicator for today

    def return_unmarked_habits(self) -> list[Habit]:
        habit_dict = {
            habit.id: habit 
            for habit in self.do_showlist_tracked()
            }
        return [
            habit_dict[di.id]
            for di in self.done_indicator.data 
            if not di.marked]

    def do_qm(self):
        # need to ID the habit, and toggle it
        # need to know which habits are active for today
        # freshly added habits should also be active for today

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
            creation_data = self.current_date.strftime("%Y-%m-%d"),
            period = period,
            isTracked = True,
            streak = 0,
            last_complete = "1900-01-01"
        )
        self.habitlist.add_habit(new_habit)

    def do_delete(self, habit: Habit) -> None:
        """CONTROLLER: removes a habit from Habitlist"""
        habit.streak = -1
        self.do_edit(habit)

    def do_edit(self, edit_habit: Habit) -> None:
        """CONTROLLER: edits a habit"""
        # Beware of 'by ref' passing of objects!
        # because of Python passing by reference, the habit gets edited
        # directly instead of a copy of it, unless explicitly deepcopied.
        # In order to avoid side-effects & unexpected behaviour: deepcopy

        # for i, habit in enumerate(self.habitlist._habitlist):
        #     if edit_habit.id == habit.id:
        #         self.habitlist._habitlist[i] = deepcopy(edit_habit)
        #         break

        # we're being passed a deepcopy, and this one gets passed to respective
        # method in the habitlist/habitanalysis class.
        self.habitlist.update_habit(edit_habit)

    def do_help(self) -> str:
        """CONTROLLER: help instructions"""
        helpstr: str = f"""HELP
        The colored letters are commands, which you should input.

        A habit can be tracked or untracked. This is a 'soft delete'/'archival'.
        
        The date is advanced manually, this is a great feature.
        You can't advance date, until each tracked habit has 
        been marked "done" or "not done". Do this with "Quick mark".

        Streaks get calculated after advancing to the next day.
        
        When you edit, you can change: track/untrack, description, or delete.

        🙟
        """
        return helpstr
    
    def do_quit(self) -> None:
        """CONTROLLER: exit logic"""
        print("entering QUIT LOGIC")
        #self.storage.date_save(self.current_date)
        self.do_save_date()
        self.storage.HL_save(self.habitlist, self.settings.FILENAME)


if __name__ == '__main__':
    print("This module is for import, not for running as main")
    # for testing & dev purposes
# if the below is removed, remove the respective test-savefiles as well
"""     st = Storage()
    hl: HabitList = st.load("controller.sav")
    c = Controller(hl, st)

    tui = TUI(c)
    tui.interact() """
