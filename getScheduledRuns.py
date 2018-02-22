import os
import sys
import json
import requests
import base64
from html import escape
from pprint import pprint
from requests.auth import HTTPBasicAuth
from datetime import datetime

AutomationContentFieldId = 5069402 # TODO: get this from another call to get all fields for this project

projectid = sys.argv[1]
APITOKEN = "ZGVtb3xlbGlzZS5jYXJtaWNoYWVsQHFhc3ltcGhvbnkuY29tOjE1NTA4NjIzMTMzNDM6MDljY2ZiMGVkZDQ4M2IzYjI0MTdlOWY5YjIyNmEzYjc"
GetTCURL = "https://demo.qtestnet.com/api/v3/projects/" + projectid + "/test-cases/"
GetTRURL = "https://demo.qtestnet.com/api/v3/projects/" + projectid + "/test-runs/"

AutomationContents = ""

if('QTE_SCHEDULED_TX_DATA' in os.environ):
    processUrl = os.environ['QTE_SCHEDULED_TX_DATA']

    #pprint("Scheduled Jobs URL: " + processUrl)

    myResponse = requests.get(url = processUrl, headers = {"Content-Type" : "application/json"})

    if(myResponse.ok):
        response = json.loads(myResponse.content)
        #print(json.dumps(response, sort_keys=True, indent=4))

        for testRun in response["QTE"]["testRuns"]:
            # Get the test run to get the test case id
            myTestRunResponse = requests.get(url = GetTRURL + testRun["Id"], headers = {"Content-Type" : "application/json", "Authorization": APITOKEN})

            if(myTestRunResponse.ok):
                myTestRun = json.loads(myTestRunResponse.content)
                #print(json.dumps(myTestRun, sort_keys=True, indent=4))
                
                # Get the test run to get the test case id
                myTestCaseResponse = requests.get(url = GetTCURL + str(myTestRun["test_case"]["id"]), headers = {"Content-Type" : "application/json", "Authorization": APITOKEN})

                if(myTestCaseResponse.ok):
                    myTestCase = json.loads(myTestCaseResponse.content)
                    #print(json.dumps(myTestCase, sort_keys=True, indent=4))
                    for field in myTestCase["properties"]:
                        if field["field_id"] == AutomationContentFieldId:
                            if AutomationContents:
                                AutomationContents = " " + AutomationContents + field["field_value"]
                            else:
                                AutomationContents = AutomationContents + field["field_value"]
                    
                else:
                    myTestCaseResponse.raise_for_status()
            else:
                myTestRunResponse.raise_for_status()
    
    else:
        myResponse.raise_for_status()
else:
    pprint("Missing QTE_SCHEDULED_TX_DATA environment variable!")

pprint(AutomationContents)