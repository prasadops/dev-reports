import requests
from requests.auth import HTTPBasicAuth
from csv import reader
import json
import datetime
import sys

if len(sys.argv) < 3:
  print("Supply required arguments")
  sys.exit()

username = sys.argv[1]
password = sys.argv[2]
end_date = sys.argv[3]

url = "https://sonar.opsmx.com/api/issues/search"
auth = HTTPBasicAuth(username, password)
headers = {
  "Accept": "application/json"
}

issueTypes = ['BUG', 'VULNERABILITY', 'CODE_SMELL']

#end_date = '2021-12-08'
end_date_imd = datetime.datetime.strptime(end_date, '%Y-%m-%d')
start_date_imd = end_date_imd + datetime.timedelta(days=-7)
start_date = start_date_imd.strftime('%Y-%m-%d')

with open('projectlist.csv', 'r') as read_obj:
  csv_reader = reader(read_obj)
  for row in csv_reader:
    current_project = row[0]

    #filename = current_project + '_rulewise_violations.csv'
    #report_file = open(filename, 'a')
    #report_file.write('RuleID,Description,IssueType,Count' + '\n')

    daily_report_filename = current_project + '_daily_rule_violations.csv'
    daily_report_file = open(daily_report_filename, 'a')
    daily_report_file.write('RuleID,Description,IssueType,Day7,Day6,Day5,Day4,Day3,Day2,Day1' + '\n')
    for issueType in issueTypes:

      parameters = {
        'componentKeys': current_project,
        'types': issueType,
        'resolved': 'false',
        'facets': 'rules',
        'createdAfter': start_date,
        'createdBefore': end_date
      }

      response = requests.request("GET", url, headers=headers, params=parameters, auth=auth)

      resp = json.loads(response.text)
      numberOfRulesViolated = len(resp['facets'][0]['values'])
      for index in range(0,numberOfRulesViolated):
        ruleID = resp['facets'][0]['values'][index]['val']
        fetchRuleDescURL = "https://sonar.opsmx.com/api/rules/search"
        fetchRuleDescParams = {
          'rule_key': ruleID
        }
        ruleDesc_response = requests.request("GET", fetchRuleDescURL, headers=headers, params=fetchRuleDescParams, auth=auth)
        ruleDesc_resp_json = json.loads(ruleDesc_response.text)
        desc = ruleDesc_resp_json['rules'][0]['name']
        #numberOfViolations = resp['facets'][0]['values'][index]['count']
        #report_file.write(ruleID + ',' + str(desc) + ',' + issueType + ',' + str(numberOfViolations) + '\n')

        daily_report_file.write(ruleID + ',' + str(desc) + ',' + issueType)
        for i in range(0,7):
          testdate = end_date_imd + datetime.timedelta(days=-i)
          testdatestr = testdate.strftime('%Y-%m-%d')

          daily_parameters = {
            'componentKeys': current_project,
            'types': issueType,
            'rules': ruleID,
            'resolved': 'false',
            'createdAfter': testdatestr,
            'createdBefore': testdatestr,
          }

          daily_response = requests.request("GET", url, headers=headers, params=daily_parameters, auth=auth)

          daily_resp = json.loads(daily_response.text)
          daily_report_file.write(',' + str(daily_resp['total']))
        daily_report_file.write('\n')
