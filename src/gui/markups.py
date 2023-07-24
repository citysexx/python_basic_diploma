from typing import List
from telebot import types
from src.bin import weather
from src.utils.funcs import profile_user
import json


buttons = json.load(open('gui/buttons.json', 'r', encoding='utf-8'))


def main(user_id: int) -> ['types.ReplyKeyboardMarkup']:
    """
    This is a function that calls a main menu.
    It returns a telebot markup object with buttons. All the markup
    functionality has been decided to take part in a separate file
    because some of them are used more than once
    """
    language = profile_user(tg_user_id=user_id, language="!load!")["language"]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    help_btn = types.KeyboardButton(buttons[language]["guide"])
    auto_location_btn = types.KeyboardButton(buttons[language]["autoloc"])
    manual_location_btn = types.KeyboardButton(buttons[language]["manual_loc"])
    owner_btn = types.KeyboardButton(buttons[language]["authors"])
    cat_real_look_btn = types.KeyboardButton(buttons[language]["real"])

    markup.add(
        help_btn,
        auto_location_btn,
        manual_location_btn,
        owner_btn,
        cat_real_look_btn
    )

    return markup


def location(user_id: int) -> ['types.ReplyKeyboardMarkup']:
    """
    This function shows up a menu to user that asks for the location
    """
    language = profile_user(tg_user_id=user_id, language="!load!")["language"]
    markup = types.ReplyKeyboardMarkup(
        is_persistent=False,
        one_time_keyboard=False,
        resize_keyboard=True
    )

    location_btn = types.KeyboardButton(
        text=buttons[language]["share_geo"],
        request_location=True
    )

    main_menu_btn = types.KeyboardButton(buttons[language]["to_main"])
    markup.add(location_btn, main_menu_btn)

    return markup


def weather_main(user_id: int) -> ['types.ReplyKeyboardMarkup']:
    """
    This function opens a menu where the user is offered to choose for when
    he wants to get a forecast (for now or future)
    """
    language = profile_user(tg_user_id=user_id, language="!load!")["language"]
    markup = types.ReplyKeyboardMarkup(
        is_persistent=False,
        one_time_keyboard=False,
        resize_keyboard=True,
        row_width=1
    )
    current_weather_btn = types.KeyboardButton(buttons[language]["weather_now"])
    forecast_weather_btn = types.KeyboardButton(buttons[language]["forecast"])
    main_menu_btn = types.KeyboardButton(buttons[language]["to_main"])

    markup.add(
        current_weather_btn,
        forecast_weather_btn,
        main_menu_btn
    )

    return markup


def interactive_help(user_id: int) -> ['types.ReplyKeyboardMarkup']:
    """
    This set of buttons is called when user called help and received
    a list of commands. He can enter these commands, but for dumb people we
    usually need dumb and simple gui (buttons)
    """
    language = profile_user(tg_user_id=user_id, language="!load!")["language"]
    markup = types.ReplyKeyboardMarkup(
        is_persistent=False,
        one_time_keyboard=False,
        resize_keyboard=True,
        row_width=1
    )

    auto_location_btn = types.KeyboardButton(buttons[language]["autoloc"])
    manual_location_btn = types.KeyboardButton(buttons[language]["manual_loc"])
    # subscribe_btn
    main_menu_btn = types.KeyboardButton(buttons[language]["to_main"])

    markup.add(
        auto_location_btn,
        manual_location_btn,
        main_menu_btn
    )

    return markup


def confirm_city(from_results: List, user_id: int) -> ['types.ReplyKeyboardMarkup']:
    """
    This markup pops up in the manual search only. After all the variants are provided
    """
    language = profile_user(tg_user_id=user_id, language="!load!")["language"]
    markup = types.ReplyKeyboardMarkup(
        is_persistent=False,
        one_time_keyboard=False,
        resize_keyboard=True,
        row_width=1
    )

    for index, city_info in enumerate(from_results):
        pack = [
            item
            for item in
            [city_info["name"],
             city_info["region"],
             city_info["country"],
             str(city_info["lat"]) + ',' + str(city_info["lon"])]
            if item
        ]

        label = f'{index + 1}. {", ".join(pack)}'
        button = types.KeyboardButton(f'{label}\n')
        markup.add(button)

    no_city_btn = types.KeyboardButton(buttons[language]["no_my_city"])
    main_menu_btn = types.KeyboardButton(buttons[language]["to_main"])
    markup.add(no_city_btn, main_menu_btn)

    return markup


def to_main_menu(user_id: int) -> ['types.ReplyKeyboardMarkup']:
    """
    This func consists of just a button to the main menu
    """
    language = profile_user(tg_user_id=user_id, language="!load!")["language"]
    markup = types.ReplyKeyboardMarkup(
        is_persistent=False,
        one_time_keyboard=False,
        resize_keyboard=True,
        row_width=1
    )
    main_menu_btn = types.KeyboardButton(buttons[language]["to_main"])
    markup.add(main_menu_btn)

    return markup


def forecast_variants(user_id: int) -> ['types.ReplyKeyboardMarkup']:
    """
    This markup offers the user to choose the period of forecast
    """
    language = profile_user(tg_user_id=user_id, language="!load!")["language"]
    markup = types.ReplyKeyboardMarkup(
        is_persistent=False,
        one_time_keyboard=False,
        resize_keyboard=True,
        row_width=1
    )
    today_btn = types.KeyboardButton(buttons[language]["for_today"])
    tomorrow_btn = types.KeyboardButton(buttons[language]["for_tomorrow"])
    three_days_btn = types.KeyboardButton(buttons[language]["for_three_days"])
    main_menu_btn = types.KeyboardButton(buttons[language]["to_main"])

    markup.add(
        today_btn,
        tomorrow_btn,
        three_days_btn,
        main_menu_btn
    )

    return markup


def if_wants_hourly_forecast(forecast_object: ['weather.ForecastWeather'],
                             user_id: int) -> ['types.ReplyKeyboardMarkup']:
    language = profile_user(tg_user_id=user_id, language="!load!")["language"]
    markup = types.ReplyKeyboardMarkup(
        is_persistent=False,
        one_time_keyboard=False,
        resize_keyboard=True,
        row_width=1
    )

    for daily_forecast in forecast_object.daily_forecasts:
        markup.add(types.KeyboardButton(f'{buttons[language]["hourly_for"]} {daily_forecast.date}'))

    markup.add(types.KeyboardButton(buttons[language]["manual_loc"]))
    markup.add(types.KeyboardButton(buttons[language]["weather_now"]))
    markup.add(types.KeyboardButton(buttons[language]["to_main"]))

    return markup


def period_wants_hourly_forecast(user_id: int) -> ['types.ReplyKeyboardMarkup']:
    """
    This keyboard is activated when the user chooses for what period of time
    (night, morning, day, evening) he wants hourly forecast
    Returns:
        telebot markup
    """
    language = profile_user(tg_user_id=user_id, language="!load!")["language"]
    markup = types.ReplyKeyboardMarkup(
        is_persistent=False,
        one_time_keyboard=False,
        resize_keyboard=True,
        row_width=1
    )

    markup.add(types.KeyboardButton(buttons[language]["for_morning"]))
    markup.add(types.KeyboardButton(buttons[language]["for_day"]))
    markup.add(types.KeyboardButton(buttons[language]["for_evening"]))
    markup.add(types.KeyboardButton(buttons[language]["for_night"]))
    markup.add(types.KeyboardButton(buttons[language]["to_main"]))

    return markup


def language_select() -> ['types.ReplyKeyboardMarkup']:
    """language select keyboard"""
    markup = types.ReplyKeyboardMarkup(
        is_persistent=False,
        one_time_keyboard=False,
        resize_keyboard=True,
        row_width=1
    )

    markup.add(types.KeyboardButton('🇷🇺️ Русский'))
    markup.add(types.KeyboardButton('🇬🇧️ English'))

    return markup


if __name__ == '__main__':
    raise UserWarning(f'Not designed as a launcher!!!')
