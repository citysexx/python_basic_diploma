import re
import telebot
from typing import Dict, AnyStr, List
from swagger_client.rest import ApiException
from src.utils.regex import *
import src.bin.weather as weather
from telebot import types


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


def interpret(message: ['types.Message']) -> AnyStr:
    """
    This function is needed for the program to understand the user's
    buttons press as corresponding commands
    """
    pure_str = message.text

    if pure_str == "❓️ Какие команды ты можешь выполнять?" or pure_str == '/help':
        return '/help'
    if pure_str == "👨‍💻️ Где твой хозяин, кто тебя создал?" or pure_str == '/authors':
        return '/authors'
    if pure_str == "🖼️ Как ты выглядишь в реальной жизни?" or pure_str == '/real':
        return '/real'
    if pure_str == '👈️ Вернуться в главное меню' or pure_str == '/main':
        return '/main'
    if pure_str == '👇️ Какая погода у меня тут?' or pure_str == '/autoloc':
        return '/autoloc'
    if pure_str == '⚡️ Погода прямо сейчас' or pure_str == '/now':
        return '/now'
