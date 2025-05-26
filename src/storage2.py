import json
import sys
import dataclasses
from typing import Any

from src.habit import Period, Habit, HabitAnalysis, BestStreak


# TODO: add Singleton pattern: class attr or decorator
class Storage:
    """STORAGE2: all the methods needed for loading & saving of our data"""
    def __init__(self):
        pass 

    def date_save(self,
                  date: str,
                  filename: str = "datefile.sav") -> None:
        """STORAGE: writes the date value to file"""
        with open(filename, 'w') as f:
            f.write(date)

    def date_load(self, filename: str = "datefile.sav") -> str:
        """STORAGE: loads the date value from file"""
        with open(filename, 'r') as f:
            date: str = f.readline().rstrip('\n').strip()
        return date

    def HL_save(self,
                habit_list: HabitAnalysis,
                filename: str = "default_savefile.sav") -> None:
        """STORAGE: saves the Habitlist instance (to JSON to file)"""
        #habit_list: HabitList) -> None:
        with open(filename,"w") as file:
        #with open(self.savefile, 'r') as file:
            json.dump({"_habitlist":
                       [
                           self.to_JSON(habit) 
                           for habit in habit_list.return_all()
                        ]
                       }, file)

    def HL_load(self, filename: str = "default_savefile.sav") -> HabitAnalysis:
        """STORAGE: loads the Habitlist from storage, and transforms into instance"""
        try:
            with open(filename,"r") as file:
                data = json.load(file)
                habits: list[Habit] = [
                    self.from_JSON(habit) 
                    for habit in data["_habitlist"]
                    ]
                return HabitAnalysis(habits)
        except Exception as e:
            print(f"could not load savefile, error: {e}")
            sys.exit(1)

    def to_JSON(self, habit: Habit):
        """STORAGE: transforms a Habit instance into JSON"""
        habit_dict : dict[str, str | Period | bool | int | dict[str, Any]]
        habit_dict = {
                    "id" : habit.id,
                    "description": habit.description,
                    "creation_data" : habit.creation_data,
                    "period": habit.period.name,
                    "is_tracked": habit.is_tracked,
                    "streak": habit.streak,
                    "last_complete": habit.last_complete,
                    "record": dataclasses.asdict(habit.record)
                    }
        return habit_dict

    def from_JSON(self, data: dict[str, Any]) -> Habit:
        """STORAGE: transforms JSON into a Habit instance"""

        record_data = data["record"]
        best_streak = BestStreak(
            on_date = str(record_data.get("on_date","1900-01-01")),
            max_streak = int(record_data.get("max_streak", 0)),
            )
        
        id: int = int(data["id"])
        description: str = str(data["description"])
        creation: str = str(data["creation_data"])
        period: Period = Period[str(data["period"])]
        is_tracked : bool = bool(data["is_tracked"])
        streak: int = int(data["streak"])
        last_complete: str = str(data["last_complete"])
        record: BestStreak = best_streak
        return Habit(id, 
                     description, 
                     creation, 
                     period, 
                     is_tracked, 
                     streak, 
                     last_complete,
                     record,
                     )
    

if __name__ == "__main__":
    print("This module is for importing, not for running directly")