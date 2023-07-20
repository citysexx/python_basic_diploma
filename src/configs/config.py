from typing import List, AnyStr, Dict
from os import path, chdir, curdir


# token for telegram api
TELEGRAM_TOKEN = '6026006509:AAESkijXYtVNtWkElHDalJXD0HV25LLc1Ck'
# token for weather api
WEATHER_TOKEN = 'f46bffc37c7c4747b7681757232106'

# Fix the paths, making it possible to access from all files and dirs
needed_dir = path.join('utils', 'bot_template_responses')
current_dir = path.abspath(curdir)
working_dir = ''
while True:
    try:
        open(path.join(current_dir, needed_dir, 'cat_quotes.txt'), 'r', encoding='utf-8')
    except FileNotFoundError:
        current_dir = path.join(current_dir, '..')
    else:
        working_dir = path.join(current_dir, needed_dir)
        break
# quotas from cats
OPENING_PHRASES: List[AnyStr] = [
    phrase.rstrip() for phrase in open(path.join(working_dir, 'cat_quotes.txt'), 'r', encoding='utf-8')
]
GUIDE: AnyStr = '\n'.join(
    [
        line.rstrip() for line in open(path.join(working_dir, 'guide.txt'), 'r', encoding='utf-8')
    ]
)
WELCOME: AnyStr = '\n'.join(
    [
        line.rstrip() for line in open(path.join(working_dir, 'welcome.txt'), 'r', encoding='utf-8')
    ]
)
# here will be the responses to the phrases thrown by the user.
CURSE_RESPONSES: List = [
    line.rstrip() for line in open(
        path.join(working_dir, 'curse.txt'),
        'r',
        encoding='utf-8'
    )
]
BYE_RESPONSES: List = [
    line.rstrip() for line in open(
        path.join(working_dir, 'bye.txt'),
        'r',
        encoding='utf-8'
    )
]
HI_RESPONSES: List = [
    line.rstrip() for line in open(
        path.join(working_dir, 'hi.txt'),
        'r',
        encoding='utf-8'
    )
]
THX_RESPONSES: List = [
    line.rstrip() for line in open(
        path.join(working_dir, 'thx.txt'),
        'r',
        encoding='utf-8'
    )
]
# the responses need to be packed into the dictionary for an easier access
TO_USER_RAW_RESPONSES: Dict[AnyStr, List] = {
        "hi": HI_RESPONSES,
        "bye": BYE_RESPONSES,
        "curse": CURSE_RESPONSES,
        "thx": THX_RESPONSES
    }

if __name__ == '__main__':
    raise UserWarning(f'Not designed as a launcher!!!')
