from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List

class Period(Enum):
    daily = auto()
    weekly = auto()
    monthly = auto()

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
    # Use @property method for streak calculation?
    # But how to know beforehand if at currenttime streak is still valid?
    def toggle_tracked(self):
        self.isTracked = not self.isTracked
    def un_track(self):
        self.isTracked = False
    def track(self):
        self.isTracked = True

@dataclass
class HabitList:
    _habitlist : List[Habit] = field(default_factory=list)
    _len : int = 0

    def return_all(self) -> List[Habit]:
        return self._habitlist
    
    def return_tracked(self) -> List[Habit]:
        return [habit for habit in self._habitlist if habit.isTracked]
    
    def return_same_period(self, period: Period) -> List[Habit]:
        return [habit for habit in self._habitlist
                 if habit.period == period and habit.isTracked]
    
    def return_longest_streak_all(self) -> int:
        #longest: int = -1
        #ft = filter(, self.habitlist)
        # TODO: check behaviour when multiple values or empty
        return max([length.streak for length in self._habitlist])
        
        
    def return_longest_streak(self, habit: Habit) -> int:
        # TODO: check behaviour when returning multiple values or empty
        return max([stored_habit.streak for stored_habit in self._habitlist
                     if stored_habit == habit ])
        
    def add_habit(self, habit: Habit) -> None:
        self._habitlist.append(habit)


        