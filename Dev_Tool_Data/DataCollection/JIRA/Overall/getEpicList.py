from csv import reader
import requests
from requests.auth import HTTPBasicAuth
import json
import sys

if len(sys.argv) < 3:
  print("Supply required arguments")
  sys.exit()


#release_id = 'ISD 3.11'
release_id = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

url = "https://devopsmx.atlassian.net/rest/api/2/search"
auth = HTTPBasicAuth(username, password)

headers = {
  "Accept": "application/json"
}

epicListFile = open('release_epic_list.csv', 'a')
epicListFile.write('EpicKey,Status,Priority,Assignee,CreatedOn,UpdatedOn,SprintName,Component,AggregateTimeSpent,AggregateTotalTime' + '\n')

link_issue_file = open('epic_linked_issue_list.csv', 'a')
link_issue_file.write('EpicKey,LinkIssueKey,LinkIssueType,LinkType,CreatedOn,UpdatedOn,Status,Priority,Assignee,AggregateTimeSpent,AggregateTotalTime,OriginalTimeEstimate' + '\n')

worklog_file = open('epic_linked_worklogs.csv', 'a')
worklog_file.write('EpicKey,IssueKey,WorklogAuthor,WorklogStartTime,WorklogTimeSpentInSeconds' + '\n')

query = "issuetype = Epic AND fixVersion = '" + release_id + "'"
start_at_int = 0
max_results_int = 100
total_results = 1000

while start_at_int < total_results:    
  parameters = {
    'jql': query,
    'startAt': start_at_int,
    'maxResults': max_results_int
  }

  response = requests.request(
    "GET",
    url,
    headers=headers,
    params=parameters,
    auth=auth
  )

  resp_json = json.loads(response.text)
  list_length = len(resp_json['issues'])
  total_epic_count = resp_json['total']

  for index in range(list_length):
    key = resp_json['issues'][index]['key']
    status = resp_json['issues'][index]['fields']['status']['name']
    priority = resp_json['issues'][index]['fields']['priority']['name']
    try:
      assignee = resp_json['issues'][index]['fields']['assignee']['displayName']
    except TypeError:
      assignee = 'Unassigned'
    createdOn = resp_json['issues'][index]['fields']['created']
    updatedOn = resp_json['issues'][index]['fields']['updated']
    try:    
      sprintName = resp_json['issues'][index]['fields']['customfield_10104'][0]['name']
    except TypeError:
      sprintName = "Undefined"
    component = resp_json['issues'][index]['fields']['components'][0]['name']
    aggregate_time_spent = resp_json['issues'][index]['fields']['aggregateprogress']['progress']
    aggregate_total_time = resp_json['issues'][index]['fields']['aggregateprogress']['total']
    epicListFile.write(key + ',' + status + ',' + priority + ',' + assignee + ',' + createdOn + ',' + updatedOn + ',' + sprintName + ',' + component + ',' + str(aggregate_time_spent) + ',' + str(aggregate_total_time) + '\n')
 
    linked_issues_count = len(resp_json['issues'][index]['fields']['issuelinks'])
    if linked_issues_count > 0:
      for link_index in range(linked_issues_count):
        link_name = resp_json['issues'][index]['fields']['issuelinks'][link_index]['type']['name']
        if link_name == 'Relates':
          continue
        try:
          link_issue_key = resp_json['issues'][index]['fields']['issuelinks'][link_index]['inwardIssue']['key']
          link_issue_type = resp_json['issues'][index]['fields']['issuelinks'][link_index]['inwardIssue']['fields']['issuetype']['name']
          if link_issue_type == 'Epic':
            continue
          link_status = resp_json['issues'][index]['fields']['issuelinks'][link_index]['inwardIssue']['fields']['status']['name']
          link_priority = resp_json['issues'][index]['fields']['issuelinks'][link_index]['inwardIssue']['fields']['priority']['name']
        except KeyError:
          link_issue_key = resp_json['issues'][index]['fields']['issuelinks'][link_index]['outwardIssue']['key']
          link_issue_type = resp_json['issues'][index]['fields']['issuelinks'][link_index]['outwardIssue']['fields']['issuetype']['name']
          if link_issue_type == 'Epic':
            continue
          link_status = resp_json['issues'][index]['fields']['issuelinks'][link_index]['outwardIssue']['fields']['status']['name']
          link_priority = resp_json['issues'][index]['fields']['issuelinks'][link_index]['outwardIssue']['fields']['priority']['name']

        issue_query = 'issue% = ' + link_issue_key
        parameters = {
          'jql': query,
        }
        issue_response = requests.request(
          "GET",
          url,
          headers=headers,
          params=parameters,
          auth=auth
        )
        issue_response_json = json.loads(issue_response.text)
        try:
          link_assignee = issue_response_json['issues'][0]['fields']['assignee']['displayName']
        except TypeError:
          link_assignee = 'Unassigned'
        link_created = issue_response_json['issues'][0]['fields']['created']
        link_updated = issue_response_json['issues'][0]['fields']['updated']
        link_time_spent = issue_response_json['issues'][0]['fields']['aggregateprogress']['progress']
        link_time_total = issue_response_json['issues'][0]['fields']['aggregateprogress']['total']
        link_original_estimate = issue_response_json['issues'][0]['fields']['timeoriginalestimate']

        link_issue_file.write(key + ',' + link_issue_key + ',' + link_issue_type + ',' + link_name + ',' + link_created + ',' + link_updated + ',' + link_status + ',' + link_priority + ',' + link_assignee + ',' + str(link_time_spent) + ',' + str(link_time_total) + ',' + str(link_original_estimate) + '\n')

        get_linked_worklog_url = "https://devopsmx.atlassian.net/rest/api/3/issue/" + link_issue_key + "/worklog"
        get_linked_worklog_params = {}
        get_linked_work_log_resp = requests.request(
          "GET",
          get_linked_worklog_url,
          headers=headers,
          params=get_linked_worklog_params,
          auth=auth
        )
        linked_worklog_json = json.loads(get_linked_work_log_resp.text)
        number_of_worklogs_1 = len(linked_worklog_json['worklogs'])
        linked_worklog_str = ""
        if number_of_worklogs_1 > 0:
          for log_idx_1 in range(number_of_worklogs_1):
            author_1 = linked_worklog_json['worklogs'][log_idx_1]['author']['displayName']
            started_1 = linked_worklog_json['worklogs'][log_idx_1]['started']
            logged_seconds_1 = linked_worklog_json['worklogs'][log_idx_1]['timeSpentSeconds']
            worklog_file.write(key + ',' + link_issue_key + ',' + author_1 + ',' + started_1 + ',' + str(logged_seconds_1) + '\n')

  start_at_int = start_at_int + max_results_int
  total_results = total_epic_count
