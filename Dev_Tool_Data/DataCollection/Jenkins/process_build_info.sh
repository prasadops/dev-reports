python3 getListOfJobs.py $1 $2 $3 $4

echo "JobName,NumberOfBuilds,Successful,Failed,Aborted" > job_status_report.csv 
for job in $(tail -n+2 job_list.csv | cut -d , -f 1 | sort | uniq);do
  weekly_number_of_builds=$(grep "^$job," build_list.csv | wc -l | sed 's/^ *//g')
  success_counter=$(grep "^$job," build_list.csv | grep ",SUCCESS," | wc -l | sed 's/^ *//g')
  failure_counter=$(grep "^$job," build_list.csv | grep ",FAILURE," | wc -l | sed 's/^ *//g')
  aborted_counter=$(grep "^$job," build_list.csv | grep ",ABORTED," | wc -l | sed 's/^ *//g')
  echo "$job,$weekly_number_of_builds,$success_counter,$failure_counter,$aborted_counter" >> job_status_report.csv
done

declare -a nightly_jobs=("Dev-audit-service-jpa" "Dev-build-analytics-master" "Dev-build-commongate-master" "Dev-build-dashboard-master" "Dev-build-datascience-master" "Dev-build-platform-master" "Dev-build-oes-api-master" "Dev-ui-master-build" "Dev-build-visibility-master")

declare -a aona_jobs=("Dev-audit-service-jpa" "Dev-autopilot-build-branch-ds-ms" "Dev-ds-build-branch-ds-ms" "Dev-platformservice-build-branch" "Dev-dashboardservice-build-branch" "Dev-sapor-build-branch" "Dev-visibilityservice-build-branch" "Dev-build-commongate-branch")

declare -a gitpr_jobs=("Dev-Autopilot_Test_PR_New" "Dev-dashboardservice-build-branch-vault" "Dev-Test_PR-oes-gate" "Dev-Test_PR-oes-ui" "Dev-platformservice-build-branch-vault" "Dev-Test_PR-oes-api" "Dev-visibilityservice-build-branch-vault")

echo "JobName,NumberOfBuilds,Successful,Failure,Aborted" > nightly_status_report.csv
echo "JobName,NumberOfBuilds,Successful,Failure,Aborted" > aona_status_report.csv
echo "JobName,NumberOfBuilds,Successful,Failure,Aborted" > gitpr_status_report.csv

for nightly_job in "${nightly_jobs[@]}";do
  build_count=$(grep "^$nightly_job," build_list.csv | wc -l | sed 's/^ *//g')
  success_count=$(grep "^$nightly_job," build_list.csv | grep "SUCCESS" | wc -l | sed 's/^ *//g')
  failure_count=$(grep "^$nightly_job," build_list.csv | grep "FAILURE" | wc -l | sed 's/^ *//g')
  aborted_count=$(grep "^$nightly_job," build_list.csv | grep "ABORTED" | wc -l | sed 's/^ *//g')
  echo "$nightly_job,$build_count,$success_count,$failure_count,$aborted_count" >> nightly_status_report.csv
done

total_nightly_builds=$(tail -n+2 nightly_status_report.csv | cut -d , -f 2 | awk '{s+=$1} END {print s}')
total_nightly_success=$(tail -n+2 nightly_status_report.csv | cut -d , -f 3 | awk '{s+=$1} END {print s}')
total_nightly_failure=$(tail -n+2 nightly_status_report.csv | cut -d , -f 4 | awk '{s+=$1} END {print s}')
total_nightly_aborted=$(tail -n+2 nightly_status_report.csv | cut -d , -f 5 | awk '{s+=$1} END {print s}')

echo "Total,$total_nightly_builds,$total_nightly_success,$total_nightly_failure,$total_nightly_aborted" >> nightly_status_report.csv

for aona_job in "${aona_jobs[@]}";do
  build_count=$(grep "^$aona_job," build_list.csv | wc -l | sed 's/^ *//g')
  success_count=$(grep "^$aona_job," build_list.csv | grep "SUCCESS" | wc -l | sed 's/^ *//g')
  failure_count=$(grep "^$aona_job," build_list.csv | grep "FAILURE" | wc -l | sed 's/^ *//g')
  aborted_count=$(grep "^$aona_job," build_list.csv | grep "ABORTED" | wc -l | sed 's/^ *//g')
  echo "$aona_job,$build_count,$success_count,$failure_count,$aborted_count" >> aona_status_report.csv
done

total_aona_builds=$(tail -n+2 aona_status_report.csv | cut -d , -f 2 | awk '{s+=$1} END {print s}')
total_aona_success=$(tail -n+2 aona_status_report.csv | cut -d , -f 3 | awk '{s+=$1} END {print s}')
total_aona_failure=$(tail -n+2 aona_status_report.csv | cut -d , -f 4 | awk '{s+=$1} END {print s}')
total_aona_aborted=$(tail -n+2 aona_status_report.csv | cut -d , -f 5 | awk '{s+=$1} END {print s}')

echo "Total,$total_aona_builds,$total_aona_success,$total_aona_failure,$total_aona_aborted" >> aona_status_report.csv

for gitpr_job in "${gitpr_jobs[@]}";do
  build_count=$(grep "^$gitpr_job," build_list.csv | wc -l | sed 's/^ *//g')
  success_count=$(grep "^$gitpr_job," build_list.csv | grep "SUCCESS" | wc -l | sed 's/^ *//g')
  failure_count=$(grep "^$gitpr_job," build_list.csv | grep "FAILURE" | wc -l | sed 's/^ *//g')
  aborted_count=$(grep "^$gitpr_job," build_list.csv | grep "ABORTED" | wc -l | sed 's/^ *//g')
  echo "$gitpr_job,$build_count,$success_count,$failure_count,$aborted_count" >> gitpr_status_report.csv
done

total_gitpr_builds=$(tail -n+2 gitpr_status_report.csv | cut -d , -f 2 | awk '{s+=$1} END {print s}')
total_gitpr_success=$(tail -n+2 gitpr_status_report.csv | cut -d , -f 3 | awk '{s+=$1} END {print s}')
total_gitpr_failure=$(tail -n+2 gitpr_status_report.csv | cut -d , -f 4 | awk '{s+=$1} END {print s}')
total_gitpr_aborted=$(tail -n+2 gitpr_status_report.csv | cut -d , -f 5 | awk '{s+=$1} END {print s}')

echo "Total,$total_gitpr_builds,$total_gitpr_success,$total_gitpr_failure,$total_gitpr_aborted" >> gitpr_status_report.csv
