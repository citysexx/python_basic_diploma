from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
import swagger_client
from swagger_client.rest import ApiException as ApiWeatherException
from os import getenv


def dummy_tested_success() -> bool:
    """
    a dummy launch of the telegramapi and weatherapi with the keys to check
    if the keys in the env are correctly entered
    """

    try:
        # launch a dummy tgbot
        test_bot = TeleBot(getenv("TELEGRAM_TOKEN"))
        test_bot.get_me()

        # launch a dummy weather api
        configuration = swagger_client.Configuration()
        configuration.proxy = getenv('PROXY_CONF', None)
        configuration.api_key['key'] = getenv("WEATHER_TOKEN")
        api_instance = swagger_client.APIsApi(swagger_client.ApiClient(configuration))
        api_instance.realtime_weather('Vladivostok')

    except ApiTelegramException:
        return False

    except ApiWeatherException:
        return False

    return True


if __name__ == '__main__':
    raise UserWarning("Not designed as a launcher!")
