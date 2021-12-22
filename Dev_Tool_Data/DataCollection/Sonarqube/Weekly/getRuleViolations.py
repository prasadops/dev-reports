import requests
from requests.auth import HTTPBasicAuth
from csv import reader
import json
import sys

n = len(sys.argv)
if n < 4:
  print("Pass required arguments")
  sys.exit()

username = sys.argv[1]
password = sys.argv[2]
start_date = sys.argv[3]
end_date = sys.argv[4]

url = "https://sonar.opsmx.com/api/issues/search"
auth = HTTPBasicAuth(username, password)
headers = {
  "Accept": "application/json"
}


issueTypes = ['BUG', 'VULNERABILITY', 'CODE_SMELL']

#start_date = '2021-12-02'
#end_date = '2021-12-08'

with open('projectlist.csv', 'r') as read_obj:
  csv_reader = reader(read_obj)
  for row in csv_reader:
    current_project = row[0]
    for issueType in issueTypes:

      filename = current_project+'_'+issueType+'_violations.csv'
      report_file = open(filename, 'a')
      report_file.write('RuleID,Description,Count' + '\n')

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
        numberOfViolations = resp['facets'][0]['values'][index]['count']
        report_file.write(ruleID + ',' + str(desc) + ',' + str(numberOfViolations) + '\n')
