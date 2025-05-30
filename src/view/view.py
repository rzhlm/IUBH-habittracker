from __future__ import annotations
from typing import TYPE_CHECKING
import os
import datetime as dt
from copy import deepcopy
from collections.abc import Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod

from src.model.constants import Motivational
from src.model.habit import Period
from src.view.colorprint import cprint


if TYPE_CHECKING:
    from src.controller.controller import Controller
    from src.model.habit import Habit

# TODO: add debug & info logging

# initialize custom color-print functions (curried), in this namespace
yprint: Callable[[str],None] = cprint() # yellow print func
rprint: Callable[[str],None] = cprint("\033[31m") #red print func
tprint: Callable[[str],None] = cprint("\t") # adds a tab in front

@dataclass
class MenuChoices:
    """VIEW: the data structure to bundle a TUI-menu-item"""
    name: str
    command: str
    func: Callable[[], None]
    

class View(ABC):
    """VIEW: The ABC from which GUI, TUI and others inherit"""
    #single_instance = True

    @abstractmethod
    def interact(self):
        pass

class GUI(View):
    """VIEW: placeholder for GUI class"""
    def interact(self):
        pass


class TUI(View):
    """VIEW: The TUI class, with all of its methods
    The flow (REPL) is as follows:
    # TUI: 
    # interact -> splash -> help -> show_menulist -> mainmenu_input
    #
    # interact
    #   -> Splash
    #   -> Help, instructions
    #   REPL:
    #       -> Show Menulist
    #       -> take input
    #       input valid:
    #           -> mainmenu_input
    #               -> goto chosen function
    #       input invalid:
    #           -> error message    
    """

    def __init__(self, controller: Controller):
        
        self.repl_quit: bool = False
        self.controller: Controller = controller
        self.choices: list[MenuChoices] = self.init_menulist()
        self.colors: dict[str, str] = {
            "red": "\033[31m",
            "yellow" : "\033[0;33m",
            "green" : "\033[0;32m",
            "reset" : "\033[0m",
        }

    def get_date(self) -> dt.datetime:
        """VIEW/TUI: gets date value from controller instance"""
        return self.controller.current_date

    def init_menulist(self) -> list[MenuChoices]:
        """VIEW/TUI: initializes the menulist"""
        # TODO: add setter & check for duplicate commands
        return [
        MenuChoices("Main menu / Clear","m", self.goto_main),
        MenuChoices("Advance date","adv", self.goto_advance_date),
        MenuChoices("Quick mark","qm",self.begin_quickmark),
        MenuChoices("Analysis", "a", self.goto_analysis),
        MenuChoices("Show list (all) (EXPERT MODE, " +\
                    "shows deleted & untracked)", "sl", self.goto_showlist),
        MenuChoices(" Show list (tracked)", "slt", self.goto_showlist_tracked),
        MenuChoices(" Show list (same period, tracked)", "slp", self.goto_showlist_period),
        MenuChoices("Add Habit", "ah", self.goto_add),
        MenuChoices("Edit Habit", "e", self.begin_edit),
        MenuChoices("----", "-", self.clear),
        MenuChoices("Help", "?", self.goto_help),
        MenuChoices("Quit","q", self.goto_quit),
        ]
        
    def splash_screen(self) -> None:
        """VIEW/TUI: displays splash screen"""
        
        welcome = """
            WELCOME TO THE HABIT TRACKING APP !
            ===================================
        """
        
        self.clear()
        print(welcome)
        # TODO: make some kind of animation and/or music
        print(Motivational.MOTIVATIONAL)
        #print("first screen / remember to add pause again")
        # TODO: make sure not Win Console or default Mac Terminal
        self.pause()
        self.goto_help()
        self.pause()
        
    def set_default_colors(self) -> tuple[str, str]:
        """VIEW/TUI: returns the default color values"""
        color: str = self.colors["yellow"]
        reset: str = self.colors["reset"]
        return (color, reset)

    def show_menulist(self) -> None:
        """VIEW/TUI: prints menulist"""
        print("-" * 80)
        c, r = self.set_default_colors()
        strf: str = self.controller.settings.DTSTRF
        curr_date: dt.datetime = self.get_date()
        weekday: str = curr_date.strftime("%A")
        curr_str: str = curr_date.strftime(strf)

        num_tomark: int = len(self.controller.return_unmarked_habits())
        #breakpoint()

        ## Last day of Month && Sunday:
        # 2022-07-31
        # 2022-10-30
        # 2024-03-31
        # 2025-08-31
                
        # TODO: should not be here, should be separate functionality,
        # too crowded
        # Print notice on Sundays, if not also last day of month
        if curr_date.weekday() == 6 and not self.controller\
                                        .is_last_day_of_month(curr_date):
            print(f"{c}current date:{r} {curr_str} ({weekday}) " +\
                  "Weekly streaks advance tonight!")
            
        # print notice on last day of month, if not Sunday
        elif curr_date.weekday() != 6 and self.controller\
                                        .is_last_day_of_month(curr_date):
            print(f"{c}current date:{r} {curr_str} ({weekday}) " +\
                  "Monthly streaks advance tonight!")
            
        # print notice on Sundays && last of months
        elif curr_date.weekday() == 6 and self.controller\
                                        .is_last_day_of_month(curr_date):
            print(f"{c}current date:{r} {curr_str} ({weekday}) " +\
                  "Monthly & weekly streaks " +\
                    "advances tonight!")
        else:
            print(f"{c}current date:{r} {curr_str} ({weekday})")

        # TODO: IF TIME BEFORE SUBMIT, DO THIS FIRST:
        # TODO: refactor this and simplify logic, too nested
        # perhaps= .is_menu_type(menutype)->bool, and match/case
        #print(f"\n{c}Choose an option: {r}")
        yprint("\nChoose an option: ")
        for choice in self.choices:
            if not choice.name.startswith(" "):
                # if startswith space, move slightly right (next branch)
                # here: normal menu item

                # adv-date: add remaining + colorize/capitalize if ready
                if choice.command == "adv":
                    if num_tomark:
                        # Not ready: there are still habits to mark done/not-done
                        print(f'[{c}{choice.command}{r}] \t{choice.name}' +\
                              f' (still {c}{num_tomark}{r} habits to mark)')
                    else:
                        # Ready: all habits for the day are marked
                        g = self.colors["green"]
                        print(f'[{c}{choice.command}{r}] \t{choice.name}!' +\
                              f'{g} (READY!){r}')
                else:
                    # normal menu item
                    print(f'[{c}{choice.command}{r}] \t{choice.name}')
            else:
                # this is to push the submenu slightly to the right
                print(f' [{c}{choice.command}{r}] \t{choice.name}')
                
        print("-" * 80)    

    def mainmenu_input(self, input_action: str) -> None:
        """VIEW/TUI: gets user input in REPL"""
        if input_action.strip() not in [choice.command for choice in self.choices]:
                self.invalid_input()
                #return
        for choice in self.choices:
            if input_action.strip() == choice.command:
                choice.func()
                #return
            
    def interact(self, message: str = "") -> None:
        """VIEW/TUI: The main REPL method, called from MAIN"""
        self.clear()
        self.splash_screen()

        # REPL:
        while not self.repl_quit:
            self.show_menulist()
            c, r = self.set_default_colors()
            inp = input(f'{c}Make your choice: {r}')

            try:
                self.mainmenu_input(inp.lower())

            except Exception as e:
                print(f"VIEW/TUI: self.interact: Exception: {e}")
                print("broke out of 'While True: try/except'")
                break
                
        # print("exited main loop (self.interact)")
        # breakpoint()
        yprint("Do your habits! No excuses!")
        self.controller.do_quit()

    def invalid_input(self) -> None:
        """VIEW/TUI: prints that input is invalid"""
        rprint("Input not valid")

    def goto_advance_date(self) -> None:
        """VIEW/TUI: advances the date to new value"""
        if self.controller.is_ready_to_advance():
            self.clear()
            print("going to next day")
            # advancencement logic here
            self.controller.do_advance_date()
        else:
            # not-yet-advancencement logic
            rprint("Can't advance to tomorrow, still habits to mark!")
            self.pause()
            yprint("Please mark these, with Quick Mark:")
            self.print_table_head()
            for to_mark in self.controller.return_unmarked_habits():
                print(to_mark)

    def goto_main(self) -> None:
        """VIEW/TUI: placeholder function for getting to main menu
        Currently just clears the screen."""
        self.clear()

    def begin_quickmark(self) -> None:
        """VIEW/TUI: the method which asks user for input on which
        habits to mark as done/not-done (is called 'marking')"""
        self.clear()
        self.print_table_head()
        
        unmarked_habits = self.controller.return_unmarked_habits()
        
        if not unmarked_habits:
            yprint("All habits marked! You can advance date.")
            self.pause()
            return
        
        for to_mark in unmarked_habits:
            print(to_mark)

        yprint("Which ID would you like to mark (done/not-done)?" +\
               "('q' to return)")
        try:
            mark_id: str = input("ID:")[:4].strip()
            if mark_id.lower().startswith('q'):
                return
            elif mark_id.isnumeric():
                id: int = int(mark_id)
            else:
                self.invalid_input()
                self.pause()
                return
            
        except Exception as e:
            print(f"TUI:Problem in marking input, {e}")
            self.pause()
            return
        
        found: bool = False
        for habit in unmarked_habits:
            if id == habit.id: # type: ignore
                # TODO: reimplement HabitAnalysis with a dict instead of list
                # edit_habit = habit # by ref, so the actual habit gets edited!
                mark_habit: Habit = deepcopy(habit) 
                found: bool = True
                break
        if not found:
            rprint("ID not in list!")
            self.pause()
            return
    
        self.finish_quickmark(mark_habit) # type: ignore

    def finish_quickmark(self, habit: Habit) -> None:
        """VIEW/TUI: method which takes a selected habit and asks for input on
        whether it was done or not done that day"""

        # note: habit is deepcopy() of an existing habit
        yprint("Done 'd', or Not Done 'n'? ('q' to return)")
        action: str = input().strip()[:1].lower()
        match action:
            case 'd':
                self.controller.mark_habit_done(habit)
            case 'n':
                self.controller.mark_habit_not_done(habit)
            case 'q':
                return
            case _:
                self.invalid_input()
                self.pause()

        self.controller.do_qm()
        self.begin_quickmark()
        #print(self.controller.done_indicator)

    def goto_analysis(self) -> None:
        # self.controller.do_analysis()
        self.clear()
        yprint("Here follows an analysis of some habit properties:")
        print("-" * 80)
        
        # 1. What is the current top streak?
        # current longest streak all
        yprint("The CURRENT top streak (tracked):")
        top: Habit = self.controller.habitlist.return_current_longest_streak_all()
        
        if not top:
            tprint("No habits!\n")
        else:
            tprint(f"id: {top.id}")
            tprint(f"{top.streak} unit streak on {top.last_complete}, " +\
                f"with period: {top.period}")
            tprint(f"Habit description: {top.description}\n")

        # 2. What is the past top streak?
        # past longest streak all
        yprint("The past top streak (incl deleted & untracked):")
        top_p: Habit = self.controller.habitlist\
                                            .return_past_longest_streak_all()
        
        if not top_p:
            tprint("No habits!\n")
        else:
            tprint(f"id: {top_p.id}")
            tprint(f"{top_p.record.max_streak} unit streak " +\
                f"on {top_p.record.on_date}, with period: {top_p.period}")
            tprint(f"Habit description: {top_p.description}\n")

        print("-" * 80)
        # ----------------------------------------------------------------------

        # 3. What is the current top_streak, for a period?
        # current longest streak period
        yprint("The CURRENT top streak per period (tracked):")
        for period in Period:
            top_cu_pe = self.controller.habitlist\
                                .return_current_longest_streak_period(period)
            yprint(f"\t* Period: {period}")
            if not top_cu_pe:
                tprint("No habits!\n")
            else:
                tprint(f"id: {top_cu_pe.id}")
                tprint(f"{top_cu_pe.streak} unit streak " +\
                       f"on {top_cu_pe.last_complete}")
                tprint(f"Habit description: {top_cu_pe.description}\n")

        # What is the past top_streak, for a period?
        # past longest streak period
        yprint("The past top streak per period (incl deleted & untracked):")
        for period in Period:
            top_pa_pe: Habit | None = self.controller.\
                            habitlist.return_past_longest_streak_period(period)
            yprint(f"\t* Period: {period}")
            if not top_pa_pe:
                tprint("No habits!")
            else:
                tprint(f"id: {top_pa_pe.id}")
                tprint(f"{top_pa_pe.record.max_streak} unit streak " +\
                       f"on {top_pa_pe.record.on_date}")
                tprint(f"Habit description: {top_pa_pe.description}\n")
        
    def print_table_head(self) -> None:
        """VIEW/TUI: prints the header of the Habit table"""
        #"obj(".ljust(7) +\
        #c, r = self.set_default_colors()
        header: str = \
        "|id".ljust(6) +\
        "|start date".ljust(12) +\
        "|period".ljust(8) +\
        "|track?".ljust(7) +\
        "|streak".ljust(6) +\
        "|last done".ljust(11) +\
        "|description\t" +\
        ")"
        yprint(header.expandtabs(3))
        yprint(f"{'_' * 80}")
    
    def goto_showlist(self, option: str | None = None) -> None:
        """VIEW/TUI: shows user-requested type of habitlist"""
        self.clear()
        self.print_table_head()        

        if option is None:
            for habit in self.controller.do_showlist():
                print(habit)
            # id, creation, period, isTracked, streak, desc
        elif option == "tracked":
            for habit in self.controller.do_showlist_tracked():
                print(habit)
        elif option == "period":
            period = self.period_picker()
            period_habits: list[Habit] = self.controller.do_showlist_period(period)
            if len(period_habits) == 0:
                self.clear()
                rprint("No habits with this periodicity")
            else:
                self.clear()
                self.print_table_head()
                for habit in period_habits:
                    #print("inside the loop, test")
                    print(habit)
                #print("test after habit loop")
        else:
            raise NotImplementedError("option not existing in goto_showlist")
        
    def goto_showlist_tracked(self) -> None:
        """VIEW/TUI: connector function for getting a list of tracked habits"""
        self.goto_showlist(option = "tracked")

    def goto_showlist_period(self) -> None:
        """VIEW/TUI: connector function for getting habits with same periods """
        self.goto_showlist(option = "period")

    def period_picker(self) -> Period:
        """VIEW/TUI: prints the available periods and asks user which"""
        self.clear()
        for i, p in enumerate(Period, start=1):
            print(f"{p}: {i}")

        c,r = self.set_default_colors()
        period_inp: str = ""
        try:
            period_inp: str = input(f"{c}Which period? (1, 2, 3): {r}")[:4]\
            .strip()
            length = len(Period)
            if period_inp not in [str(i) for i in range(1, length + 1)]:
                _, r = self.set_default_colors()
                rprint("Invalid selection!")
                rprint("setting period to default: daily")
                period = Period.daily # TODO: an explicit Period.default
                self.pause()
                return period
        except Exception as e:
            print(f"VIEW/TUI: period_picker, exception: {e}")
            self.pause()

        match period_inp:
            case "1":
                period = Period.daily
            case "2":
                period = Period.weekly
            case "3":
                period = Period.monthly
            case _:
                raise NotImplementedError("period-input problem")
        return period
        
    def goto_add(self) -> None:
        """VIEW/TUI: prints & input for adding habit (passing to controller)"""
        # need to add to habitlist, and give it an ID
        self.clear()
        period: Period = self.period_picker()

        c, r = self.set_default_colors()
        print(f"{c}\nDescription? (type 'q.' to return ('q_dot'))")
        # "q." because "quit smoking" also starts with 'q'
        print("max 35 char, more will be cut off)")
        print("until here, circa:".ljust(34,"-") + f"|{r}")

        descript_input: str = input()[:35]
        if descript_input.lower().startswith('q.'):
            return
        
        self.controller.do_add(period, descript_input)

    def begin_edit(self) -> None:
        """VIEW/TUI: gets & validates input for the habit to edit"""
        yprint("Which ID would you like to edit? ('q' to return)")
        try:
            edit_id: str = input("ID:")[:4].strip()
            if edit_id.lower().startswith('q'):
                return
            elif edit_id.isnumeric():
                id: int = int(edit_id)
            else:
                self.invalid_input()
                self.pause()
                return
        except Exception as e:
            print(f"TUI:Problem in edit input, {e}")
            self.pause()

        found: bool = False
        for habit in self.controller.do_showlist():
            if id == habit.id: # type: ignore
                # TODO: reimplement HabitAnalysis with a dict instead of list
                # edit_habit = habit # by ref, so the actual habit gets edited!
                # IMHO passing a pointer would be cleaner than this weird stuff
                edit_habit = deepcopy(habit) 
                found = True
                break
        if not found:
            rprint("ID not in list!")
            self.pause()
            return
        
        self.goto_finish_edit(edit_habit) # type: ignore
        # typechecker error: unbound
        # it does not seem unbound, as to arrive here, the error paths
        # have already been dealt with.

    def goto_finish_edit(self, habit: Habit) -> None:
        """VIEW/TUI: displays and sends off Habit for editing to Controller"""
        # delete : streak = -1
        # id, start date, streak: not modifyible
        # period, track, description: modifyible
        
        # before edit:
        self.clear()
        self.print_table_head()
        print(habit)
        
        # edit:
        # period, track, description: modifyible
        try:
            quit: bool = False
            while not quit:
                #self.clear()
                yprint("Which edit? " +\
                      "Track/untrack 't'," +\
                        "Description 'desc'," +\
                            "Delete 'del'?")
                yprint("('q' to return)")

                edit_select: str = input()[:4].lower().strip()
                match edit_select:
                    case 't':
                        habit.toggle_tracked()
                        self.controller.do_edit(habit)
                        yprint("Tracking toggled!")
                        self.print_table_head()
                        print(habit)
                        print("-" * 80)
                        #self.pause()
                    case 'desc':
                        yprint("New description: (max length 35)")
                        yprint(f"{'-' * 34}|")
                        new_descr: str = input()[:35]
                        habit.description = new_descr
                        self.controller.do_edit(habit)

                        yprint("Description changed!")
                        self.print_table_head()
                        print(habit)
                        print("-" * 80)
                    case 'del':
                        # habit.streak = -1
                        #breakpoint()
                        self.controller.do_delete(habit)
                        #print(f"{c}habit deleted! (kindof){r}")
                        yprint("habit deleted! (kind of)")
                        return
                        #self.pause()
                    case 'q':
                        quit = True
                    case _:
                        self.invalid_input()
                        self.pause()
            pass
        except Exception as e:
            print(f"VIEW/TUI: finish_edit, exception: {e}")
            self.pause()
            return

        #self.controller.do_edit(habit)

        # after edit
        pass

    def goto_help(self) -> None:
        """VIEW/TUI: prints help info"""
        #self.clear()
        helpstr: str = self.controller.do_help()
        print(helpstr)
        
    def goto_quit(self) -> None:
        """VIEW/TUI: exits the REPL"""
        self.clear()
        self.controller.do_quit()
        # ↑ is already run once at exit of REPL
        # ↑ can probably be removed, to avoid unnecessary disk activity
        # raise GeneratorExit()
        self.repl_quit = True
    
    def clear(self) -> None:
        """VIEW/TUI: clears the shell screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pause(self) -> None:
        """VIEW/TUI: aks user to press any key to continue"""
        os.system("pause" if os.name == "nt" 
        else 'bash -c \
        \'read -p "Press any key to continue \n" -n 1 -r -s\'')


if __name__ == "__main__":
    print("This module does not run directly, import only")