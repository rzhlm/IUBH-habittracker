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
    timeline: List[]
    isTracked: bool

@dataclass
class HabitList:
    habitlist : List[Habit]
