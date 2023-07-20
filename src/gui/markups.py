from typing import List, AnyStr
from telebot import types
from src.bin import weather


def main() -> ['types.ReplyKeyboardMarkup']:
    """
    This is a function that calls a main menu.
    It returns a telebot markup object with buttons. All the markup
    functionality has been decided to take part in a separate file
    because some of them are used more than once
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    help_btn = types.KeyboardButton("❓️ Какие команды ты можешь выполнять?")
    owner_btn = types.KeyboardButton("👨‍💻️ Где твой хозяин, кто тебя создал?")
    cat_real_look_btn = types.KeyboardButton("🖼️ Как ты выглядишь в реальной жизни?")

    markup.add(
        help_btn,
        owner_btn,
        cat_real_look_btn
    )

    return markup


def location() -> ['types.ReplyKeyboardMarkup']:
    """
    This function shows up a menu to user that asks for the location
    """
    markup = types.ReplyKeyboardMarkup(
        is_persistent=False,
        one_time_keyboard=False,
        resize_keyboard=True
    )

    location_btn = types.KeyboardButton(
        text="📍️ Поделиться своей геопозицией",
        request_location=True
    )

    main_menu_btn = types.KeyboardButton('👈️ Вернуться в главное меню')
    markup.add(location_btn, main_menu_btn)

    return markup


def weather_main() -> ['types.ReplyKeyboardMarkup']:
    """
    This function opens a menu where the user is offered to choose for when
    he wants to get a forecast (for now or future)
    """
    markup = types.ReplyKeyboardMarkup(
        is_persistent=False,
        one_time_keyboard=False,
        resize_keyboard=True,
        row_width=1
    )
    current_weather_btn = types.KeyboardButton('⚡️ Погода прямо сейчас')
    forecast_weather_btn = types.KeyboardButton('⌚️ Прогноз погоды')
    main_menu_btn = types.KeyboardButton('👈️ Вернуться в главное меню')

    markup.add(
        current_weather_btn,
        forecast_weather_btn,
        main_menu_btn
    )

    return markup


def interactive_help() -> ['types.ReplyKeyboardMarkup']:
    """
    This set of buttons is called when user called help and received
    a list of commands. He can enter these commands, but for dumb people we
    usually need dumb and simple gui (buttons)
    """
    markup = types.ReplyKeyboardMarkup(
        is_persistent=False,
        one_time_keyboard=False,
        resize_keyboard=True,
        row_width=1
    )

    auto_location_btn = types.KeyboardButton('🧭️ Искать по моему местоположению')
    manual_location_btn = types.KeyboardButton('🔍️ Искать другой город')
    # subscribe_btn
    main_menu_btn = types.KeyboardButton('👈️ Вернуться в главное меню')

    markup.add(
        auto_location_btn,
        manual_location_btn,
        main_menu_btn
    )

    return markup


def confirm_city(from_results: List) -> ['types.ReplyKeyboardMarkup']:
    """
    This markup pops up in the manual search only. After all the variants are provided
    """
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

    no_city_btn = types.KeyboardButton('Моего города тут нет')
    main_menu_btn = types.KeyboardButton('👈️ Вернуться в главное меню')
    markup.add(no_city_btn, main_menu_btn)

    return markup


def to_main_menu() -> ['types.ReplyKeyboardMarkup']:
    """
    This func consists of just a button to the main menu
    """
    markup = types.ReplyKeyboardMarkup(
        is_persistent=False,
        one_time_keyboard=False,
        resize_keyboard=True,
        row_width=1
    )
    main_menu_btn = types.KeyboardButton('👈️ Вернуться в главное меню')
    markup.add(main_menu_btn)

    return markup


def forecast_variants() -> ['types.ReplyKeyboardMarkup']:
    """
    This markup offers the user to choose the period of forecast
    """

    markup = types.ReplyKeyboardMarkup(
        is_persistent=False,
        one_time_keyboard=False,
        resize_keyboard=True,
        row_width=1
    )
    today_btn = types.KeyboardButton('На сегодня')
    tomorrow_btn = types.KeyboardButton('На завтра')
    three_days_btn = types.KeyboardButton('На три дня')
    main_menu_btn = types.KeyboardButton('👈️ Вернуться в главное меню')

    markup.add(
        today_btn,
        tomorrow_btn,
        three_days_btn,
        main_menu_btn
    )

    return markup


def if_wants_hourly_forecast(forecast_object: ['weather.ForecastWeather']) -> ['types.ReplyKeyboardMarkup']:
    markup = types.ReplyKeyboardMarkup(
        is_persistent=False,
        one_time_keyboard=False,
        resize_keyboard=True,
        row_width=1
    )

    for daily_forecast in forecast_object.daily_forecasts:
        markup.add(types.KeyboardButton(f'Почасовой прогноз на {daily_forecast.date}'))

    markup.add(types.KeyboardButton('👈️ Вернуться в главное меню'))

    return markup


def period_wants_hourly_forecast() -> ['types.ReplyKeyboardMarkup']:
    """
    This keyboard is activated when the user chooses for what period of time
    (night, morning, day, evening) he wants hourly forecast
    Returns:
        telebot markup
    """
    markup = types.ReplyKeyboardMarkup(
        is_persistent=False,
        one_time_keyboard=False,
        resize_keyboard=True,
        row_width=1
    )

    markup.add(types.KeyboardButton('На утро (6-12 часов)'))
    markup.add(types.KeyboardButton('На день (12-18 часов)'))
    markup.add(types.KeyboardButton('На вечер (18-24 часа)'))
    markup.add(types.KeyboardButton('На ночь (0-6 часов)'))
    markup.add(types.KeyboardButton('👈️ Вернуться в главное меню'))

    return markup


if __name__ == '__main__':
    raise UserWarning(f'Not designed as a launcher!!!')
