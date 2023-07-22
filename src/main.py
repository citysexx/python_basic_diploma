from dotenv import load_dotenv
from src.test import test
from src.utils.funcs import mute_env, chenv
import importlib


def main() -> None:
    """main body"""
    chenv()
    load_dotenv()
    print('Validating API keys...')

    while not test():
        print('Access denied! Some of the keys is wrong!')
        mute_env()
        load_dotenv(override=True)

    tg = importlib.import_module('src.bin.telegramapi')
    print('Access granted!')
    print('Bot is running...')
    tg.bot.polling(none_stop=True)
    print('Bot has been stopped.')


if __name__ == '__main__':
    main()
