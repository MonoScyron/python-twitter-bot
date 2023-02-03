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
    def __init__(self, email: str, username: str, password: str):
        """
        :param email: Registered email of the bot
        :param username: Username of the bot
        :param password: Password of the bot
        """
        self.email = email
        self.username = username
        self.password = password
        opt = Options()
        # FIXME: Chrome doesn't start in headless properly
        opt.add_argument('--headless')
        self.bot = webdriver.Chrome()
        self.wait = WebDriverWait(self.bot, timeout=5)

    def login(self) -> None:
        """
        Log into Twitter using provided bot credentials
        :return: None
        """
        bot = self.bot
        wait = self.wait
        bot.get('https://twitter.com/login')

        # Enter email
        email_input = wait.until(ec.visibility_of_element_located((By.NAME, 'text')))
        email_input.send_keys(self.email)
        email_input.send_keys(Keys.RETURN)

        try:
            # Check if Twitter is suspicious about your account
            if 'phone number' in wait.until(ec.visibility_of_element_located((By.ID, 'modal-header'))).text:
                # Verify username
                username_input = wait.until(ec.visibility_of_element_located((By.NAME, 'text')))
                username_input.send_keys(self.username)
                username_input.send_keys(Keys.RETURN)
                # Then enter password
                pwd_input = wait.until(ec.visibility_of_element_located((By.NAME, 'password')))
                pwd_input.send_keys(self.password)
                pwd_input.send_keys(Keys.RETURN)
        except TimeoutException:
            # Enter password directly if not sus
            pwd_input = wait.until(ec.visibility_of_element_located((By.NAME, 'password')))
            pwd_input.send_keys(self.password)
            pwd_input.send_keys(Keys.RETURN)

    def tweet(self, text: str) -> None:
        bot = self.bot
        wait = self.wait
        # FIXME: For some reason, this get() causes Twitter to log the bot out
        bot.get('https://twitter.com/compose/tweet')

        text_input = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'public-DraftEditor-content')))
        text_input.send_keys(text)
        ActionChains(bot).key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(Keys.CONTROL).preform()
