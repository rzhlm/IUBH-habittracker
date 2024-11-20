import pytest
from typing import List

from src.habit import Period, Habit, HabitList

@pytest.fixture
def create_habits() -> List[Habit]:
    #Habit(description=, creation_data=, period=, isTracked=, streak=)
    return [
        Habit(id=1, description="daily_Habit_tracked", creation_data="2023-11-1", 
              period=Period.daily, isTracked=True, streak=5),
        Habit(id=2, description="weekly_not_tracked",creation_data="2023-11-1",
              period=Period.weekly, isTracked=False, streak=5),
        Habit(id=3, description="montly_tracked", creation_data="2023-11-1",
               period=Period.monthly, isTracked=True, streak=11),
        Habit(id=4, description="daily_tracked2", creation_data="2023-11-1",
               period=Period.daily, isTracked=True, streak=16),
        Habit(id=5, description="daily_tracked3", creation_data="2023-11-1",
               period=Period.daily, isTracked=False, streak=17),
        Habit(id=6, description="daily_tracked3", creation_data="2023-12-1",
               period=Period.daily, isTracked=True, streak=17),               
        
    ]

@pytest.fixture
def habit_list(create_habits: List[Habit]) -> HabitList:
    #hl: HabitList = HabitList(create_habits)
    #return hl
    return HabitList(create_habits)
"""
def test_period():
    pass

    
def test_habit():
    pass
"""

def test_return_tracked(habit_list: HabitList):
    tracked : List[Habit] = habit_list.return_tracked()
    assert len(tracked) == 4
    for habit in tracked:
        assert habit.isTracked

def test_return_same_period(habit_list: HabitList):
    same_period : List[Habit] = habit_list.return_same_period(Period.daily)
    assert len(same_period) == 3
    for habit in same_period:
        assert habit.period == Period.daily

def test_return_longest_streak_all(habit_list: HabitList):
    assert habit_list.return_longest_streak_all() == 17

#@pytest.mark.xfail
def test_return_longest_streak(habit_list: HabitList,
                                create_habits: List[Habit]):
    habits: Habit = create_habits[0]
    assert habit_list.return_longest_streak(habits) == 5

def test_add_habit(habit_list: HabitList):
    to_add: Habit = Habit(id=10, 
                          description = "desc", 
                          creation_data = "2023-1-1",
                        period = Period.monthly,
                         isTracked = True,
                        streak = 6,
                        )
    habit_list.add_habit(to_add)
    assert to_add in habit_list.return_all()