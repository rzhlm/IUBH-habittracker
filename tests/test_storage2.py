from __future__ import annotations
from typing import Any
import os
from dataclasses import asdict

import pytest

from tests.test_habit import habit_list, create_habits # noqa # type: ignore
from src.model.storage import Storage
from src.model.habit import Habit, HabitAnalysis


# ##############################################################################
# Definitions

testfile_name: str = "test_save.sav"
testdatefile_name: str = "test_date_save.sav"
testdate_date: str = "2020-01-01"

# ##############################################################################
# Fixtures

@pytest.fixture
def testfile() -> str:
    """Fixture which fixes the testfile name"""
    return testfile_name

@pytest.fixture
def test_date_file() -> str:
    """Fixture which fixes the testdatefile name"""
    return testdatefile_name

@pytest.fixture
def date() -> str:
    """fixture which returns a string with the date"""
    return testdate_date

@pytest.fixture
def st() -> Storage:
    """Fixture which fixes a Storage instance"""
    return Storage()

# ##############################################################################
# Test functions

def test_save(st: Storage, habit_list: HabitAnalysis, testfile: str):
    """tests the save function"""
    # in order to make a savefile, comment out all the os.remove
    # the savefile will ocnsist of the test data.
    if os.path.exists(testfile):
        os.remove(testfile)
        # ↑ this one should be uncommented normally
        pass
    st.HL_save(habit_list, testfile)
    assert os.path.exists(testfile)
    os.remove(testfile)
    # ↑ this one should be uncommented normally
    
def test_load(st: Storage, habit_list: HabitAnalysis, testfile: str):
    """tests the load function"""
    st.HL_save(habit_list, testfile)
    hl: HabitAnalysis = st.HL_load(testfile)
    for habit, load_habit in zip(habit_list.return_all(), hl.return_all()):
        assert habit.id == load_habit.id
        assert habit.description == load_habit.description
        assert habit.creation_data == load_habit.creation_data
        assert habit.period == load_habit.period
        assert habit.is_tracked == load_habit.is_tracked
        assert habit.streak == load_habit.streak
        assert habit.last_complete == load_habit.last_complete
        assert habit.record == load_habit.record
    os.remove(testfile)
    # ↑ this one should be uncommented normally

def test_to_JSON(st: Storage, create_habits: list[Habit]):
    """tests that a Habit converts to JSON properly"""
    first_habit = create_habits[0]
    correct: dict[str, Any] =  {
        "id": 1,
        "description": "daily_Habit_tracked",
        "creation_data": "2023-09-01",
        "period": "daily",
        "is_tracked": True,
        "streak": 5,
        "last_complete" : "2023-11-01",
        "record": {"on_date": "2023-10-01", "max_streak": 10},
        }
    assert st.to_JSON(first_habit) == correct

def test_from_JSON(st: Storage, ):
    """tests that JSON converts to a Habit"""
    test_habit: dict[str, Any] = {
        "id" : 1,
        "description": "daily_Habit_tracked",
        "creation_data": "2023-09-01",
        "period": "daily",
        "is_tracked": True,
        "streak": 5,
        "last_complete": "2023-11-01",
        "record": {"on_date": "2023-10-01", "max_streak": 10},
        }
    habit: Habit = st.from_JSON(test_habit)

    assert habit.id == test_habit["id"]
    assert habit.description == test_habit["description"]
    assert habit.creation_data == test_habit["creation_data"]
    assert habit.period.name == test_habit["period"]
    assert habit.is_tracked == test_habit["is_tracked"]
    assert habit.streak == test_habit["streak"]
    assert habit.last_complete == test_habit["last_complete"]
    assert asdict(habit.record) == test_habit["record"]

def test_save_date(st: Storage, date: str, test_date_file: str) -> None:
    """tests that the date is stored into the datefile"""
    if os.path.exists(test_date_file):
        os.remove(test_date_file)
        # ↑ this one should be uncommented normally
    st.date_save(date, test_date_file)
    assert os.path.exists(test_date_file)
    os.remove(test_date_file)

def test_date_load(st: Storage, date: str, test_date_file: str):
    """tests that the date loads from the savefile"""
    st.date_save(date, test_date_file)
    date_loaded: str = st.date_load(test_date_file)
    assert date == date_loaded
    os.remove(test_date_file)
    # ↑ this one should be uncommented normally
