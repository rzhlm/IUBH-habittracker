from habit import Habit, HabitList
from storage2 import Storage

class Controller:
    def __init__(self, habitlist: HabitList = None,
                  storage: Storage = None):
        self.habitlist: HabitList = habitlist
        self.storage : Storage = storage
        pass

    def do_qm(self):
        print("1.inside QM (Controller)")
        pass
    def do_analysis(self):
        print("1.inside Analysis (Controller)")
        pass
    def do_showlist(self):
        print("1.Inside showlist(Controller)")
        pass
    def do_add(self):
        print("1.Inside add (Controller)")
        pass
    def do_edit(self):
        print("1. Inside Edit (Controller)")
        pass
    def do_quit(self):
        print("1.Inside Quit (controller)")
        pass

if __name__ == '__main__':
    # for testing & dev purposes
    st = Storage()
    hl: HabitList = st.load()
