python3 getEpicList.py "$1" $2 $3 
python3 getOverallIssuesInRelease.py $2 $3

bash aggregator.sh

echo "IssueType,TotalCount,ToDo,InProgress,InVerification,PRRaised,Merged,Done" > issue_type_state_counter_report.csv

### Getting EPIC State Counter
total_epics=$(tail -n+2 release_epic_list.csv | wc -l | sed 's/^ *//g')
epics_in_todo=$(tail -n+2 release_epic_list.csv | grep ",To Do," | wc -l | sed 's/^ *//g')
epics_in_progress=$(tail -n+2 release_epic_list.csv | grep ",In Progress," | wc -l | sed 's/^ *//g')
epics_in_verification=$(tail -n+2 release_epic_list.csv | grep ",In Verification," | wc -l | sed 's/^ *//g')
epics_pr_raised=$(tail -n+2 release_epic_list.csv | grep ",PR Raised," | wc -l | sed 's/^ *//g')
epics_merged=$(tail -n+2 release_epic_list.csv | grep ",Merged," | wc -l | sed 's/^ *//g')
epics_done=$(tail -n+2 release_epic_list.csv | grep ",Done," | wc -l | sed 's/^ *//g')

### Getting Linked Issues State Counter
total_linked_issues=$(tail -n+2 aggregate_issue_list.csv | wc -l | sed 's/^ *//g')
linked_issues_in_todo=$(tail -n+2 aggregate_issue_list.csv | grep ",To Do," | wc -l | sed 's/^ *//g')
linked_issues_in_progress=$(tail -n+2 aggregate_issue_list.csv | grep ",In Progress," | wc -l | sed 's/^ *//g')
linked_issues_in_verification=$(tail -n+2 aggregate_issue_list.csv | grep ",In Verification," | wc -l | sed 's/^ *//g')
linked_issues_pr_raised=$(tail -n+2 aggregate_issue_list.csv | grep ",PR Raised," | wc -l | sed 's/^ *//g')
linked_issues_merged=$(tail -n+2 aggregate_issue_list.csv | grep ",Merged," | wc -l | sed 's/^ *//g')
linked_issues_done=$(tail -n+2 aggregate_issue_list.csv | grep ",Done," | wc -l | sed 's/^ *//g')


### Getting Total Issues State Counter
overall_total_issues=$(($total_epics + $total_linked_issues))
overall_issues_in_todo=$(($epics_in_todo + $linked_issues_in_todo))
overall_issues_in_progress=$(($epics_in_progress + $linked_issues_in_progress))
overall_issues_in_verification=$(($epics_in_verification + $linked_issues_in_verification))
overall_issues_pr_raised=$(($epics_pr_raised + $linked_issues_pr_raised))
overall_issues_merged=$(($epics_merged + $linked_issues_merged))
overall_issues_done=$(($epics_done + $linked_issues_done))


### Create Issue Type State Counter Report
echo "Total,$overall_total_issues,$overall_issues_in_todo,$overall_issues_in_progress,$overall_issues_in_verification,$overall_issues_pr_raised,$overall_issues_merged,$overall_issues_done" >> issue_type_state_counter_report.csv
echo "Epic,$total_epics,$epics_in_todo,$epics_in_progress,$epics_in_verification,$epics_pr_raised,$epics_merged,$epics_done" >> issue_type_state_counter_report.csv

declare -a issue_types=("Story" "Task" "Sub-task" "Bug" "Test Case")
declare -a statuses=("To Do" "In Progress" "In Verification" "PR Raise" "Merged" "Done")
for issue_type in "${issue_types[@]}";do
  total_count=$(grep ",$issue_type" aggregate_issue_list.csv | wc -l | sed 's/^ *//g')
  printf %s "$issue_type,$total_count" >> issue_type_state_counter_report.csv
  for status in "${statuses[@]}";do
    status_count=$(grep ",$issue_type" aggregate_issue_list.csv | grep ",$status" | wc -l | sed 's/^ *//g')
    printf %s ",$status_count" >> issue_type_state_counter_report.csv 
  done
  echo "" >> issue_type_state_counter_report.csv
done

### Create Priority State Counter Report

echo "IssueType,Priority,ToDo,InProgress,InVerification,PRRaised,Merged,Done" > issue_priority_state_counter_report.csv

declare -a priorities=("Highest" "High" "Medium" "Low" "Lowest")



issue_type="Epic"

for priority in "${priorities[@]}";do
  printf %s "$issue_type,$priority" >> issue_priority_state_counter_report.csv
  for status in "${statuses[@]}";do
    priority_status_count=$(grep ",$priority" release_epic_list.csv | grep ",$status" | wc -l | sed 's/^ *//g')
    printf %s ",$priority_status_count" >> issue_priority_state_counter_report.csv
  done
  echo "" >> issue_priority_state_counter_report.csv
done

for issue_type in "${issue_types[@]}";do
  for priority in "${priorities[@]}";do
    printf %s "$issue_type,$priority" >> issue_priority_state_counter_report.csv
    for status in "${statuses[@]}";do
      priority_status_count=$(grep ",$issue_type" aggregate_issue_list.csv | grep ",$priority" | grep ",$status" | wc -l | sed 's/^ *//g')
      printf %s ",$priority_status_count" >> issue_priority_state_counter_report.csv
    done
    echo "" >> issue_priority_state_counter_report.csv
  done
done

tail -n+2 epic_linked_worklogs.csv >> worklogs.csv

echo "Assignee,TimeSpentInSeconds" > worklog_report.csv

IFS=$'\n'
for assignee in $(tail -n+2 worklogs.csv | cut -d , -f 3 | sort | uniq);do
  timespent_sec=$(tail -n+2 worklogs.csv | grep "$assignee" | cut -d , -f 5 | awk '{s+=$1} END {print s}')
  echo "$assignee,$timespent_sec" >> worklog_report.csv
done

python3 getStalenessReport.py
