import telebot
from src.configs.config import TELEGRAM_TOKEN
import recorder
from src.utils.regex import *
import re


bot = telebot.TeleBot(TELEGRAM_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
    Привет. Ты счастливчик, потому что тебе удалось одним из первых тестировать меня.
    Напиши любой город, а я дам текущую погоду в нем. Мяу!\
    """)


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
    if any(re.search(template, message.text) for template in hi_regex):
        bot.reply_to(message, 'здесь будет один из ответов на приветствие')

    if any(re.search(template, message.text) for template in bye_regex):
        bot.reply_to(message, 'здесь будет ответ на прощание, один из ответов')

    if any(re.search(template, message.text) for template in thanks_regex):
        bot.reply_to(message, 'здесь скоро появится ответ бота на благодарность(будет случайно выбирать из инета)')

    if any(re.search(template, message.text) for template in help_regex) or \
       any(re.search(template, message.text) for template in curse_regex):
        bot.reply_to(message, 'здесь будет фича предложения помощи')

    if any(re.search(template, message.text) for template in current_regex):
        bot.reply_to(message, 'говорится о текущем моменте, здесь будет текущая погода')

    if any(re.search(template, message.text) for template in future_regex):
        bot.reply_to(message, 'говорится о будущем, здесь будет прогноз')
    #try:
        #bot.reply_to(message, weather.current_weather(message.text))
    #except ApiException:
        #bot.reply_to(message, 'Город не найден. Попробуйте написать латиницей либо проверьте правильность ввода')
    recorder.log_message(message)


if __name__ == '__main__':
    bot.infinity_polling()
