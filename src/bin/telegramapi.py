import telebot

from src.bin import weather
from src.configs.config import TELEGRAM_TOKEN, GUIDE
import recorder
from src.utils.funcs import from_string
from telebot import types


bot = telebot.TeleBot(TELEGRAM_TOKEN)


# Handle '/start' and '/main commands'
@bot.message_handler(commands=['start', 'main'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    help_btn = types.KeyboardButton("❓️Какие команды ты можешь выполнять?")
    owner_btn = types.KeyboardButton("👨‍💻️Где твой хозяин, кто тебя создал?")
    cat_real_look_btn = types.KeyboardButton("🖼️Как ты выглядишь в реальной жизни?")

    markup.add(
        help_btn,
        owner_btn,
        cat_real_look_btn
    )
    if message.text == '/start':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\n'
                                          f'Добро пожаловать! '
                                          f'Используйте кнопки ниже для навигации.',
                         reply_markup=markup)
    else:
        bot.reply_to(message, 'Главное меню', reply_markup=markup)


# handle the /autoloc command
@bot.message_handler(commands=['autoloc'])
def send_weather_by_loc(message):
    markup = types.ReplyKeyboardMarkup(is_persistent=False,
                                       one_time_keyboard=True,
                                       resize_keyboard=True)
    location_btn = types.KeyboardButton(text="📍️Поделиться своей геопозицией",
                                        request_location=True)
    main_menu_btn = types.KeyboardButton('/main')
    markup.add(location_btn, main_menu_btn)
    bot.send_message(chat_id=message.chat.id,
                     text='Поделитесь своим местоположением, чтобы продолжить. Нажмите на кнопку ниже:',
                     reply_markup=markup)


# handle the /manualloc command
@bot.message_handler(commands=['manualloc'])
def send_weather_manually(message):
    # TODO Здесь надо запросить город у пользователя, передавать в погодный
    #  апи серч, и искать его, предлагая варианты. Если они его не устраивают,
    #  то вводит заново, либо выбирает. и идем как в функции выше
    #  здесь также, меню, с кнопкой назад. Кнопка назад поведет в главное меню,
    #  в данном случае. Также команда /main, /start
    bot.reply_to(message, 'manual weather set menu')
    pass


# Handle messages with content_type 'location'
@bot.message_handler(content_types=['location'])
def echo_message(message):
    loc_from_string = str(message.location.latitude) + ',' + str(message.location.longitude)
    location_data = weather.search_locations(loc_from_string)
    city_name = location_data[0]['name']
    region_name = location_data[0]['region']
    country_name = location_data[0]['country']
    bot.reply_to(message, f'Ваше местоположение: {city_name}, {region_name}, {country_name}')
    # TODO регион иногда пустой. Предусмотреть это, там лишняя запятая. Наверное, join.
    # TODO сделать меню погоды либо current либо опциональная, на прогноз. Либо астрономи
    bot.reply_to(message, weather.current_weather(loc_from_string))
    recorder.log_message(message)


# handle questions from the main menu
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_text_message(message):
    pure_str = message.text
    if pure_str == "❓️Какие команды ты можешь выполнять?" or pure_str == '/help':
        bot.send_message(message.chat.id, GUIDE)
    if pure_str == "👨‍💻️Где твой хозяин, кто тебя создал?" or pure_str == '/authors':
        bot.send_message(message.chat.id, 'Github моего хозяина:\nhttps://github.com/citysexx')
    if pure_str == "🖼️Как ты выглядишь в реальной жизни?" or pure_str == '/real':
        bot.send_photo(message.chat.id,
                       'https://photos.app.goo.gl/4Nx8uEyyqFjf6NCv6',
                       caption='Вот так я выгляжу, когда не работаю')


if __name__ == '__main__':
    bot.infinity_polling()
