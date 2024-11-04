import json
from habit import Period, Habit, HabitList
from typing import List
from enum import Enum


class Storage:
    def save(self, habit_list: HabitList) -> None:
        with open("savefile.sav","w") as file:
            json.dump({"_habitlist":
                       [self.to_JSON(habit) 
                        for habit in habit_list._habitlist]
                       }, file)

    def load(self) -> HabitList:
        with open("savefile.sav","r") as file:
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
        creation: str = str(data["creation"])
        period: Period = Period[str(data["period"])]
        isTracked : bool = bool(data["isTracked"])
        streak = int(data["streak"])
        return Habit(description, creation, period, isTracked, streak)