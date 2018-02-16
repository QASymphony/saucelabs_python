/////// Pulse version
var payload = body;
var testResults = payload.result; 
var projectId = payload.projectId;
var cycleId = payload["test-cycle"];

//////// Commandline version
// var fs = require('fs');
// xml2js = require('xml2js');
// var projectId = 73292; // Demo - Sauce Labs Integration Project
// var cycleId = 1118427; // Demo - Sauce Labs Integration Project
/// TODO: Remove above

var testLogs = [];
function FormatLogs(tr) {
    //emitEvent('SlackEvent', { FormattingJUnitLogs: testResults });
    var testResults = JSON.parse(tr);
    
    //console.log("JSON test case: " + testResults.testsuite);
       
    testResults.testsuite.testcase.forEach(function(tc) {
        var tcResult = tc["$"];
        var tcName = "";

        // Format the name
        if(!tcResult.name) 
            tcName = "Unnamed";
        else 
            tcName = tcResult.name.substring(0, tcResult.name.indexOf('['));

        TCStatus = "PASS";
        
        var errmsg = "";
        if(tc.failure) {
            TCStatus = "FAIL";
            errmsg = JSON.stringify(tc.failure);
        }

        var reportingLog = {
            exe_start_date: new Date(), // TODO this could use the time to complete to be more precise
            exe_end_date: new Date(),
            module_names: [
                'JUnitTests'
            ],
            name: tcName,
            automation_content: tcResult.classname + "::" + tcName,
            note: errmsg
        };

        // There are no steps here, so we'll add one step entry
        var testStepLogs = [{
            order: 0,
            description: tcName,
            expected_result: tcName,
            status: TCStatus
        }];

        reportingLog.description = "Test case imported from Python Test"
        reportingLog.status = TCStatus;
        reportingLog.test_step_logs = testStepLogs;
        testLogs.push(reportingLog);
    });

    var formattedResults = {
        "projectId" : projectId,
        "test-cycle" : cycleId,
        "logs" : testLogs
    };

    return formattedResults;

}

var parser = new xml2js.Parser();
fs.readFile('results.xml', function(err, data) {
    parser.parseString(data, function (err, result) {
        var formattedResults = FormatLogs(JSON.stringify(result));

        /// Command line version
        // Write new file
        // var payload = fs.writeFile('formattedResults.json', JSON.stringify(formattedResults, null, "  " ), 'utf8', function() {
        //     console.log("File written: formattedResults.json");
        // });
    
        // Pulse Version
        // Emit next fxn to upload results/parse
        emitEvent('UpdateQTestAndScenarioWithFormattedResultsEvent', formattedResults );
    });
});



