import pytest

@pytest.mark.usefixtures('driver')
class TestCommentSandbox(object):

    def test_comment_submission(self, driver):
        driver.get('https://saucelabs-sample-test-frameworks.github.io/training-test-page')
        email_text_field = driver.find_element_by_id("fbemail")
        email_text_field.send_keys("elisecarmichael@qasymphony.com")

        email_text_field = driver.find_element_by_id("comments")
        thanks_text = "Thanks for helping me test out the sauce labs integration to qTest Launch!"
        email_text_field.send_keys(thanks_text)

        driver.find_element_by_id("submit").click()

        text = driver.find_element_by_id("your_comments").text
        assert thanks_text in text

    def test_comment_submission_expectfail(self, driver):
        assert 0
