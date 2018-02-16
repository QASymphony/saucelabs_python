import pytest

@pytest.mark.usefixtures('driver')
class TestStaticSandbox(object):

    def test_basic_link(self, driver):
        driver.get('https://saucelabs-sample-test-frameworks.github.io/training-test-page')
        driver.find_element_by_id("i_am_a_link").click()

        title = "I am another page title - Sauce Labs"
        assert title == driver.title