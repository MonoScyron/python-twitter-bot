"""
Controls your Twitter bot, uses WebDriverTwitter to access Twitter
"""

import json

import tracery
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
from tracery.modifiers import base_english

import webdrivertwitter


class TwitterBot:
    def __init__(self, email: str, username: str, password: str):
        """
        :param email: Registered email of the twitter bot
        :param username: Username of the twitter bot
        :param password: Password of the twitter bot
        """
        self.__mods = {"rmd": self.__rm_definitive}
        # TODO: Uncomment this (commented to save time debugging, webdriver is slow)
        self.__twitter = webdrivertwitter.WebDriverTwitter(email=email, username=username, password=password)

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
        # TODO: Given {svg ...} tag, pass <svg>...</svg> to generate_svg()
        #   Return path to generated png from the svg
        # Return as relative path
        return None

    @staticmethod
    def __generate_svg(svg: str) -> str:
        """
        Generates PNG image from a SVG html tag (<svg>...</svg>)
        :param svg: SVG to generate
        :return: Relative path to generated PNG
        """
        to_temp = "./img/svg/temp_svg"
        svg_f = open(f"{to_temp}.svg", "w")
        svg_f.write(svg)
        svg_f.close()
        svg_pic = svg2rlg(f"{to_temp}.svg")
        renderPM.drawToFile(svg_pic, f"{to_temp}.png")
        return f"{to_temp}.png"

    @staticmethod
    def __rm_definitive(text: str) -> str:
        """
        Remove the definitive article of the text\n
        Ex: "The Beatles" -> "Beatles"
        Modifier should only be used on nouns and noun phrases\n
        :param text: Text to modify
        :return: Modified text
        """
        if text.lower().startswith("the"):
            return text[3:].strip()
        else:
            return text
