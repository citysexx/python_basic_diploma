import re
import telebot
from src.bin import weather
from src.configs.config import TELEGRAM_TOKEN, GUIDE, WELCOME, TO_USER_RAW_RESPONSES, GENERIC_PHRASES
from src.bin import recorder
from src.utils.funcs import interpret, profile_user, feel_msg, provide_random_phrase
from src.gui import markups
import pickle


# get api token
bot = telebot.TeleBot(TELEGRAM_TOKEN)


# Handle '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """This function is called at start"""
    # log msg
    recorder.log_message(message)
    profile_user(
        tg_user_id=message.from_user.id,
        username=message.from_user.first_name,
        usersecondname=message.from_user.last_name,
        current_location="not set",
        provided_location="not set",
        desired_forecast_date="not set",
        current_forecast="none",
        registered="true",
        active_window='/lang',
        language='none',
        first_visit=True
    )

    bot.send_message(
        message.chat.id,
        "Выберите язык/Select language",
        reply_markup=markups.language_select()
    )


@bot.message_handler(commands=['lang'])
def lang_pick(message):
    """This function is called to choose language"""
    # log msg
    recorder.log_message(message)

    profile_user(
        tg_user_id=message.from_user.id,
        active_window='/lang'
    )

    bot.send_message(
        message.chat.id,
        "Выберите язык/Select language",
        reply_markup=markups.language_select()
    )


# Handle messages with content_type 'location', goes after using /autoloc
@bot.message_handler(content_types=['location'])
def echo_location_message(message):
    """This function processes location input"""
    # log location request
    recorder.log_message(message)

    # establish location of user from message
    loc_from_string = str(message.location.latitude) + ',' + str(message.location.longitude)

    # handle json config for this user and, for this particular case, we mute
    # current location logs
    profile_user(
        tg_user_id=message.from_user.id,
        current_location=loc_from_string,
        provided_location=True
    )
    current_language = profile_user(
        tg_user_id=message.from_user.id,
        language='!load!'
    )["language"]

    location_data = weather.search_locations(loc_from_string)

    location_text_data = [
        item for item in [
            location_data[0]['name'],
            location_data[0]['region'],
            location_data[0]['country']
        ]
        if item
    ]

    bot.send_message(
        chat_id=message.chat.id,
        text=GENERIC_PHRASES[current_language]["tell_location"].format(
            location=", ".join(location_text_data),
            nl='\n'
        ),
        reply_markup=markups.weather_main(message.from_user.id)
    )


# Handle messages with content_type 'voice', goes after entering a voice msg
@bot.message_handler(content_types=['voice'])
def echo_location_message(message):
    """This function envisages voices message input control"""
    current_language = profile_user(
        tg_user_id=message.from_user.id,
        language="!load!"
    )["language"]

    bot.send_message(
        chat_id=message.chat.id,
        text=GENERIC_PHRASES[current_language]["voice_reject"]
    )


# handle everything else
@bot.message_handler(content_types=['text'], func=lambda message: True)
def echo_text_message(message):
    """
    This function accepts all commands and all text inputs and processes them
    accordingly. To ensure the multi-user access, all the data is to be stored
    in their profiles rather than python code variables,
    so that they have profiles, to which the ACTIVE WINDOW DATA is saved,
    among other data
    """
    # instantly log input
    recorder.log_message(message)

    # init an active window (bot should know where the user is)
    loaded_data = profile_user(
        tg_user_id=message.from_user.id,
        active_window="!load!",
        language="!load!",
        current_location="!load!",
        provided_location="!load!",
        desired_forecast_date="!load!",
        current_forecast="!load!"
    )

    active_window = loaded_data["active_window"]
    current_language = loaded_data["language"]
    existing_location = loaded_data["current_location"]
    provided_location = loaded_data["provided_location"]
    desired_date = loaded_data["desired_forecast_date"]
    forecast_loads = loaded_data["current_forecast"]
    forecast: ['weather.ForecastWeather'] or ['None'] = None

    if forecast_loads != 'none':
        forecast: ['weather.ForecastWeather'] = pickle.loads(
            eval(loaded_data["current_forecast"])
        )

    if interpret(message) == '/help':
        bot.send_message(
            message.chat.id,
            GUIDE[current_language],
            reply_markup=markups.interactive_help(message.from_user.id)
        )
        return

    if interpret(message) == '/authors':
        bot.send_message(message.chat.id, GENERIC_PHRASES[current_language]["github"].format(
            nl='\n'
        ))
        return

    if interpret(message) == '/real':
        bot.send_photo(message.chat.id,
                       'https://photos.app.goo.gl/4Nx8uEyyqFjf6NCv6',
                       caption=GENERIC_PHRASES[current_language]["caption"])
        return

    if interpret(message) == '/main':
        bot.send_message(
            message.chat.id,
            GENERIC_PHRASES[current_language]["main_menu"],
            reply_markup=markups.main(message.from_user.id)
        )
        profile_user(
            tg_user_id=message.from_user.id,
            active_window='/main',
            provided_location=False
        )
        return

    if interpret(message) == '/autoloc':
        bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_PHRASES[current_language]["share_loc"],
            reply_markup=markups.location(message.from_user.id)
        )
        return

    if interpret(message) == '/manualloc':
        bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_PHRASES[current_language]["input_city"],
            reply_markup=markups.to_main_menu(message.from_user.id)
        )
        profile_user(tg_user_id=message.from_user.id, active_window='/manualloc')
        return

    if interpret(message) == '/now':

        if not existing_location or not provided_location:
            bot.send_message(
                chat_id=message.chat.id,
                text=GENERIC_PHRASES[current_language]["input_ctrl_city"],
                reply_markup=markups.interactive_help(message.from_user.id)
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text=weather.CurrentWeather(existing_location, current_language).__str__(),
                reply_markup=markups.weather_main(message.from_user.id)
            )

        return

    if interpret(message) == '/forecast':

        if not existing_location or not provided_location:
            bot.send_message(
                chat_id=message.chat.id,
                text=GENERIC_PHRASES[current_language]["input_ctrl_city"],
                reply_markup=markups.interactive_help(message.from_user.id)
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text=GENERIC_PHRASES[current_language]["forecast_for"],
                reply_markup=markups.forecast_variants(message.from_user.id)
            )
        profile_user(tg_user_id=message.from_user.id, active_window='/choose_forecast_time')
        return

    # taking into account pure input, we should resist the unnecessary
    # user inputs. For example, the user will enter city in the main menu,
    # which we do not need. So, below there is a solution to this problem.
    # We switch active windows (commands) anytime the user enters commands and
    # after input comes, the checks and the code is led to the needed 'if'
    # language switcher
    if active_window == '/lang':
        welcome_lang = 'none'
        if message.text == '🇬🇧️ English':
            welcome_lang = 'en'
            profile_user(tg_user_id=message.from_user.id,
                         language='en',
                         active_window='/main')
            bot.send_message(
                chat_id=message.chat.id,
                text='Language set. To switch language, enter /lang',
                reply_markup=markups.main(message.from_user.id)
            )

        if message.text == '🇷🇺️ Русский':
            welcome_lang = 'ru'
            profile_user(tg_user_id=message.from_user.id,
                         language='ru',
                         active_window='/main')
            bot.send_message(
                chat_id=message.chat.id,
                text='Язык установлен. Чтобы поменять его, введите /lang',
                reply_markup=markups.main(message.from_user.id)
            )
        if profile_user(tg_user_id=message.from_user.id, first_visit="!load!")["first_visit"]:
            bot.send_message(
                chat_id=message.chat.id,
                text=WELCOME[welcome_lang],
                reply_markup=markups.main(message.from_user.id)
            )
            profile_user(tg_user_id=message.from_user.id, first_visit=False)
        return

    # if user is in the menu of manual choice of city
    if active_window == '/manualloc':
        location_data = weather.search_locations(message.text)
        resulting_string = ''

        if location_data:
            for index, result in enumerate(location_data):
                resulting_string += GENERIC_PHRASES[current_language]["search_result"].format(
                    nl='\n',
                    order=index + 1,
                    city=result["name"],
                    region=result["region"] if result["region"] else "Не указан",
                    country=result["country"],
                    coord=str(result["lat"]) + "," + str(result["lon"]),
                    id=result["id"]
                )
            bot.send_message(
                chat_id=message.chat.id,
                text=GENERIC_PHRASES[current_language]["search_result_all"].format(
                    nl='\n', search_result=resulting_string
                ),
                reply_markup=markups.confirm_city(location_data, message.from_user.id)
            )
            profile_user(tg_user_id=message.from_user.id, active_window='/city_confirmation')
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text=GENERIC_PHRASES[current_language]["not_found"]
            )
        return

    if active_window == '/city_confirmation':
        if message.text == 'Моего города тут нет':
            bot.send_message(chat_id=message.chat.id,
                             text=GENERIC_PHRASES[current_language]["city_not_in_list"],
                             reply_markup=markups.interactive_help(message.from_user.id))
            profile_user(tg_user_id=message.from_user.id, active_window='None')
            return

        if not re.match(r'\b(\d)+\. (.+), (-)?(\d)+\.(-)?(\d+),(-)?(\d)+\.(-)?(\d+)\b', message.text):
            bot.send_message(message.chat.id, GENERIC_PHRASES[current_language]["tested_prevented"])
            return

        bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_PHRASES[current_language]["chosen_place"].format(
                nl='\n', place=message.text[3:]
            ),
            reply_markup=markups.weather_main(message.from_user.id)
        )
        result = weather.search_locations(message.text[3:].split(', ')[-1])
        profile_user(
            tg_user_id=message.from_user.id,
            current_location=f'{str(result[0]["lat"]) + "," + str(result[0]["lon"])}',
            provided_location=True,
            active_window='None'
        )
        return

    if active_window == '/choose_forecast_time':

        if message.text == markups.buttons[current_language]["for_today"]:
            forecast = weather.ForecastWeather(
                geo=existing_location,
                number_of_days=1,
                moment="today",
                language=current_language
            )

            bot.send_message(
                chat_id=message.chat.id,
                text=f'{forecast.__str__()}',
                reply_markup=markups.if_wants_hourly_forecast(forecast, message.from_user.id)
            )
            # serialize the class ForecastWeather and dump it into the user's
            # json to further use in the weather provision in OTHER functions
            # that do not cross the scope with each other.
            # Actual for the conditions below as well
            profile_user(
                tg_user_id=message.from_user.id,
                current_forecast=pickle.dumps(forecast),
                active_window='/offered_hourly'
            )
            return

        if message.text == markups.buttons[current_language]["for_tomorrow"]:
            forecast = weather.ForecastWeather(
                geo=existing_location,
                number_of_days=2,
                moment="tomorrow",
                language=current_language
            )

            bot.send_message(
                chat_id=message.chat.id,
                text=f'{forecast.__str__()}',
                reply_markup=markups.if_wants_hourly_forecast(forecast, message.from_user.id)
            )

            profile_user(
                tg_user_id=message.from_user.id,
                current_forecast=pickle.dumps(forecast),
                active_window='/offered_hourly'
            )
            return

        if message.text == markups.buttons[current_language]["for_three_days"]:
            forecast = weather.ForecastWeather(
                geo=existing_location,
                number_of_days=3,
                moment="three_days",
                language=current_language
            )
            bot.send_message(
                chat_id=message.chat.id,
                text=f'{forecast.__str__()}',
                reply_markup=markups.if_wants_hourly_forecast(forecast, message.from_user.id)
            )

            profile_user(
                tg_user_id=message.from_user.id,
                current_forecast=pickle.dumps(forecast),
                active_window='/offered_hourly'
            )
            return
        bot.send_message(message.chat.id, GENERIC_PHRASES[current_language]["tested_prevented"])

    if active_window == '/offered_hourly' and \
            re.match(r'\b(Почасовой прогноз на|Hourly forecast for) \d{4}-\d{2}-\d{2}\b', message.text):

        # fetch what period of day the user wants
        bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_PHRASES[current_language]["choose_daytime"],
            reply_markup=markups.period_wants_hourly_forecast(message.from_user.id)
        )
        profile_user(
            tg_user_id=message.from_user.id,
            active_window='/enter_period',
            desired_forecast_date=message.text.split()[3]
        )
        return

    if active_window == '/enter_period':

        # find the needed day in the forecast
        for daily_forecast in forecast.daily_forecasts:
            if daily_forecast.date == desired_date:
                needed_forecast_inst = daily_forecast
                break
        else:
            raise NotImplementedError

        if message.text == markups.buttons[current_language]["for_morning"]:
            bot.send_message(
                chat_id=message.chat.id,
                text=f'{needed_forecast_inst.give_hourly_forecast(period=range(6,13))}',
                reply_markup=markups.interactive_help(message.from_user.id)
            )
            profile_user(
                tg_user_id=message.from_user.id,
                desired_forecast_date='none',
                current_forecast='none',
                active_window='none',
                provided_location=False
            )
            return

        if message.text == markups.buttons[current_language]["for_day"]:
            bot.send_message(
                chat_id=message.chat.id,
                text=f'{needed_forecast_inst.give_hourly_forecast(period=range(12, 19))}',
                reply_markup=markups.interactive_help(message.from_user.id)
            )
            profile_user(
                tg_user_id=message.from_user.id,
                desired_forecast_date='none',
                current_forecast='none',
                active_window='none',
                provided_location=False
            )
            return

        if message.text == markups.buttons[current_language]["for_evening"]:
            bot.send_message(
                chat_id=message.chat.id,
                text=f'{needed_forecast_inst.give_hourly_forecast(period=range(18, 24))}',
                reply_markup=markups.interactive_help(message.from_user.id)
            )
            profile_user(
                tg_user_id=message.from_user.id,
                desired_forecast_date='none',
                current_forecast='none',
                active_window='none',
                provided_location=False
            )
            return

        if message.text == markups.buttons[current_language]["for_night"]:
            bot.send_message(
                chat_id=message.chat.id,
                text=f'{needed_forecast_inst.give_hourly_forecast(period=range(0, 7))}',
                reply_markup=markups.interactive_help(message.from_user.id)
            )
            profile_user(
                tg_user_id=message.from_user.id,
                desired_forecast_date='none',
                current_forecast='none',
                active_window='none',
                provided_location=False
            )
            return

        bot.send_message(message.chat.id, GENERIC_PHRASES[current_language]["tested_prevented"])

    # check msg for some inputs
    is_any_interaction = feel_msg(message, current_language)
    if any([item is True for item in is_any_interaction.values()]):
        compiled_response_string = str()
        # find True flags and throw a response to each after compiling the string
        for key, value in is_any_interaction.items():
            if value and key != 'help':
                compiled_response_string += provide_random_phrase(
                    TO_USER_RAW_RESPONSES[key][current_language]
                ) + '\n'

        if compiled_response_string:
            bot.send_message(message.chat.id, compiled_response_string)

        if is_any_interaction['help']:
            bot.send_message(
                message.chat.id,
                GUIDE[current_language],
                reply_markup=markups.interactive_help(message.from_user.id)
            )

        return

    bot.send_message(message.chat.id, GENERIC_PHRASES[current_language]["misunderstanding"])


if __name__ == '__main__':
    raise UserWarning(GENERIC_PHRASES["dont_launch_here"])
