from dataclasses import dataclass #, field
from enum import Enum, auto
from copy import deepcopy


class Period(Enum):
    daily = auto()
    weekly = auto()
    monthly = auto()

    def __str__(self) -> str:
        return f"{self.name}".ljust(7)

@dataclass
class BestStreak:
    """HABIT: the structure which stores date & streak of best streak
    for each habit"""
    on_date: str
    max_streak: int

@dataclass
class Habit:
    """HABIT: the structure which defines a habit"""
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
        """HABIT: The string representation when printed"""
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
        
    def toggle_tracked(self):
        """HABIT: Toggles Tracked bool of Habit"""
        self.is_tracked = not self.is_tracked
    def un_track(self):
        """HABIT: turns Tracked bool to False"""
        self.is_tracked = False
    def track(self):
        """HABIT: turns Tracked bool to True"""
        self.is_tracked = True

#@dataclass
class HabitAnalysis:
    """HABIT: stores a list of all the habits, counts them
    + all the methods to retrieve, update, add, etc."""
    
    def __init__(self, habitlist: list[Habit]):
        self._habitlist = habitlist
        self._len = len(habitlist)

    def get_len(self) -> int:
        """HABIT: gets the length of the habitlist: number of habits"""
        return self._len
    
    def add_habit(self, habit: Habit) -> None:
        """HABIT: adds Habit instance to _habitlist,
        and updates counter of total stored habits"""
        self._habitlist.append(habit)
        self._len += 1
        #breakpoint()
    
    def get_habit_by_id(self, id: int) -> Habit:
        """HABIT: returns the habit when given its ID"""
        # TODO: make this into a self.value (dict), to avoid repeating
        # but needs to be updated at habit creation & edit
        habit_dict = {
                    habit.id: habit 
                    for habit in self.return_all()
                    }
        #return deepcopy(habit_dict[id])
        return habit_dict[id]
            
    def update_habit(self, new_habit: Habit):
        """HABIT: updates a habit in the habitlist
        (overwrites it with a new copy)"""
        #self._habitlist[]
        for i, habit in enumerate(self._habitlist):
            if new_habit.id == habit.id:
                self._habitlist[i] = deepcopy(new_habit)
                #self._habitlist[i] = new_habit
                # need deepcopy to prevent a Heisenbug
                # TODO: find heisenbug, remove deepcopy
                break

    def return_all(self) -> list[Habit]:
        """HABIT: returns all habits (also untracked & deleted)"""
        return self._habitlist
    
    def return_tracked(self) -> list[Habit]:
        """HABIT: returns tracked habits (not untracked & deleted)"""
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
                )
    
    def return_same_period(self, period: Period) -> list[Habit]:
        """HABIT: returns tracked habits with same periodicity"""
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
        """HABIT: returns longest streak of all habits
        -> Habit"""
        # required to be functional
        #longest: int = -1
        #ft = filter(, self.habitlist)
        # TODO: check behaviour when multiple values or empty
        #return max([length.streak for length in self._habitlist])

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
        return max_

        
    def return_past_longest_streak_all(self) -> BestStreak:
        """HABIT: returns the record of habit with  highest past streak.
        -> BestStreak object
        also looks in untracked habits!!
        """
        # required to be functional
        top_habit = max(
                        self._habitlist,
                        key = lambda habit: habit.record.max_streak)
        return self.get_habit_by_id(top_habit.id).record
        
    def return_current_longest_streak_period(
                                            self,
                                            period: Period
                                            ) -> tuple[str, int]:
        """HABIT: returns the current longest streak of a particular period
        ->tuple(date: str, streak: int)"""
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
        
        if top_habit is None:
            return ("", 0)
        return (top_habit.last_complete, top_habit.streak)

    
    def return_past_longest_streak_period(self, period: Period) -> BestStreak:
        """HABIT: returns the past longest streak of a particular period
        -> BestStreak object"""
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
        if top_habit is None:
            return BestStreak("1900-01-01",0)
        return self.get_habit_by_id(top_habit.id).record

        


if __name__ == "__main__":
    print("This module is for importing, not for running directly")