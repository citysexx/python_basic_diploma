from __future__ import print_function
from typing import AnyStr, List
import swagger_client
from swagger_client.rest import ApiException
import ast
from weathers import CurrentWeather
import src.configs.config


# Configure API key authorization: ApiKeyAuth
configuration = swagger_client.Configuration()
configuration.api_key['key'] = src.configs.config.WEATHER_TOKEN

# create an instance of the API class
api_instance = swagger_client.APIsApi(swagger_client.ApiClient(configuration))


def current_weather(city: AnyStr) -> ['CurrentWeather'] or None:
    """
    This function gets current weather in the city the user wants.
    It requests the information from the weather api and dumps the received
    response to a class CurrentWeather. If there is no response,
    """
    api_response = api_instance.realtime_weather(city, lang='ru')

    if api_response:
        # the following line makes a dictionary out of InlineResponse200 instance.
        # as the json decoder would not handle the response from this particular api,
        # the reason being that it needs a str instance, not InlineResponse200
        data = ast.literal_eval(str(api_response))
        current = CurrentWeather(data)

        return current

    return None


def search_locations(data: AnyStr) -> List or None:
    """
    This function serves as a search engine for the entered data. Due to
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
    user_town = input('Введите город >>> ').title()
    print(current_weather(user_town).__str__())
