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
        tg_user_name=message.from_user.first_name,
        tg_user_surname=message.from_user.last_name,
        key='registered',
        new_val='true'
    )

    bot.send_message(
        message.chat.id,
        WELCOME,
        reply_markup=markups.main()
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
    profile_user(message.from_user.id, 'current_location', loc_from_string)
    profile_user(message.from_user.id, 'provided_location', True)
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
        text=GENERIC_PHRASES["tell_location"].format(
            location=", ".join(location_text_data),
            nl='\n'
        ),
        reply_markup=markups.weather_main()
    )


# Handle messages with content_type 'voice', goes after entering a voice msg
@bot.message_handler(content_types=['voice'])
def echo_location_message(message):
    """This function envisages voices message input control"""
    bot.send_message(
        chat_id=message.chat.id,
        text=GENERIC_PHRASES["voice_reject"]
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
    active_window = profile_user(message.from_user.id, 'active_window', load_only=True)

    if interpret(message) == '/help':
        bot.send_message(message.chat.id, GUIDE, reply_markup=markups.interactive_help())
        return

    if interpret(message) == '/authors':
        bot.send_message(message.chat.id, GENERIC_PHRASES["github"].format(
            nl='\n'
        ))
        return

    if interpret(message) == '/real':
        bot.send_photo(message.chat.id,
                       'https://photos.app.goo.gl/4Nx8uEyyqFjf6NCv6',
                       caption=GENERIC_PHRASES["caption"])
        return

    if interpret(message) == '/main':
        bot.send_message(message.chat.id, GENERIC_PHRASES["main_menu"], reply_markup=markups.main())
        profile_user(message.from_user.id, 'active_window', '/main')
        profile_user(message.from_user.id, 'provided_location', False)
        return

    if interpret(message) == '/autoloc':
        bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_PHRASES["share_loc"],
            reply_markup=markups.location()
        )
        return

    if interpret(message) == '/manualloc':
        bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_PHRASES["input_city"],
            reply_markup=markups.to_main_menu()
        )
        profile_user(message.from_user.id, 'active_window', '/manualloc')
        return

    if interpret(message) == '/now':
        existing_location = profile_user(message.from_user.id, 'current_location', load_only=True)
        provided_location = profile_user(message.from_user.id, 'provided_location', load_only=True)

        if not existing_location or not provided_location:
            bot.send_message(
                chat_id=message.chat.id,
                text=GENERIC_PHRASES["input_ctrl_city"],
                reply_markup=markups.interactive_help()
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text=weather.CurrentWeather(existing_location).__str__(),
                reply_markup=markups.weather_main()
            )

        return

    if interpret(message) == '/forecast':

        existing_location = profile_user(message.from_user.id, 'current_location', load_only=True)
        provided_location = profile_user(message.from_user.id, 'provided_location', load_only=True)

        if not existing_location or not provided_location:
            bot.send_message(
                chat_id=message.chat.id,
                text=GENERIC_PHRASES["input_ctrl_city"],
                reply_markup=markups.interactive_help()
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text=GENERIC_PHRASES["forecast_for"],
                reply_markup=markups.forecast_variants()
            )
        profile_user(message.from_user.id, 'active_window', '/choose_forecast_time')
        return

    # taking into account pure input, we should resist the unnecessary
    # user inputs. For example, the user will enter city in the main menu,
    # which we do not need. So, below there is a solution to this problem.
    # We switch active windows (commands) anytime the user enters commands and
    # after input comes, the checks and the code is led to the needed 'if'

    # if user is in the menu of manual choice of city
    if active_window == '/manualloc':
        location_data = weather.search_locations(message.text)
        resulting_string = ''

        if location_data:
            for index, result in enumerate(location_data):
                resulting_string += GENERIC_PHRASES["search_result"].format(
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
                text=GENERIC_PHRASES["search_result_all"].format(
                    nl='\n', search_result=resulting_string
                ),
                reply_markup=markups.confirm_city(location_data)
            )
            profile_user(message.from_user.id, 'active_window', '/city_confirmation')
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text=GENERIC_PHRASES["not_found"]
            )
        return

    if active_window == '/city_confirmation':
        if message.text == 'Моего города тут нет':
            bot.send_message(chat_id=message.chat.id,
                             text=GENERIC_PHRASES["city_not_in_list"],
                             reply_markup=markups.interactive_help())
            profile_user(message.from_user.id, 'active_window', 'None')
            return

        if not re.match(r'\b(\d)+\. (.+), (-)?(\d)+\.(-)?(\d+),(-)?(\d)+\.(-)?(\d+)\b', message.text):
            bot.send_message(message.chat.id, GENERIC_PHRASES["tested_prevented"])
            return

        bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_PHRASES["chosen_place"].format(
                nl='\n', place=message.text[3:]
            ),
            reply_markup=markups.weather_main()
        )
        result = weather.search_locations(message.text[3:].split(', ')[-1])
        profile_user(message.from_user.id,
                     'current_location',
                     f'{str(result[0]["lat"]) + "," + str(result[0]["lon"])}'
                     )
        profile_user(message.from_user.id, 'provided_location', True)
        profile_user(message.from_user.id, 'active_window', 'None')

    if active_window == '/choose_forecast_time':
        current_loc = profile_user(message.from_user.id, 'current_location', load_only=True)

        if message.text == 'На сегодня':
            forecast = weather.ForecastWeather(geo=current_loc, number_of_days=1, moment="today")
            bot.send_message(
                chat_id=message.chat.id,
                text=f'{forecast.__str__()}',
                reply_markup=markups.if_wants_hourly_forecast(forecast)
            )
            # serialize the class ForecastWeather and dump it into the user's
            # json to further use in the weather provision in OTHER functions
            # that do not cross the scope with each other.
            # Actual for the conditions below as well
            profile_user(message.from_user.id, 'current_forecast', pickle.dumps(forecast))
            profile_user(message.from_user.id, 'active_window', '/offered_hourly')
            return

        if message.text == 'На завтра':
            forecast = weather.ForecastWeather(geo=current_loc, number_of_days=2, moment="tomorrow")
            bot.send_message(
                chat_id=message.chat.id,
                text=f'{forecast.__str__()}',
                reply_markup=markups.if_wants_hourly_forecast(forecast)
            )

            profile_user(message.from_user.id, 'current_forecast', pickle.dumps(forecast))
            profile_user(message.from_user.id, 'active_window', '/offered_hourly')
            return

        if message.text == 'На три дня':
            forecast = weather.ForecastWeather(geo=current_loc, number_of_days=3, moment="three_days")
            bot.send_message(
                chat_id=message.chat.id,
                text=f'{forecast.__str__()}',
                reply_markup=markups.if_wants_hourly_forecast(forecast)
            )

            profile_user(message.from_user.id, 'current_forecast', pickle.dumps(forecast))
            profile_user(message.from_user.id, 'active_window', '/offered_hourly')
            return
        bot.send_message(message.chat.id, GENERIC_PHRASES["tested_prevented"])

    if active_window == '/offered_hourly' and \
            re.match(r'\bПочасовой прогноз на \d{4}-\d{2}-\d{2}\b', message.text):

        # fetch what period of day the user wants
        bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_PHRASES["choose_daytime"],
            reply_markup=markups.period_wants_hourly_forecast()
        )

        profile_user(message.from_user.id, 'active_window', '/enter_period')
        profile_user(message.from_user.id, 'desired_forecast_date', message.text.split()[3])

    if active_window == '/enter_period':
        # deserialize the class ForecastWeather from the json file
        forecast: ['weather.ForecastWeather'] = pickle.loads(
            eval(profile_user(message.from_user.id, 'current_forecast', load_only=True))
        )
        # take the remembered date from the user
        desired_date = profile_user(message.from_user.id, 'desired_forecast_date', load_only=True)

        # find the needed day in the forecast
        for daily_forecast in forecast.daily_forecasts:
            if daily_forecast.date == desired_date:
                needed_forecast_inst = daily_forecast
                break
        else:
            raise NotImplementedError

        if message.text == 'На утро (6-12 часов)':
            bot.send_message(
                chat_id=message.chat.id,
                text=f'{needed_forecast_inst.give_hourly_forecast(period=range(6,13))}',
                reply_markup=markups.interactive_help()
            )
            profile_user(message.from_user.id, 'desired_forecast_date', 'none')
            profile_user(message.from_user.id, 'current_forecast', 'none')
            profile_user(message.from_user.id, 'active_window', 'none')
            profile_user(message.from_user.id, 'provided_location', False)

            return

        if message.text == 'На день (12-18 часов)':
            bot.send_message(
                chat_id=message.chat.id,
                text=f'{needed_forecast_inst.give_hourly_forecast(period=range(12, 19))}',
                reply_markup=markups.interactive_help()
            )
            profile_user(message.from_user.id, 'desired_forecast_date', 'none')
            profile_user(message.from_user.id, 'current_forecast', 'none')
            profile_user(message.from_user.id, 'active_window', 'none')
            profile_user(message.from_user.id, 'provided_location', False)

            return

        if message.text == 'На вечер (18-24 часа)':
            bot.send_message(
                chat_id=message.chat.id,
                text=f'{needed_forecast_inst.give_hourly_forecast(period=range(18, 24))}',
                reply_markup=markups.interactive_help()
            )
            profile_user(message.from_user.id, 'desired_forecast_date', 'none')
            profile_user(message.from_user.id, 'current_forecast', 'none')
            profile_user(message.from_user.id, 'active_window', 'none')
            profile_user(message.from_user.id, 'provided_location', False)

            return

        if message.text == 'На ночь (0-6 часов)':
            bot.send_message(
                chat_id=message.chat.id,
                text=f'{needed_forecast_inst.give_hourly_forecast(period=range(0, 7))}',
                reply_markup=markups.interactive_help()
            )
            profile_user(message.from_user.id, 'desired_forecast_date', 'none')
            profile_user(message.from_user.id, 'current_forecast', 'none')
            profile_user(message.from_user.id, 'active_window', 'none')
            profile_user(message.from_user.id, 'provided_location', False)

            return

        bot.send_message(message.chat.id, GENERIC_PHRASES["tested_prevented"])

    # check msg for some inputs
    is_any_interaction = feel_msg(message)
    if any([item is True for item in is_any_interaction.values()]):
        compiled_response_string = str()
        # find True flags and throw a response to each after compiling the string
        for key, value in is_any_interaction.items():
            if value and key != 'help':
                compiled_response_string += provide_random_phrase(
                    TO_USER_RAW_RESPONSES[key]
                ) + '\n'

        if compiled_response_string:
            bot.send_message(message.chat.id, compiled_response_string)

        if is_any_interaction['help']:
            bot.send_message(message.chat.id, GUIDE, reply_markup=markups.interactive_help())

        return

    bot.send_message(message.chat.id, GENERIC_PHRASES["misunderstanding"])


if __name__ == '__main__':
    raise UserWarning(GENERIC_PHRASES["dont_launch_here"])
