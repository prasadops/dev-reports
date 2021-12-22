import requests
from requests.auth import HTTPBasicAuth
import datetime
import json
import sys

if len(sys.argv) < 4:
  print("Supply required arguments")
  sys.exit()

username = sys.argv[1]
password = sys.argv[2]
analytic_start_date = sys.argv[3]
analytic_end_date = sys.argv[4]


analytic_start_date_obj = datetime.datetime.strptime(analytic_start_date,"%Y-%m-%d")
analytic_end_date_obj= datetime.datetime.strptime(analytic_end_date,"%Y-%m-%d")

url = "https://jenkins.opsmx.net:8181/jenkins/api/json"
auth = HTTPBasicAuth(username, password)

headers = {
  "Accept": "application/json"
}

parameters = {}

response = requests.request(
  "GET",
  url,
  headers=headers,
  params=parameters,
  auth=auth
)
resp_json = json.loads(response.text)

number_of_jobs = len(resp_json['jobs'])
number_of_views = len(resp_json['views'])

job_list = open('job_list.csv', 'a')
job_list.write('JobName,JobColor' + '\n')

view_list = open('view_list.csv', 'a')
view_list.write('ViewName' + '\n')

build_info_file = open('build_list.csv', 'a')
build_info_file.write('JobName,BuildName,BuildId,BuildNum,BuildTimeStamp,BuildResult,BuildEstimateDuration,BuildDuration' + '\n')

for job_idx in range(number_of_jobs):
  job_name = resp_json['jobs'][job_idx]['name']
  job_color = resp_json['jobs'][job_idx]['color']
  job_list.write(job_name + ',' + job_color + '\n')

  get_build_info_url = "https://jenkins.opsmx.net:8181/jenkins/job/" + job_name + "/api/json"

  build_info_parameters = {
    'tree': 'builds[fullDisplayName,id,number,timestamp,result,estimatedDuration,duration]'
  }

  build_info_resp = requests.request(
    "GET",
    get_build_info_url,
    headers=headers,
    params=build_info_parameters,
    auth=auth
  )
  build_info_json = json.loads(build_info_resp.text)
  number_of_builds = len(build_info_json['builds'])
  for build_idx in range(number_of_builds):
    build_name = build_info_json['builds'][build_idx]['fullDisplayName']
    build_id = build_info_json['builds'][build_idx]['id']
    build_num = build_info_json['builds'][build_idx]['number']
    build_timestamp = build_info_json['builds'][build_idx]['timestamp']
    build_dt_obj = datetime.datetime.fromtimestamp(int(build_timestamp)/1000)
    if build_dt_obj < analytic_start_date_obj or build_dt_obj > analytic_end_date_obj:
      print("Found older timestamp of build for ", job_name)
      continue
    build_result = build_info_json['builds'][build_idx]['result']
    build_estimate_duration = build_info_json['builds'][build_idx]['estimatedDuration']
    build_duration = build_info_json['builds'][build_idx]['duration']
    build_info_file.write(job_name + ',' + build_name + ',' + str(build_id) + ',' + str(build_num) + ',' + str(build_timestamp) + ',' + build_result + ',' + str(build_estimate_duration) + ',' + str(build_duration) + '\n')

for view_idx in range(number_of_views):
  view_name = resp_json['views'][view_idx]['name']
  view_list.write(view_name + '\n')
