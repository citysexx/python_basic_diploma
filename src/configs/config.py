from typing import List, AnyStr, Dict
from os import path, curdir, getenv


# token for telegram api
TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
# token for weather api
WEATHER_TOKEN = getenv("WEATHER_TOKEN")

# Fix the paths, making it possible to access from all files and dirs
needed_dir = path.join('utils', 'bot_template_responses')
current_dir = path.abspath(curdir)
working_dir = ''
while True:
    try:
        open(path.join(current_dir, needed_dir, 'en', 'cat_quotes.txt'), 'r', encoding='utf-8').close()
    except FileNotFoundError:
        current_dir = path.join(current_dir, '..')
    else:
        working_dir = path.join(current_dir, needed_dir)
        break

# quotas from cats
OPENING_PHRASES: Dict[AnyStr, List] = {
    "ru": [phrase.rstrip() for phrase in open(path.join(working_dir, 'ru', 'cat_quotes.txt'), 'r', encoding='utf-8')],
    "en": [phrase.rstrip() for phrase in open(path.join(working_dir, 'en', 'cat_quotes.txt'), 'r', encoding='utf-8')]
}
# multilingual guide (help)
GUIDE: Dict[AnyStr, AnyStr] = {
    "ru": '\n'.join(
        [
            line.rstrip() for line in open(path.join(working_dir, 'ru', 'guide.txt'), 'r', encoding='utf-8')
        ]
        ),
    "en": '\n'.join(
        [
            line.rstrip() for line in open(path.join(working_dir, 'en', 'guide.txt'), 'r', encoding='utf-8')
        ]
        )}
# welcome msg
WELCOME: Dict[AnyStr, AnyStr] = {
    "ru": '\n'.join(
        [
            line.rstrip() for line in open(path.join(working_dir, 'ru', 'welcome.txt'), 'r', encoding='utf-8')
        ]
        ),
    "en": '\n'.join(
        [
            line.rstrip() for line in open(path.join(working_dir, 'en', 'welcome.txt'), 'r', encoding='utf-8')
        ]
        )}

# here will be the responses to the phrases thrown by the user.
CURSE_RESPONSES: Dict[AnyStr, List] = {
    "ru":
        [
            line.rstrip() for line in open(
                path.join(working_dir, 'ru', 'curse.txt'),
                'r',
                encoding='utf-8'
            )
        ],
    "en":
        [
            line.rstrip() for line in open(
                path.join(working_dir, 'en', 'curse.txt'),
                'r',
                encoding='utf-8'
            )
        ]
}

BYE_RESPONSES: Dict[AnyStr, List] = {
    "ru":
        [
            line.rstrip() for line in open(
                path.join(working_dir, 'ru', 'bye.txt'),
                'r',
                encoding='utf-8'
            )
        ],
    "en":
        [
            line.rstrip() for line in open(
                path.join(working_dir, 'en', 'bye.txt'),
                'r',
                encoding='utf-8'
            )
        ]
}

HI_RESPONSES: Dict[AnyStr, List] = {
    "ru":
        [
            line.rstrip() for line in open(
                path.join(working_dir, 'ru', 'hi.txt'),
                'r',
                encoding='utf-8'
            )
        ],
    "en":
        [
            line.rstrip() for line in open(
                path.join(working_dir, 'en', 'hi.txt'),
                'r',
                encoding='utf-8'
            )
        ]
}

THX_RESPONSES: Dict[AnyStr, List] = {
    "ru":
        [
            line.rstrip() for line in open(
                path.join(working_dir, 'ru', 'thx.txt'),
                'r',
                encoding='utf-8'
            )
        ],
    "en":
        [
            line.rstrip() for line in open(
                path.join(working_dir, 'en', 'thx.txt'),
                'r',
                encoding='utf-8'
            )
        ]
}

# the responses need to be packed into the dictionary for an easier access
TO_USER_RAW_RESPONSES: Dict[AnyStr, Dict] = {
        "hi": HI_RESPONSES,
        "bye": BYE_RESPONSES,
        "curse": CURSE_RESPONSES,
        "thx": THX_RESPONSES
    }

# the template phrases from the bot as notifications or instructions
GENERIC_PHRASES: Dict[AnyStr, Dict[AnyStr, AnyStr]] = {
    "ru":
        {line.rstrip().split('><')[0]: line.rstrip().split('><')[1]
            for line in open(path.join(working_dir, 'ru', 'notifications.txt'), 'r', encoding='utf-8')},
    "en":
        {line.rstrip().split('><')[0]: line.rstrip().split('><')[1]
            for line in open(path.join(working_dir, 'en', 'notifications.txt'), 'r', encoding='utf-8')},
}

if __name__ == '__main__':
    raise UserWarning(f'Not designed as a launcher!!!')
