- [x] Give list of all tracked habits
- [x] Give list of all habits with same period
- [ ] Return longest streak of all habits
- [ ] Return longest streak for chosen habits

- [ ]  Habit has action & period
-  [ ] An action/task can be checked off
-  [ ] Miss = break
-  [ ] streak
-  [ ] Analysis of best & worst

-  [x] At least Weekly & Daily periods
-  [ ] min 5 preloaded (w & d) habits, with min 4 weeks of data
-  [ ] creation date + date/time of task completion



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