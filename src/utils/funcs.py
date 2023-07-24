import telebot
from src.utils.regex import *
from telebot import types
import json
from os import path, mkdir
from random import choice


inputs_en: Dict[AnyStr, AnyStr] = json.load(open(path.join('.', 'gui/buttons.json'), 'r', encoding='utf-8'))["en"]
inputs_ru: Dict[AnyStr, AnyStr] = json.load(open(path.join('.', 'gui/buttons.json'), 'r', encoding='utf-8'))["ru"]


def feel_msg(user_input: ['telebot.types.Message'], language: AnyStr) -> Dict[AnyStr, bool]:
    """
    This function accepts the user's message from telegram and defines the
    intention of message using regex.

    Args:
        user_input: a telebot Message object that the user enters
        language: a language to feel

    Returns:
        A string that defines the user's intention of message he writes
    """

    # grab text from object Message
    string: AnyStr = user_input.text

    # negative flags dict
    flags: Dict[AnyStr, bool] = {
        "hi": False,
        "curse": False,
        "help": False,
        "thx": False,
        "bye": False
    }

    # compare the regex and the string. If the msg somehow corresponds the regex,
    # the flag in dict will be set True.
    # I planned the program should take flags and prepare a string here to answer

    if any([re.search(help_single_regex, string) for help_single_regex in help_regex[language]]):
        flags["help"] = True
    if any([re.search(hi_single_regex, string) for hi_single_regex in hi_regex[language]]):
        flags["hi"] = True
    if any([re.search(bye_single_regex, string) for bye_single_regex in bye_regex[language]]):
        flags["bye"] = True
    if any([re.search(curse_single_regex, string) for curse_single_regex in curse_regex[language]]):
        flags["curse"] = True
    if any([re.search(thx_single_regex, string) for thx_single_regex in thanks_regex[language]]):
        flags["thx"] = True

    return flags


def interpret(message: ['types.Message']) -> AnyStr:
    """
    This function is needed for the program to understand the user's
    buttons press as corresponding commands
    """
    pure_str = message.text

    if pure_str in [inputs_en["guide"], inputs_ru["guide"]] or pure_str == '/help':
        return '/help'
    if pure_str in [inputs_en["authors"], inputs_ru["authors"]] or pure_str == '/authors':
        return '/authors'
    if pure_str in [inputs_en["real"], inputs_ru["real"]] or pure_str == '/real':
        return '/real'
    if pure_str in [inputs_en["to_main"], inputs_ru["to_main"]] or pure_str == '/main':
        return '/main'
    if pure_str in [inputs_en["autoloc"], inputs_ru["autoloc"]] or pure_str == '/autoloc':
        return '/autoloc'
    if pure_str in [inputs_en["manual_loc"], inputs_ru["manual_loc"]] or pure_str == '/manualloc':
        return '/manualloc'
    if pure_str in [inputs_en["weather_now"], inputs_ru["weather_now"]] or pure_str == '/now':
        return '/now'
    if pure_str in [inputs_en["forecast"], inputs_ru["forecast"]] or pure_str == '/forecast':
        return '/forecast'


def profile_user(*,
                 tg_user_id: int,
                 **kwargs) -> Dict or None:
    """
    This function refers to the work on the project and database structure and
    is meant to accomplish several tasks in frames of database management:

    SAVE INFO:
        i) create a json file for the user (if not exists)
        ii) deserialize it
        iii) add attributes of this json if none
        iv) the new value of each attribute
        v) serialize and save it

    LOAD INFO:
        i) create a json file for the user (if not exists)
        ii) deserialize it
        iii) return a dict with the needed keys and values

    By short, this function works with the user's config. The func will be
    needed in several cases and different attributes are to be edited,
    this is why it has been decided to create this func.

    Attributes:
        :param tg_user_id: int number defining a current user who wrote the msg
        :param kwargs: keys and values to load/save
    """
    # check what the function has been called for (SAVE OR LOAD).
    # We go in kwargs and check if all values are load OR all values NOT load.
    # Otherwise, we raise exception, because it is irrational to use profiling
    # both for load and save simultaneously
    all_loads = all([val == "!load!" for val in kwargs.values()])
    all_saves = all([val != "!load!" for val in kwargs.values()])

    if not all_loads and not all_saves:
        raise NotImplementedError('You cannot use this function for load '
                                  'and save purposes simultaneously!')

    # define func mode. 'l' for load and 's' for save.
    mode = 'l' if all_loads else 's'

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
                'username': kwargs["username"] if kwargs["username"] else "unknown",
                'usersecondname': kwargs["usersecondname"] if kwargs["usersecondname"] else "unknown"
            }
        profile.flush()

    # if we load, we return the dict with the needed info for further work
    if mode == 'l':
        return {key: profile_data[key] for key in kwargs.keys()}

    # go work with the profile data if we need to save it
    for key, val in kwargs.items():
        # sometimes we receive bytes, non-serializable to JSON item, here is the fix
        if isinstance(val, bytes):
            profile_data[key] = str(val)
            continue
        profile_data[key] = val

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


def mute_env() -> None:
    """func writes env variables into the .env"""
    path_to_env = path.join('.', '.env')

    telegram_api_key = input('Enter Telegram API key >>> ')
    weather_api_key = input('Enter Weather API key >>> ')

    with open(path_to_env, 'w') as env_file:
        env_file.write(f"TELEGRAM_TOKEN={telegram_api_key}")
        env_file.write("\n")
        env_file.write(f"WEATHER_TOKEN={weather_api_key}")
        env_file.flush()


def chenv() -> None:
    """create an empty .env file if there is none"""
    path_to_env = path.join('.', '.env')

    if path.exists(path_to_env):
        return

    with open(path_to_env, 'w') as new_env:
        new_env.write("TELEGRAM_TOKEN=none\nWEATHER_TOKEN=none\n")


if __name__ == '__main__':
    raise UserWarning(f'Not designed as a launcher!!!')
