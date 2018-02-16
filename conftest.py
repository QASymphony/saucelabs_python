import pytest
import json
import logging
from os import environ

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.remote_connection import RemoteConnection

saucebrowsers = [{
        "platform": "Windows 10",
        "browserName": "MicrosoftEdge",
        "version": "14.14393"
    }, 
    {
        "platform": "Windows 10",
        "browserName": "firefox",
        "version": "49.0"
    }, 
    {
        "platform": "Windows 7",
        "browserName": "internet explorer",
        "version": "11.0"
    }, 
    {
        "platform": "OS X 10.11",
        "browserName": "safari",
        "version": "10.0"
    }, 
    {
        "platform": "OS X 10.11",
        "browserName": "chrome",
        "version": "54.0"
    }]

localbrowsers = [{
        "platform": "local",
        "browserName": "chrome"
    }] 
def pytest_addoption(parser):
    parser.addoption("-L","--location",
                    dest="location",
                    action="append",
                    help="Location. Valid options are local (via chrome driver) and sauce")

def pytest_generate_tests(metafunc):
    #logging.warning("verify!", json.dumps(val))

    if metafunc.config.option.location[0] == "sauce":
        metafunc.parametrize('browser_config',
                        saucebrowsers,
                        ids=_generate_param_ids('browserConfig', saucebrowsers),
                        scope='function')
    else: # For local, will parameterize differently
        metafunc.parametrize('browser_config', localbrowsers)


def _generate_param_ids(name, values):
    return [("<%s:%s>" % (name, value)).replace('.', '_') for value in values]

@pytest.yield_fixture(scope='function')
def driver(request, browser_config):

    if browser_config["platform"] == "local":
        browser = webdriver.Chrome() 
    
        yield browser
        browser.quit()
    else: 
        # if the assignment below does not make sense to you please read up on object assignments.
        # The point is to make a copy and not mess with the original test spec.
        desired_caps = dict()
        desired_caps.update(browser_config)
        test_name = request.node.name
        build_tag = environ.get('BUILD_TAG', None)
        tunnel_id = environ.get('TUNNEL_IDENTIFIER', None)
        username = environ.get('SAUCE_USERNAME', None)
        access_key = environ.get('SAUCE_ACCESS_KEY', None)

        selenium_endpoint = "https://%s:%s@ondemand.saucelabs.com:443/wd/hub" % (username, access_key)
        desired_caps['build'] = build_tag
        desired_caps['tunnelIdentifier'] = tunnel_id
        desired_caps['name'] = test_name

        executor = RemoteConnection(selenium_endpoint, resolve_ip=False)
        browser = webdriver.Remote(
            command_executor=executor,
            desired_capabilities=desired_caps
        )

        # This is specifically for SauceLabs plugin.
        # In case test fails after selenium session creation having this here will help track it down.
        # creates one file per test non ideal but xdist is awful
        if browser is not None:
            with open("%s.testlog" % browser.session_id, 'w') as f:
                f.write("SauceOnDemandSessionID=%s job-name=%s\n" % (browser.session_id, test_name))
        else:
            raise WebDriverException("Never created!")

        yield browser
        # Teardown starts here
        # report results
        try:
            browser.execute_script("sauce:job-result=%s" % str(not request.node.rep_call.failed).lower())
            browser.quit()
        except WebDriverException:
            # we can ignore the exceptions of WebDriverException type -> We're done with tests.
            print('Warning: The driver failed to quit properly. Check test and server side logs.')


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # this sets the result as a test attribute for SauceLabs reporting.
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)