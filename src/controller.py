# lots of trouble with imports, 
# (temporarily) solved by '.env' file with PYTHONPATH hardcoded
# some kind of venv-related problem

from __future__ import annotations
from src.habit import Habit, Period
from typing import TYPE_CHECKING
from src.constants import Settings
import datetime as dt
#from copy import deepcopy
from dataclasses import dataclass
import sys

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
        self.current_date: dt.date = self.load_date()
        self.ready_to_advance = False
        self.done_indicator = self.init_done_indicator_list()

    def init_done_indicator_list(self) -> DoneIndicatorList:
        #if self.done_indicator:
        #    del self.done_indicator

        di_temp: list[DoneIndicator] = [
            DoneIndicator(habit.id, marked = False, done = False)
            for habit in self.do_showlist_tracked()]
        return DoneIndicatorList(self.current_date, di_temp)
    
    def addto_indicator_list(self, habit: Habit) -> None:
        di = DoneIndicator(habit.id, False, False)
        self.done_indicator.data.append(di)

    def do_save_date(self) -> None:
        """CONTROLLER: saves the date (passes to STORAGE)"""
        #self.current_date = date
        strf = self.settings.DTSTRF
        date_str = self.current_date.strftime(strf)
        self.storage.date_save(date_str)

    def load_date(self) -> dt.date:
        strf = self.settings.DTSTRF
        try:
            loaded_date = self.storage.date_load()
        except Exception as e:
            print(f"can't read datefile! error: {e}")
            sys.exit(1)
        date_dt = dt.datetime.strptime(loaded_date, strf)
        return date_dt
        #return date_dt.date()

    def dt_to_str(self, date: dt.date) -> str:
        format = self.settings.DTSTRF
        return date.strftime(format)

    def str_to_dt(self, date_str: str) -> dt.date:
        strf = self.settings.DTSTRF
        date_dt = dt.datetime.strptime(date_str, strf)
        return date_dt

    def are_all_habits_marked(self) -> bool:
        if self.done_indicator.today == self.current_date:
            return all(di.marked for di in self.done_indicator.data)
        return False
        # raise Exception("CONTROLLER: are_all_habits_marked: logic error")

    def is_ready_to_advance(self) -> bool:
        if self.done_indicator.today == self.current_date:
            if self.are_all_habits_marked():
                self.ready_to_advance = True
                return True
            return False
        return False
        # raise Exception("CONTROLLER: is_ready_to_advance: logic error")

    def mark_habit_done(self, passed_habit: Habit) -> None:
        strf = self.settings.DTSTRF
        passed_habit.last_complete = self.current_date.strftime(strf)
        self.habitlist.update_habit(passed_habit)
        #print(passed_habit)
        #print(self.habitlist)
        #print(self.done_indicator)
        #os.system('pause')

        for di in self.done_indicator.data:
            if passed_habit.id == di.id:
                di.marked = True
                di.done = True
                #print("TRUE")
                #print(self.done_indicator)
                #os.system("pause")
                break

    def mark_habit_not_done(self, habit: Habit) -> None:
        for di in self.done_indicator.data:
            if habit.id == di.id:
                di.marked = True
                break

    def is_habit_done_timely(self, habit: Habit) -> bool:
        """"CONTROLLER: checks if habit is done on time"""
        habit_dt = self.str_to_dt(habit.last_complete)
        diff = (self.current_date - habit_dt).days

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
                raise ValueError(f"non-existing period: {habit}")

    def is_habit_done_in_period(self, habit: Habit, period_days: int) -> bool:
        """CONTROLLER: is habit done in the period until day before the current?
        (for weekly/monthly habits at tehir edges)"""
        habit_dt = self.str_to_dt(habit.last_complete)
        diff = (self.current_date - habit_dt).days
        return 1 <= diff <= period_days

    def is_habit_done_last_week(self, habit: Habit) -> bool:
        """CONTROLLER: is habit done in previous calendar week.
        test on subsequent monday."""
        last_completion_date = self.str_to_dt(habit.last_complete)
        last_week_start = self.current_date - dt.timedelta(days=7)
        last_week_end = self.current_date - dt.timedelta(days=1)
        return last_week_start <= last_completion_date <= last_week_end

    def is_habit_done_last_month(self, habit: Habit) -> bool:
        """CONTROLLER: is habit done in previous calendar month?
        Test on 1st day of new month."""
        # if today is 1st March, is habit.last_complete
        # in the month of February?

        prev_date = self.current_date - dt.timedelta(days=1)
        last_complete_date = self.str_to_dt(habit.last_complete)
        # if self.current_date.month == 1:
        #     prev_year = self.current_date.year - 1
        #     prev_month = 12
        # else:
        #     prev_year = self.current_date.year
        #     prev_month = self.current_date.month - 1
        return last_complete_date.year == prev_date.year and \
            last_complete_date.month == prev_date.month

    def update_streak(self, habit: Habit) -> None:
        """CONTROLLER: updates the streak (if necessary), based on the periodicity"""
        habit.streak += 1

    def do_advance_date(self) -> None:
        """CONTROLLER: advances the manual date"""
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
                        # checked every monday
                        # meaning: is habit done in calendar-week?
                        # dt.weekday: 0=monday, 6=sunday
                        if self.current_date.weekday() == 0:
                            #if self.is_habit_done_last_week(habit):
                            if self.is_habit_done_timely(habit):
                                self.update_streak(habit)
                            else:
                                habit.streak = 0
                    case Period.monthly:
                        # reset on 1st of next month
                        # meaning: is habit done in calendar-month?
                        if self.current_date.day == 1:
                            #if self.is_habit_done_last_month(habit):
                            if self.is_habit_done_timely(habit):
                                self.update_streak(habit)
                            else:
                                habit.streak = 0
                    case _:
                        raise ValueError("CONTROLLER: do_advance_date, invalid period")

            # advance date
            self.current_date = self.current_date + dt.timedelta(days=1)

            # create new done_indicator for new day
            self.done_indicator = self.init_done_indicator_list()

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
        strf = self.settings.DTSTRF
        id: int = self.habitlist.get_len() + 1
        new_habit: Habit = Habit(
            id = id,
            description = description,
            creation_data = self.current_date.strftime(strf),
            period = period,
            isTracked = True,
            streak = 0,
            last_complete = "1900-01-01"
        )
        self.habitlist.add_habit(new_habit)
        self.addto_indicator_list(new_habit)
        #breakpoint()

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
        helpstr: str = """HELP
        The colored letters are commands, which you should input.

        A habit can be tracked or untracked. 
        (untracked: is for 'archival'/'soft deletion').
        
        The date is advanced manually, this is a great feature.
        You can't advance the date, until each tracked habit has 
        been marked "done" or "not done". Do this with "Quick mark".

        Daily streaks get calculated *after* advancing to the next day.
        Weekly streaks get calculated *after* advancing from Monday to Tuesday.
        Monthly streaks get calculated *after* advancing from 1st to 2nd 
        of the month.

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