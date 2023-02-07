"""
Controls your Twitter bot, uses SeleniumTwitter to access Twitter
"""

import json
import seleniumtwitter
import tracery
from tracery.modifiers import base_english


class TwitterBot:
    def __init__(self, email: str, username: str, password: str):
        """
        :param email: Registered email of the twitter bot
        :param username: Username of the twitter bot
        :param password: Password of the twitter bot
        """
        self.__mods = {"rmd": self.__rm_definitive}
        # TODO: Uncomment this (commented to save time debugging, webdriver is slow)
        self.__twitter = seleniumtwitter.SeleniumTwitter(email=email, username=username, password=password)

    def shutdown(self) -> None:
        """
        Shuts bot down
        :return: None
        """
        self.__twitter.teardown()

    def make_tweet_from_json(self, path: str = "./rules/tracery.json") -> None:
        # TODO: Generate tweet and post it
        grammar = tracery.Grammar(json.load(open(path)))
        grammar.add_modifiers(base_english)
        grammar.add_modifiers(self.__mods)

        text = grammar.flatten("#origin#")
        # TODO: Parse text for images
        #   {img ./blah/blah.jpg} should be parsed into relative path
        #   {svg <svg>...</svg>} should be generated & parsed into relative path

        # TODO: Actually tweet the text + pics
        # self.__twitter.tweet(text=text)
        print(text)

    def get_image(self, tag: str) -> str:
        # TODO: Given {img ...} tag, return path to image
        # TODO: Given {svg ...} tag, generate svg and return path to generated image, delete svg after tweeted
        # Return as relative path
        return None

    def generate_svg(self, svg: str) -> str:
        # TODO: Generate an svg from given str and save as image in img folder, return path to image
        # Return as relative path
        # TODO: Delete svg once it is tweeted
        return None

    @staticmethod
    def __rm_definitive(text: str, *params) -> str:
        """
        Remove the definitive article of the text\n
        Ex: "The Beatles" -> "Beatles"
        Modifier should only be used on nouns and noun phrases\n
        :param text: Text to modify
        :param params: No params accepted
        :return:
        """
        if text.lower().startswith("the"):
            return text[3:].strip()
        else:
            return text
