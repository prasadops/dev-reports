import requests
from requests.auth import HTTPBasicAuth
import json
import sys

if len(sys.argv) < 2:
  print("Supply required arguments")
  sys.exit()

username = sys.argv[1]
password = sys.argv[2]

url = "https://sonar.opsmx.com/api/components/search_projects"
auth = HTTPBasicAuth(username, password)

headers = {
  "Accept": "application/json"
}

response = requests.request("GET", url, headers=headers, auth=auth)

resp = json.loads(response.text)
searchresults = len(resp['components'])

myfile = open('projectlist.csv', 'a')

for index in range(searchresults):
  myfile.write(resp['components'][index]['key']+','+resp['components'][index]['name'] + '\n');
