import telebot
from src.bin import weather
from src.configs.config import TELEGRAM_TOKEN, GUIDE
import recorder
from src.utils.funcs import from_string, interpret
from src.gui import markups


bot = telebot.TeleBot(TELEGRAM_TOKEN)


# Handle '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):

    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}!\n'
                                      f'Добро пожаловать! Вы используете погодного бота. '
                                      f'Примите участие в разработке, пробуя и тестируя. '
                                      f'Используйте кнопки ниже для навигации.',
                     reply_markup=markups.main())


# Handle messages with content_type 'location', goes after using /autoloc
@bot.message_handler(content_types=['location'])
def echo_location_message(message):
    loc_from_string = str(message.location.latitude) + ',' + str(message.location.longitude)
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
        text=f'Ваше местоположение:\n{", ".join(location_text_data)}\n'
             f'Выберите дальнейшие действия:',
        reply_markup=markups.weather_main()
    )

    # TODO сделать меню погоды либо current либо опциональная, на прогноз. Либо астрономи

    recorder.log_message(message)


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


# handle questions from the main menu
@bot.message_handler(content_types=['text'])
def echo_text_message(message):

    if interpret(message) == '/help':
        bot.send_message(message.chat.id, GUIDE, reply_markup=markups.interactive_help())

    if interpret(message) == '/authors':
        bot.send_message(message.chat.id, 'Github моего хозяина:\nhttps://github.com/citysexx')

    if interpret(message) == '/real':
        bot.send_photo(message.chat.id,
                       'https://photos.app.goo.gl/4Nx8uEyyqFjf6NCv6',
                       caption='Вот так я выгляжу, когда не работаю')

    if interpret(message) == '/main':
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=markups.main())

    if interpret(message) == '/autoloc':
        bot.send_message(
            chat_id=message.chat.id,
            text='Поделитесь своим местоположением, чтобы продолжить. Нажмите на кнопку ниже:',
            reply_markup=markups.location()
        )

    if interpret(message) == '/now':
        bot.send_message(
            chat_id=message.chat.id,
            text=weather.current_weather('vladivostok').__str__()
        )


if __name__ == '__main__':
    bot.infinity_polling()
