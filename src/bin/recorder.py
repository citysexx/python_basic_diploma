import telebot
from datetime import datetime
from os import mkdir


def log_message(message: ['telebot.types.Message']) -> None:
    """
    This function logs history: who, when and what wrote to the bot.
    The recordings depend on a message type.
    """
    try:
        mkdir('logs')
    except FileExistsError:
        pass

    string = ''

    with open('logs/user_history.log', 'a', encoding='utf-8') as file:
        if message.location:
            dict_from_loc = eval(str(message.location))
            string = f'On {datetime.utcfromtimestamp(message.date)} GMT ' \
                     f'user {message.from_user.first_name} ' \
                     f'{message.from_user.last_name} ' \
                     f'shared the location ({dict_from_loc["latitude"]},{dict_from_loc["longitude"]}) with bot.\n'
        elif message.text:
            string = f'On {datetime.utcfromtimestamp(message.date)} GMT ' \
                     f'user {message.from_user.first_name} ' \
                     f'{message.from_user.last_name} ' \
                     f'wrote to the bot "{message.text}"\n'

        if not string:
            raise NotImplementedError

        file.write(string)
        print(string.rstrip())
        file.flush()


if __name__ == '__main__':
    raise UserWarning(f'Not designed as a launcher!!!')
