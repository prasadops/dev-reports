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

severities = ['BLOCKER', 'CRITICAL', 'MAJOR', 'INFO', 'MINOR']

report_file = open('daily_severity_report.csv', 'a')
report_file.write('ProjectName,Severity,Day7,Day6,Day5,Day4,Day3,Day2,Day1' + '\n')
#today = datetime.datetime.now().date()
today = datetime.datetime.strptime(end_date, '%Y-%m-%d')

with open('projectlist.csv', 'r') as read_obj:
  csv_reader = reader(read_obj)
  for row in csv_reader:
    current_project = row[0]

    for severity in severities:
      report_file.write(current_project)
      report_file.write(',' + severity)
      for i in range(0,7):
        testdate = today + datetime.timedelta(days=-i)
        testdatestr = testdate.strftime('%Y-%m-%d')
      
        parameters = {
          'componentKeys': current_project,
          'createdAfter': testdatestr,
          'createdBefore': testdatestr,
          'resolved': 'false',
          'severities': severity
        }

        response = requests.request("GET", url, headers=headers, params=parameters, auth=auth)

        resp = json.loads(response.text)
        report_file.write(',' + str(resp['total']))
      report_file.write('\n')
