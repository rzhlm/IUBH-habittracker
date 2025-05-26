import pytest
#from typing import List

from src.habit import Period, Habit, HabitAnalysis, BestStreak

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

def test_return_tracked(habit_list: HabitAnalysis):
    tracked : list[Habit] = habit_list.return_tracked()
    assert len(tracked) == 4
    for habit in tracked:
        assert habit.is_tracked

def test_return_same_period(habit_list: HabitAnalysis):
    same_period : list[Habit] = habit_list.return_same_period(Period.daily)
    assert len(same_period) == 3
    for habit in same_period:
        assert habit.period == Period.daily

def test_return_longest_streak_all(habit_list: HabitAnalysis):
    assert habit_list.return_longest_streak_all() == 17

#@pytest.mark.xfail
def test_return_longest_streak(habit_list: HabitAnalysis,
                                create_habits: list[Habit]):
    habits: Habit = create_habits[0]
    assert habit_list\
        .return_longest_streak_specific(habits) == ("2023-11-01", 5)

def test_add_habit(habit_list: HabitAnalysis):
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