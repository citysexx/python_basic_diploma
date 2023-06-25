# file for configs
from typing import List, AnyStr


# token for telegram api
TELEGRAM_TOKEN = '6026006509:AAESkijXYtVNtWkElHDalJXD0HV25LLc1Ck'
# token for weather api
WEATHER_TOKEN = 'f46bffc37c7c4747b7681757232106'
# quotas from cats
OPENING_PHRASES: List[AnyStr] = [
    phrase.rstrip() for phrase in open('utils/cat_quotes.txt', 'r', encoding='utf-8')
]
