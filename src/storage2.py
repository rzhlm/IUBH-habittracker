import json
from src.habit import Period, Habit, HabitList
#from habit import Period, Habit, HabitList
# -> don't run directly from VSC, run with: python -m src.storage2

from typing import List



# TODO: add Singleton pattern: class attr or decorator
class Storage:
    def __init__(self):
        pass 

    def save(self, 
             habit_list: HabitList,
               filename: str = "default_savefile.sav") -> None:
             #habit_list: HabitList) -> None:
        with open(filename,"w") as file:
        #with open(self.savefile, 'r') as file:
            json.dump({"_habitlist":
                       [self.to_JSON(habit) 
                        for habit in habit_list.return_all()]
                       }, file)

    def load(self, filename: str = "default_savefile.sav") -> HabitList:
    #def load(self) -> HabitList:
        with open(filename,"r") as file:
            data = json.load(file)
            habits: List[Habit] = [self.from_JSON(habit) 
                      for habit in data["_habitlist"]]
            return HabitList(habits)

    def to_JSON(self, habit: Habit):
        habit_dict : dict[str, str | Period | bool | int]
        habit_dict = {
                    "id" : habit.id,
                    "description": habit.description,
                    "creation_data" : habit.creation_data,
                    "period": habit.period.name,
                    "isTracked": habit.isTracked,
                    "streak": habit.streak,
        }
        return habit_dict

    def from_JSON(self, data: dict[str, str | int | bool]) -> Habit:
        id: int = int(data["id"])
        description: str = str(data["description"])
        creation: str = str(data["creation_data"])
        period: Period = Period[str(data["period"])]
        isTracked : bool = bool(data["isTracked"])
        streak = int(data["streak"])
        return Habit(id, description, creation, period, isTracked, streak)