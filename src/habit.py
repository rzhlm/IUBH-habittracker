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
    #_habitlist : list[Habit] = field(default_factory=lambda: [])
    #_len : int = 0

    def __init__(self, habitlist: list[Habit]):
        self._habitlist = habitlist
        self._len = len(habitlist)

    def get_len(self) -> int:
        """HABIT: gets the length of the habitlist: number of habits"""
        return self._len
    
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
        """HABIT: returns tracked habits"""
        return [habit 
                for habit in self._habitlist 
                if habit.is_tracked and
                habit.streak != -1 # flagged as deleted: streak = -1
                ] 
    
    def return_same_period(self, period: Period) -> list[Habit]:
        """HABIT: returns habits with same periodicity"""
        return [habit 
                for habit in self._habitlist
                if habit.period == period and
                habit.is_tracked and
                habit.streak != -1 # flagged as deleted: streak = -1
                ]
    
    def return_longest_streak_all(self) -> Habit:
        """HABIT: returns longest streak of all habits"""
        #longest: int = -1
        #ft = filter(, self.habitlist)
        # TODO: check behaviour when multiple values or empty
        return max([length.streak for length in self._habitlist])
    
    def return_longest_ever_all(self) -> Habit:
        pass
        
    def return_longest_streak_specific(self, habit: Habit) -> tuple[str, int]:
        """HABIT: returns the longest streak of a particular habit
        tuple(date: str, streak: int)"""
        # TODO: check behaviour when returning multiple values or empty
        # added default for now, but will fail at the other end.
        return max(
                (
                (h.last_complete, h.streak)
                for h in self._habitlist if h == habit
                ), key = lambda x: x[1], default=("", 0)
                )


        return (
            the_date_it_occured,
            max([stored_habit.streak for stored_habit in self._habitlist
                     if stored_habit == habit ])
                     )
    
    def return_longest_ever_specific(self, habit: Habit) -> Habit:
        pass
        
    def add_habit(self, habit: Habit) -> None:
        """HABIT: adds Habit instance to _habitlist,
        and updates counter of total stored habits"""
        self._habitlist.append(habit)
        self._len += 1
        #breakpoint()


if __name__ == "__main__":
    print("This module is for importing, not for running directly")