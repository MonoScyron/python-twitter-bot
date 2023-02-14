"""
Interface with Twitter via a WebDriver
"""
import os
import undetected_chromedriver as uc
from time import sleep
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


# ? TODO: Consider switching to playwright [https://playwright.dev/python/docs/intro]
class WebDriverTwitter:
    def __init__(self, email: str, username: str, password: str, headless=True):
        """
        :param email: Registered email of the twitter account
        :param username: Username of the twitter account
        :param password: Password of the twitter account
        """
        self.__email = email
        self.__username = username
        self.__password = password

        if headless:
            opt_chrome = uc.ChromeOptions()
            opt_chrome.headless = True
            opt_chrome.add_argument('--headless')
            self.__driver = uc.Chrome(options=opt_chrome)
        else:
            self.__driver = uc.Chrome()

        self.__wait = WebDriverWait(self.__driver, timeout=5)
        self.logged_in = False

    def teardown(self) -> None:
        """
        Closes all processes related to the webdriver
        :return: None
        """
        # FIXME: Teardown causes WinError
        self.__driver.quit()

    def tweet(self, text: str = None, pics: list[str] = None) -> None:
        """
        Post a tweet
        :param text: Text to be tweeted
        :param pics: Path of pics to be tweeted, up to 4
        :return: None
        """
        if not self.logged_in:
            self.login()

        browser = self.__driver
        wait = self.__wait
        browser.get('https://twitter.com/compose/tweet')

        if text:
            text_input: WebElement = wait.until(
                ec.visibility_of_element_located((By.CLASS_NAME, 'public-DraftEditor-content')))
            text_input.send_keys(text)
        if pics:
            pic_input: WebElement = wait.until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]')))
            for p in pics:
                pic_input.send_keys(os.path.abspath(p))
                sleep(1)

        # Send tweet
        ActionChains(browser).key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(Keys.CONTROL).perform()
        sleep(3)

    def login(self) -> None:
        """
        Login to Twitter with provided credentials
        :return: None
        """
        browser = self.__driver
        wait = self.__wait
        browser.get('https://twitter.com/login')

        # Enter email
        email_input = wait.until(ec.visibility_of_element_located((By.NAME, 'text')))
        email_input.clear()
        email_input.send_keys(self.__email)
        email_input.send_keys(Keys.RETURN)

        try:
            # Check if Twitter is suspicious about your account
            if 'phone number' in wait.until(ec.visibility_of_element_located((By.ID, 'modal-header'))).text:
                # Verify username
                username_input = wait.until(ec.visibility_of_element_located((By.NAME, 'text')))
                username_input.send_keys(self.__username)
                username_input.send_keys(Keys.RETURN)
                # Then enter password
                pwd_input = wait.until(ec.visibility_of_element_located((By.NAME, 'password')))
                pwd_input.clear()
                pwd_input.send_keys(self.__password)
                pwd_input.send_keys(Keys.RETURN)
        except TimeoutException:
            # Enter password directly if not sus
            pwd_input = browser.find_element(By.NAME, 'password')
            pwd_input.clear()
            pwd_input.send_keys(self.__password)
            pwd_input.send_keys(Keys.RETURN)

        sleep(3)
        self.logged_in = True

    # TODO: DELETE THIS FUNCTION
    def get_browser(self):
        return self.__driver
