from csv import DictReader
import requests
from requests.auth import HTTPBasicAuth
import json
import datetime
import time
import sys

if len(sys.argv) < 4:
  print("Supply required arguments")
  sys.exit()

username = sys.argv[1]
password = sys.argv[2]
analytic_start_date = sys.argv[3]
analytic_end_date = sys.argv[4]

auth = HTTPBasicAuth(username, password)

headers = {
  "Accept": "application/json"
}

stale_issues_file = open('StaleIssuesInSprint.csv', 'a')
stale_issues_file.write('IssueKey,IssueType,CreatedOn,UpdatedOn,Status,Priority,Assignee,Sprint,Component,AggregateTimeSpent,AggregateTotalTime,OriginalTimeEstimate,HoursSinceLastUpdate' + '\n')

stale_issues_summary_file = open('IssueSummary.csv', 'a')

with open('ActiveSprintList.csv', 'r') as read_obj:
  csv_reader = DictReader(read_obj)
  for row in csv_reader:
    active_sprint_id = row['SprintId']
    get_issues_in_sprint_url = "https://devopsmx.atlassian.net/rest/agile/1.0/sprint/" + str(active_sprint_id) + "/issue"
    query = 'created < "' + analytic_start_date + '" AND updated < "' + analytic_start_date + '"'
 
    start_at_int = 0
    max_results_int = 100
    total_results = 1000
  
    while start_at_int < total_results:
      
      get_stale_issues_in_sprint_params = {
        'jql': query,
        'startAt': start_at_int,
        'maxResults': max_results_int
      }

      stale_issues_in_sprint_response = requests.request(
        "GET",
        get_issues_in_sprint_url,
        headers=headers,
        params=get_stale_issues_in_sprint_params,
        auth=auth
      )
    
      issues_in_sprint_json = json.loads(stale_issues_in_sprint_response.text)
      total_issues_in_sprint = issues_in_sprint_json['total']
      print(total_issues_in_sprint)
      list_length = len(issues_in_sprint_json['issues'])

      for index in range(list_length):
        key = issues_in_sprint_json['issues'][index]['key']
        issue_type = issues_in_sprint_json['issues'][index]['fields']['issuetype']['name']
        createdOn = issues_in_sprint_json['issues'][index]['fields']['created']
        updatedOn = issues_in_sprint_json['issues'][index]['fields']['updated']
        updated_time_cut = str(updatedOn)[:-9]
        updated_time_cut = time.strptime(updated_time_cut, '%Y-%m-%dT%H:%M:%S')
        updated_time_cut = time.mktime(updated_time_cut)

        current_time_raw = datetime.datetime.now()
        current_time = (current_time_raw.strftime("%Y-%m-%dT%H:%M:%S"))
        current_time = time.strptime(current_time, '%Y-%m-%dT%H:%M:%S')
        current_time = time.mktime(current_time)       

        last_updated_since = current_time - updated_time_cut
        last_updated_since_hrs = int(last_updated_since)//3600

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
        summary = issues_in_sprint_json['issues'][index]['fields']['summary']

        stale_issues_file.write(key + ',' + issue_type + ',' + createdOn + ',' + updatedOn + ',' + status + ',' + priority + ',' + assignee + ',' + sprint + ',' + component + ',' + str(aggregate_time_spent) + ',' + str(aggregate_total_time) + ',' + str(original_time_estimate) + ',' + str(last_updated_since_hrs) + '\n')

        stale_issues_summary_file.write(key + ',' + '"' + summary + '"' + '\n')
      start_at_int = start_at_int + max_results_int
      total_results = total_issues_in_sprint
