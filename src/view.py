from typing import List
from enum import Enum, auto

# Intention to make Abstract Fact or Facade for choice of UI
# Either TUI or GUI
# and only allow a single instance at a time

class Choices(Enum):
    main = auto()
    quickmark = auto()
    analysis = auto()
    show_list = auto()
    add_habit = auto()
    edit = auto()
    
class View:
    #single_instance = True

    def __init__(self):
        pass
    
    def UI(self):
        pass


class TUI:
    def __init__(self):
        choices: List[str] = []

    def splash_screen(self):
        pass

    def interact(self):
        while True:
            pass

class GUI:
    pass