# lots of trouble with imports, 
# (temporarily) solved by '.env' file with PYTHONPATH hardcoded
# some kind of venv or PATH-related problem
# ::: only on Windows laptop, no problem on Linux or macOS

from __future__ import annotations
from typing import TYPE_CHECKING
import sys
import datetime as dt
from dataclasses import dataclass

from src.model.habit import Habit, Period, BestStreak
from src.model.constants import Settings


if TYPE_CHECKING:
    from src.model.storage import Storage
    from src.model.habit import HabitAnalysis


@dataclass
class DoneIndicator:
    """CONTROLLER:DoneIndicator:
    is a 'struct'/dataclass for keeping track of status of a single habit """
    id: int
    marked: bool
    done: bool


@dataclass
class DoneIndicatorList:
    """CONTROLLER: DoneIndicatorList:
    bundles all the DoneIndicators of all the tracked habits
    + the day for which they are marked (= done or not done)"""
    today: dt.datetime
    data: list[DoneIndicator]

# TODO: split methods off into separate modules
# eg Init/Exit, Date, Interface, Marking

class Controller:
    """CONTROLLER: Controller: 
    C part of the MVC"""
    def __init__(self, habitlist: HabitAnalysis,
                  storage: Storage):
        self.settings: Settings = Settings()
        self.habitlist: HabitAnalysis = habitlist
        self.storage : Storage = storage
        self.current_date: dt.datetime = self.load_date()
        self.ready_to_advance = False
        self.done_indicator = self.init_done_indicator_list()
        self.habitlist.register_observer(self.sync_done_indicators)

    def sync_done_indicators(self) -> None:
        """CONTROLLER: Controller: 
        syncs DoneIndicatorList to always match tracked habits.
        Is called automatically (if my observer pattern works),
        when habitlist gets changed."""

        tracked_ids: list[int] = [
                                    habit.id
                                    for habit in self.do_showlist_tracked()
                                ]
        self.done_indicator.data = [
                                    di
                                    for di in self.done_indicator.data
                                    if di.id in tracked_ids
                                ]
        
        existing_ids: list[int] = [
                                    di.id
                                    for di in self.done_indicator.data
                                    ]
        
        for habit in self.do_showlist_tracked():
            if habit.id not in existing_ids:
                self.done_indicator.data.append(
                    DoneIndicator(habit.id, marked=False, done=False)
                                            )

    def init_done_indicator_list(self) -> DoneIndicatorList:
        """CONTROLLER: Controller: 
        makes the DoneIndicatorList, for keeping track of which
        habits are still to be checked off for each current day"""
        #if self.done_indicator:
        #    del self.done_indicator

        di_temp: list[DoneIndicator] = [
            DoneIndicator(habit.id, marked = False, done = False)
            for habit in self.do_showlist_tracked()]
        return DoneIndicatorList(self.current_date, di_temp)
    
    def addto_indicator_list(self, habit: Habit) -> None:
        """CONTROLLER: Controller: 
        adds a newly created habit to the DoneIndicatorList"""
        # not needed anymore now with Observer pattern
        di = DoneIndicator(habit.id, False, False)
        self.done_indicator.data.append(di)

    def do_save_date(self) -> None:
        """CONTROLLER: Controller: 
        saves the date (passes to STORAGE)"""
        #self.current_date = date
        strf = self.settings.DTSTRF
        date_str = self.current_date.strftime(strf)
        try:
            self.storage.date_save(date_str)
        except Exception as e:
            print(f"could not save datefile! error: {e}")
            sys.exit(1)

    def load_date(self) -> dt.datetime:
        """CONTROLLER: Controller: 
        loads the datestring from storage and makes it datetime"""
        strf: str = self.settings.DTSTRF
        try:
            loaded_date: str = self.storage.date_load()
        except Exception as e:
            print(f"can't read datefile! error: {e}")
            sys.exit(1)

        date_dt: dt.datetime = dt.datetime.strptime(loaded_date, strf)
        return date_dt
        #return date_dt.date()

    def dt_to_str(self, date: dt.datetime) -> str:
        """CONTROLLER: Controller: 
        turns a datetime into string, with our configured format"""
        format: str = self.settings.DTSTRF
        return date.strftime(format)

    def str_to_dt(self, date_str: str) -> dt.datetime:
        """CONTROLLER: Controller:
        turns a string into datetime, using our configured format"""
        strf: str = self.settings.DTSTRF
        date_dt: dt.datetime = dt.datetime.strptime(date_str, strf)
        return date_dt

    def are_all_habits_marked(self) -> bool:
        """CONTROLLER: Controller: 
        checks if all the habits for today have been marked"""
        if self.done_indicator.today == self.current_date:
            return all(di.marked for di in self.done_indicator.data)
        return False
        # raise Exception("CONTROLLER: are_all_habits_marked: logic error")

    def is_ready_to_advance(self) -> bool:
        """CONTROLLER: Controller:
        checks whether all habits are marked, in order to advance the date."""
        if self.done_indicator.today == self.current_date:
            if self.are_all_habits_marked():
                self.ready_to_advance = True
                return True
            return False
        return False
        # raise Exception("CONTROLLER: is_ready_to_advance: logic error")

    def mark_habit_done(self, passed_habit: Habit) -> None:
        """CONTROLLER: Controller: 
        1) modifies the last_complete date of a habit, in the habitlist
        2) modifies the DoneIndicator for that habit to 'done'"""
        strf: str  = self.settings.DTSTRF
        passed_habit.last_complete = self.current_date.strftime(strf)
        self.habitlist.update_habit(passed_habit)
        #breakpoint()

        for di in self.done_indicator.data:
            if passed_habit.id == di.id:
                di.marked = True
                di.done = True
                #breakpoint()
                break

    def mark_habit_not_done(self, habit: Habit) -> None:
        """CONTROLLER: Controller: 
        marks a habit in the DoneIndicatorList,
        as not done (but marked for that day)"""
        for di in self.done_indicator.data:
            if habit.id == di.id:
                di.marked = True
                break

    def is_habit_done_timely(self, habit: Habit) -> bool:
        """"CONTROLLER: Controller: 
        checks if habit is done on time
        depending on its periodicity"""
        habit_dt: dt.datetime = self.str_to_dt(habit.last_complete)
        diff: int = (self.current_date - habit_dt).days

        match habit.period:
            case Period.daily:
                # done today (note: today is new day after the rollover!)
                return diff == 0
            case Period.weekly:
                # done in the past 7 days
                # a diff of 6 is also possible, depending on how you
                # define how much time has passed and if a streak
                # becomes missed on or after the period.
                return diff <= 7
            case Period.monthly:
                # done in the past 31 days. Same caveat as above
                return diff <= 31
            case _:
                raise ValueError(f"non-expected period: {habit}")

    def update_streak(self, habit: Habit) -> None:
        """CONTROLLER:Controller: 
        updates the streak with 1 unit"""
        habit.streak += 1
        if habit.streak > habit.record.max_streak:
            habit.record = BestStreak(self.dt_to_str(self.current_date), habit.streak)

    def do_advance_date(self) -> None:
        """CONTROLLER: Controller:
        advances the manual date"""
        if self.is_ready_to_advance():
            # update streaks, for done
            for habit in self.habitlist.return_all():
                
                match habit.period:
                    case Period.daily:
                        if self.is_habit_done_timely(habit):
                            self.update_streak(habit)
                        else:
                            # not done: streak loss
                            habit.streak = 0
                    case Period.weekly:
                        # checked after every monday
                        # meaning: is habit done in previous calendar-week?
                        # dt.weekday: 0=monday, 6=sunday
                        if self.current_date.weekday() == 0:
                            if self.is_habit_done_timely(habit):
                                self.update_streak(habit)
                            else:
                                habit.streak = 0
                    case Period.monthly:
                        # check after 1st of next month
                        # meaning: is habit done in calendar-month?
                        if self.current_date.day == 1:
                            if self.is_habit_done_timely(habit):
                                self.update_streak(habit)
                            else:
                                habit.streak = 0
                    case _:
                        raise ValueError("CONTROLLER: do_advance_date, \
                                         undefined period")

            # advance date
            self.current_date = self.current_date + dt.timedelta(days=1)

            # create new done_indicator for new day
            self.done_indicator = self.init_done_indicator_list()

    def return_unmarked_habits(self) -> list[Habit]:
        """CONTROLLER: Controller: 
        finds the habits which for the current day have not yet
        been marked as 'done' or 'not done'."""
        habit_dict = {
            habit.id: habit 
            for habit in self.do_showlist_tracked()
            }
        return [
            habit_dict[di.id]
            for di in self.done_indicator.data 
            if not di.marked and
            di.id in habit_dict # crash on delete otherwise
            ]

    def do_qm(self):
        """CONTROLLER: Controller: 
        placeholder for QuickMark logic, if needed"""
        pass

    def do_analysis(self):
        """CONTROLLER: Controller: 
        placeholder for Analysis logic, if needed"""
        pass

    def do_showlist(self) -> list[Habit]:
        """CONTROLLER: Controller: 
        returns a list of all habits"""
        return self.habitlist.return_all() or []

    def do_showlist_tracked(self) -> list[Habit]:
        """CONTROLLER: Controller: 
        returns a list of tracked habits"""
        return self.habitlist.return_tracked() or []
    
    def do_showlist_period(self, period: Period) -> list[Habit]:
        """CONTROLLER: Controller: 
          returns all habits with same periodicity"""
        return self.habitlist.return_same_period(period) or []

    def do_add(self, period: Period, description: str) -> None:
        """CONTROLLER: Controller: 
        adds a new habit to Habitlist"""
        # id, start-date, period, track, streak, last-done, desc
        strf: str = self.settings.DTSTRF
        id: int = self.habitlist.get_len() + 1
        new_habit: Habit = Habit(
            id = id,
            description = description,
            creation_data = self.current_date.strftime(strf),
            period = period,
            is_tracked = True,
            streak = 0,
            last_complete = "1900-01-01",
            record = BestStreak("1900-01-01", -1),
        )
        self.habitlist.add_habit(new_habit)
        # self.addto_indicator_list(new_habit) # now done by Observer
        #breakpoint()

    def do_delete(self, habit: Habit) -> None:
        """CONTROLLER: Controller: 
        flags a habit from Habitlist as 'deleted'"""
        habit.streak = -1
        self.do_edit(habit)
        self.done_indicator.data = [
                                    di 
                                    for di in self.done_indicator.data
                                    if di.id != habit.id]

    def do_edit(self, edit_habit: Habit) -> None:
        """CONTROLLER: Controller: 
        edits a habit"""
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
        """CONTROLLER:Controller: 
        help instructions"""

        helpstr: str = """HELP
        The colored letters are commands, which you should input.

        A habit can be tracked or untracked. 
        (untracked: is for 'archival'/'soft deletion').
        
        The date is advanced manually, this is a great feature.
        (It does not use your system date)
        You can't advance the date, until each tracked habit has 
        been marked "done" or "not done". Do this with "Quick mark".

        -Daily streaks get calculated *after* advancing to the next day.

        -Weekly streaks get calculated *after* advancing from Monday to Tuesday.
        (i.e. the evaluation theoretically happens on midnight at Monday)
        (i.e. the streak runs from Monday 23:59 to next Monday 23:59)
        
        -Monthly streaks get calculated *after* advancing from 1st to 2nd 
        of the month. (A monthly streak is defined as being done 
        in the previous 31 days, even if the month is shorter.)
        (i.e. the evaluation theoretically happens on midnight on the 1st day)
        (i.e. the streak runs from 1st 23:59 to next 1st at 23:59 )

        When you edit, you can change: track/untrack, description, or delete.

        EXPERT MODE: for easy evaluation. Streak of -1 is used 
        to flag a deleted habit.
        """
        return helpstr
    
    def do_quit(self) -> None:
        """CONTROLLER: Controller: 
        exit logic"""
        #print("entering QUIT LOGIC")
        self.do_save_date()
        self.storage.HL_save(self.habitlist, self.settings.FILENAME)


if __name__ == '__main__':
    print("This module is for import, not for running as main")