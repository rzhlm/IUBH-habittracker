import pytest
from copy import deepcopy

from src.habit import Period, Habit, HabitAnalysis, BestStreak


# ##############################################################################
# FIXTURES

@pytest.fixture
def create_habits() -> list[Habit]:
    
    return [
        Habit(
            id=1,
            description = "daily_Habit_tracked",
            creation_data="2023-09-01",
            period=Period.daily,
            is_tracked=True,
            streak=5,
            last_complete = "2023-11-01",
            record = BestStreak("2023-10-01", 10),
            ),
        Habit(
            id = 2,
            description = "weekly_not_tracked",
            creation_data="2023-09-01",
            period = Period.weekly,
            is_tracked = False,
            streak=5,
            last_complete = "2023-11-01",
            record = BestStreak("2023-10-01", 10),
            ),            
        Habit(
            id = 3,
            description = "montly_tracked",
            creation_data="2023-09-01",
            period=Period.monthly,
            is_tracked=True,
            streak=11,
            last_complete = "2023-11-01",
            record = BestStreak("2023-10-01", 10),
            ),
        Habit(
            id = 4,
            description = "daily_tracked2",
            creation_data="2023-09-01",
            period = Period.daily,
            is_tracked = True,
            streak=16,
            last_complete = "2023-11-01",
            record = BestStreak("2023-10-01", 10),
            ),
        Habit(
            id=5,
            description="daily_tracked3",
            creation_data="2023-09-01",
            period=Period.daily,
            is_tracked=False,
            streak=17,
            last_complete="2023-11-01",
            record = BestStreak("2023-10-01", 10),
            ),
        Habit(
            id = 6,
            description = "daily_tracked3",
            creation_data="2023-09-01",
            period = Period.daily,
            is_tracked = True,
            streak = 17,
            last_complete = "2023-11-01",
            record = BestStreak("2023-10-01", 10),
            ),        
    ]

@pytest.fixture
def habit_list(create_habits: list[Habit]) -> HabitAnalysis:
    #hl: HabitList = HabitList(create_habits)
    #return hl
    return HabitAnalysis(create_habits)

# ##############################################################################
# FUNCTIONS

def test_get_len(habit_list: HabitAnalysis, create_habits: list[Habit]):
    """Test that get_len() returns the correct number of habits"""
    expected = len(create_habits)
    actual = habit_list.get_len()
    assert actual == expected

def test_add_habit(habit_list: HabitAnalysis):
    """Test that .add_havit() correctly adds habits"""
    to_add: Habit = Habit(id = 10, 
                          description = "desc", 
                          creation_data = "2023-01-01",
                          period = Period.monthly,
                          is_tracked = True,
                          streak = 6,
                          last_complete = "2023-01-01",
                          record = BestStreak("2023-10-01", 10),
                          )
    habit_list.add_habit(to_add)
    assert to_add in habit_list.return_all()

def test_get_habit_by_id(habit_list: HabitAnalysis, 
                         create_habits: list[Habit]):
    """Test that .get_habit_by_id() returns the correct habit"""
    for expected in create_habits:
        retrieved_habit = habit_list.get_habit_by_id(expected.id)
        assert retrieved_habit == expected

def test_update_habit(habit_list: HabitAnalysis):
    """Test that .update_habit() updates correctly"""
    original = habit_list.get_habit_by_id(1)
    
    updated_habit = deepcopy(original)
    updated_habit.description = "UPDATE TEST"
    updated_habit.streak = 111
    
    habit_list.update_habit(updated_habit)
    new_habit = habit_list.get_habit_by_id(1)
    assert new_habit.description == "UPDATE TEST"
    assert new_habit.streak == 111

def test_return_all(habit_list: HabitAnalysis, create_habits: list[Habit]):
    """Test that .return_all() returns all habits, aslo untracked & deleted"""
    all_ = habit_list.return_all()
    assert len(all_) == len(create_habits)
    assert all_ == create_habits

def test_return_tracked(habit_list: HabitAnalysis):
    """Test that .return_tracked returns only the tracked habits
    (not the deleted or untracked)"""
    tracked : list[Habit] = habit_list.return_tracked()
    assert len(tracked) == 4
    for habit in tracked:
        assert habit.is_tracked
        assert habit.streak != -1

    
def test_return_same_period(habit_list: HabitAnalysis):
    same_period : list[Habit] = habit_list.return_same_period(Period.daily)
    assert len(same_period) == 3
    for habit in same_period:
        assert habit.period == Period.daily
        assert habit.is_tracked
        assert habit.streak != -1

def test_return_current_longest_streak_all(habit_list: HabitAnalysis):
    """Test that .return_current_longest_streak_all 
    returns the habit with the highest streak"""
    longest_habit = habit_list.return_current_longest_streak_all()
    assert longest_habit.streak == 17


#@pytest.mark.xfail
# def test_return_current_longest_streak_specific(habit_list: HabitAnalysis,
#                                 create_habits: list[Habit]):
#     habits: Habit = create_habits[0]
#     assert habit_list\
#         .return_current_longest_streak_period(habits) == ("2023-11-01", 5)


def test_return_past_longest_streak_all(habit_list: HabitAnalysis):
    """Test that .return_past_longest_streak_all returns BestStreak for
    habit with the highest past streak.
    """
    for index, habit in enumerate(habit_list._habitlist): # type: ignore
        if habit.id == 3:
            habit.record = BestStreak("2023-09-30", 20)
            habit_list._habitlist[index] = habit  # type: ignore
            break
    
    best_record = habit_list.return_past_longest_streak_all()
    assert best_record.max_streak == 20
    assert best_record.on_date == "2023-09-30"
