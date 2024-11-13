from typing import List
from enum import Enum, auto
#from collections import namedtuple
from typing import NamedTuple, Callable

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

    
class View:
    #single_instance = True
    def __init__(self):
        pass
    
    def UI(self):
        pass


class TUI:
    def __init__(self):
        #choices: List[str] = []
        #choices = namedtuple("Choices", ["name", "command", "func"])
        main = ChoicesNT("Main menu","m",goto_main)
        quickmark = ChoicesNT("Quick mark","qm", goto_qm)
        analysis = ChoicesNT("Analysis", "a", goto_analysis)
        show_list = ChoicesNT("Show list", "sl", goto_showlist)
        add_habit = ChoicesNT("Add Habit", "ah", goto_add)
        edit = ChoicesNT("Edit", "e", goto_edit)
        

    def splash_screen(self):
        welcome = """
        WELCOME TO THE HABBIT TRACKING APP !
        ====================================
        """
        print(welcome)

    def interact(self):
        self.splash_screen()
        while True:
            pass

class GUI:
    pass