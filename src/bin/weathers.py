from typing import Dict, Any, AnyStr
from random import choice
from src.configs.config import OPENING_PHRASES


class CurrentWeather:
    """
    This class (just like ALL the classes below) is needed to fully tell and
    easily access (with getters), all properties of an incoming response.
    This class makes it easier because the dict class by key would be not
    pythonic enough to represent in code
    """
    def __init__(self, data: Dict) -> None:

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
        string = f'"{choice(OPENING_PHRASES)}"\n' \
                 f'Погода сейчас:\n\n' \
                 f'Населенный пункт: {self.city}\nСтрана: {self.country}\nУсловия: {self.condition}.\n' \
                 f'Температура воздуха: {self.temp} градуса(ов) по Цельсию,\n' \
                 f'Ощущается как: {self.feels_like} градусов по Цельсию\n' \
                 f'Ветер: {self.wind_dir} {self.wind_speed} км/ч, ' \
                 f'порывы ветра до {self.gust_speed} км/ч\n' \
                 f'Влажность воздуха: {self.humidity} процентов\n' \
                 f'Давление: {self.pressure} кПа\n' \
                 f'Видимость: {self.visibility} км\n' \
                 f'Индекс ультрафиолетового излучения: {self.uv_index}\n' \
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
