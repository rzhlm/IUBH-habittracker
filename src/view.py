from typing import List
from enum import Enum, auto
#from collections import namedtuple
from typing import NamedTuple, Callable
from constants import Motivational
from dataclasses import dataclass
import os

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
    
    def __init__(self):
        self.choices = self.init_choices()
        self.colors = {
            "red": "\033[31m",
            "yellow" : "\033[0;33m",
            "green" : "\033[0;32m",
            "reset" : "\033[0m"
        }
        self.color = "\033[31m" # red
        self.reset = "\033[0m" # reset

    def init_choices(self) -> List[Choice3]:
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
        os.system('pause')
        
    def show_choices(self) -> None:
        # TODO: somekind of decorator or print_color function
        print("Choose an option: ")
        #cmd = f""
        for choice in self.choices:
            print(f"[{self.colors["yellow"]}{choice.command}{self.reset}] \t{choice.name}")
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
            
            #print(message)
            self.show_choices()
            # TODO: somekind of decorator or print_color function
            inp = input(f"{self.colors["yellow"]}Make your choice: {self.colors["reset"]}")

            try:
                self.do_input(inp.lower())
            except:
                print("first exit")
                break
        
        print("exited main loop")

    def goto_main(self):
        #break
        self.clear()
        #print("inside main")
        
        pass

    
    def invalid_input(self):
        self.clear()
        print(f"{self.colors["red"]}Input not valid{self.colors["reset"]}")

    def goto_qm(self):
        self.clear()
        print("inside QM")

    def goto_analysis(self):
        self.clear()
        # SHOULD CALL THE FUNCTIONAL ANALYSIS MODULE
        print("inside analysis")

    def goto_showlist(self):
        self.clear()
        print("inside show list")

    def goto_add(self):
        self.clear()
        print("inside add")

    def goto_edit(self):
        self.clear()
        print("inside edit")

    def goto_quit(self):
        raise Exception()

    def clear(self):
        os.system('cls' if os.name=='nt' else 'clear')
class GUI:
    pass


if __name__ == "__main__":
    t = TUI()
    t.interact()