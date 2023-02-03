"""
TwitterBot class
"""

from time import sleep
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class TwitterBot:
    def __init__(self, email: str, username: str, password: str, headless=True):
        """
        :param email: Registered email of the bot
        :param username: Username of the bot
        :param password: Password of the bot
        """
        self.__email = email
        self.__username = username
        self.__password = password

        if headless:
            opt_chrome = Options()
            opt_chrome.add_argument('--headless')
            self.bot = webdriver.Chrome(
                options=opt_chrome
            )
        else:
            self.bot = webdriver.Chrome()

        self.__wait = WebDriverWait(self.bot, timeout=5)
        self.logged_in = False

    def __login(self) -> None:
        """
        Login to Twitter with provided credentials
        :return: None
        """
        bot = self.bot
        wait = self.__wait
        bot.get('https://twitter.com/login')

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
            pwd_input = wait.until(ec.visibility_of_element_located((By.NAME, 'password')))
            pwd_input.clear()
            pwd_input.send_keys(self.__password)
            pwd_input.send_keys(Keys.RETURN)

        self.logged_in = True

    def tweet(self, text: str) -> None:
        if not self.logged_in:
            self.__login()
            sleep(3)

        bot = self.bot
        wait = self.__wait
        bot.get('https://twitter.com/compose/tweet')

        text_input = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'public-DraftEditor-content')))
        text_input.send_keys(text)
        ActionChains(bot).key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(Keys.CONTROL).perform()

    def test_browser(self) -> None:
        """
        Open google.com as a test
        :return: None
        """
        bot = self.bot
        bot.get('https://www.google.com/')
        sleep(10)
