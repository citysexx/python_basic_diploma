from telebot import types


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

    auto_location_btn = types.KeyboardButton('👇️ Какая погода у меня тут?')
    manual_location_btn = types.KeyboardButton('👉️ Какая погода у них там?')
    # subscribe_btn
    main_menu_btn = types.KeyboardButton('👈️ Вернуться в главное меню')

    markup.add(
        auto_location_btn,
        manual_location_btn,
        main_menu_btn
    )

    return markup
