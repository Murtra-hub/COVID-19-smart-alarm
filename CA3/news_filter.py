""" This module colects the top news that will be used in the main module """

import json
from newsapi import NewsApiClient


def get_news():
    """ This function colects and process al the data and returns a string with
    the content of the top news notifications of the main module """

    #Read configuration file and sets the parameters
    with open('config.json', 'r') as configfile:
        news = json.load(configfile)
        api_key = news["news"]["api_key"]
        country = news["news"]["country"]
        language = news["news"]["language"]

    newsapi = NewsApiClient(api_key=api_key)

    #Information is extracted and stored
    top_headlines = newsapi.get_top_headlines(language=language,
                                              country= country)

    articles_titles = []

    #Titles of the top news are saved on a list
    for article in top_headlines['articles']:
        articles_titles.append(article['title'])

    string_articles = str(articles_titles)
    final_articles = str(string_articles.replace("[", "").replace("]", ""))

    return final_articles
