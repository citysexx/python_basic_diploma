import re

import telebot
from typing import Dict, AnyStr, List

from swagger_client.rest import ApiException

from src.utils.regex import *
import src.bin.weather as weather


def from_string(user_input: ['telebot.types.Message']) -> Dict[AnyStr, List]:
    """
    This function accepts the user's message from telegram and extracts keywords
    from them using regex. Then the function switches flags inside a dictionary
    and returns the set of actions the program must conduct

    Args:
        user_input: a telebot Message object that the user enters
    """
    string: AnyStr = user_input.text
    pattern = re.compile(re.compile(r'\b\w+\b'))
    keywords = re.findall(pattern, string)
    flags: Dict[AnyStr, List] = {'keywords': keywords,
                                 'said_hi': [re.findall(template, string) for template in hi_regex],
                                 'said_bye': [re.findall(template, string) for template in bye_regex],
                                 'said_thanks': [re.findall(template, string) for template in thanks_regex],
                                 'asked_help': [re.findall(template, string) for template in help_regex],
                                 'cursed': [re.findall(template, string) for template in curse_regex],
                                 'said_curr': [re.findall(template, string) for template in current_regex],
                                 'said_future': [re.findall(template, string) for template in future_regex],
                                 'said_cities': []}
    # TODO В значениях словаря содержатся списки, но там есть еще списки. Их надо разложить. Поработать с регуляркой,
    #  определяющей город

    for word in keywords:

        try:
            city_responded = weather.current_weather(word)
        except ApiException:
            pass
        else:
            flags['said_cities'].append(city_responded.city)

    return flags
