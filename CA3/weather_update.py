""" This module colects the weather information that will be used in the main module """

import requests
import json


def get_weather():
    """ This function colects and process al the data and returns a string with
    the content of the weather notifications of the main module """

    #Read configuration file and sets the parameters
    with open('config.json', 'r') as configfile:
        weather = json.load(configfile)
        api_key = weather["weather"]["api_key"]
        base_url = weather["weather"]["base_url"]
        city_name = weather["weather"]["city_name"]

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    info = response.json()

    #Relevant information is extracted
    air_temperature = round(info["main"]["temp"]-273.15, 2)
    feels_like = round(info["main"]["feels_like"]-273.15, 2)
    weather_description = info["weather"][0]["description"]
    location_name = info["name"]

    location_temp_text = "At "+ str(location_name)+" the air temperature is " + str(air_temperature)
    feels_like_temp =  ", but it feels like " +  str(feels_like)
    weather_description_text = ". The weather description is " + str(weather_description) + "."

    return location_temp_text + feels_like_temp + weather_description_text
