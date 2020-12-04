""" This module test the functionality of the main file """

from weather_update import get_weather
from news_filter import get_news
from get_covid_cases import get_cases
from time_conversions import alarm_to_time

def tests() -> None:
    """ This function does the tests """

    #check it converts the time correctly
    assert alarm_to_time("2020-12-04T00:29") == 1607038140.0, "alarm_to_time: FAILED"
    #check if it returns a string
    assert type(get_weather()) == str, "get_weather: FAILED"
    #check if it returns a string
    assert type(get_news()) == str, "get_news: FAILED"
    #check if it returns a string
    assert type(get_cases()) == str, "get_cases: FAILED"

