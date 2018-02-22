/////// Pulse version
var payload = body;
var testResults = payload.result; 
var projectId = payload.projectId;
var cycleId = payload["test-cycle"];

xml2js = require('xml2js');

//////// Commandline version
// var fs = require('fs');
// 
// var projectId = 73292; // Demo - Sauce Labs Integration Project
// var cycleId = 1118427; // Demo - Sauce Labs Integration Project
/// TODO: Remove above

var testLogs = [];
function FormatLogs(tr) {
    
    var testResults = JSON.parse(tr);
    //emitEvent('SlackEvent', { FormattingJUnitLogs: testResults });
       
    testResults.testsuite.testcase.forEach(function(tc) {
        var tcResult = tc["$"];
        var tcName = "";

        // Format the name
        var note = "";
        if(!tcResult.name) 
            tcName = "Unnamed";
        else 
            tcName = tcResult.name.substring(0, tcResult.name.indexOf('['));
            note = tcResult.name;

        TCStatus = "PASS";
        
        if(tc.failure) {
            TCStatus = "FAIL";
            if(note)
                note = "\n" + JSON.stringify(tc.failure);
            else
                note = JSON.stringify(tc.failure);
        }

        // The automation content is what we're going to use to run this later so it's important to get that format for Python pytest
        //$file :: $classname (after the last .) :: $name (before the [)
        var tcShortClassName = tcResult.classname.substring(tcResult.classname.lastIndexOf('.') + 1)
        var auto = tcResult.file + "::" + tcShortClassName + "::" + tcName;

        var reportingLog = {
            exe_start_date: new Date(), // TODO this could use the time to complete to be more precise
            exe_end_date: new Date(),
            module_names: [
                'JUnitTests'
            ],
            name: tcName,
            automation_content: auto,
            note: note
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

 // Pulse Version
var parser = new xml2js.Parser();
parser.parseString(testResults, function (err, result) {
    var formattedResults = FormatLogs(JSON.stringify(result));
    emitEvent('UpdateQTestAndScenarioWithFormattedResultsEvent', formattedResults );
});



/// Command line version
// fs.readFile('results.xml', function(err, data) {
//     parser.parseString(data, function (err, result) {
//         var formattedResults = FormatLogs(JSON.stringify(result));
//         Write new file
//         var payload = fs.writeFile('formattedResults.json', JSON.stringify(formattedResults, null, "  " ), 'utf8', function() {
//             console.log("File written: formattedResults.json");
//         });
//     });
// });



