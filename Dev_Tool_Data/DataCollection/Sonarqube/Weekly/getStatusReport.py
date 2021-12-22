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

statuses = ['OPEN', 'CONFIRMED', 'REOPENED', 'RESOLVED', 'CLOSED']

#start_date = '2021-12-02'
#end_date = '2021-12-08'

report_file = open('status_report.csv', 'a')
report_file.write('ProjectName,Open,Confirmed,Reopened,Resolved,Closed' + '\n')

with open('projectlist.csv', 'r') as read_obj:
  csv_reader = reader(read_obj)
  for row in csv_reader:
    current_project = row[0]
    report_file.write(current_project)
    for status in statuses:
      parameters = {
        'componentKeys': current_project,
        'statuses': status,
        'createdAfter': start_date,
        'createdBefore': end_date
      }

      response = requests.request("GET", url, headers=headers, params=parameters, auth=auth)

      resp = json.loads(response.text)
      print(current_project,':',status,':',resp['total'])
      report_file.write(',' + str(resp['total']))
    report_file.write('\n')
