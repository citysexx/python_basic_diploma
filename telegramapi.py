import telebot
from swagger_client.rest import ApiException
from utils.config import TELEGRAM_TOKEN
import weather
import recorder


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
    try:
        bot.reply_to(message, weather.current_weather(message.text))
    except ApiException:
        bot.reply_to(message, 'Город не найден. Попробуйте написать латиницей либо проверьте правильность ввода')
    recorder.log_message(message)


if __name__ == '__main__':
    bot.infinity_polling()
