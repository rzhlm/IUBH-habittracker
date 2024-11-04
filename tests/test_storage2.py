import pytest
from src.storage2 import Storage
from src.habit import Period, Habit, HabitList
from tests.test_habit import create_habits, habit_list
#from typing import List, Callable
import os

st = Storage()
testfile: str = "test_save.sav"

"""
@pytest.fixture
def create_habits() -> List[Habit]:
    #Habit(description=, creation_data=, period=, isTracked=, streak=)
    return [
        Habit(description="daily_Habit_tracked", creation_data="2023-11-1", 
              period=Period.daily, isTracked=True, streak=5),
        Habit(description="weekly_not_tracked",creation_data="2023-11-1",
              period=Period.weekly, isTracked=False, streak=5),
        Habit(description="montly_tracked", creation_data="2023-11-1",
               period=Period.monthly, isTracked=True, streak=11),
        Habit(description="daily_tracked2", creation_data="2023-11-1",
               period=Period.daily, isTracked=True, streak=16),
        Habit(description="daily_tracked3", creation_data="2023-11-1",
               period=Period.daily, isTracked=False, streak=17),
        Habit(description="daily_tracked3", creation_data="2023-12-1",
               period=Period.daily, isTracked=True, streak=17),               
        
    ]

"""

def test_save(habit_list, testfile: str):
    
    if os.path.exists(testfile):
        os.remove(testfile)
        
    #ch: List[Habit] = create_habits()
    #hl : HabitList = habit_list
    #hl = habit_list(ch)
    st.save(habit_list, testfile)
    assert os.path.exists(testfile)
    os.remove(testfile)
    
    

def test_load(testfile: str):
    
    st.save(habit_list, testfile)
    hl = st.load(testfile)
    for habit, load_habit in zip(habit_list._habitlist, hl._habitlist):
        assert habit.description == load_habit.description
        assert habit.creation_data == load_habit.creation_data
        assert habit.period == load_habit.period
        assert habit.isTracked == load_habit.isTracked
        assert habit.streak == load_habit.streak
    os.remove(testfile)


def test_to_JSON():
    pass

def test_from_JSON():
    pass