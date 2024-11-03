import pytest
from typing import List

from src.habit import Period, Habit, HabitList

@pytest.fixture
def create_habits() -> List[Habit]:
    #Habit(description=, creation_data=, period=, isTracked=, streak=)
    return [
        Habit(description="daily_Habit_tracked", creation_data="2024-11-1", 
              period=Period.daily, isTracked=True, streak=5),
        Habit(description="weekly_not_tracked",creation_data="2024-11-1",
              period=Period.weekly, isTracked=False, streak=5),
        Habit(description="montly_tracked", creation_data="2024-11-1",
               period=Period.monthly, isTracked=True, streak=11)
        
    ]

@pytest.fixture()
def create_habit_list(create_habits: List[Habit]):
    hl: HabitList = HabitList(create_habits)
    return hl

def test_period():
    pass

def test_habit():
    pass

def test_return_tracked():
    pass

def test_return_same_period():
    pass

def test_return_longest_streak_all():
    pass

def test_return_longest_streak():
    pass

def test_add_habit():
    pass