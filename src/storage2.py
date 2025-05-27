import json
import os
import sys
import dataclasses
from typing import Any
#import datetime as dt

from src.habit import Period, Habit, HabitAnalysis, BestStreak
from src.constants import Settings


# TODO: add Singleton pattern: class attr or decorator
class Storage:
    """STORAGE2: Storage: 
    all the methods needed for loading & saving of our data"""
    def __init__(self):
        self.settings = Settings()

    def date_save(self,
                  date: str,
                  filename: str = "datefile.sav") -> None:
        """STORAGE2: Storage:
        writes the date value to file"""

        with open(filename, 'w') as f:
            f.write(date)

    def date_load(self, filename: str = "datefile.sav") -> str:
        """STORAGE: Storage:
        loads the date value from file"""
        # if no datefile exists, take system date and make that the file
        if not os.path.exists(filename):
            #strf = self.settings.DTSTRF
            #today = dt.date.today()
            #date_str = today.strftime(strf)
            defined_date = "2022-05-01"
            
            try:
                #self.date_save(date_str)
                self.date_save(defined_date)
            except Exception as e:
                print(f"No datefile! Could not generate datefile! error: {e}")
                sys.exit(1)          

        with open(filename, 'r') as f:
            date: str = f.readline().rstrip('\n').strip()
        return date

    def HL_save(self,
                habit_list: HabitAnalysis,
                filename: str = "default_savefile.sav") -> None:
        """STORAGE: Storage: 
        saves the Habitlist instance (to JSON to file)"""
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
        """STORAGE: Storage: 
        loads the Habitlist from storage, and transforms 
        into instance"""
        # TODO: if no file exists, create a blank file 
        # with 1 demo habit for each period in it
        #breakpoint()

        if not os.path.exists(filename):
            try:
                self.generate_savefile()
                #raise NotImplementedError("No savefile, and generation not yet implemented!")
                # either generate one from code
                # or copy from a default one which is always shipped
            except Exception as e:
                print(f"No savefile! Could not generate default! error: {e}")
                sys.exit(1)          

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

    def to_JSON(self, habit: Habit) -> dict[str, Any]:
        """STORAGE: Storage:
        transforms a Habit instance into JSON"""
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
        """STORAGE: Storage:
        transforms JSON into a Habit instance"""

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
    
    def generate_savefile(self):
        """STORAGE2: Storage:
         Creates the save-file, which conforms to the 
        requirements"""

        habit1: Habit = Habit(id = 1,
                    description = "Memorise top 500 french words",
                    creation_data = "2021-01-01",
                    period = Period.daily,
                    is_tracked = False,
                    streak = 101,
                    last_complete = "2021-08-19",
                    record = BestStreak("2021-08-19", 21),
                        )
        
        habit2: Habit = Habit(id = 2,
                    description = "Stretch iliopsoas muscles",
                    creation_data = "2021-01-01",
                    period = Period.daily,
                    is_tracked = False,
                    streak = -1,
                    last_complete = "2021-08-20",
                    record = BestStreak("2021-08-17", 11),
                        )
    
        habit3: Habit = Habit(id = 3,
                    description = "Stretch iliopsoas muscles",
                    creation_data = "2021-01-01",
                    period = Period.daily,
                    is_tracked = True,
                    streak = 62,
                    last_complete = "2022-05-01",
                    record = BestStreak("2021-08-20", 231),
                        )
        
        habit4: Habit = Habit(id = 4,
                    description = "Memorise top 3000 german words",
                    creation_data = "2021-01-02",
                    period = Period.daily,
                    is_tracked = True,
                    streak = 29,
                    last_complete = "2022-05-01",
                    record = BestStreak("2021-05-04", 123),
                        )
        
        habit5: Habit = Habit(id = 5,
                    description = "Solve weekly Project Euler",
                    creation_data = "2021-01-03",
                    period = Period.weekly,
                    is_tracked = True,
                    streak = 9,
                    last_complete = "2022-05-01",
                    record = BestStreak("2021-10-08", 40),
                        )
        
        habit6: Habit = Habit(id = 6,
                    description = "Read >=1 Computer Science book",
                    creation_data = "2021-01-04",
                    period = Period.weekly,
                    is_tracked = True,
                    streak = 7,
                    last_complete = "2022-05-01",
                    record = BestStreak("2021-06-11", 23),
                        )

        habit7: Habit = Habit(id = 7,
                    description = "Print invoices for VAT declaration",
                    creation_data = "2021-01-05",
                    period = Period.monthly,
                    is_tracked = True,
                    streak = 3,
                    last_complete = "2022-05-01",
                    record = BestStreak("2021-11-27", 11),
                        )


        habit_list: list[Habit] = [habit1,
                                   habit2,
                                   habit3,
                                   habit4,
                                   habit5,
                                   habit6,
                                   habit7,]   
        habit_analysis: HabitAnalysis = HabitAnalysis(habit_list)

        #self.HL_save(habit_analysis, "savefile-PAT.sav")
        self.HL_save(habit_analysis, self.settings.FILENAME)

if __name__ == "__main__":
    print("This module is for importing, not for running directly")