import pytest #apparently not needed according to typechecker. Works without
from src.storage2 import Storage
from src.habit import Habit, HabitList #, Period
from tests.test_habit import habit_list, create_habits # noqa # type: ignore
#from typing import List
import os

#st = Storage()


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


testfile_name: str = "test_save.sav"
testdatefile_name: str = "test_date_save.sav"
testdate_date: str = "2020-1-1"

@pytest.fixture
def testfile() -> str:
    return testfile_name

@pytest.fixture
def test_date_file() -> str:
    return testdatefile_name

@pytest.fixture
def date() -> str:
    return testdate_date

@pytest.fixture
def st() -> Storage:
    return Storage()

def test_save(st: Storage, habit_list: HabitList, testfile: str):
    # in order to make the savefile, comment out all the os.remove

    if os.path.exists(testfile):
        os.remove(testfile)
        # ↑ this one should be uncommented normally
        pass
    st.HL_save(habit_list, testfile)
    #st.save(habit_list)
    assert os.path.exists(testfile)
    os.remove(testfile)
    # ↑ this one should be uncommented normally
    
    #_ = habit_list
    #_ = create_habits
    

def test_load(st: Storage, habit_list: HabitList, testfile: str):
    
    st.HL_save(habit_list, testfile)
    hl: HabitList = st.HL_load(testfile)
    #hl: HabitList = st.load()
    for habit, load_habit in zip(habit_list.return_all(), hl.return_all()):
        assert habit.description == load_habit.description
        assert habit.creation_data == load_habit.creation_data
        assert habit.period == load_habit.period
        assert habit.isTracked == load_habit.isTracked
        assert habit.streak == load_habit.streak
    os.remove(testfile)
    # ↑ this one should be uncommented normally


def test_to_JSON(st: Storage, create_habits: list[Habit]):
    first_habit = create_habits[0]
    #print(st.to_JSON(first_habit))
    correct: dict[str, str|int|bool] =  {
        "id": 1,
        "description": "daily_Habit_tracked",
        "creation_data": "2023-11-1",
        "period": "daily",
        "isTracked": True,
        "streak": 5,
        "last_complete" : "2023-11-1",
        }
    assert st.to_JSON(first_habit) == correct


def test_from_JSON(st: Storage, ):
    test_habit: dict[str, str|int|bool] = {
        "id" : 1,
        "description": "daily_Habit_tracked",
        "creation_data": "2023-11-1",
        "period": "daily",
        "isTracked": True,
        "streak": 5,
        "last_complete": "2023-11-1",
        }
    habit = st.from_JSON(test_habit)

    assert habit.description == test_habit["description"]
    assert habit.creation_data == test_habit["creation_data"]
    assert habit.period.name == test_habit["period"]
    assert habit.isTracked == test_habit["isTracked"]
    assert habit.streak == test_habit["streak"]


def test_save_date(st: Storage, date: str, test_date_file: str) -> None:
    if os.path.exists(test_date_file):
        os.remove(test_date_file)
        # ↑ this one should be uncommented normally
    st.date_save(date, test_date_file)
    assert os.path.exists(test_date_file)
    os.remove( test_date_file)

def test_date_load(st: Storage, date: str, test_date_file: str):
    st.date_save(date, test_date_file)
    date_loaded: str = st.date_load(test_date_file)
    assert date == date_loaded
    os.remove(test_date_file)
    # ↑ this one should be uncommented normally
