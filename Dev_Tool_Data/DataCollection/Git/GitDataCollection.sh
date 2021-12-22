#!/bin/bash +x

url="OpsMx/"

startingday="$1"
endingday="$2"

echo start date is $startingday  end date is $endingday
#declare -a repolist=("Analytics")
#declare -a repolist=("oes-ui")
declare -a repolist=("Analytics" "oes-ui" "oes-api" "oes-test" "audit-client-service" "gate" "platform-service" "visibility-service" "dashboard-service" "audit-service")

echo repoName, OpenPRCount, MergedPRCount, ClosedPRCount, ForcefullyClosedPR, CommitsInOpenPRs, CommitsInMergedPRs, CommitsInClosedPRs, CommitsInForcefullyClosedPRs, NumberofJiraIDs, NumberOfFilesChanged, NumberOfLinesChanged, NumberOfLinesAdded, NumberOfLinesDeleted, NumberOfContributors > repostats.csv

echo repoName, PRAuthor , RepoURL , PRURL , JiraURL > pr-jira-matrix.csv

echo repoName, author , repourl , PRurl , commiturl , fileschanged , lineschanged , linesadded, linesdeleted > author-pr-matrix.csv

for repo in "${repolist[@]}"
do
  echo "Analyzing repository: $repo"
  for state in "open" "merged" "closed" "forceclosed"
  do
    echo "Analyzing data for PRs in $state state"
    if [ $state != "forceclosed" ];then
      if [ $state == "open" ];then
        op="created"
      else
        op=$state
      fi
      
      ##### Fetching PR List between starting and ending date in specific state
      gh pr list -L 1000 --repo $url$repo --state $state --search "$op:$startingday..$endingday" > "$repo"-prlist-"$state".csv
      
    elif [ $state == "forceclosed" ];then
      grep -v MERGED "$repo"-prlist-closed.csv > "$repo"-prlist-forceclosed.csv
    fi
   

    ##### Fetching PRNumbers
    cat "$repo"-prlist-"$state".csv | awk '{print $1}' > "$repo"-prnumbers-"$state".csv

    ##### Adding PR Number of Consolidated PR List
    cat "$repo"-prnumbers-"$state".csv >> "$repo"-prnumbers.csv

   
    ##### Fetch commits in each PR

    while read -r prnum;
    do
      echo $state prnumber is "$prnum" ;
      #gh pr view --repo $url$repo  ${prnum} > a.csv

      gh api repos/$url$repo/pulls/$prnum/commits --jq '.[].sha' > "$repo"-"$prnum"-commits-"$state".csv
      #gh api repos/$url$repo/pulls/$prnum/commits --jq '.[].sha' > "$repo"-"$prnum"-commits.csv
       
      cat "$repo"-"$prnum"-commits-"$state".csv  >> "$repo"-commits-"$state".csv
      #cat "$repo"-"$prnum"-commits.csv  >> "$repo"-commits-"$state".csv
    done < "$repo"-prnumbers-"$state".csv


    ##### Sorting list of commits state wise

    cat "$repo"-commits-"$state".csv | sort -u > "$repo"-sorted-commits-"$state".csv


    ##### Changes made in each commit
    
    while read -r commit;
    do
      numberoffileschanged=$(gh api repos/$url$repo/commits/$commit --jq '.files.[].filename' | wc -l | sed 's/^ *//g')
      committer=$(gh api repos/$url$repo/commits/$commit --jq '.commit.committer.name')
      totalchanges=$(gh api repos/$url$repo/commits/$commit --jq '.stats.total')
      additions=$(gh api repos/$url$repo/commits/$commit --jq '.stats.additions')
      deletions=$(gh api repos/$url$repo/commits/$commit --jq '.stats.deletions')
      #author=$(gh api repos/$url$repo/commits/$commit --jq '.author.login')
      echo "$commit, $committer, $numberoffileschanged, $totalchanges, $additions, $deletions" >> "$repo"-linechanges-$state.csv
      #echo "$commit, $committer, $numberoffileschanged, $totalchanges, $additions, $deletions" >> "$repo"-linechanges.csv
    done < "$repo"-sorted-commits-$state.csv    
    echo "CommitID, Committer, FilesChanged, LinesChanges, LinesAdded, LinesDeleted" > "$repo"-linechanges-sorted-"$state".csv 
    cat "$repo"-linechanges-$state.csv | sort | uniq >> "$repo"-linechanges-sorted-"$state".csv
  done

  ##### Sorting Consolidated PR List
  cat "$repo"-prnumbers.csv | sort | uniq >> "$repo"-prnumbers-sorted.csv


  ##### Adding change data to Consolidated List
  cat "$repo"-linechanges.csv| sort | uniq  >> $repo-linechanges-sorted.csv 

  ##### Fetching JIRA IDs 
  while read -r prnum;
  do
    gh pr view --repo $url$repo  ${prnum} > b.csv
    dos2unix b.csv

    #jiraid=$(cat b.csv | grep https | grep 'OP-[^ ,]*' -o)
    jiraid=$(cat b.csv | grep 'OP-[^ ,][0-9]*' -o | head -1)
    
    author=$(cat b.csv | grep author | awk '{print $2}')
    
    if [ "XX${jiraid}" == "XX" ];then
      jiraid="Nan"
      echo $repo, $author , $url$repo , $url$repo/pull/$prnum , Nan >> pr-jira-matrix.csv 
    else
      echo $repo, $author , $url$repo , $url$repo/pull/$prnum , https://devopsmx.atlassian.net/browse/$jiraid >> pr-jira-matrix.csv 
    fi
    echo $prnum, $jiraid, $author >> "$repo"-"$prnum"-jiraids.csv
    
    cat "$repo"-"$prnum"-jiraids.csv >>"$repo"-jiraids.csv
  done < "$repo"-prnumbers-sorted.csv

  ##### Counting Number of Jira IDs
  numberofjiras=$(cut -d ',' -f 2 "$repo"-jiraids.csv | grep -v Nan | sort | uniq | wc -l | sed 's/^ *//g') 
  echo "Number of JIRA IDS: $numberofjiras"

  ##### Counting Number of PRs in each state
  numberofprs_closed=$(cat "$repo"-prnumbers-closed.csv | wc -l | sed 's/^ *//g')
  numberofprs_open=$(cat "$repo"-prnumbers-open.csv | wc -l | sed 's/^ *//g')
  numberofprs_merged=$(cat "$repo"-prnumbers-merged.csv | wc -l | sed 's/^ *//g')
  numberofprs_forceclosed=$(cat "$repo"-prnumbers-forceclosed.csv | wc -l | sed 's/^ *//g')

  echo "No. of PRs Open: $numberofprs_open"
  echo "No. of PRs Merged: $numberofprs_merged"
  echo "No. of PRs Closed: $numberofprs_closed"
  echo "No. of PRs Force Closed: $numberofprs_forceclosed"

 
  ##### Counting number of commits in each state
  numberofcommits_closed=$(cat "$repo"-commits-closed.csv | wc -l | sed 's/^ *//g')
  numberofcommits_open=$(cat "$repo"-commits-open.csv | wc -l | sed 's/^ *//g')
  numberofcommits_merged=$(cat "$repo"-commits-merged.csv | wc -l | sed 's/^ *//g')
  numberofcommits_forceclosed=$(cat "$repo"-commits-forceclosed.csv | wc -l | sed 's/^ *//g')
    
  echo "Number of Commits in Open PRs: ${numberofcommits_open}"
  echo "Number of Commits in Merged PRs: $numberofcommits_merged"
  echo "Number of Commits in Closed PRs: $numberofcommits_closed"
  echo "Number of Commits in Force Closed PRs: $numberofcommits_forceclosed"
  
  numberofcommitters=$(cut -d ',' -f 2 "$repo"-linechanges-* | sort | uniq | wc -l | sed 's/^ *//g')
  numberofcommitters=$(( $numberofcommitters-1 ))
  if [ "$numberofcommits_open" != "0" ];then
    totalfileschanged_open=$(cat "$repo"-linechanges-open.csv| cut -d , -f 3 | awk '{totalfilesopen += $0} END{print totalfilesopen}')
    totallineschanged_open=$(cat "$repo"-linechanges-open.csv| cut -d , -f 4 | awk '{totallinesopen += $0} END{print totallinesopen}')
    totallinesadded_open=$(cat "$repo"-linechanges-open.csv| cut -d , -f 5 | awk '{totaladdopen += $0} END{print totaladdopen}')
    totallinesdeleted_open=$(cat "$repo"-linechanges-open.csv| cut -d , -f 6 | awk '{totaldeleteopen += $0} END{print totaldeleteopen}')
  else
    totalfileschanged_open=0
    totallineschanged_open=0
    totallinesadded_open=0
    totallinesdeleted_open=0
  fi

  if [ "$numberofcommits_closed" != "0" ];then
    totalfileschanged_closed=$(cat "$repo"-linechanges-closed.csv| cut -d , -f 3 | awk '{totalfilesclosed += $0} END{print totalfilesclosed}')
    totallineschanged_closed=$(cat "$repo"-linechanges-closed.csv| cut -d , -f 4 | awk '{totallinesclosed += $0} END{print totallinesclosed}')
    totallinesadded_closed=$(cat "$repo"-linechanges-closed.csv| cut -d , -f 5 | awk '{totaladdclosed += $0} END{print totaladdclosed}')
    totallinesdeleted_closed=$(cat "$repo"-linechanges-closed.csv| cut -d , -f 6 | awk '{totaldeleteclosed += $0} END{print totaldeleteclosed}')
  else
    totalfileschanged_closed=0
    totallineschanged_closed=0
    totallinesadded_closed=0
    totallinesdeleted_closed=0
  fi

  if [ "$numberofcommits_merged" != "0" ];then
    totalfileschanged_merged=$(cat "$repo"-linechanges-merged.csv| cut -d , -f 3 | awk '{totalfilesmerged += $0} END{print totalfilesmerged}')
    totallineschanged_merged=$(cat "$repo"-linechanges-merged.csv| cut -d , -f 4 | awk '{totallinesmerged += $0} END{print totallinesmerged}')
    totallinesadded_merged=$(cat "$repo"-linechanges-merged.csv| cut -d , -f 5 | awk '{totaladdmerged += $0} END{print totaladdmerged}')
    totallinesdeleted_merged=$(cat "$repo"-linechanges-merged.csv| cut -d , -f 6 | awk '{totaldeletemerged += $0} END{print totaldeletemerged}')
  else
    totalfileschanged_merged=0
    totallineschanged_merged=0
    totallinesadded_merged=0
    totallinesdeleted_merged=0
  fi

  if [ "$numberofcommits_forceclosed" != "0" ];then
    totalfileschanged_forceclosed=$(cat "$repo"-linechanges-forceclosed.csv| cut -d , -f 3 | awk '{totalfilesforceclosed += $0} END{print totalfilesforceclosed}')
    totallineschanged_forceclosed=$(cat "$repo"-linechanges-forceclosed.csv| cut -d , -f 4 | awk '{totallinesforceclosed += $0} END{print totallinesforceclosed}')
    totallinesadded_forceclosed=$(cat "$repo"-linechanges-forceclosed.csv| cut -d , -f 5 | awk '{totaladdforceclosed += $0} END{print totaladdforceclosed}')
    totallinesdeleted_forceclosed=$(cat "$repo"-linechanges-forceclosed.csv| cut -d , -f 6 | awk '{totaldeleteforceclosed += $0} END{print totaldeleteforceclosed}')
  else
    totalfileschanged_forceclosed=0
    totallineschanged_forceclosed=0
    totallinesadded_forceclosed=0
    totallinesdeleted_forceclosed=0
  fi
  
  totalfileschanged=$(($totalfileschanged_open + $totalfileschanged_merged + $totalfileschanged_forceclosed))
  totallineschanged=$(($totallineschanged_open + $totallineschanged_merged + $totallineschanged_forceclosed))
  totallinesadded=$(($totallinesadded_open + $totallinesadded_merged + $totallinesadded_forceclosed))
  totallinesdeleted=$(($totallinesdeleted_open + $totallinesdeleted_merged + $totallinesdeleted_forceclosed))

  echo "Total number of files changed: $totalfileschanged"
  echo "Total number of lines changed: $totallineschanged"
  echo "Total number of lines added: $totallinesadded"
  echo "Total number of lines deleted: $totallinesdeleted"
  echo "Total number of unique contributors: $numberofcommitters"

  echo $repo, $numberofprs_open, $numberofprs_merged, $numberofprs_closed, $numberofprs_forceclosed, $numberofcommits_open, $numberofcommits_merged, $numberofcommits_closed, $numberofcommits_forceclosed, $numberofjiras, $totalfileschanged, $totallineschanged, $totallinesadded, $totallinesdeleted, $numberofcommitters >> repostats.csv

#  while read -r prnum;
#  do
#    while read -r commit;
#    do
#      author=$( gh api repos/opsmx/$repo/commits/$commit --jq '.commit.author.name')
#      fileschanged=$(cat "$repo"-linechanges.csv | grep "$commit" | cut -d , -f 3 | wc -l )
#      lineschanged=$(cat "$repo"-linechanges.csv | grep "$commit" | cut -d , -f 4 | wc -l )
#      linesadded=$(cat "$repo"-linechanges.csv | grep "$commit" | cut -d , -f 5 | wc -l )
#      linesdeleted=$(cat "$repo"-linechanges.csv | grep "$commit" | cut -d , -f 6 | wc -l )
#      echo $author , $url$repo , $url$repo/pull/$prnum , $url$repo/pull/$prnum/commits/$commit , $fileschanged , $lineschanged >> author-pr-matrix.csv
#    done < "$repo"-"$prnum"-commits.csv
#  done < "$repo"-prnumbers-sorted.csv
done
#
#cat author-pr-matrix.csv | awk '{print $2}' | sort -u | grep -v author > authors.csv
#
#echo author , numberoffiles , numberoflines > author-contrib.csv
#for author in $(cat authors.csv)
#do
#  cat author-pr-matrix.csv | grep $author | awk '{print $6}' > $author-files.csv
#  cat author-pr-matrix.csv | grep $author | awk '{print $7}' > $author-lines.csv
#  numberoffiles=$(awk '{ sum += $1 } END { print sum }' "$author"-files.csv)
#  numberoflines=$(awk '{ sum += $1 } END { print sum }' "$author"-lines.csv)
#  echo $author , $numberoffiles , $numberoflines >> author-contrib.csv
#
#done
