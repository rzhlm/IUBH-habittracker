
REQUIREMENTS:
-  [x] At least Weekly & Daily periods
-  [x] 5 preloaded (w & d) habits, with min 4 weeks of data
-  [x] creation date + date/time of task completion

- [x] Give list of all tracked habits
- [x] Give list of all habits with same period
- [x] Return longest streak of all habits
- [x] Return longest streak for chosen habits

- [x] MAKE TESTS FOR FUNCS & METHODS

OTHER TODO:
- [x]  Habit has action & period
-  [x] An action/task can be checked off
-  [x] Miss = break
-  [x] streak
-  [x] Analysis of best
-  [x] Save state on exit
-  [x] save state on edit

- [ ] add notice to best use winterminal, not console; nor default Mac terminal

Habit spec:
- eaxtly 5
- min 1 wkly, min 1 daily
- each min 4 weeks of data


=================

This was an intention,
the actual design is altered:
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