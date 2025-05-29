import pytest
from copy import deepcopy

from src.model.habit import Period, Habit, HabitAnalysis, BestStreak


# ##############################################################################
# FIXTURES

@pytest.fixture
def create_habits() -> list[Habit]:
    """Fixture which fixes a list of Habits to use in testing"""
    
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
    """Fixture which transforms the previous fixture
    into a HabitAnalysis instance"""
    #hl: HabitList = HabitList(create_habits)
    #return hl
    return HabitAnalysis(create_habits)

# ##############################################################################
# FUNCTIONS

def test_register_observer(habit_list: HabitAnalysis) -> None:
    """Test register_observer: appends in observer list"""
    calls: list[str] = []
    
    def observer() -> None:
        calls.append("observer called")
    assert observer not in habit_list._observers # type: ignore
    
    habit_list.register_observer(observer)
    assert observer in habit_list._observers # type: ignore

def test_notify_observers(habit_list: HabitAnalysis) -> None:
    """Test notify_observers: calls all callbacks."""
    
    call_count: list[int] = [0, 0]
    def observer1() -> None:
        call_count[0] += 1

    def observer2() -> None:
        call_count[1] += 1

    habit_list.register_observer(observer1)
    habit_list.register_observer(observer2)
    habit_list.notify_observers()
    assert call_count[0] == 1
    assert call_count[1] == 1

def test_get_len(habit_list: HabitAnalysis, create_habits: list[Habit]):
    """Test that get_len() returns the correct number of habits"""
    expected = len(create_habits)
    actual = habit_list.get_len()
    assert actual == expected

def test_add_habit(habit_list: HabitAnalysis):
    """Test that add_havit() correctly adds habits"""
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
    """Test that get_habit_by_id() returns the correct habit"""
    for expected in create_habits:
        retrieved_habit = habit_list.get_habit_by_id(expected.id)
        assert retrieved_habit == expected

def test_update_habit(habit_list: HabitAnalysis):
    """Test that update_habit() updates correctly"""
    original: Habit = habit_list.get_habit_by_id(1)
    
    updated_habit: Habit = deepcopy(original)
    updated_habit.description = "UPDATE TEST"
    updated_habit.streak = 111
    
    habit_list.update_habit(updated_habit)
    new_habit: Habit = habit_list.get_habit_by_id(1)
    assert new_habit.description == "UPDATE TEST"
    assert new_habit.streak == 111

def test_return_all(habit_list: HabitAnalysis, create_habits: list[Habit]):
    """Test that return_all() returns all habits, aslo untracked & deleted"""
    all_: list[Habit] = habit_list.return_all()
    assert len(all_) == len(create_habits)
    assert all_ == create_habits

def test_return_tracked(habit_list: HabitAnalysis):
    """Test that return_tracked returns only the tracked habits
    (not the deleted or untracked)"""
    tracked : list[Habit] = habit_list.return_tracked()
    assert len(tracked) == 4
    for habit in tracked:
        assert habit.is_tracked
        assert habit.streak != -1
    
def test_return_same_period(habit_list: HabitAnalysis):
    """Test that return_same_period returns habits only with that period"""
    same_period : list[Habit] = habit_list.return_same_period(Period.daily)
    assert len(same_period) == 3
    for habit in same_period:
        assert habit.period == Period.daily
        assert habit.is_tracked
        assert habit.streak != -1

def test_return_current_longest_streak_all(habit_list: HabitAnalysis):
    """Test that return_current_longest_streak_all 
    returns the habit with the highest streak"""
    longest_habit: Habit = habit_list.return_current_longest_streak_all()
    assert longest_habit.streak == 17

#@pytest.mark.xfail
# def test_return_current_longest_streak_specific(habit_list: HabitAnalysis,
#                                 create_habits: list[Habit]):
#     habits: Habit = create_habits[0]
#     assert habit_list\
#         .return_current_longest_streak_period(habits) == ("2023-11-01", 5)

def test_return_past_longest_streak_all(habit_list: HabitAnalysis):
    """Test that return_past_longest_streak_all returns BestStreak for
    habit with the highest past streak.
    """
    for index, habit in enumerate(habit_list._habitlist): # type: ignore
        if habit.id == 3:
            habit.record = BestStreak("2023-09-30", 20)
            habit_list._habitlist[index] = habit  # type: ignore
            break
    
    best: Habit = habit_list.return_past_longest_streak_all()
    assert best.record.max_streak == 20
    assert best.record.on_date == "2023-09-30"


def test_return_current_longest_streak_period(habit_list: HabitAnalysis):
    """Test that return_current_longest_streak_period returns habit with
    highest current streak for that period (or None)."""
    
    daily_habit: Habit|None = habit_list.return_current_longest_streak_period(Period.daily)
    assert daily_habit is not None
    assert daily_habit.period == Period.daily
    assert daily_habit.streak == 17
    assert daily_habit.id == 6

    weekly_habit: Habit|None = habit_list.return_current_longest_streak_period(Period.weekly)
    assert weekly_habit is None

    monthly_habit: Habit|None = habit_list\
                        .return_current_longest_streak_period(Period.monthly)
    assert monthly_habit is not None
    assert monthly_habit.period == Period.monthly
    assert monthly_habit.streak == 11
    assert monthly_habit.id == 3


def test_return_past_longest_streak_period(habit_list: HabitAnalysis):
    """Test that return_past_longest_streak_period returns habit with 
    top past streak, for the period (or None)."""
    
    # modify the BestStreak fixtures, as they all use the same values.

    # daily
    for idx, habit in enumerate(habit_list._habitlist): # type: ignore
        if habit.period == Period.daily and habit.id == 4:
            habit.record = BestStreak("2023-11-22", 20)
            habit_list._habitlist[idx] = habit # type: ignore
            break

    # monthly
    for idx, habit in enumerate(habit_list._habitlist): # type: ignore
        if habit.period == Period.monthly:
            habit.record = BestStreak("2023-11-23", 25)
            habit_list._habitlist[idx] = habit  # type: ignore
            break

    daily_habit = habit_list.return_past_longest_streak_period(Period.daily)
    assert daily_habit is not None
    assert daily_habit.period == Period.daily
    assert daily_habit.id == 4
    assert daily_habit.record.max_streak == 20

    weekly_habit = habit_list.return_past_longest_streak_period(Period.weekly)
    assert weekly_habit is not None
    assert weekly_habit.period == Period.weekly
    assert weekly_habit.record.max_streak == 10

    monthly_habit = habit_list.return_past_longest_streak_period(Period.monthly)
    assert monthly_habit is not None
    assert monthly_habit.period == Period.monthly
    assert monthly_habit.record.max_streak == 25