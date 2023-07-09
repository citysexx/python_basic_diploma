import telebot
from src.configs.config import TELEGRAM_TOKEN, GUIDE
import recorder
from src.utils.funcs import from_string
from telebot import types


bot = telebot.TeleBot(TELEGRAM_TOKEN)


# Handle '/start' and '/main commands'
@bot.message_handler(commands=['start', 'main'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    help_btn = types.KeyboardButton("/help")
    auto_location_btn = types.KeyboardButton("/autoloc", request_location=True)
    custom_location_btn = types.KeyboardButton("/manualloc")
    regex_search_btn = types.KeyboardButton("/smartsearch")
    news_channel_btn = types.KeyboardButton("/newsread")
    post_to_news_channel_btn = types.KeyboardButton("/newsshare")
    random_meme_btn = types.KeyboardButton("/meme")
    manage_subscription_btn = types.KeyboardButton("/sub")

    markup.add(
        help_btn,
        auto_location_btn,
        custom_location_btn,
        regex_search_btn,
        news_channel_btn,
        post_to_news_channel_btn,
        random_meme_btn,
        manage_subscription_btn
    )

    bot.reply_to(message, 'Главное меню', reply_markup=markup)


# handle /help command
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, GUIDE)


# handle the /autoloc command
@bot.message_handler(commands=['autoloc'])
def send_welcome(message):
    # локация запрашивается в кнопке. надо выцепить оттуда координаты и дать в
    # поисковую строку погодного апи
    # TODO Здесь надо прикрутить локационный сервис телеграм апи,
    #  который в свою очередь передаст координаты погодному апи. Погодный апи
    #  найдет город с помощью координат и выдаст текст: Ваш город - Такой то.
    #  Предложит меню с кнопкой назад тоже
    bot.reply_to(message, 'weather by loc')
    pass


# handle the /manualloc command
@bot.message_handler(commands=['manualloc'])
def send_welcome(message):
    # TODO Здесь надо запросить город у пользователя, передавать в погодный
    #  апи серч, и искать его, предлагая варианты. Если они его не устраивают,
    #  то вводит заново, либо выбирает. и идем как в функции выше
    #  здесь также, меню, с кнопкой назад. Кнопка назад поведет в главное меню,
    #  в данном случае. Также команда /main, /start
    bot.reply_to(message, 'manual weather set menu')
    pass


# handle experimental /smartsearch command.
@bot.message_handler(commands=['smartsearch'])
def send_welcome(message):
    # TODO Здесь открывается тот самый смарт серч с регулярками,
    #  (прежде описание) который мы создавали.
    #  Не забывай про кнопки назад и гл. меню
    bot.reply_to(message, 'smartsearch')
    pass


# handle /newsread command.
@bot.message_handler(commands=['newsread'])
def send_welcome(message):
    # TODO Здесь открывается ссылка на канал с новостями, куда шлют юзеры свои
    #  приколы с погодой
    bot.reply_to(message, 'link to the news channel')
    pass


# handle /newsshare command.
@bot.message_handler(commands=['newsshare'])
def send_welcome(message):
    # TODO Здесь будет форма, где юзер напишет текст, заполнит форму,
    #  и прикрепит фото. Здесь надо прикрутить модерацию контента,
    #  чтобы непристойности не постились
    bot.reply_to(message, 'share weather news with us!')
    pass


# handle /meme command.
@bot.message_handler(commands=['meme'])
def send_welcome(message):
    # TODO Здесь выдается рандомный мем про котов, думай над апи
    bot.reply_to(message, 'here must be a meme')
    pass


# handle /sub command.
@bot.message_handler(commands=['sub'])
def send_welcome(message):
    # TODO Здесь надо прикрутить менюшку, где предложат юзеру настроить рассылки
    bot.reply_to(message, 'subscription menu')
    pass

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    # TODO какие должны быть у программы входные данные по приоритетам:
    #  1. Приветствие. Если программа видит что с ней здороваются, здоровается сначала.
    #  2. Дата. Если прога видит что то похожее на дату, обрабатывает это и передает в погодное апи как аргумент
    #  3. Город. Если прога видит что то похожее на населенный пункт
    #  (для этого проведем серч и если апи еррор, то нету),
    #  то этот город тоже идет после коррекции в аргумент.
    #  если таких несколько, предлагает выбрать из списка
    #  4. мат или просьба о помощи ПРИ ОТСУТСТВИИ вышеуказанных ключевых: предлагает помощь, при достаточных входных
    #  данных прога игнорит мат (может пожурить просто)
    #  5. слово МЕМ. рандом мем про котиков из инета
    #  6. Рассказать о природном явлении. То есть отправить боту фото и описание. В будущем будет канал куда
    #  бот будет постить новости погоды. ФИЛЬТРЫ ФИЛЬТРЫ И ЕЩЕ РАЗ ФИЛЬТРЫ
    #  7. Прощание и благодарность. Если они содержатся в тексте, то в конце ответа прога тоже взаимствует с юзером
    #  8. При отсутствии одного из первых ТРЕХ входных аргументов надо спращивать вдогонку соответствующие данные

    # TODO ТЗ: написать функцию для "флагования" этих всех штук, и она должна возвращать пока что просто словесное
    #  описание действия робота при введенном тексте

    # TODO Реализовать голосовой ввод данных. Можно сделать синтезатор речи в ответ. Поглядеть библиотеки подобные можно.
    #  ЭТО БУДЕТ СИЛЬНЕЙШИЙ ДИПЛОМ

    result_flags = from_string(message)
    bot.reply_to(message, result_flags.__str__())
    #try:
        #bot.reply_to(message, weather.current_weather(message.text))
    #except ApiException:
        #bot.reply_to(message, 'Город не найден. Попробуйте написать латиницей либо проверьте правильность ввода')
    recorder.log_message(message)


if __name__ == '__main__':
    bot.infinity_polling()
