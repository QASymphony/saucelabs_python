# saucelabs_python
An example of integration with the Automation Host's Shell Agent integrated into Sauce Labs - In Python, using PyTest.

### Environment
1. Install Python
2. Install pip for package management

### Local setup
Set your selenium driver to run at `http://localhost:4444/wd/hub`

*   All tests running locally:
    ```$ pytest tests --location local --resultlog results.txt --junitxml=results.xml```

*   A specific test file running localy:
    ```pytest tests/test_static_sandbox.py --location local --resultlog results.txt --junitxml=result.xml```

*   Tests in Parallel:
    ```$ pytest -s -n 10 tests --location local --resultlog results.txt --junitxml=results.xml```


### Set up sauce labs
Two environment variables are needed for access:
SAUCE_USERNAME=<your sauce labs username>
SAUCE_ACCESS_KEY=<your sauce labs access key>

The sauce labs access key can be found here: # TODO ADD GIF

### Install prerequisites to run
    ```$ pip install -r requirements.txt```

### Running Tests locally with chrome driver

### Running Tests against Sauce:  -n option designates number of parallel tests and -s to disable output capture.

*  Tests one at time:
    ```$ pytest tests --location sauce --resultlog results.txt --junitxml=results.xml```

*  Tests in Parallel:
    ```$ pytest -s -n 10 tests --location sauce --resultlog results.txt --junitxml=results.xml```

* Dump session ids for the SauceLabs CI plugins:
    ```$ cat $(find . -name "*.testlog")```

### Automation Host Integration
There are two shell scripts that can be included with the automation host.

##Run all tests
This will run all the tests in your tests folder within your python project against the location specified (local or sauce)

```shell.sh```

Call with either within your shell agent
```/Users/elise/Repos/saucelabs/saucelabs_python/shell.sh local $QTE.projectId```

or

```/Users/elise/Repos/saucelabs/saucelabs_python/shell.sh local $QTE.projectId```

##Run specific tests
This will use the automation content's to execute just the tests specified in the location specified (local or sauce)

```specificshell.sh```

Call with either within your shell agent
```/Users/elise/Repos/saucelabs/saucelabs_python/shell.sh local $QTE.projectId```

or

```/Users/elise/Repos/saucelabs/saucelabs_python/shell.sh sauce $QTE.projectId```
