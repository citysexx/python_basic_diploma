import re


# templates that the program should consider as saying goodbye
bye_regex = [
    re.compile(r'\bпок(а)|(еда)\w?', re.IGNORECASE),
    re.compile(r'\bдо\s*свид\w?', re.IGNORECASE),
    re.compile(r'\bдо\s*скоро\w?', re.IGNORECASE),
    re.compile(r'проща\w*', re.IGNORECASE),
    re.compile(r'\bд[ао] (завтра\w?)|(\bвстречи\b)', re.IGNORECASE),
    re.compile(r'\bувидимся\s?', re.IGNORECASE),
    re.compile(r'\bЧао\b|\bАрив[ие]дерчи\b', re.IGNORECASE),
    re.compile(r'\bспок(ойной)|(оки)\s?(ночи)?\b', re.IGNORECASE)
]

# templates that the program should consider as saying goodbye
hi_regex = [
    re.compile(r'\bпривет\w?', re.IGNORECASE),
    re.compile(r'\bзд[ао]ров[ао]*\w?', re.IGNORECASE),
    re.compile(r'\bсал[ая]м\b', re.IGNORECASE),
    re.compile(r'(\bдобрый|доброго|добр(о)?е|доброй) (утро\b|утра\b|ночи\b|вечер\b|вечера\b|дня\b|день\b|времени суток\b)', re.IGNORECASE),
    re.compile(r'\b(з)?дра(вствуйте)|(сьт[ие])|(тути)\b', re.IGNORECASE),
    re.compile(r'\bку(-)?(ку)?\b', re.IGNORECASE),
    re.compile(r'\bшалом\b', re.IGNORECASE),
    re.compile(r'\bд[ао]ров\b', re.IGNORECASE),
    re.compile(r'\bсалют\b', re.IGNORECASE)
]

# templates that the program should consider as saying thanks
thanks_regex = [
    re.compile(r'\bспасибо\w?', re.IGNORECASE),
    re.compile(r'\bот\s*[Дд]уши\w?', re.IGNORECASE),
    re.compile(r'\bблагодар\w*', re.IGNORECASE),
    re.compile(r'\bспс\w*', re.IGNORECASE),
    re.compile(r'\bкруто\b', re.IGNORECASE)
]

# templates that the program should consider as asking for help
help_regex = [
    re.compile(r'\bпомо[гщ]\w+', re.IGNORECASE),
    re.compile(r'\bне\s?(\bмогу\b|\bзнаю\b|\bпонимаю\b|\bпонятно\b|\bпонять\b)\b', re.IGNORECASE),
    re.compile(r'\bкак\b|\bпочему\b|\bгде\b|\bзачем\b', re.IGNORECASE),
    re.compile(r'\bхелп\b|\bhelp\b|\bподдержка\b|\bвопрос\b|\bчаво\b|\bfaq\b', re.IGNORECASE),
    re.compile(r'(\bпомоги(те)?\b|\bнужно\b|\bнадо\b|\bнеобходимо\b) (\bпонять\b|\bузнать\b|\bразобраться\b|\bнайти\b|\bнаходить\b|\bдайте\b)', re.IGNORECASE),
    re.compile(r'\b(есть)? вопрос\b', re.IGNORECASE)
]

# if a user curses, the program offers help anyway
curse_regex = [
    re.compile(r'[^ру]бля([тд])?\w?', re.IGNORECASE),
    re.compile(r'ху[йяеюи]\w?', re.IGNORECASE),
    re.compile(r'((про)|(у)|(на)|(об[ьъ])|(раз[ьъ])|(в[ъь])|(за)|(до))[её]б([ауоиел])?\w?', re.IGNORECASE),
    re.compile(r'\b[её]б([ауоиел])?\w?', re.IGNORECASE),
    re.compile(r'пизд', re.IGNORECASE),
    re.compile(r'хер((ня)|(ли)|(а)|(у)|(ов)|(ен)|(ну))\w?')
]

# templates that the program should consider as talking about the present time
current_regex = [
    re.compile(r'сегодня[\w\s]?', re.IGNORECASE),
    re.compile(r'\bсейчас\w?', re.IGNORECASE),
    re.compile(r'(в|на) (этот|эту) (час|минуту)', re.IGNORECASE),
    re.compile(r'онлайн|online|синоптики|сводка|метео', re.IGNORECASE)
]

# templates that the program should consider as talking about the future time
future_regex = [
    re.compile(r'[^доа] завтра\b', re.IGNORECASE),
    re.compile(r'date', re.IGNORECASE),
    re.compile(r'\bпонедельник\b|\bвторник\b|\bсреда\b|\bчетверг\b|\bпятница\b|\bсуббота\b|\bвоскресенье\b', re.IGNORECASE),
    re.compile(r'\bближайшие дни\b', re.IGNORECASE),
    re.compile(r'\bпослезавтра\b', re.IGNORECASE),
    re.compile(r'\bнедел\w?', re.IGNORECASE),
    re.compile(r'вероятность чего то (грозы)', re.IGNORECASE),
    re.compile(r'\bпрогноз|\bсиноптики\b|\bсводка\b|\bметео', re.IGNORECASE),
    re.compile(r'\bутром\b|\bдн[её]м\b|\bвечером\b|\bночью\b', re.IGNORECASE)
]

# templates that depict the nature phenomenon
nature_disasters_regex = [
    re.compile(r'')
]


