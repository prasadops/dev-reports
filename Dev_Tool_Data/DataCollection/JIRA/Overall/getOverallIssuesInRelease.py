from csv import DictReader
import requests
from requests.auth import HTTPBasicAuth
import json
import sys

if len(sys.argv) < 2:
  print("Supply required arguments")
  sys.exit()

username = sys.argv[1]
password = sys.argv[2]

url = "https://devopsmx.atlassian.net/rest/api/2/search"

auth = HTTPBasicAuth(username, password)

headers = {
  "Accept": "application/json"
}

epic_linked_issues_file = open('epicwise_issue_list.csv', 'a') 
epic_linked_issues_file.write('EpicKey,IssueKey,IssueType,CreatedOn,UpdatedOn,Status,Priority,Assignee,SprintName,Component,SubTasksCount,NumberOfLinkedIssues,AggregateTimeSpent,AggregateTotalTime,OriginalTimeEstimate' + '\n')

link_issue_file = open('linked_issue_list.csv', 'a')
link_issue_file.write('EpicKey,IssueKey,LinkIssueKey,LinkIssueType,LinkType,CreatedOn,UpdatedOn,Status,Priority,Assignee,AggregateTimeSpent,AggregateTotalTime,OriginalTimeEstimate' + '\n')

worklog_file = open('worklogs.csv', 'a')
worklog_file.write('EpicKey,IssueKey,WorklogAuthor,WorklogStartTime,WorklogTimeSpentInSeconds' + '\n')

with open('release_epic_list.csv', 'r') as read_obj:
  csv_reader = DictReader(read_obj)
  for row in csv_reader:
    current_epic = row['EpicKey']

    query = 'linkedissue = ' + current_epic + ' AND issue != ' + current_epic


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
      response_json = json.loads(response.text)
      list_length = len(response_json['issues'])
      total_issue_count = response_json['total']


      for index in range(list_length):
        key = response_json['issues'][index]['key']
        issue_type = response_json['issues'][index]['fields']['issuetype']['name']
        createdOn = response_json['issues'][index]['fields']['created']
        updatedOn = response_json['issues'][index]['fields']['updated']
        status = response_json['issues'][index]['fields']['status']['name']
        priority = response_json['issues'][index]['fields']['priority']['name']
        try:
          assignee = response_json['issues'][index]['fields']['assignee']['displayName']
        except TypeError:
          assignee = 'Unassigned'
        try:
          sprint = response_json['issues'][index]['fields']['customfield_10104'][0]['name']
        except TypeError:
          sprint = 'Undefined'
        component = response_json['issues'][index]['fields']['components'][0]['name']
        subtask_count = len(response_json['issues'][index]['fields']['subtasks'])
        linked_issues_count = len(response_json['issues'][index]['fields']['issuelinks'])
        aggregate_time_spent = response_json['issues'][index]['fields']['aggregateprogress']['progress']
        aggregate_total_time = response_json['issues'][index]['fields']['aggregateprogress']['total']
        original_time_estimate = response_json['issues'][index]['fields']['timeoriginalestimate']
        epic_linked_issues_file.write(current_epic + ',' + key + ',' + issue_type + ',' + createdOn + ',' + updatedOn + ',' + status + ',' + priority + ',' + assignee + ',' + sprint + ',' + component + ',' + str(subtask_count) + ',' + str(linked_issues_count) + ',' + str(aggregate_time_spent) + ',' + str(aggregate_total_time) + ',' + str(original_time_estimate) + '\n')

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
            worklog_file.write(current_epic + ',' + key + ',' + author + ',' + started + ',' + str(logged_seconds) + '\n')
            
        if linked_issues_count > 0:
          for link_index in range(linked_issues_count):
            link_name = response_json['issues'][index]['fields']['issuelinks'][link_index]['type']['name']
            if link_name == 'Relates':
              continue
            try:
              link_issue_key = response_json['issues'][index]['fields']['issuelinks'][link_index]['inwardIssue']['key']
              link_issue_type = response_json['issues'][index]['fields']['issuelinks'][link_index]['inwardIssue']['fields']['issuetype']['name']
              link_status = response_json['issues'][index]['fields']['issuelinks'][link_index]['inwardIssue']['fields']['status']['name']
              link_priority = response_json['issues'][index]['fields']['issuelinks'][link_index]['inwardIssue']['fields']['priority']['name']
            except KeyError:
              link_issue_key = response_json['issues'][index]['fields']['issuelinks'][link_index]['outwardIssue']['key']
              link_issue_type = response_json['issues'][index]['fields']['issuelinks'][link_index]['outwardIssue']['fields']['issuetype']['name']
              link_status = response_json['issues'][index]['fields']['issuelinks'][link_index]['outwardIssue']['fields']['status']['name']
              link_priority = response_json['issues'][index]['fields']['issuelinks'][link_index]['outwardIssue']['fields']['priority']['name']
            
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
            
            link_issue_file.write(current_epic + ',' + key + ',' + link_issue_key + ',' + link_issue_type + ',' + link_name + ',' + link_created + ',' + link_updated + ',' + link_status + ',' + link_priority + ',' + link_assignee + ',' + str(link_time_spent) + ',' + str(link_time_total) + ',' + str(link_original_estimate) + '\n')
   
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
                worklog_file.write(current_epic + ',' + link_issue_key + ',' + author_1 + ',' + started_1 + ',' + str(logged_seconds_1) + '\n')

      start_at_int = start_at_int + max_results_int
      total_results = total_issue_count
