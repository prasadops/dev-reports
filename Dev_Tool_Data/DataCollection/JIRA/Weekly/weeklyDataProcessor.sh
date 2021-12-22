echo "IssueType,TotalCount,ToDo,InProgress,InVerification,PRRaised,Merged,Done" > new_issue_type_state_counter_report.csv
echo "IssueType,TotalCount,ToDo,InProgress,InVerification,PRRaised,Merged,Done" > old_issue_type_state_counter_report.csv

declare -a issue_types=("Epic" "Story" "Task" "Sub-task" "Bug" "Test")
declare -a statuses=("To Do" "In Progress" "In Verification" "PR Raise" "Merged" "Done")

for issue_type in "${issue_types[@]}";do
  total_count=$(grep ",$issue_type" NewIssuesInSprint.csv | wc -l | sed 's/^ *//g')
  printf %s "$issue_type,$total_count" >> new_issue_type_state_counter_report.csv
  for status in "${statuses[@]}";do
    status_count=$(grep ",$issue_type" NewIssuesInSprint.csv | grep ",$status" | wc -l | sed 's/^ *//g')
    printf %s ",$status_count" >> new_issue_type_state_counter_report.csv
  done
  echo "" >> new_issue_type_state_counter_report.csv
done

for issue_type in "${issue_types[@]}";do
  total_count=$(grep ",$issue_type" WorkedUponIssuesInSprint.csv | wc -l | sed 's/^ *//g')
  printf %s "$issue_type,$total_count" >> old_issue_type_state_counter_report.csv
  for status in "${statuses[@]}";do
    status_count=$(grep ",$issue_type" WorkedUponIssuesInSprint.csv | grep ",$status" | wc -l | sed 's/^ *//g')
    printf %s ",$status_count" >> old_issue_type_state_counter_report.csv
  done
  echo "" >> old_issue_type_state_counter_report.csv
done

echo "IssueType,Priority,ToDo,InProgress,InVerification,PRRaised,Merged,Done" > new_issue_priority_state_counter_report.csv
echo "IssueType,Priority,ToDo,InProgress,InVerification,PRRaised,Merged,Done" > old_issue_priority_state_counter_report.csv

declare -a priorities=("Highest" "High" "Medium" "Low" "Lowest")

for issue_type in "${issue_types[@]}";do
  for priority in "${priorities[@]}";do
    printf %s "$issue_type,$priority" >> new_issue_priority_state_counter_report.csv
    for status in "${statuses[@]}";do
      priority_status_count=$(grep ",$issue_type" NewIssuesInSprint.csv | grep ",$priority" | grep ",$status" | wc -l | sed 's/^ *//g')
      printf %s ",$priority_status_count" >> new_issue_priority_state_counter_report.csv
    done
    echo "" >> new_issue_priority_state_counter_report.csv
  done
done

for issue_type in "${issue_types[@]}";do
  for priority in "${priorities[@]}";do
    printf %s "$issue_type,$priority" >> old_issue_priority_state_counter_report.csv
    for status in "${statuses[@]}";do
      priority_status_count=$(grep ",$issue_type" WorkedUponIssuesInSprint.csv | grep ",$priority" | grep ",$status" | wc -l | sed 's/^ *//g')
      printf %s ",$priority_status_count" >> old_issue_priority_state_counter_report.csv
    done
    echo "" >> old_issue_priority_state_counter_report.csv
  done
done


echo "Assignee,TimeSpentInSeconds" > worklog_report.csv

IFS=$'\n'
for assignee in $(tail -n+2 Worklog.csv | cut -d , -f 2 | sort | uniq);do
  timespent_sec=$(tail -n+2 Worklog.csv | grep "$assignee" | cut -d , -f 4 | awk '{s+=$1} END {print s}')
  echo "$assignee,$timespent_sec" >> worklog_report.csv
done
