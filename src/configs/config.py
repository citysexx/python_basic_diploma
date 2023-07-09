# file for configs
from typing import List, AnyStr
from os import path, curdir


# token for telegram api
TELEGRAM_TOKEN = '6026006509:AAESkijXYtVNtWkElHDalJXD0HV25LLc1Ck'
# token for weather api
WEATHER_TOKEN = 'f46bffc37c7c4747b7681757232106'
# quotas from cats
OPENING_PHRASES: List[AnyStr] = [
    phrase.rstrip() for phrase in open(path.join(curdir, '..', 'utils', 'cat_quotes.txt'), 'r', encoding='utf-8')
]
GUIDE: AnyStr = '\n'.join(
    [
        line.rstrip() for line in open(path.join(curdir, '..', 'utils', 'guide.txt'), 'r', encoding='utf-8')
    ]
)
