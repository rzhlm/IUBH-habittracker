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
class Habit:
    # if adding here, modify testing
    # and modify savefiles
    id: int
    description: str
    creation_data: str
    period: Period
    #timeline: List[]
    isTracked: bool
    streak : int
    last_complete: str
    # Use @property method for streak calculation?
    # But how to know beforehand if at currenttime streak is still valid?

    def __str__(self):
        #f"|{self.last_complete}".ljust(11) +\
        never = "1900-01-01"
        last = "never" if self.last_complete == never else self.last_complete
        #repr: str =  "Habit(".ljust(7) + \
        repr: str =  f"|{self.id}".ljust(6) + \
        f"|{self.creation_data}".ljust(12) +\
        f"|{self.period}".ljust(8) +\
        f"|{self.isTracked}".ljust(7) +\
        f"|{self.streak}".ljust(7) + \
        f"|{last}".ljust(11) +\
        f"|{self.description} )"

        return repr.expandtabs(3)
        
    def toggle_tracked(self):
        """HABIT: Toggles Tracked bool of Habit"""
        self.isTracked = not self.isTracked
    def un_track(self):
        """HABIT: turns Tracked bool to False"""
        self.isTracked = False
    def track(self):
        """HABIT: turns Tracked bool to True"""
        self.isTracked = True

#@dataclass
class HabitAnalysis:
    #_habitlist : list[Habit] = field(default_factory=lambda: [])
    #_len : int = 0

    def __init__(self, habitlist: list[Habit]):
        self._habitlist = habitlist
        self._len = len(habitlist)

    def get_len(self) -> int:
        """HABITLIST: gets the length of the habitlist"""
        return self._len
    
    def update_habit(self, new_habit: Habit):
        #self._habitlist[]
        for i, habit in enumerate(self._habitlist):
            if new_habit.id == habit.id:
                self._habitlist[i] = deepcopy(new_habit)
                #self._habitlist[i] = new_habit
                # need deepcopy to prevent a Heisenbug
                # TODO: find heisenbug, remove deepcopy
                break

    def return_all(self) -> list[Habit]:
        """HABITLIST: returns all habits (also untracked & deleted)"""
        return self._habitlist
    
    def return_tracked(self) -> list[Habit]:
        """HABITLIST: returns tracked habits"""
        return [habit 
                for habit in self._habitlist 
                if habit.isTracked and
                habit.streak != -1 # streak = -1 if flagged as deleted
                ] 
    
    def return_same_period(self, period: Period) -> list[Habit]:
        """HABITLIST: returns habits with same periodicity"""
        return [habit 
                for habit in self._habitlist
                if habit.period == period and
                habit.isTracked and
                habit.streak != -1 # streak = -1 if flagged as deleted
                ]
    
    def return_longest_streak_all(self) -> int:
        """HABITLIST: returns longest streak of all habits"""
        #longest: int = -1
        #ft = filter(, self.habitlist)
        # TODO: check behaviour when multiple values or empty
        return max([length.streak for length in self._habitlist])
        
        
    def return_longest_streak(self, habit: Habit) -> int:
        # TODO: check behaviour when returning multiple values or empty
        return max([stored_habit.streak for stored_habit in self._habitlist
                     if stored_habit == habit ])
        
    def add_habit(self, habit: Habit) -> None:
        """HABITLIST: adds Habit instance to Habitlist, and updates counter"""
        self._habitlist.append(habit)
        self._len += 1
        #breakpoint()


if __name__ == "__main__":
    print("This module is for importing, not for running directly")