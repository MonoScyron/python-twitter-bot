"""
Controls your Twitter bot, uses SeleniumTwitter to access Twitter
"""

import json
import tracery
import seleniumtwitter
from typing import Tuple
from tracery.modifiers import base_english


class TwitterBot:
    def __init__(self, email: str, username: str, password: str):
        """
        :param email: Registered email of the twitter bot
        :param username: Username of the twitter bot
        :param password: Password of the twitter bot
        """
        # TODO: Uncomment this (commented to save time debugging, webdriver is slow)
        # self.__twitter = seleniumtwitter.SeleniumTwitter(email=email, username=username, password=password)

    def generate_tweet(self, path: str = "./rules/tracery.json") -> None:
        # TODO: Generate tweet and post it
        # TODO: Add custom grammer for "The" (definitive article)
        #   TODO: Article shouldn't be capitalized UNLESS it is first word
        #   TODO: Article should be removed if name is plural
        grammar = tracery.Grammar(json.load(open(path)))
        grammar.add_modifiers(base_english)
        print(grammar.flatten("#origin#"))

    def get_image(self, url: str) -> str:
        # TODO: Check if url image is already downloaded in img folder, if not download_img(), return path to image
        # ? Return as absolute path or relative path
        return None

    def download_img(self, url: str) -> str:
        # TODO: Download an image to the img folder, return path to download
        # ? Return as absolute path or relative path
        return None

    def generate_svg(self, svg: str) -> str:
        # TODO: Generate an svg from given str and save as image in img folder, return path to image
        # ? Return as absolute path or relative path
        # TODO: Delete svg once done
        return None
