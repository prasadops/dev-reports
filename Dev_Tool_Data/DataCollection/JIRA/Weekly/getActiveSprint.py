from csv import DictReader
import requests
from requests.auth import HTTPBasicAuth
import json
import datetime
import time
import sys

if len(sys.argv) < 5:
  print("Supply required arguments")
  sys.exit()

board_id = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
analytic_start_date = sys.argv[4]
analytic_end_date = sys.argv[5]

analytic_start_date_obj = datetime.datetime.strptime(analytic_start_date, "%Y-%m-%d")
analytic_end_date_obj = datetime.datetime.strptime(analytic_end_date, "%Y-%m-%d")

get_active_sprint_url = "https://devopsmx.atlassian.net/rest/agile/1.0/board/" + board_id + "/sprint"
auth = HTTPBasicAuth(username, password)

headers = {
  "Accept": "application/json"
}

get_active_sprint_parameters = {
}

active_sprint_response = requests.request(
  "GET",
  get_active_sprint_url,
  headers=headers,
  params=get_active_sprint_parameters,
  auth=auth
)

active_sprint_file = open('ActiveSprintList.csv', 'a')
active_sprint_file.write('SprintId,SprintName,SprintStartDate,SprintEndDate,SprintCurrentStatus,AnalyticFlag' + '\n')

new_issues_file = open('NewIssuesInSprint.csv', 'a')
new_issues_file.write('IssueKey,IssueType,CreatedOn,UpdatedOn,Status,Priority,Assignee,Sprint,Component,AggregateTimeSpent,AggregateTotalTime,OriginalTimeEstimate' + '\n')

worked_upon_issues_file = open('WorkedUponIssuesInSprint.csv', 'a')
worked_upon_issues_file.write('IssueKey,IssueType,CreatedOn,UpdatedOn,Status,Priority,Assignee,Sprint,Component,AggregateTimeSpent,AggregateTotalTime,OriginalTimeEstimate' + '\n')

worklog_file = open('Worklog.csv', 'a')
worklog_file.write('IssueKey,Assignee,StartTime,TimeSpentInSeconds' + '\n')

issue_summary_file = open('IssueSummary.csv', 'a')
issue_summary_file.write('IssueKey,Summary' + '\n')

active_sprint_json = json.loads(active_sprint_response.text)
number_of_sprints = len(active_sprint_json['values'])

for sprint_idx in range(number_of_sprints):
  originBoardId = active_sprint_json['values'][sprint_idx]['originBoardId']
  if str(originBoardId) == board_id:
    sprint_status = active_sprint_json['values'][sprint_idx]['state']
    if sprint_status == 'active' or sprint_status == 'closed':
      sprint_id = active_sprint_json['values'][sprint_idx]['id']
      sprint_name = active_sprint_json['values'][sprint_idx]['name']
      sprint_start_date = str(active_sprint_json['values'][sprint_idx]['startDate'])[0:10]
      sprint_end_date = str(active_sprint_json['values'][sprint_idx]['endDate'])[0:10]
      sprint_start_date_obj = datetime.datetime.strptime(sprint_start_date, "%Y-%m-%d")
      sprint_end_date_obj = datetime.datetime.strptime(sprint_end_date, "%Y-%m-%d")
      if sprint_end_date_obj <= analytic_end_date_obj and sprint_end_date_obj >= analytic_end_date_obj:
        analytic_flag = "on"
      elif sprint_status == 'active' and sprint_start_date_obj <= analytic_end_date_obj:
        analytic_flag = "on"
      else:
        analytic_flag = "off" 
   
      active_sprint_file.write(str(sprint_id) + ',' + sprint_name + ',' + sprint_start_date + ',' + sprint_end_date + ',' + sprint_status + ',' + analytic_flag + '\n')

active_sprint_file.close()

#print("Check")

with open('ActiveSprintList.csv', 'r') as read_obj:
  csv_reader = DictReader(read_obj)
  for row in csv_reader:
    active_sprint_id = row['SprintId']
#    print(active_sprint_id)
    get_issues_in_sprint_url = "https://devopsmx.atlassian.net/rest/agile/1.0/sprint/" + str(active_sprint_id) + "/issue"
    query = 'created >= "' + analytic_start_date + '" AND created <= "' + analytic_end_date + '"'
 
    start_at_int = 0
    max_results_int = 100
    total_results = 1000
  
    while start_at_int < total_results:
      
      get_new_issues_in_sprint_params = {
        'jql': query,
        'startAt': start_at_int,
        'maxResults': max_results_int
      }

      new_issues_in_sprint_response = requests.request(
        "GET",
        get_issues_in_sprint_url,
        headers=headers,
        params=get_new_issues_in_sprint_params,
        auth=auth
      )
    
      issues_in_sprint_json = json.loads(new_issues_in_sprint_response.text)
#      print(issues_in_sprint_json)
      total_issues_in_sprint = issues_in_sprint_json['total']
      print(total_issues_in_sprint)
      list_length = len(issues_in_sprint_json['issues'])

      for index in range(list_length):
        key = issues_in_sprint_json['issues'][index]['key']
        issue_type = issues_in_sprint_json['issues'][index]['fields']['issuetype']['name']
        createdOn = issues_in_sprint_json['issues'][index]['fields']['created']
        updatedOn = issues_in_sprint_json['issues'][index]['fields']['updated']
        status = issues_in_sprint_json['issues'][index]['fields']['status']['name']
        priority = issues_in_sprint_json['issues'][index]['fields']['priority']['name']
        try:
          assignee = issues_in_sprint_json['issues'][index]['fields']['assignee']['displayName']
        except TypeError:
          assignee = 'Unassigned'
        try:
          sprint = issues_in_sprint_json['issues'][index]['fields']['customfield_10104'][0]['name']
        except TypeError:
          sprint = 'Undefined'
        component = issues_in_sprint_json['issues'][index]['fields']['components'][0]['name']
        aggregate_time_spent = issues_in_sprint_json['issues'][index]['fields']['aggregateprogress']['progress']
        aggregate_total_time = issues_in_sprint_json['issues'][index]['fields']['aggregateprogress']['total']
        original_time_estimate = issues_in_sprint_json['issues'][index]['fields']['timeoriginalestimate']
        issue_summary = issues_in_sprint_json['issues'][index]['fields']['summary']

        new_issues_file.write(key + ',' + issue_type + ',' + createdOn + ',' + updatedOn + ',' + status + ',' + priority + ',' + assignee + ',' + sprint + ',' + component + ',' + str(aggregate_time_spent) + ',' + str(aggregate_total_time) + ',' + str(original_time_estimate) + '\n')

        issue_summary_file.write(key + ',' + '"' + issue_summary + '"' + '\n')

        get_worklog_url = "https://devopsmx.atlassian.net/rest/api/3/issue/" + key + "/worklog"
        get_worklog_params = {}
        get_work_log_resp = requests.request(
          "GET",
          get_worklog_url,
          headers=headers,
          params=get_worklog_params,
          auth=auth
        )
        worklog_json = json.loads(get_work_log_resp.text)
        number_of_worklogs = len(worklog_json['worklogs'])
        worklog_str = ""
        if number_of_worklogs > 0:
          for log_idx in range(number_of_worklogs):
            author = worklog_json['worklogs'][log_idx]['author']['displayName']
            started = worklog_json['worklogs'][log_idx]['started']
            logged_seconds = worklog_json['worklogs'][log_idx]['timeSpentSeconds']
            worklog_file.write(key + ',' + author + ',' + started + ',' + str(logged_seconds) + '\n')

      start_at_int = start_at_int + max_results_int
      total_results = total_issues_in_sprint

    query = 'created < "' + analytic_start_date + '" AND updated >= "' + analytic_start_date + '"'
    start_at_int_1 = 0
    max_results_int_1 = 100
    total_results_1 = 1000

    while start_at_int_1 < total_results_1:

      get_worked_upon_issues_in_sprint_params = {
        'jql': query,
        'startAt': start_at_int_1,
        'maxResults': max_results_int_1
      }

      worked_upon_issues_in_sprint_response = requests.request(
        "GET",
        get_issues_in_sprint_url,
        headers=headers,
        params=get_worked_upon_issues_in_sprint_params,
        auth=auth
      )

      issues_in_sprint_json_1 = json.loads(worked_upon_issues_in_sprint_response.text)
      total_worked_upon_issues_in_sprint = issues_in_sprint_json_1['total']
      print(total_worked_upon_issues_in_sprint)
      list_length_1 = len(issues_in_sprint_json_1['issues'])

      for index in range(list_length_1):
        key = issues_in_sprint_json_1['issues'][index]['key']
        issue_type = issues_in_sprint_json_1['issues'][index]['fields']['issuetype']['name']
        createdOn = issues_in_sprint_json_1['issues'][index]['fields']['created']
        updatedOn = issues_in_sprint_json_1['issues'][index]['fields']['updated']
        status = issues_in_sprint_json_1['issues'][index]['fields']['status']['name']
        priority = issues_in_sprint_json_1['issues'][index]['fields']['priority']['name']
        try:
          assignee = issues_in_sprint_json_1['issues'][index]['fields']['assignee']['displayName']
        except TypeError:
          assignee = 'Unassigned'
        try:
          sprint = issues_in_sprint_json_1['issues'][index]['fields']['customfield_10104'][0]['name']
        except TypeError:
          sprint = 'Undefined'
        component = issues_in_sprint_json_1['issues'][index]['fields']['components'][0]['name']
        aggregate_time_spent = issues_in_sprint_json_1['issues'][index]['fields']['aggregateprogress']['progress']
        aggregate_total_time = issues_in_sprint_json_1['issues'][index]['fields']['aggregateprogress']['total']
        original_time_estimate = issues_in_sprint_json_1['issues'][index]['fields']['timeoriginalestimate']

        issue_summary = issues_in_sprint_json_1['issues'][index]['fields']['summary']

        worked_upon_issues_file.write(key + ',' + issue_type + ',' + createdOn + ',' + updatedOn + ',' + status + ',' + priority + ',' + assignee + ',' + sprint + ',' + component + ',' + str(aggregate_time_spent) + ',' + str(aggregate_total_time) + ',' + str(original_time_estimate) + '\n')

        issue_summary_file.write(key + ',' + '"' + issue_summary + '"' + '\n')

        get_worklog_url = "https://devopsmx.atlassian.net/rest/api/3/issue/" + key + "/worklog"
        get_worklog_params = {}
        get_work_log_resp = requests.request(
          "GET",
          get_worklog_url,
          headers=headers,
          params=get_worklog_params,
          auth=auth
        )
        worklog_json = json.loads(get_work_log_resp.text)
        number_of_worklogs = len(worklog_json['worklogs'])
        worklog_str = ""
        if number_of_worklogs > 0:
          for log_idx in range(number_of_worklogs):
            author = worklog_json['worklogs'][log_idx]['author']['displayName']
            started = worklog_json['worklogs'][log_idx]['started']
            started_date = str(started)[0:10]
            started_date_obj = datetime.datetime.strptime(started_date, "%Y-%m-%d")
            if started_date_obj < analytic_start_date_obj:
              continue
            logged_seconds = worklog_json['worklogs'][log_idx]['timeSpentSeconds']
            worklog_file.write(key + ',' + author + ',' + started + ',' + str(logged_seconds) + '\n')

      start_at_int_1 = start_at_int_1 + max_results_int_1
      total_results_1 = total_worked_upon_issues_in_sprint
