<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="src/images/IMG_20230719_114642_179.jpg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">WeatherCat Bot</h3>

  <p align="center">
    Превосходный бот, дающий прогноз погоды!



## О проекте

Почему именно этот бот:
* Удобный и легкий интерфейс, с помощью которого пользователь сможет быстро найти нужную информацию
* Более 300000 городов и населенных пунктов МИРА, доступных здесь по одному запросу 
* Быстродействие благодаря оптимизированным строкам кода Python
* Умный отклик, базово очеловеченный ИИ готовит Вам примитивные ответы на благодарность, прощание, приветствие и так далее 

Если у Вас возникла проблема, или есть пожелания, напишите мне на почту: dmitriigoryachev58@gmail.com



### Powered by:

<img src="src/images/python_logo.png" alt="Logo" width="80" height="80">-




## Быстрый старт

В этой секции вам будет показано, как установить и настроить бота. Чтобы избежать ошибок, следуйте нижеприведенным указаниям:



### Установка

_Ниже приведены шаги для установки данного проекта на сервер/компьютер:_
1. Узнайте, стоит ли у вас Python. Вывод консоли должен показать версию интерпретатора:
   ```sh
   # Check the system Python version
   $ python --version

   # Check the Python 2 version
   $ python2 --version

   # Check the Python 3 version
   $ python3 --version
   ```
   Вывод консоли:
   ```console
   [OUTPUT] Python 3.10.6
   ```
2. Если у Вас не получилось узнать версию Python, Вам нужно его установить:
   - Windows/MacOS: Пройдите по ссылке https://www.python.org/downloads/ и скачайте файл. Следуйте инструкциям установщика.
   - Linux: введите это
   ```sh
   $ sudo apt-get update
   $ sudo apt-get install python3
   ```
3. Загрузите репозиторий:
   ```sh
   git clone git@gitlab.skillbox.ru:dmitrii_goriachev_1/python_basic_diploma.git
   ```
4. Зайдите в репозиторий с помощью командной строки или IDE. Вам надо быть в корне: /python_basic_diploma

5. Введите данную команду:
   ```sh
   $ python -m pip --version
   $ python3 -m pip --version
   ```
   Если у вас нет менеджера библиотек, для Linux напишите:
   ```sh
   $ sudo apt install python3-pip
   $ sudo apt install python-pip
   ```
   Для Windows:
   
6. Установите библиотеку для стороннего АПИ погоды:
   ```sh
   pip install git+https://github.com/weatherapicom/python.git
   ```

7. (для проверяющего) Никаких АПИ ключей не требуется. Апи ключ уже в конфиге прописан. Когда проект будет принят, я поменяю ключи и поставлю проект себе на сервер

8. Найдите бота в телеграме: https://t.me/smart_weatherman_bot

## Примеры использования

* Запустите бота через скрипт main.py, нажмите СТАРТ и увидите неплохое приветственное описание:

<img height="800" src="src/images/start_demo.png" width="350"/>-
* При нажатии на первую кнопку в панели вам выйдет гайд по командам:

<img height="800" src="src/images/help_demo.png" width="350"/>-
* Ищите свой город по местоположению:

<img height="800" src="src/images/location_demo.png" width="350"/>-
* Ищите любой другой город. Найдется многое:

<img height="800" src="src/images/single_search_demo.png" width="350"/>-
<img height="800" src="src/images/forecast_demo.png" width="350"/>-
* Есть населенные пункты, содержащие имя искомого, либо совпадающие с ним. Не волнуйтесь, бот умеет с этим работать:

<img height="800" src="src/images/multi_search_demo.png" width="350"/>-
* Бот чувствует Ваш настрой, и отвечает одной из 100 фраз, для повышения интерактивности:

<img height="800" src="src/images/Screenshot_20230719-111102.png" width="350"/>-
* Бот различает благодарность, приветствие, прощание, просьбу о помощи, скринов с матом не будет, но на мат он тоже отвечает достойно

<img height="400" src="src/images/Screenshot_20230719-113355.png" width="350"/>-



## Принять участие
Если есть предложения по улучшению бота, обращайтесь по моим контактам. Контакты находятся в секции "Контакты" 

## Лицензия

См. `license.txt`.

## Контакты

Dmitry Goryachev

* mailto: dmitriigoryachev58@gmail.com
* cellto: +996552479090
* Проект: https://gitlab.skillbox.ru/dmitrii_goriachev_1/python_basic_diploma
