from dataclasses import dataclass
from enum import Enum, auto
from typing import List

class Period(Enum):
    daily = auto()
    weekly = auto()
    monthly = auto()

@dataclass
class Habit:
    id: int
    description: str
    period: Period
    #timeline: List[]
    isTracked: bool

@dataclass
class HabitList:
    habitlist : List[Habit]

    def return_all(self) -> List[Habit]:
        return [habit for habit in self.habitlist if habit.isTracked]
    
    def return_same_period(self, period: Period) -> List[Habit]:
        return [habit for habit in self.habitlist if habit.period == period]
    