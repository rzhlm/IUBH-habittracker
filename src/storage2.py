import json
from src.habit import Period, Habit, HabitList
from typing import List


class Storage:
    def __init__(self, savefile: str = "savefile.sav"):
        self.savefile = savefile

    def save(self, 
             #habit_list: HabitList, filename: str = "savefile.sav") -> None:
             habit_list: HabitList) -> None:
        #with open(filename,"w") as file:
        with open(self.savefile, 'r') as file:
            json.dump({"_habitlist":
                       [self.to_JSON(habit) 
                        for habit in habit_list.return_all()]
                       }, file)

    #def load(self, filename: str = "savefile.sav") -> HabitList:
    def load(self) -> HabitList:
        with open(self.savefile,"r") as file:
            data = json.load(file)
            habits: List[Habit] = [self.from_JSON(habit) 
                      for habit in data["_habitlist"]]
            return HabitList(habits)

    def to_JSON(self, habit: Habit):
        habit_dict : dict[str, str | Period | bool | int]
        habit_dict = {
                    "description": habit.description,
                    "creation_data" : habit.creation_data,
                    "period": habit.period.name,
                    "isTracked": habit.isTracked,
                    "streak": habit.streak,
        }
        return habit_dict

    def from_JSON(self, data: dict[str, str | int | bool]) -> Habit:
        description: str = str(data["description"])
        creation: str = str(data["creation_data"])
        period: Period = Period[str(data["period"])]
        isTracked : bool = bool(data["isTracked"])
        streak = int(data["streak"])
        return Habit(description, creation, period, isTracked, streak)