import requests
from requests.auth import HTTPBasicAuth
from csv import reader
import json
import sys

if len(sys.argv) < 2:
  print("Supply required arguments")
  sys.exit()

username = sys.argv[1]
password = sys.argv[2]

url = "https://sonar.opsmx.com/api/issues/search"
auth = HTTPBasicAuth(username, password)
headers = {
  "Accept": "application/json"
}

severities = ['BLOCKER', 'CRITICAL', 'MAJOR', 'INFO', 'MINOR']
report_file = open('severity_report.csv', 'a')
report_file.write('ProjectName,Blocker,Critical,Major,Info,Minor' + '\n')

with open('projectlist.csv', 'r') as read_obj:
  csv_reader = reader(read_obj)
  for row in csv_reader:
    current_project = row[0]
    report_file.write(current_project)
    for severity in severities:
      parameters = {
        'componentKeys': current_project,
        'severities': severity,
        'resolved': 'false'
      }

      response = requests.request("GET", url, headers=headers, params=parameters, auth=auth)

      resp = json.loads(response.text)
      print(current_project,':',severity,':',resp['total'])
      report_file.write(',' + str(resp['total']))
    report_file.write('\n')
