
REQUIREMENTS:
-  [x] At least Weekly & Daily periods
-  [ ] min 5 preloaded (w & d) habits, with min 4 weeks of data
-  [ ] creation date + date/time of task completion

- [x] Give list of all tracked habits
- [x] Give list of all habits with same period
- [x] Return longest streak of all habits
- [x] Return longest streak for chosen habits

- [ ] MAKE TESTS FOR FUNCS & METHODS


OTHER TODO:
- [x]  Habit has action & period
-  [x] An action/task can be checked off
-  [x] Miss = break
-  [x] streak
-  [ ] Analysis of best & worst
-  [x] Save state on exit
-  [x] save state on edit

- [ ] add notice to best use winterminal, not console; nor default Mac terminal




# UI flow
```mermaid

flowchart TD;

 Start[Start] -->|Welcome-screen| Main{Main Menu}
 Main <--> QM[Quick Mark as completed]
 Main <--> List[List tracked habits]
List <--> Analysis[Analysis screen]
 Main <--> Analysis[Analysis screen]
 Main <--> Add[Add habit]
 Main <--> Edit[Edit tracked habit]
 Main --> Q(Quit)

List <--> Add
List <--> Edit

```