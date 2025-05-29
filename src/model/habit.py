from dataclasses import dataclass
from enum import Enum, auto
from copy import deepcopy
from collections.abc import Callable

class Period(Enum):
    daily = auto()
    weekly = auto()
    monthly = auto()

    def __str__(self) -> str:
        return f"{self.name}".ljust(7)

@dataclass
class BestStreak:
    """HABIT:BestStreak:
    the structure which stores date & streak of best streak
    for each habit"""
    on_date: str
    max_streak: int

@dataclass
class Habit:
    """HABIT:Habit:
    the structure which defines a habit"""
    # if adding here, modify testing
    # and modify savefiles
    id: int
    description: str
    creation_data: str
    period: Period
    #timeline: List[]
    is_tracked: bool
    streak : int
    last_complete: str
    record : BestStreak
    # Use @property method for streak calculation?

    def __str__(self):
        """HABIT:Habit:
        The string representation when printed"""
        #f"|{self.last_complete}".ljust(11) +\
        never = "1900-01-01"
        last = "never" if self.last_complete == never else self.last_complete
        #repr: str =  "Habit(".ljust(7) + \
        repr: str =  f"|{self.id}".ljust(6) + \
        f"|{self.creation_data}".ljust(12) +\
        f"|{self.period}".ljust(8) +\
        f"|{self.is_tracked}".ljust(7) +\
        f"|{self.streak}".ljust(7) + \
        f"|{last}".ljust(11) +\
        f"|{self.description} )"

        return repr.expandtabs(3)
        
    def toggle_tracked(self) -> None:
        """HABIT:Habit:
        Toggles Tracked bool of Habit"""
        self.is_tracked = not self.is_tracked
    def un_track(self) -> None:
        """HABIT:Habit:
        turns Tracked bool to False"""
        self.is_tracked = False
    def track(self) -> None:
        """HABIT:Habit:
        turns Tracked bool to True"""
        self.is_tracked = True

#@dataclass
class HabitAnalysis:
    """HABIT:HabitAnalysis:
    stores a list of all the habits, counts them
    + all the methods to retrieve, update, add, etc."""
    
    def __init__(self, habitlist: list[Habit]):
        # TODO: keep track of maximum ID, noth with length of list
        # but with an actual read of each added ID + increment
        self._habitlist: list[Habit] = habitlist
        #  ↑ in retrospect, obviously this should be a dictionary, not a list
        self._len: int = len(habitlist)
        #self._max_id = 0 #
        self._observers: list[Callable[[], None]] = []

    def register_observer(self, callback: Callable[[], None]) -> None:
        """HABIT:HabitAnalysis:
        adds a callback for observers (design pattern)"""
        self._observers.append(callback)

    def notify_observers(self) -> None:
        """HABIT:HabitAnalysis:
        notifies by running all the observer callbakcs"""
        for callback in self._observers:
            callback()

    def get_len(self) -> int:
        """HABIT: HabitAnalysis:
        gets the length of the habitlist: number of habits"""
        return self._len
    
    def add_habit(self, habit: Habit) -> None:
        """HABIT: HabitAnalysis:
        adds Habit instance to _habitlist,
        and updates counter of total stored habits"""
        self._len += 1
        #self.max_id += 1
        self._habitlist.append(habit)
        self.notify_observers()
        #breakpoint()
    
    def get_habit_by_id(self, id: int) -> Habit:
        """HABIT: HabitAnalysis:
        returns the habit when given its ID"""
        # TODO:  also make a self.value (dict), to avoid repeating
        # but then needs to be updated at habit creation & edit
        habit_dict = {
                    habit.id: habit 
                    for habit in self.return_all()
                    }
        #return deepcopy(habit_dict[id])
        return habit_dict[id] or None
            
    def update_habit(self, new_habit: Habit) -> None:
        """HABIT: HabitAnalysis:
        updates a habit in the habitlist (overwrites it with a new copy)"""
        #self._habitlist[]
        for i, habit in enumerate(self._habitlist):
            if new_habit.id == habit.id:
                self._habitlist[i] = deepcopy(new_habit)
                self.notify_observers()
                #self._habitlist[i] = new_habit
                # need deepcopy to prevent a Heisenbug
                # TODO: find heisenbug, remove deepcopy
                break

    def return_all(self) -> list[Habit]:
        """HABIT: HabitAnalysis:
        returns all habits (also untracked & deleted)"""
        return self._habitlist or []
    
    def return_tracked(self) -> list[Habit]:
        """HABIT: HabitAnalysis:
        returns tracked habits (not untracked & deleted)"""
        # required to be functional
        # return [habit 
        #         for habit in self._habitlist 
        #         if habit.is_tracked and
        #         habit.streak != -1 # flagged as deleted: streak = -1
        #         ] 
        return list(
                    filter(
                        lambda habit: 
                        habit.is_tracked and 
                        habit.streak != -1
                        ,self._habitlist
                        )
                ) or []
    
    def return_same_period(self, period: Period) -> list[Habit]:
        """HABIT: HabitAnalysis:
        returns tracked habits with same periodicity"""
        # required to be functional
        # return [habit 
        #         for habit in self._habitlist
        #         if habit.period == period and
        #         habit.is_tracked and
        #         habit.streak != -1 # flagged as deleted: streak = -1
        #         ]
        return list(
                    filter(
                        lambda habit:
                        habit.period == period and
                        habit.is_tracked and
                        habit.streak != -1
                        ,self._habitlist
                        )
                )
    
    def return_current_longest_streak_all(self) -> Habit:
        """HABIT: HabitAnalysis:
        returns longest streak of all habits"""
        # required to be functional

        # max = -2
        # max_id = 0
        # for habit in self._habitlist:
        #     if habit.streak > max:
        #         max = habit.streak
        #         max_id = habit.id
        
        # for habit in self._habitlist:
        #     if max_id == habit.id:
        #         return habit
        
        max_ = max(
                    # map(
                    #     lambda habit: habit.streak,
                    #     self._habitlist
                    #     )
                    self._habitlist,
                    key = lambda habit: habit.streak
                )
        
        # multiples = list(
        #                 filter(
        #                         lambda habit: habit.streak == max_,
        #                         self._habitlist
        #                 )
        #             )
        
        #return multiples[0]
        return max_ or None

        
    def return_past_longest_streak_all(self) -> Habit:
        """HABIT:HabitAnalysis:
        returns the record of habit with  highest past streak.
        also looks in untracked habits!!
        """
        # required to be functional
        top_habit = max(
                        self._habitlist,
                        key = lambda habit: habit.record.max_streak)
        return self.get_habit_by_id(top_habit.id) or None
        
    def return_current_longest_streak_period(
                                            self,
                                            period: Period
                                            ) -> Habit | None:
        """HABIT: HabitAnalysis:
        returns the current longest streak of a particular period
        for the tracked habits."""
        # required to be functional

        # max_ = -2
        # max_id = 0
        # max_date = ""
        # for habit in self.return_tracked():
        #     if habit.period == period:
        #         if habit.streak > max_:
        #             max_ = habit.streak
        #             max_id = habit.id
        #             max_date = habit.last_complete
        # return (max_date, max_)
    
        period_habits = filter(
                        lambda habit: habit.period == period,
                        self.return_tracked()
                        )
    
        top_habit = max(
                        period_habits,
                        key = lambda habit: habit.streak,
                        default = None
                    )
        
        return top_habit or None

    
    def return_past_longest_streak_period(self, period: Period) -> Habit | None:
        """HABIT: HabitAnalysis: 
        returns the past longest streak of a particular period"""
        # max_ = -2
        # max_id = 0
        # for habit in self._habitlist:
        #     if habit.period == period:
        #         if habit.record.max_streak > max_:
        #             max_ = habit.record.max_streak
        #             max_id = habit.id
        # return self.get_habit_by_id(max_id).record

        top_habit = max(
                        filter(
                            lambda habit: habit.period == period,
                            self._habitlist
                            ),
                            key=lambda habit: habit.record.max_streak,
                            default=None
                    )
        if top_habit:
            return self.get_habit_by_id(top_habit.id)
        return None

        
if __name__ == "__main__":
    print("This module is for importing, not for running directly")