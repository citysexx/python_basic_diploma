import re
from typing import Dict, AnyStr, List

# templates that the program should consider as saying goodbye
bye_regex: Dict[AnyStr, List] = {
    "ru":
        [
             re.compile(r'\bпок(а)|(еда)\w?', re.IGNORECASE),
             re.compile(r'\bдо\s*свид\w?', re.IGNORECASE),
             re.compile(r'\bдо\s*скоро\w?', re.IGNORECASE),
             re.compile(r'проща\w*', re.IGNORECASE),
             re.compile(r'\bд[ао] (завтра\w?)|(\bвстречи\b)', re.IGNORECASE),
             re.compile(r'\bувидимся\s?', re.IGNORECASE),
             re.compile(r'\bЧао\b|\bАрив[ие]дерчи\b', re.IGNORECASE),
             re.compile(r'\bспок(ойной)|(оки)\s?(ночи)?\b', re.IGNORECASE)
        ],
    "en":
        [
            re.compile(r'\b(c|see)(\s)?y[a(ou)\b]', re.IGNORECASE),
            re.compile(r'bye\b', re.IGNORECASE),
            re.compile(r'\b(c|see)(\s)?y[a(ou)](\s)?(later|tomorrow|next|soon)\b'),
            re.compile(r'\btalk(\s)?(to you)?(\s)?(\b\w\b)? (tomorrow|later|next|soon)\b'),
            re.compile(r'\bgood(\s)?(luck|night|time)\b', re.IGNORECASE),
            re.compile(r'\bfarewell\b', re.IGNORECASE),
            re.compile(r'\btill(\s)?(tomorrow|later)\b', re.IGNORECASE),
            re.compile(r'\b(gn|bb)\b', re.IGNORECASE)
        ]
}

# templates that the program should consider as saying goodbye
hi_regex: Dict[AnyStr, List] = {
    "ru":
        [
            re.compile(r'\bпривет\w?', re.IGNORECASE),
            re.compile(r'\bзд[ао]ров[ао]*\w?', re.IGNORECASE),
            re.compile(r'\bсал[ая]м\b', re.IGNORECASE),
            re.compile(r'(\bдобрый|доброго|добр(о)?е|доброй) (утро\b|утра\b|ночи\b|'
                       r'вечер\b|вечера\b|дня\b|день\b|времени суток\b)', re.IGNORECASE),
            re.compile(r'\b(з)?дра(вствуйте)|(сьт[ие])|(тути)\b', re.IGNORECASE),
            re.compile(r'\bку(-)?(ку)?\b', re.IGNORECASE),
            re.compile(r'\bшалом\b', re.IGNORECASE),
            re.compile(r'\bд[ао]ров\b', re.IGNORECASE),
            re.compile(r'\bсалют\b', re.IGNORECASE)
        ],
    "en":
        [
            re.compile(r'\bh(ey|i|ello)\b', re.IGNORECASE),
            re.compile(r'\bgood(\s)?(morning|day|evening)\b', re.IGNORECASE),
            re.compile(r'\b(wassup|what(\')?s(\s)?up)\b', re.IGNORECASE)
        ]
}

# templates that the program should consider as saying thanks
thanks_regex: Dict[AnyStr, List] = {
    "ru":
        [
            re.compile(r'\bспасибо\w?', re.IGNORECASE),
            re.compile(r'\bот\s*[Дд]уши\w?', re.IGNORECASE),
            re.compile(r'\bблагодар\w*', re.IGNORECASE),
            re.compile(r'\bспс\w*', re.IGNORECASE),
            re.compile(r'\bкруто\b', re.IGNORECASE)
        ],
    "en":
        [
            re.compile(r'\b(thanks|thank you)\b', re.IGNORECASE),
            re.compile(r'\b(thx|ty|thks)\b', re.IGNORECASE)
        ]
}

# templates that the program should consider as asking for help
help_regex: Dict[AnyStr, List] = {
    "ru":
        [
            re.compile(r'\bпомо[гщ]\w+', re.IGNORECASE),
            re.compile(r'\bне\s?(\bмогу\b|\bзнаю\b|\bпонимаю\b|\bпонятно\b|\bпонять\b)\b', re.IGNORECASE),
            re.compile(r'\bкак\b|\bпочему\b|\bгде\b|\bзачем\b', re.IGNORECASE),
            re.compile(r'\bхелп\b|\bhelp\b|\bподдержка\b|\bвопрос\b|\bчаво\b|\bfaq\b', re.IGNORECASE),
            re.compile(r'(\bпомоги(те)?\b|\bнужно\b|\bнадо\b|\bнеобходимо\b) '
                       r'(\bпонять\b|\bузнать\b|\bразобраться\b|\bнайти\b|\bнаходить\b|\bдайте\b)', re.IGNORECASE),
            re.compile(r'\b(есть)? вопрос\b', re.IGNORECASE)
        ],
    "en":
        [
            re.compile(r'\bhelp\b', re.IGNORECASE),
            re.compile(r'\bassist\w?', re.IGNORECASE),
            re.compile(r'\bcan(not|\'t)\b', re.IGNORECASE),
            re.compile(r'\b(how|why|when|where|what)\b', re.IGNORECASE),
            re.compile(r'\bI(\s)?do(not|n\'t)\b', re.IGNORECASE)
        ]
}

# if a user curses, the program blames the user for this
curse_regex: Dict[AnyStr, List] = {
    "ru":
        [
            re.compile(r'([^ру])?бля([тд])?\w?', re.IGNORECASE),
            re.compile(r'ху[йяеюи]\w?', re.IGNORECASE),
            re.compile(r'((про)|(у)|(на)|(об[ьъ])|(раз[ьъ])|(в[ъь])|(за)|(до))[её]б([ауоиел])?\w?', re.IGNORECASE),
            re.compile(r'\b[её]б([ауоиел])?\w?', re.IGNORECASE),
            re.compile(r'пизд', re.IGNORECASE),
            re.compile(r'хер((ня)|(ли)|(а)|(у)|(ов)|(ен)|(ну))\w?')
        ],
    "en":
        [
            re.compile(r'fuck', re.IGNORECASE),
            re.compile(r'shit', re.IGNORECASE),
            re.compile(r'ass([^ui][^ps][^s][^t][^a][^n][^c][^e]|\b|hole\b)', re.IGNORECASE),
            re.compile(r'dick', re.IGNORECASE),
            re.compile(r'\bscrew you\b', re.IGNORECASE)
        ]
}

if __name__ == '__main__':
    raise UserWarning(f'Not designed as a launcher!!!')
