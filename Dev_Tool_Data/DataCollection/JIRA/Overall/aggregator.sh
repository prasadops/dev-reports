cut -d , -f 1,2,3,4,5,6,7,8,13,14,15 epicwise_issue_list.csv  > aggregate_issue_list.csv

IFS=$'\n'
for line in $(tail -n+2 linked_issue_list.csv);do
  issueKey=$(echo $line | cut -d , -f 3)
  if [[ ! $(cut -d , -f 2 aggregate_issue_list.csv | grep "$issueKey") ]];then
    echo $line | cut -d , -f 1,3,4,6,7,8,9,10,11,12,13 >> aggregate_issue_list.csv
  fi
done

for line in $(tail -n+2 epic_linked_issue_list.csv);do
  issueKey=$(echo $line | cut -d , -f 2)
  if [[ ! $(cut -d , -f 2 aggregate_issue_list.csv | grep "$issueKey") ]];then
    echo $line | cut -d , -f 1,2,3,5,6,7,8,9,10,11,12 >> aggregate_issue_list.csv
  fi
done

head -1 aggregate_issue_list.csv> Story_list.csv
head -1 aggregate_issue_list.csv> Task_list.csv
head -1 aggregate_issue_list.csv > SubTask_list.csv
head -1 aggregate_issue_list.csv > Bug_list.csv
head -1 aggregate_issue_list.csv > TestCase_list.csv

grep ",Story," aggregate_issue_list.csv >> Story_list.csv
grep ",Task," aggregate_issue_list.csv >> Task_list.csv
grep ",Sub-task," aggregate_issue_list.csv >> SubTask_list.csv
grep ",Bug," aggregate_issue_list.csv >> Bug_list.csv
grep ",Test," aggregate_issue_list.csv >> TestCase_list.csv
