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

# if a user curses, the program blames the user for this
curse_regex = [
    re.compile(r'([^ру])?бля([тд])?\w?', re.IGNORECASE),
    re.compile(r'ху[йяеюи]\w?', re.IGNORECASE),
    re.compile(r'((про)|(у)|(на)|(об[ьъ])|(раз[ьъ])|(в[ъь])|(за)|(до))[её]б([ауоиел])?\w?', re.IGNORECASE),
    re.compile(r'\b[её]б([ауоиел])?\w?', re.IGNORECASE),
    re.compile(r'пизд', re.IGNORECASE),
    re.compile(r'хер((ня)|(ли)|(а)|(у)|(ов)|(ен)|(ну))\w?')
]


if __name__ == '__main__':
    raise UserWarning(f'Not designed as a launcher!!!')
