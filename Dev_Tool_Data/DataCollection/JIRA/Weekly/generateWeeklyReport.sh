python3 getActiveSprint.py $1 $2 $3 $4 $5
bash aggregator.sh
bash weeklyDataProcessor.sh
python3 getStalenessReport.py $2 $3 $4 $5
