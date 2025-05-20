from __future__ import annotations
from typing import List, Callable, TYPE_CHECKING
#from enum import Enum, auto
#from collections import namedtuple
from src.constants import Motivational
from dataclasses import dataclass
import os
#from src.controller import Controller

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

    def init_menulist(self) -> List[MenuChoices]:
        return [
        MenuChoices("Main menu","m", self.goto_main),
        MenuChoices("Quick mark","qm",self.goto_qm),
        MenuChoices("Analysis", "a", self.goto_analysis),
        MenuChoices("Show list", "sl", self.goto_showlist),
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
        print("first screen")
        # TODO: make sure not Win Console or default Mac Terminal
        self.pause()
        
    def show_menulist(self) -> None:
        # TODO: somekind of decorator or print_color function
        print("Choose an option: ")
        #cmd = f""
        for choice in self.choices:
            color = self.colors["yellow"]
            reset = self.colors["reset"]
            print(f'[{color}{choice.command}{reset}] \t{choice.name}')
            # eg: [e] Edit
        #print(f"[{self.colors["yellow"]}q{self.reset}] \tQuit")

    def do_input(self, input_action: str) -> None:
        if input_action not in [choice.command for choice in self.choices]:
                self.invalid_input()
                return
        for choice in self.choices:
            if input_action == choice.command:
                choice.func()
                return
            
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
            except:
                print("first exit")
                break
        
        print("exited main loop")

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

    def goto_showlist(self) -> None:
        self.clear()
        # Control logic
        for habit in self.controller.do_showlist():
            print(habit)
            # id, desc, creation, period, isTracked, streak

        # view logic
        print("2.inside Showlist (TUI)")

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
        raise Exception()

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