from __future__ import annotations
from typing import Callable, TYPE_CHECKING
#from enum import Enum, auto
#from collections import namedtuple
from src.constants import Motivational
from dataclasses import dataclass
import os
from src.habit import Period
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from src.controller import Controller
    from src.habit import Habit

# Intention to make Abstract Fact or Facade for choice of UI
# Either TUI or GUI
# and only allow a single instance at a time


"""
class ChoicesE(Enum):
    main = auto()
    quickmark = auto()
    analysis = auto()
    show_list = auto()
    add_habit = auto()
    edit = auto()

class ChoicesNT(NamedTuple):
    name: str
    command: str
    func: Callable[[],None]
"""

@dataclass
class MenuChoices:
    name: str
    command: str
    func: Callable[[], None]
    

class View(ABC):
    #single_instance = True

    @abstractmethod
    def interact(self):
        pass


# TUI: interact -> splash -> show_choices -> do_input
#
# interact
#   -> Splash
#   Loop:
#       -> Show choices
#       -> take input
#       input valid:
#           -> do_input
#               -> goto chosen function
#       input invalid:
#           -> error message


class GUI(View):

    def interact(self):
        pass

class TUI(View):

    def __init__(self, controller: Controller):
        self.controller: Controller = controller
        self.choices: list[MenuChoices] = self.init_menulist()
        self.colors: dict[str, str] = {
            "red": "\033[31m",
            "yellow" : "\033[0;33m",
            "green" : "\033[0;32m",
            "reset" : "\033[0m",
        }
        #self.currentdate: str = self.goto_load_date()

    # def goto_save_date(self) -> None:
    #     """VIEW/TUI: passes date val to controller for saving"""
    #     # TODO: implement save on exit
    #     # save date in storage in Controller
    #     self.controller.do_save_date(self.currentdate)
    
    def goto_load_date(self) -> str:
        """VIEW/TUI: gets date val from controller"""
        # TODO: implement load on start
        # get date from storage in Controller
        return self.controller.current_date

    def init_menulist(self) -> list[MenuChoices]:
        """VIEW/TUI: initializes the menulist"""
        return [
        MenuChoices("Main menu","m", self.goto_main),
        MenuChoices("Advance date","adv", self.goto_advance_date),
        MenuChoices("Quick mark","qm",self.goto_qm),
        MenuChoices("Analysis", "a", self.goto_analysis),
        MenuChoices("Show list (all) (debugging)", "sl", self.goto_showlist),
        MenuChoices(" Show list (tracked)", "slt", self.goto_showlist_tracked),
        MenuChoices(" Show list (same period, tracked)", "slp", self.goto_showlist_period),
        MenuChoices("Add Habit", "ah", self.goto_add),
        MenuChoices("Edit Habit", "e", self.goto_edit),
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
        print("first screen / remember to add pause again")
        # TODO: make sure not Win Console or default Mac Terminal
        # self.pause()
        # TODO: TURN PAUSE BACK ON BEFORE SUBMITTING
        
    def set_default_colors(self) -> tuple[str, str]:
        color: str = self.colors["yellow"]
        reset: str = self.colors["reset"]
        return (color, reset)

    def show_menulist(self) -> None:
        """VIEW/TUI: prints menulist"""
        print("-" * 80)
        # TODO: somekind of decorator or print_color function
        c, r = self.set_default_colors()
        print(f"{c}current date:",
              self.goto_load_date())
        print(f"\nChoose an option: {r}")
        
        for choice in self.choices:
            c, r = self.set_default_colors()
            
            if not choice.name.startswith(" "):
                print(f'[{c}{choice.command}{r}] \t{choice.name}')
            else:
                print(f' [{c}{choice.command}{r}] \t{choice.name}')
                # this is to push the submenu slightly to the right
        print("-" * 80)    
        #print(f"[{self.colors["yellow"]}q{self.reset}] \tQuit")

    def do_input(self, input_action: str) -> None:
        """VIEW/TUI: gets user input in REPL"""
        if input_action.strip() not in [choice.command for choice in self.choices]:
                self.invalid_input()
                #return
        for choice in self.choices:
            if input_action.strip() == choice.command:
                choice.func()
                #return
            
    def interact(self, message: str = "") -> None:
        """VIEW/TUI: The main REPL method"""
        #self.clear()
        self.splash_screen()
        while True:
            self.show_menulist()
            # TODO: somekind of decorator or print_color function
            color = self.colors["yellow"]
            reset = self.colors["reset"]
            inp = input(f'{color}Make your choice: {reset}')

            try:
                self.do_input(inp.lower())
            except GeneratorExit:
                # This is how I handle getting out of the input loop
                print("Intended exit, GeneratorExit")
                break
            except Exception as e:
                # This is for genuine Exceptions
                print("first exit: broke out of 'While True: try/except'")
                print(f"Exception: {e}")
                break
            finally:
                # TODO: Save state of objects
                # habitlist, and state file
                #
                pass
                
        # TODO: remark
        # Or perhaps save state here instead of in 'finally'
        # perhaps with contextmanager instead over the while loop
        print("remember to save the state at exit")
        # save habitlist with storage object in self.controller
        # save current_date with own method
        print("exited main loop (self.interact)")
        self.controller.do_quit()

    def invalid_input(self) -> None:
        """VIEW/TUI: prints that input is invalid"""
        self.clear()
        color = self.colors["red"]
        reset = self.colors["reset"]
        print(f'{color}Input not valid{reset}')

    def goto_advance_date(self) -> None:
        """VIEW/TUI: advances the date to new value"""
        newdate = ""
        self.controller.do_advance_date(newdate)

    def goto_main(self) -> None:
        """VIEW/TUI: placeholder function for getting to main menu"""
        #break
        self.clear()
        #print("inside main")        
        pass

    def goto_qm(self) -> None:
        self.clear()
        # Control logic
        self.controller.do_qm()
        # view logic
        print("2.inside QM (TUI)")


    def goto_analysis(self) -> None:
        self.clear()
        # SHOULD CALL THE FUNCTIONAL ANALYSIS MODULE
        # Control logic
        self.controller.do_analysis()
        # view logic
        print("2.inside Analysis (TUI)")

    def print_table_head(self) -> None:
        """VIEW/TUI: prints the header of the Habit table"""
        #"obj(".ljust(7) +\
        header: str = self.colors["yellow"] +\
        "|id".ljust(6) +\
        "|start date".ljust(12) +\
        "|period".ljust(8) +\
        "|track?".ljust(7) +\
        "|streak".ljust(6) +\
        "|last done".ljust(11) +\
        "|description\t" +\
        ")" + self.colors["reset"]
        print(header.expandtabs(3))
        print("-" * 80)

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
            """ self.clear()
            period = None
            for i, p in enumerate(Period, start=1):
                print(f"{p}: {i}")
            color = self.colors["yellow"]
            reset = self.colors["reset"]
            period_inp: str = input(f'{color}Which period? (1, 2, 3): {reset}')
            #print(f"{type(period_inp)=} {period_inp=}")
            if period_inp.strip() not in [str(i) for i in range(1,4)]:
                print("invalid selection")
            match period_inp.strip():
                case "1":
                    period = Period.daily
                case "2":
                    period = Period.weekly
                case "3":
                    period = Period.monthly
                case _:
                    raise NotImplementedError("period-input problem") """
            #print("test before")
            #print(f"period branch, {period=}")
            #result = self.controller.do_showlist_period(period)
            #print(result)
            #print(f"DEBUG: do_showlist_period before habit loop: {result}")
            
            period_habits: list[Habit] = self.controller.do_showlist_period(period)
            if len(period_habits) == 0:
                self.clear()
                print("No habits with this periodicity")
            else:
                self.clear()
                self.print_table_head()
                for habit in period_habits:
                    #print("inside the loop, test")
                    print(habit)
                #print("test after habit loop")
        else:
            raise NotImplementedError("option not existing in goto_showlist")
            
        #print("_" * 80)
        #return #prob not needed, testing bug
        
    def goto_showlist_tracked(self) -> None:
        """VIEW/TUI: connector function for getting a list of tracked habits"""
        self.goto_showlist(option = "tracked")

    def goto_showlist_period(self) -> None:
        """VIEW/TUI: connector function for getting habits with same periods """
        self.goto_showlist(option = "period")

    def period_picker(self) -> Period:
        """VIEW/TUI: prints the available periods and asks user which"""
        self.clear()
        period: Period | None = None
        for i, p in enumerate(Period, start=1):
            print(f"{p}: {i}")
        c,r = self.set_default_colors()
        period_inp: str = input(f'{c}Which period? (1, 2, 3): {r}')
        #print(f"{type(period_inp)=} {period_inp=}")
        if period_inp.strip() not in [str(i) for i in range(1,4)]:
            print("invalid selection")
        match period_inp.strip():
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
        print(f"{c}" +\
              "\nDescription? (max 35 char, more will be cut off)")
        print("until here, circa:".ljust(34,"-") + f"|{r}")
        descript_input: str = input()[:35]
        
        # Control logic
        self.controller.do_add(period, descript_input)

        # view logic
        # print("2.inside Add (TUI)")

    def goto_edit(self) -> None:
        """VIEW/TUI: edit, prints and gets input for habit editing 
        (passing to controller"""
        # ID should not be modifyible at all
        # also be able to delete (but keep ID)
        # delete : streak = -1
        # id, start date, streak: not modifyible
        # period, track, description: modifyible

        #self.clear()
        c, r = self.set_default_colors()
        print(f"{c}Which ID would you like to edit?{r}")
        edit_id: int = int(input("ID:"))

        self.print_table_head()
        edit_habit: Habit | None = None
        for habit in self.controller.do_showlist():
            if edit_id == habit.id:
                edit_habit = habit
        
        if edit_habit is None:
            print(f"{c}ID not in list!{r}")
            self.pause()
        else:
            pass
        
        self.controller.do_edit()
        

    def goto_help(self) -> None:
        """VIEW/TUI: prints help info"""
        self.clear()
        self.controller.do_help()
        print("2.inside Help (TUI)")
        

    def goto_quit(self) -> None:
        """VIEW/TUI: exits the REPL"""
        self.clear()
        
        
        self.controller.do_quit()
        # View logic:
        print("2. Inside Quit (view)")
        print("Bye!")
        raise GeneratorExit()
    

    def clear(self) -> None:
        """VIEW/TUI: clears the shell screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pause(self) -> None:
        """VIEW/TUI: aks user to press any key to continue"""
        os.system('pause' if os.name == 'nt' 
        else 'bash -c \
        \'read -p "Press any key to continue (POSIX)\n" -n 1 -r -s\'')



if __name__ == "__main__":
    print("This module does not run directly, import only")