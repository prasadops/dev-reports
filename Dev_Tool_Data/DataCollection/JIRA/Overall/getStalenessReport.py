from csv import DictReader
import time
import datetime

staleness_report = open('staleness_report.csv', 'a')
staleness_report.write("IssueKey,UpdatedOn,HoursSinceLastUpdate" + '\n')

with open('aggregate_issue_list.csv', 'r') as read_obj:
  csv_reader = DictReader(read_obj)
  for row in csv_reader:
    issue_key = row['IssueKey']

    last_update_time = row['UpdatedOn']
    updated_time_cut = last_update_time[:-9]
    updated_time_cut = time.strptime(updated_time_cut, '%Y-%m-%dT%H:%M:%S')
    updated_time_cut = time.mktime(updated_time_cut)
   
    current_time_raw = datetime.datetime.now()
    current_time = (current_time_raw.strftime("%Y-%m-%dT%H:%M:%S"))
    current_time = time.strptime(current_time, '%Y-%m-%dT%H:%M:%S')
    current_time = time.mktime(current_time)
    
    last_updated_since = current_time - updated_time_cut
    last_updated_since_hrs = int(last_updated_since)//3600

    staleness_report.write(issue_key + ',' + last_update_time + ',' + str(last_updated_since_hrs) + '\n')

staleness_report.close()

