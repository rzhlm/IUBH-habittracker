import datetime as dt
from copy import deepcopy

import pytest

from tests.test_habit import habit_list, create_habits  # type: ignore
from tests.test_storage2 import st # type: ignore
# type checker keeps complaining about the fixtures not being used!

from src.controller import Controller
from src.habit import Habit, HabitAnalysis, Period, BestStreak
from src.constants import Settings
from src.storage2 import Storage

# ##############################################################################
# FIXTURES

@pytest.fixture
def controller(habit_list: HabitAnalysis, st: Storage) -> Controller:
    """Fixes a Controller instance"""
    return Controller(habit_list, st)

# ##############################################################################
# TEST FUNCTIONS

def test_init_done_indicator_list(controller: Controller, habit_list: HabitAnalysis):
    """tests init_done_indicator_list: create a DoneIndicator
    per tracked habit."""
    tracked_habits = habit_list.return_tracked()
    indicators = controller.done_indicator.data
    assert len(indicators) == len(tracked_habits)
    
    tracked_ids = {habit.id for habit in tracked_habits}
    indicator_ids = {di.id for di in indicators}
    assert indicator_ids == tracked_ids

def test_addto_indicator_list(controller: Controller):
    """tests addto_indicator_list: append DoneIndicator
    to the controller's done_indicator list."""
    initial = len(controller.done_indicator.data)
    new_habit = Habit(
        id=999,
        description="Dummy Habit",
        creation_data=controller.current_date.strftime(Settings().DTSTRF),
        period=Period.daily,
        is_tracked=True,
        streak=0,
        last_complete="1900-01-01",
        record=BestStreak("1900-01-01", -1)
    )
    controller.addto_indicator_list(new_habit)
    assert len(controller.done_indicator.data) == initial + 1
    assert any(di.id == 999 for di in controller.done_indicator.data)

def test_dt_to_str_and_str_to_dt(controller: Controller):
    """test dt_to_str and str_to_dt (DateTime to str and back)"""
    orig_date = controller.current_date
    date_str = controller.dt_to_str(orig_date)
    converted = controller.str_to_dt(date_str)
    
    assert converted == orig_date

def test_are_all_habits_marked(controller: Controller):
    """test are_all_habits_marked: when every DoneIndicator is marked"""
    
    assert not controller.are_all_habits_marked()

    for di in controller.done_indicator.data:
        di.marked = True
    assert controller.are_all_habits_marked()

def test_is_ready_to_advance(controller: Controller):
    """test is_ready_to_advance: True when every DoneIndicators marked,
    for the current day."""
    
    assert not controller.is_ready_to_advance()

    for di in controller.done_indicator.data:
        di.marked = True
    
    assert controller.is_ready_to_advance()
    assert controller.ready_to_advance

def test_mark_habit_done(controller: Controller, habit_list: HabitAnalysis):
    """test mark_habit_done: update habit.last_complete equal 
    to controller.current_date"""
    tracked = habit_list.return_tracked()
    test_habit = deepcopy(tracked[0])
    exp_date_str = controller.current_date.strftime(Settings().DTSTRF)
    controller.mark_habit_done(test_habit)
    assert test_habit.last_complete == exp_date_str
    
    for di in controller.done_indicator.data:
        if di.id == test_habit.id:
            assert di.marked and di.done
            break
    else:
        pytest.fail("DoneIndicator for the updated habit not found.")

def test_mark_habit_not_done(controller: Controller, habit_list: HabitAnalysis):
    """test mark_habit_not_done: mark DoneIndicator, 
    but not set the 'done' flag."""
    tracked = habit_list.return_tracked()
    test_habit = deepcopy(tracked[0])
    
    for di in controller.done_indicator.data:
        if di.id == test_habit.id:
            di.marked = False
            di.done = False

    controller.mark_habit_not_done(test_habit)

    for di in controller.done_indicator.data:
        if di.id == test_habit.id:
            assert di.marked and not di.done
            break

def test_is_habit_done_timely(controller: Controller, habit_list: HabitAnalysis):
    """test is_habit_done_timely: True when habit.last_complete is timely
    for that period."""
    habit = deepcopy(habit_list.return_all()[0])
    
    habit.last_complete = controller.current_date.strftime(Settings().DTSTRF)
    assert controller.is_habit_done_timely(habit)
    
    past = controller.current_date - dt.timedelta(days=2)
    habit.last_complete = past.strftime(Settings().DTSTRF)
    if habit.period == Period.daily:
        assert not controller.is_habit_done_timely(habit)

def test_update_streak(controller: Controller, habit_list: HabitAnalysis):
    """test update_streak: increment streak. If new streak 
    above habit.record.max_streak, the BestStreak updates"""
    habit = deepcopy(habit_list.return_all()[0])
    orig_record = habit.record.max_streak
    habit.streak = orig_record
    controller.update_streak(habit)
    assert habit.streak == orig_record + 1
    assert habit.record.max_streak == habit.streak

def test_do_advance_date(controller: Controller, habit_list: HabitAnalysis):
    """test do_advance_date: advance controller.current_date by one day,
    update habit streaks, reinitialize the done_indicator list."""
    for di in controller.done_indicator.data:
        di.marked = True
    
    current_str = controller.current_date.strftime(Settings().DTSTRF)
    for habit in habit_list.return_all():
        habit.last_complete = current_str
    
    old_date = controller.current_date
    controller.do_advance_date()
    assert controller.current_date == old_date + dt.timedelta(days=1)
    assert controller.done_indicator.today == controller.current_date

def test_return_unmarked_habits(controller: Controller):
    """test return_unmarked_habits: return habits where done_indicator
    is not yet marked."""
    
    unmarked = controller.return_unmarked_habits()
    tracked_ids = {h.id for h in controller.do_showlist_tracked()}
    unmarked_ids = {h.id for h in unmarked}
    assert unmarked_ids == tracked_ids
    
    if controller.done_indicator.data:
        controller.done_indicator.data[0].marked = True
    new_unmarked = controller.return_unmarked_habits()
    assert len(new_unmarked) == len(controller.done_indicator.data) - 1

def test_do_showlist(controller: Controller, habit_list: HabitAnalysis):
    """test do_showlist:  return same as habitlist.return_all()."""
    assert controller.do_showlist() == habit_list.return_all()

def test_do_showlist_tracked(controller: Controller, habit_list: HabitAnalysis):
    """test do_showlist_tracked: return the tracked habits."""
    assert controller.do_showlist_tracked() == habit_list.return_tracked()

def test_do_showlist_period(controller: Controller, habit_list: HabitAnalysis):
    """Test do_showlist_period: return habits by period"""
    period = Period.daily
    assert \
        controller\
            .do_showlist_period(period) == habit_list\
                                                .return_same_period(period)

def test_do_add(controller: Controller, habit_list: HabitAnalysis):
    """Test do_add: create a new habit, add it to the habitlist, 
    store in done indicator"""
    orig_len = habit_list.get_len()
    controller.do_add(Period.daily, "NEW TEST HABIT")
    new_len = habit_list.get_len()
    assert new_len == orig_len + 1
    
    new_ids = {
                h.id
                for h in habit_list.return_all()
                if h.description == "NEW TEST HABIT"
            }
    indicator_ids = {
                    di.id
                    for di in controller.done_indicator.data
                    }
    assert new_ids.issubset(indicator_ids)

def test_do_delete_and_do_edit(controller: Controller, habit_list: HabitAnalysis):
    """Test do_delete: mark a habit as deleted"""
    original = habit_list._habitlist[0] # type: ignore
    habit_copy = deepcopy(original)
    controller.do_delete(habit_copy)
    updated = habit_list.get_habit_by_id(habit_copy.id)
    assert updated.streak == -1

    # Now change the description and update via do_edit.
    habit_edit = deepcopy(updated)
    habit_edit.description = "Edited Description"
    controller.do_edit(habit_edit)
    updated_after = habit_list.get_habit_by_id(habit_edit.id)
    assert updated_after.description == "Edited Description"

def test_do_help(controller: Controller):
    """Test for do_help, looking for words in the return string"""
    help_text = controller.do_help()
    assert "HELP" in help_text
    assert "Quick mark" in help_text

