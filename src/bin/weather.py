from __future__ import print_function
from typing import List, Dict, Any, AnyStr
import swagger_client
import ast
from src.configs.config import OPENING_PHRASES, WEATHER_TOKEN
from src.utils.funcs import decode_western_time_format, provide_random_phrase
# не трогать дейттайм! Хоть он типа и не используется, но он нужен для АПИ прогноза
import datetime

# Configure API key authorization: ApiKeyAuth
configuration = swagger_client.Configuration()
configuration.api_key['key'] = WEATHER_TOKEN

# create an instance of the API class
api_instance = swagger_client.APIsApi(swagger_client.ApiClient(configuration))


class CurrentWeather:
    """
    This class (just like ALL the classes below) is needed to fully tell and
    easily access (with getters), all properties of an incoming response.
    This class makes it easier because the dict class by key would be not
    pythonic enough to represent in code
    """

    def __init__(self, geo: AnyStr) -> None:
        # request current weather
        api_inline_response = api_instance.realtime_weather(geo, lang='ru')
        data = ast.literal_eval(str(api_inline_response))

        # main
        self.__current = data['current']
        self.__location = data['location']

        # location
        self.__country = self.__location['country']
        self.__city = self.__location['name']
        self.__region = self.__location['region']
        self.__time_zone_region = self.__location['tz_id']
        self.__latitude = self.__location['lat']
        self.__longitude = self.__location['lon']
        self.__local_time = self.__location['localtime']

        # current conditions
        self.__air_quality = self.__current['air_quality']
        self.__cloud = self.__current['cloud']
        self.__condition = self.__current['condition']['text']
        self.__condition_icon_link = self.__current['condition']['icon']
        self.__feels_like = self.__current['feelslike_c']
        self.__gust_speed = self.__current['gust_kph']
        self.__humidity = self.__current['humidity']
        self.__updated_time = self.__current['last_updated']
        self.__precipitation = self.__current['precip_mm']
        self.__pressure = self.__current['pressure_mb']
        self.__temp = self.__current['temp_c']
        self.__uv_index = self.__current['uv']
        self.__visibility = self.__current['vis_km']
        self.__wind_speed = self.__current['wind_kph']
        self.__is_bright = int(self.__current['is_day'])
        self.__wind_dir = self.__current['wind_degree']

    def __str__(self) -> AnyStr:
        """describe current weather for user"""
        string = f'"{provide_random_phrase(OPENING_PHRASES)}"\n' \
                 f'Погода сейчас:\n\n' \
                 f'Населенный пункт: {self.city}\nСтрана: {self.country}\nУсловия: {self.condition}.\n' \
                 f'Температура воздуха: {self.temp}°C\n' \
                 f'Ощущается как: {self.feels_like}°C\n' \
                 f'Ветер: {self.wind_dir} {self.wind_speed} км/ч, ' \
                 f'порывы ветра до {self.gust_speed} км/ч\n' \
                 f'Влажность воздуха: {self.humidity} процентов\n' \
                 f'Давление: {self.pressure} кПа\n' \
                 f'Видимость: {self.visibility} км\n' \
                 f'Индекс УФ излучения: {self.uv_index}\n' \
                 f'Осадки: {self.precipitation} мм\n\n' \
                 f'Информация обновлена в {self.updated_time}\n' \
                 f'Местное время: {self.local_time}\n' \
                 f'Зона: {self.time_zone_region}.'
        return string

    @property
    def country(self) -> Any:
        return self.__country

    @property
    def city(self) -> Any:
        return self.__city

    @property
    def region(self) -> Any:
        return self.__region

    @property
    def time_zone_region(self) -> Any:
        return self.__time_zone_region

    @property
    def latitude(self) -> Any:
        return self.__latitude

    @property
    def longitude(self) -> Any:
        return self.__longitude

    @property
    def local_time(self) -> Any:
        return self.__local_time

    @property
    def air_quality(self) -> Any:
        return self.__air_quality

    @property
    def cloud(self) -> Any:
        return self.__cloud

    @property
    def condition(self) -> Any:
        return self.__condition.lower()

    @property
    def condition_icon_link(self) -> Any:
        return self.__condition_icon_link

    @property
    def feels_like(self) -> Any:
        return self.__feels_like

    @property
    def gust_speed(self) -> Any:
        return self.__gust_speed

    @property
    def humidity(self) -> Any:
        return self.__humidity

    @property
    def updated_time(self) -> Any:
        return self.__updated_time

    @property
    def precipitation(self) -> Any:
        return self.__precipitation

    @property
    def pressure(self) -> Any:
        return self.__pressure

    @property
    def temp(self) -> Any:
        return self.__temp

    @property
    def uv_index(self) -> Any:
        return self.__uv_index

    @property
    def visibility(self) -> Any:
        return self.__visibility

    @property
    def wind_speed(self) -> Any:
        return self.__wind_speed

    @property
    def is_bright(self) -> Any:
        return 'at day' if self.__is_bright else 'at night'

    @property
    def wind_dir(self) -> Any:

        winds: Dict[AnyStr, Dict] = {
            'e': {'name': 'восточный', 'degree': range(900 - 225, 900 + 225)},
            's': {'name': 'южный', 'degree': range(1800 - 225, 1800 + 225)},
            'w': {'name': 'западный', 'degree': range(2700 - 225, 2700 + 225)},
            'ne': {'name': 'северо-восточный', 'degree': range(450 - 225, 450 + 225)},
            'se': {'name': 'юго-восточный', 'degree': range(1350 - 225, 2700 + 225)},
            'sw': {'name': 'юго-западный', 'degree': range(2250 - 225, 2700 + 225)},
            'nw': {'name': 'северо-западный', 'degree': range(3150 - 225, 2700 + 225)},
        }

        for wind_data in winds.values():
            if self.__wind_dir * 10 in wind_data['degree']:
                return wind_data['name']
        return 'северный'


class ForecastWeather:
    """
    This class stores logs about the forecast weather for the given time period
    """

    def __init__(self, geo: AnyStr, number_of_days: int, moment: AnyStr) -> None:

        # make a weather API request to forecast
        api_inline_response = api_instance.forecast_weather(geo, number_of_days, lang='ru')
        data = eval(str(api_inline_response))
        self.__moment = moment

        # city location text info
        self.__name = data["location"]["name"]
        self.__country = data["location"]["country"]
        self.__localtime = data["location"]["localtime"]

        # take the necessary information only out of the result (logs) below:
        # init the forecast logs
        self.__forecast_days = [
            ForecastDay(item) for item in data["forecast"]["forecastday"]
        ]

    def __str__(self) -> AnyStr:
        open_phr = f'"{provide_random_phrase(OPENING_PHRASES)}"'
        loc_description = f'Населенный пункт: {self.name}\n' \
                          f'Страна: {self.country}\n' \
                          f'Местное время: {self.localtime}'
        report = ''

        for index, forecast_day in enumerate(self.__forecast_days):

            if self.__moment == "tomorrow" and index == 1:
                report += forecast_day.__str__() + '\n'

            if self.__moment == "today":
                report += self.__forecast_days[0].__str__() + '\n'

            if self.__moment == "three_days" and index in range(0, 3):
                report += forecast_day.__str__() + '\n'

        return f'{open_phr}\n\n{loc_description}\n\n{report}'

    @property
    def name(self) -> AnyStr:
        return self.__name

    @property
    def country(self) -> AnyStr:
        return self.__country

    @property
    def localtime(self) -> AnyStr:
        return self.__localtime

    @property
    def daily_forecasts(self) -> List:
        return self.__forecast_days


class ForecastDay:
    """
    This class is solely for the usage inside a Forecast class.
    This describes weather within a day only
    """
    def __init__(self, day_cover: Dict):
        """
        Initializes the forecast for a single day
        Args:
            day_cover: This is a dictionary of items that the program received
            __from API
        """
        self.__day_report = day_cover
        self.__date = day_cover["_date"]

        # temperature
        self.__maximum_temp = day_cover["day"]["maxtemp_c"]
        self.__average_temp = day_cover["day"]["avgtemp_c"]
        self.__minimum_temp = day_cover["day"]["mintemp_c"]

        # wind
        self.__max_wind = day_cover["day"]["maxwind_kph"]

        # precipitation
        self.__precipitation = day_cover["day"]["totalprecip_mm"]

        # visibility
        self.__average_visibility = day_cover["day"]["avgvis_km"]

        # humidity
        self.__average_humidity = day_cover["day"]["avghumidity"]

        # precipitation probability
        self.__if_rain = False if not int(day_cover["day"]["daily_will_it_rain"]) \
            else True
        self.__rain_likelihood = day_cover["day"]["daily_chance_of_rain"]

        self.__if_snow = False if not int(day_cover["day"]["daily_will_it_snow"]) \
            else True
        self.__snow_likelihood = day_cover["day"]["daily_chance_of_snow"]

        # conditions
        self.__condition = day_cover["day"]["condition"]["text"]

        # uv index
        self.__uv_index = day_cover["day"]["uv"]

        # sunset - sunrise
        self.__sunrise_time = day_cover["astro"]["sunrise"]
        self.__sunset_time = day_cover["astro"]["sunset"]

        # an hourly weather for the given day
        self.__hourly_forecasts = [
            HourlyForecast(data_for_hour)
            for data_for_hour in day_cover["hour"]
        ]

    def __str__(self) -> AnyStr:
        """
        Describes daily weather
        Returns:
            string report
        """
        return f'============\nПрогноз на {self.date}:\n' \
               f'{self.condition}.\n' \
               f'Максимальная температура: {self.max_temp}°C\n' \
               f'Минимальная температура: {self.min_temp}°C\n' \
               f'Ожидается в среднем за день: {self.avg_temp}°C\n' \
               f'Ветер усилится до {self.max_wind} км/ч,\n' \
               f'Ожидаемое количество осадков: {self.precipitation} мм\n' \
               f'Средняя видимость: {self.avg_visibility} км\n' \
               f'Средняя влажность воздуха: {self.avg_humidity}%\n' \
               f'Будет ли дождь: {"ДА" if int(self.is_rain) else "НЕТ"}\n' \
               f'Вероятность дождя: {self.rain_probability}%\n' \
               f'Будет ли снег: {"ДА" if int(self.is_snow) else "НЕТ"}\n' \
               f'Вероятность снега: {self.snow_probability}%\n' \
               f'Индекс УФ излучения: {self.uv}\n' \
               f'Восход: {self.when_sunrise}\n' \
               f'Закат: {self.when_sunset}\n' \
               f'Время местное.\n============\n'

    @property
    def date(self) -> Any:
        return str(self.__date)

    @property
    def max_temp(self) -> Any:
        return self.__maximum_temp

    @property
    def min_temp(self) -> Any:
        return self.__minimum_temp

    @property
    def avg_temp(self) -> Any:
        return self.__average_temp

    @property
    def max_wind(self) -> Any:
        return self.__max_wind

    @property
    def precipitation(self) -> Any:
        return self.__precipitation

    @property
    def avg_visibility(self) -> Any:
        return self.__average_visibility

    @property
    def avg_humidity(self) -> Any:
        return self.__average_humidity

    @property
    def is_rain(self) -> bool:
        return self.__if_rain

    @property
    def rain_probability(self) -> Any:
        return self.__rain_likelihood

    @property
    def is_snow(self) -> bool:
        return self.__if_snow

    @property
    def snow_probability(self) -> Any:
        return self.__snow_likelihood

    @property
    def condition(self) -> Any:
        return self.__condition

    @property
    def uv(self) -> Any:
        return self.__uv_index

    @property
    def when_sunrise(self) -> Any:
        return decode_western_time_format(self.__sunrise_time)

    @property
    def when_sunset(self) -> Any:
        return decode_western_time_format(self.__sunset_time)

    def give_hourly_forecast(self, *, period: ['range']) -> AnyStr:
        """
        This method provides an hourly summary of the weather depending
        on what hour range you set to it

        Args:
            period: this is a range instance meaning the user's
            input of the hours, within which the hourly forecast is to be provided

        Returns:
            a weather report in string
        """
        hourly_report = ''

        for index, hourly_forecast in enumerate(self.__hourly_forecasts):

            if index in period:
                hourly_report += hourly_forecast.__str__()

        return hourly_report


class HourlyForecast:
    """
    This class contains information on the weather every hour.
    There will not be any __str__() method because it will not be used in other
    classes but the info will be returned depending on the range of hours you set
    """
    def __init__(self, data: Dict):

        # time
        self.__time = data["time"]

        # precipitation chances
        self.__chance_of_rain = data["chance_of_rain"]
        self.__chance_of_snow = data["chance_of_snow"]

        # conditions
        self.__condition = data["condition"]["text"]

        # wind power
        self.__wind_strength = data["wind_kph"]
        self.__gust_strength = data["gust_kph"]

        # temperature and feels like temperature
        self.__temp = data["temp_c"]
        self.__feels_like = data["feelslike_c"]

    @property
    def time(self) -> Any:
        return self.__time

    @property
    def rain_chance(self) -> Any:
        return self.__chance_of_rain

    @property
    def snow_chance(self) -> Any:
        return self.__chance_of_snow

    @property
    def condition(self) -> Any:
        return self.__condition

    @property
    def wind(self) -> Any:
        return self.__wind_strength

    @property
    def gust(self) -> Any:
        return self.__gust_strength

    @property
    def temperature(self) -> Any:
        return self.__temp

    @property
    def feels(self) -> Any:
        return self.__feels_like

    def __str__(self) -> AnyStr:
        return f'============\nНа {self.time.split()[1]}\n' \
               f'{self.condition}.\n' \
               f'Температура воздуха: {self.temperature}°C\n' \
               f'Ощущается как: {self.feels}°C\n' \
               f'Скорость ветра: {self.wind} км/ч\n' \
               f'Порывы до: {self.gust} км/ч\n' \
               f'Шанс дождя: {self.rain_chance}\n' \
               f'Шанс снега: {self.snow_chance}\n' \
               f'============\n\n'


def search_locations(data: AnyStr) -> List or None:
    """
    This function serves as a search engine for the entered logs. Due to
    the fact that, if the user enters city name, the various cities can appear
    as a result. According to the API, the user can also enter postal code and
    location in decimal degrees. This function searches the results from string
    and returns a list of possible variants. If nothing found, None is returned.

    Attributes:
        :param data: This is a string which can represent either a city name
        or anything else related to city (e.g. postal, location)

    """
    api_response = api_instance.search_autocomplete_weather(data)
    if api_response:
        return api_response

    return None


if __name__ == '__main__':
    # showcase current weather
    current_weather = CurrentWeather('Vladivostok')
    print(current_weather)
    # showcase forecast
    forecast_weather = ForecastWeather(geo='Vladivostok', number_of_days=1, moment='today')
    print(forecast_weather)
    # showcase forecast hourly
    print(forecast_weather.daily_forecasts[0].give_hourly_forecast(period=range(0, 7)))
