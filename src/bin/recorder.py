import telebot
from datetime import datetime
from os import mkdir


def log_message(message: ['telebot.types.Message']) -> None:
    """This function logs history: who, when and what wrote to the bot"""

    try:
        mkdir('../data')
    except FileExistsError:
        pass

    with open('../data/history.log', 'a', encoding='utf-8') as file:
        string = f'On {datetime.utcfromtimestamp(message.date)} ' \
                 f'user {message.from_user.first_name} ' \
                 f'{message.from_user.last_name} ' \
                 f'wrote {message.text}\n'
        file.write(string)
        print(string.rstrip())
        file.flush()
