import unittest
import time, random
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class YoutubeUrl(unittest.TestCase):

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options = chrome_options)
        self.driver.implicitly_wait(5)

    def test(self):
        driver = self.driver
        # open youtube and pass the sign in-terms pop-ups
        driver.get("https://www.youtube.com/")
        driver.find_element_by_xpath("//div[@id='dismiss-button']/yt-button-renderer/a/paper-button[@id='button']").click()
        driver.switch_to.frame(driver.find_element_by_id('iframe'))
        driver.find_element_by_id("introAgreeButton").click()
        driver.switch_to.default_content()
        # click on Tranding button and on a random video from trending list
        driver.find_element_by_partial_link_text('Trending').click()
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("title-wrapper"))
        videoList = driver.find_elements_by_id("title-wrapper")
        videoList[random.randint(0,len(videoList))].click()
        url = driver.current_url
        time.sleep(1)
        # open a new tab with the same video and check if the url is the same
        driver.execute_script('''window.open("'''+url+'''","_blank");''')
        urlNew = driver.current_url
        assert urlNew == url
        time.sleep(1)

    def tearDown(self):
        self.driver.close()


def suite():
    suite = unittest.TestSuite()
    suite.addTest(YoutubeUrl("test"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

