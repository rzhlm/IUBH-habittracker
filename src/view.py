from typing import List
#from enum import Enum, auto
#from collections import namedtuple
from typing import NamedTuple, Callable
from constants import Motivational
from dataclasses import dataclass
import os
#from controller import Controller

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
class Choice3:
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
    
    def __init__(self, controller = None):
        self.controller = controller
        self.choices = self.init_menulist()
        self.colors = {
            "red": "\033[31m",
            "yellow" : "\033[0;33m",
            "green" : "\033[0;32m",
            "reset" : "\033[0m"
        }
        #self.color = "\033[31m" # red
        #self.reset = "\033[0m" # reset

    def init_menulist(self) -> List[Choice3]:
        return [
        Choice3("Main menu","m",self.goto_main),
        Choice3("Quick mark","qm",self.goto_qm),
        Choice3("Analysis", "a", self.goto_analysis),
        Choice3("Show list", "sl", self.goto_showlist),
        Choice3("Add Habit", "ah", self.goto_add),
        Choice3("Edit", "e", self.goto_edit),
        Choice3("Quit","q",self.goto_quit)
        ]
        
    def splash_screen(self) -> None:
        
        welcome = """
            WELCOME TO THE HABIT TRACKING APP !
            ===================================
        """
        
        self.clear()
        print(welcome)
        # TODO: make some kind of animation and/or music
        print(Motivational.motivational)
        print("first screen")
        # TODO: make sure not Win Console or default Mac Terminal
        #print("press any key to continue")
        #os.system('pause')
        self.pause()
        
    def show_menulist(self) -> None:
        # TODO: somekind of decorator or print_color function
        print("Choose an option: ")
        #cmd = f""
        for choice in self.choices:
            print(f"[{self.colors["yellow"]}{choice.command}{self.colors["reset"]}] \t{choice.name}")
            # eg: [e] Edit
        #print(f"[{self.colors["yellow"]}q{self.reset}] \tQuit")

    def do_input(self, input_action: str):
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
            inp = input(f"{self.colors["yellow"]}Make your choice: {self.colors["reset"]}")

            try:
                self.do_input(inp.lower())
            except:
                print("first exit")
                break
        
        print("exited main loop")

    def invalid_input(self):
        self.clear()
        print(f"{self.colors["red"]}Input not valid{self.colors["reset"]}")

    def goto_main(self):
        #break
        self.clear()
        #print("inside main")
        
        pass

    def goto_qm(self):
        self.clear()

        # Control logic
        self.controller.do_qm()
        # view logic
        print("2.inside QM (TUI)")


    def goto_analysis(self):
        self.clear()
        # SHOULD CALL THE FUNCTIONAL ANALYSIS MODULE
        
        # Control logic
        self.controller.do_analysis()
        # view logic
        print("2.inside Analysis (TUI)")

    def goto_showlist(self):
        self.clear()
        # Control logic
        for habit in self.controller.do_showlist():
            print(habit)

        # view logic
        print("2.inside Showlist (TUI)")

    def goto_add(self):
        self.clear()
        # Control logic
        self.controller.do_add()
        # view logic
        print("2.inside Add (TUI)")

    def goto_edit(self):
        self.clear()
        # Control logic
        self.controller.do_edit()
        # view logic
        print("2.inside Edit (TUI)")

    def goto_quit(self):
        self.clear()
        
        #Controller logic
        self.controller.do_quit()
        # View logic:
        print("2. Inside Quit (view)")
        print("Bye!")
        raise Exception()

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pause(self):
        os.system('pause' if os.name == 'nt' 
        else 'read -p "Press any key to continue (POSIX)" -n 1 -r -s')
class GUI:
    pass


if __name__ == "__main__":
    # for testing & dev purposes
    controller = Controller()
    tui = TUI(controller)
    tui.interact()