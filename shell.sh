#!/bin/bash

location=$1
projectid=$2

echo location: $location
echo projectid: $projectid

# TODO: Update local code/test base
# git -C /Users/elise/Repos/folder_name pull


# Execute tests locally
if [ $location = 'local' ]
then
    pytest tests --location local --resultlog results.txt --junitxml=result.xml

else # Execute tests against sauce labs
    pytest tests --location sauce --resultlog results.txt --junitxml=result.xml
fi

# Send raw results to Pulse for parsing
#Read in file
logs=$(<results.xml)
# echo "$logs"

# NOTE, this test-cycle is hard coded for the project this is running for
# use process.env.QTE_SCHEDULED_TX_DATA (https://support.qasymphony.com/hc/en-us/articles/115004483563-Using-the-Shell-Agent)
# to make this more robust

# NOTE2: The url is in the Automation Integration project under the demo account for parsing results
curl -X POST \
  https://pulse.qas-labs.com/api/v1/webhooks/5a01e95fff85516fe58bbcf0/emNvHmCrX8sDq6yPp/eae61941-e9cf-42c0-a553-4117640b705e \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{
    "test-cycle" : 1118427, 
    "result" : "$logs",
    "projectId" : '"$projectid"'
}'

 echo DONE