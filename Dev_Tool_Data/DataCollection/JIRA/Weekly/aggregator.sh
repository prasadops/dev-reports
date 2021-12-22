head -1 NewIssuesInSprint.csv > Epic_list.csv
head -1 NewIssuesInSprint.csv > Story_list.csv
head -1 NewIssuesInSprint.csv > Task_list.csv
head -1 NewIssuesInSprint.csv > SubTask_list.csv
head -1 NewIssuesInSprint.csv > Bug_list.csv
head -1 NewIssuesInSprint.csv > TestCase_list.csv

grep ",Epic," NewIssuesInSprint.csv >> Epic_list.csv
grep ",Story," NewIssuesInSprint.csv >> Story_list.csv
grep ",Task," NewIssuesInSprint.csv >> Task_list.csv
grep ",Sub-task," NewIssuesInSprint.csv >> SubTask_list.csv
grep ",Bug," NewIssuesInSprint.csv >> Bug_list.csv
grep ",Test," NewIssuesInSprint.csv >> TestCase_list.csv

grep ",Epic," WorkedUponIssuesInSprint.csv >> Epic_list.csv
grep ",Story," WorkedUponIssuesInSprint.csv >> Story_list.csv
grep ",Task," WorkedUponIssuesInSprint.csv >> Task_list.csv
grep ",Sub-task," WorkedUponIssuesInSprint.csv >> SubTask_list.csv
grep ",Bug," WorkedUponIssuesInSprint.csv >> Bug_list.csv
grep ",Test," WorkedUponIssuesInSprint.csv >> TestCase_list.csv
