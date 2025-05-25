import json
from src.habit import Period, Habit, HabitAnalysis
import sys
#from habit import Period, Habit, HabitList
# -> don't run directly from VSC, run with: python -m src.storage2

#from typing import List



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
        habit_dict : dict[str, str | Period | bool | int]
        habit_dict = {
                    "id" : habit.id,
                    "description": habit.description,
                    "creation_data" : habit.creation_data,
                    "period": habit.period.name,
                    "isTracked": habit.isTracked,
                    "streak": habit.streak,
                    "last_complete": habit.last_complete,
                    }
        return habit_dict

    def from_JSON(self, data: dict[str, str | int | bool]) -> Habit:
        """STORAGE: transforms JSON into a Habit instance"""
        id: int = int(data["id"])
        description: str = str(data["description"])
        creation: str = str(data["creation_data"])
        period: Period = Period[str(data["period"])]
        isTracked : bool = bool(data["isTracked"])
        streak: int = int(data["streak"])
        last_complete: str = str(data["last_complete"])
        return Habit(id, 
                     description, 
                     creation, 
                     period, 
                     isTracked, 
                     streak, 
                     last_complete,
                     )
    

if __name__ == "__main__":
    print("This module is for importing, not for running directly")