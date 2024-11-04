import json
from habit import Period, Habit, HabitList


class Storage:
    def save(self, habit_list: HabitList) -> None:
        with open("savefile.sav","w") as file:
            json.dump({"_habitlist":
                       [self.to_JSON(habit) 
                        for habit in habit_list._habitlist]
                       }, file
                      )

    def load(self):
        pass

    def to_JSON(self, pass):
        pass

    def from_JSON(self, pass):
        pass