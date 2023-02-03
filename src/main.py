"""
Main driver
"""

import twitterbot
from time import sleep
from dotenv import dotenv_values

env = dotenv_values('.env')
bot = twitterbot.TwitterBot(email=env.get("EMAIL"), username=env.get("USERNAME"), password=env.get("PASSWORD"))

# TODO: Write driver
