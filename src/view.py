from typing import List
from enum import Enum, auto
#from collections import namedtuple
from typing import NamedTuple, Callable
from constants import Motivational
from dataclasses import dataclass

# Intention to make Abstract Fact or Facade for choice of UI
# Either TUI or GUI
# and only allow a single instance at a time

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

class TUI:
    
    def __init__(self):
        self.choices = self.init_choices()
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
        ]
        
    def splash_screen(self):
        
        welcome = """
            WELCOME TO THE HABIT TRACKING APP !
            ====================================
        """
        
    
        print(welcome)
        print(Motivational.motivational)
        
    def show_choices(self):
        print("Choose an option: ")
        for choice in self.choices:
            print(f"[{self.color}{choice.command}{self.reset}] \t{choice.name}")
            # eg: [e] Edit
        print(f"[{self.color}q{self.reset}] \tQuit")

    def do_input(self, input_action: str):
        for choice in self.choices:
            if input_action == self.choice:
                choice.func()
                return
        print("Input not valid")
        

    def interact(self):
        self.splash_screen()
        while True:
            self.show_choices()
            #print all options:
            #color = "\033[31m" #red
            inp = input("Make your choice: ")
            #print("\033[0m") # reset

            # make this into a class, but which type?
            match inp:
                case "q":
                    print("Quitting...")
                    break
                case _:
                    self.do_input
            

    def goto_main(self):
        pass
    def goto_qm(self):
        pass
    def goto_analysis(self):
        pass
    def goto_showlist(self):
        pass
    def goto_add(self):
        pass
    def goto_edit(self):
        pass

class GUI:
    pass


if __name__ == "__main__":
    t = TUI()
    t.interact()