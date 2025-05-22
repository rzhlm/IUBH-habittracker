#from __future__ import annotations
from typing import Callable, TYPE_CHECKING
#from enum import Enum, auto
#from collections import namedtuple
from src.constants import Motivational
from dataclasses import dataclass
import os
from src.habit import Period


if TYPE_CHECKING:
    from src.controller import Controller

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

    
class View:
    #@abstractmethod
    #def interact(self):
    #    pass

    #single_instance = True
    def __init__(self):
        pass
    
    def UI(self):
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

class TUI:
        
    def __init__(self, controller: Controller):
        self.controller: Controller = controller
        self.choices = self.init_menulist()
        self.colors = {
            "red": "\033[31m",
            "yellow" : "\033[0;33m",
            "green" : "\033[0;32m",
            "reset" : "\033[0m",
        }
        #self.color = "\033[31m" # red
        #self.reset = "\033[0m" # reset

    def init_menulist(self) -> list[MenuChoices]:
        return [
        MenuChoices("Main menu","m", self.goto_main),
        MenuChoices("Quick mark","qm",self.goto_qm),
        MenuChoices("Analysis", "a", self.goto_analysis),
        MenuChoices("Show list (all)", "sl", self.goto_showlist),
        MenuChoices(" Show list (tracked)", "slt", self.goto_showlist_tracked),
        MenuChoices(" Show list (same period, tracked)", "slp", self.goto_showlist_period),
        MenuChoices("Add Habit", "ah", self.goto_add),
        MenuChoices("Edit", "e", self.goto_edit),
        MenuChoices("Help", "?", self.goto_help),
        MenuChoices("Quit","q", self.goto_quit),
        ]
        
    def splash_screen(self) -> None:
        
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
        #self.pause()
        # TODO: TURN PAUSE BACK ON BEFORE SUBMITTING
        
    def show_menulist(self) -> None:
        # TODO: somekind of decorator or print_color function
        print("Choose an option: ")
        
        for choice in self.choices:
            color = self.colors["yellow"]
            reset = self.colors["reset"]
            if not choice.name.startswith(" "):
                print(f'[{color}{choice.command}{reset}] \t{choice.name}')
            else:
                print(f' [{color}{choice.command}{reset}] \t{choice.name}')
            
        #print(f"[{self.colors["yellow"]}q{self.reset}] \tQuit")

    def do_input(self, input_action: str) -> None:
        if input_action.strip() not in [choice.command for choice in self.choices]:
                self.invalid_input()
                #return
        for choice in self.choices:
            if input_action.strip() == choice.command:
                choice.func()
                #return
            
    def interact(self, message: str ="") -> None:
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
                break
            except Exception as e:
                print("first exit: broke out of 'While True: try/except'")
                print(f"Exception: {e}")
                break
        
        print("exited main loop (self.interact)")

    def invalid_input(self) -> None:
        self.clear()
        color = self.colors["red"]
        reset = self.colors["reset"]
        print(f'{color}Input not valid{reset}')

    def goto_main(self) -> None:
        #break
        self.clear()
        #print("inside main")
        
        pass

    def goto_qm(self) -> None:
        """QuickMark: Links the TUI command to the Controller action"""
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
        header: str = "obj(".ljust(7) +\
        "|id \t" +\
        "|start date\t" +\
        "|period ".ljust(7) +\
        "|track?".ljust(7) +\
        "|streak".ljust(6) +\
        "|description\t" +\
        ")"
        print(header.expandtabs(3))
        print("-" * 80)

    def goto_showlist(self, option: str | None = None) -> None:
        self.clear()
        #print("2.inside Showlist (TUI)")
        self.print_table_head()        

        if option == None:
            for habit in self.controller.do_showlist():
                print(habit)
            # id, creation, period, isTracked, streak, desc
        elif option == "tracked":
            for habit in self.controller.do_showlist_tracked():
                print(habit)
        elif option == "period":
            self.clear()
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
                    raise NotImplementedError("period-input problem")
            #print("test before")
            #print(f"period branch, {period=}")
            #result = self.controller.do_showlist_period(period)
            #print(result)
            #print(f"DEBUG: do_showlist_period before habit loop: {result}")
            
            period_habits = self.controller.do_showlist_period(period)
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
            
        print("_" * 80)
        #return #prob not needed, testing bug
        
    def goto_showlist_tracked(self) -> None:
        self.goto_showlist(option = "tracked")

    def goto_showlist_period(self) -> None:
        self.goto_showlist(option = "period")

    def goto_add(self) -> None:
        # need to add to habitlist, and give it an ID

        self.clear()
        # Control logic
        self.controller.do_add()

        # view logic
        print("2.inside Add (TUI)")

    def goto_edit(self) -> None:
        # modify everything, except the ID.
        # also be able to delete (but keep ID)

        self.clear()
        # Control logic
        self.controller.do_edit()
        # view logic
        print("2.inside Edit (TUI)")

    def goto_help(self) -> None:
        self.clear()
        self.controller.do_help()
        print("2.inside Help (TUI)")
        

    def goto_quit(self) -> None:
        self.clear()
        
        #Controller logic
        self.controller.do_quit()
        # View logic:
        print("2. Inside Quit (view)")
        print("Bye!")
        raise GeneratorExit()

    def clear(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pause(self) -> None:
        os.system('pause' if os.name == 'nt' 
        else 'bash -c \
        \'read -p "Press any key to continue (POSIX)\n" -n 1 -r -s\'')
class GUI:
    pass


if __name__ == "__main__":
    pass
    # for testing & dev purposes
"""     controller = Controller()
    tui = TUI(controller)
    tui.interact() """