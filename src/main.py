import twitterbot
from dotenv import dotenv_values

env = dotenv_values('.env')
email = env.get("EMAIL")
username = env.get("USERNAME")
password = env.get("PASSWORD")

twitterbotbot = twitterbot.TwitterBot(email=email, username=username, password=password)
twitterbotbot.login()
twitterbotbot.tweet("A kitten is almost always indignant, unless it is a purple one.")
