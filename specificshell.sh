#!/bin/bash

location=$1
projectid=$2

echo location: $location
echo projectid: $projectid

# TODO: Update local code/test base
#git pull

# This script prints out a space separated lists of scheduled runs (space separated automation contents)
scheduledRuns=$(python3 getScheduledRuns.py "$projectid")

#The output adds extra 's around the string, so let's strip them
trimmedRuns=$(echo $scheduledRuns | tr -d "[='=]")

pytest $trimmedRuns --location local --resultlog results.txt --junitxml=result.xml 


# Execute tests locally
if [ $location = 'local' ]
then
    pytest tests --location local --resultlog results.txt --junitxml=result.xml

else # Execute tests against sauce labs
    pytest tests --location sauce --resultlog results.txt --junitxml=result.xml
fi

# Send raw results to Pulse for parsing
# Read in file
logs=$(<result.xml)
logs=`echo $logs|tr '\n' ' '`
logs=`echo $logs|tr '"' "'"`

# TODO: Could be more clever about how we get the cycle id - maybe the parent suite or cycle? Depends on your setup
request='{
    "test-cycle" : 1118427, 
    "result" : "'"$logs"'",
    "projectId" : '"$projectid"'
}'

echo "$request"

# NOTE2: The url is in the Automation Integration project under the demo account for parsing results
curl -X POST \
  https://pulse.qas-labs.com/api/v1/webhooks/5a01e95fff85516fe58bbcf0/c672e4415a1d5d175f6de726/1ed65eb8-efe2-4179-8e0c-a32476273762 \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d "$request"

 echo DONE