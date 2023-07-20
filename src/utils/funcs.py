import telebot
from typing import Dict, AnyStr, Any, Optional, List
from src.utils.regex import *
from telebot import types
import json
from os import path, mkdir
from random import choice


def feel_msg(user_input: ['telebot.types.Message']) -> Dict[AnyStr, bool]:
    """
    This function accepts the user's message from telegram and defines the
    intention of message using regex.

    Args:
        user_input: a telebot Message object that the user enters

    Returns:
        A string that defines the user's intention of message he writes
    """

    # grab text from object Message
    string: AnyStr = user_input.text

    # negative flags dict
    flags: Dict[AnyStr, bool] = {
        "help": False,
        "hi": False,
        "bye": False,
        "curse": False,
        "thx": False
    }

    # compare the regex and the string. If the msg somehow corresponds the regex,
    # the flag in dict will be set True.
    # I planned the program should take flags and prepare a string here to answer

    if any([re.search(help_single_regex, string) for help_single_regex in help_regex]):
        flags["help"] = True
    if any([re.search(hi_single_regex, string) for hi_single_regex in hi_regex]):
        flags["hi"] = True
    if any([re.search(bye_single_regex, string) for bye_single_regex in bye_regex]):
        flags["bye"] = True
    if any([re.search(curse_single_regex, string) for curse_single_regex in curse_regex]):
        flags["curse"] = True
    if any([re.search(thx_single_regex, string) for thx_single_regex in thanks_regex]):
        flags["thx"] = True

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
    if pure_str == '🧭️ Искать по моему местоположению' or pure_str == '/autoloc':
        return '/autoloc'
    if pure_str == '🔍️ Искать другой город' or pure_str == '/manualloc':
        return '/manualloc'
    if pure_str == '⚡️ Погода прямо сейчас' or pure_str == '/now':
        return '/now'
    if pure_str == '⌚️ Прогноз погоды' or pure_str == '/forecast':
        return '/forecast'


def profile_user(tg_user_id: int,
                 key: AnyStr,
                 new_val: Optional[Any] = None, *,
                 load_only: bool = False,
                 tg_user_name: Optional[AnyStr] = None,
                 tg_user_surname: Optional[AnyStr] = None) -> Dict or None:
    """
    This function refers to the work on the project and database structure and
    is meant to accomplish several tasks in frames of database management:
    i) create a json file for the user (if not exists)
    ii) deserialize it
    iii) change an attribute of this json (attribute name is passed as an argument)
    iv) the new value of the attribute (new value should be passed into
    the function too)
    v) serialize and save it

    By short, this function works with the user's config. The func will be
    needed in several cases and different attributes are to be edited,
    this is why it has been decided to create this func.

    Attributes:
        :param tg_user_id: int number defining a current user who wrote the msg
        :param key: an attribute to change
        :param new_val: a new value to set
        :param load_only: a bool value defining if it's needed to load or save json
        :param tg_user_name: Optional. Name of the user if we need it
        :param tg_user_surname: Optional. Surname of the user if we need it
    """
    if not path.exists(path.join('profiles')):
        mkdir(path.join('profiles'))
    path_to_config = path.join('profiles', f'{tg_user_id}.json')

    # check if file exists and, if not, 'touch' it
    if not path.exists(path_to_config):
        temp_file = open(path_to_config, 'a')
        temp_file.flush()
        temp_file.close()

    # deserialize the json
    with open(path_to_config, 'r', encoding='utf-8') as profile:
        try:
            profile_data = json.load(profile)
        except json.decoder.JSONDecodeError:
            profile_data = {
                'userid': tg_user_id,
                'username': tg_user_name if tg_user_name else "unknown",
                'usersecondname': tg_user_surname if tg_user_surname else "unknown"
            }
        profile.flush()

    # then we check the flag load_only which tells what to do with the file,
    # load only or write (write by default)
    if load_only:
        try:
            fetched_data = profile_data[key]
        except KeyError:
            return None
        else:
            return fetched_data

    # sometimes we receive bytes, non-serializable to JSON item, here is the fix
    if isinstance(new_val, bytes):
        new_val = str(new_val)

    profile_data[key] = new_val

    with open(path_to_config, 'w', encoding='utf-8') as profile_dump:
        json.dump(profile_data, profile_dump, indent=4)
        profile_dump.flush()


def decode_western_time_format(time: AnyStr) -> AnyStr:
    """
    API offers a western time somewhere. This short function will transform
    these dumb PMs and AMs to a proper 24H format
    Args:
        time: str: a string object of format "04:20 PM"

    Returns:
        a 24H format string, "16:20"
    """

    post_meridiem = True if time.split()[1] == "PM" else False

    if post_meridiem:
        hour = int(time.split()[0].split(':')[0]) + 12
        time = str(hour) + time[2:]

    return time[:-2]


def provide_random_phrase(phrase_list: List) -> AnyStr:
    """
    This function takes a list of phrases and returns a random response
    Args:
        phrase_list: a list of phrases that are used by the bot in some
    situations

    Returns:
        Any string. Response
    """
    return choice(phrase_list)


if __name__ == '__main__':
    raise UserWarning(f'Not designed as a launcher!!!')
