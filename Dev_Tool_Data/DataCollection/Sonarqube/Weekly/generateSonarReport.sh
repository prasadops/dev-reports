username="$1"
password="$2"
start_date="$3"
end_date="$4"

python3 getProjectList.py $1 $2
python3 getIssueTypesData.py $1 $2 $3 $4
python3 getSeverityData.py $1 $2 $3 $4
python3 getScopeData.py $1 $2 $3 $4
python3 getResolutionReport.py $1 $2 $3 $4
python3 getStatusReport.py $1 $2 $3 $4
python3 getCreationDateWiseData.py $1 $2 $3 $4
python3 getRuleViolations.py $1 $2 $3 $4
