""" This module colects the covid cases information that will be used in the main module """

from requests import get

def get_cases():
    """ This function process al the data and returns a string with
    the content of the covid cases notifications of the main module """

    def get_data(url):
        """ This function colects al the data that will be processed in the get_cases function"""

        response = get(url, timeout=10)
        if response.status_code >= 400:
            raise RuntimeError(f'Request failed: { response.text }')
        return response.json()

    endpoint = (
        'https://api.coronavirus.data.gov.uk/v1/data?'
        'filters=areaType=nation;areaName=england&'
        'structure={"date":"date","NewCases":"newCasesByPublishDate","cumcases":"cumCasesByPublishDate","rate":"cumCasesBySpecimenDateRate"}'
    )

    data = get_data(endpoint)
    important_data = data["data"]
    newcases = str(important_data[0]['NewCases'])
    cumcases = str(important_data[0]['cumcases'])
    rate = str(important_data[1]['rate'])

    new_cases_text = 'New cases: '+  newcases + " - "
    cumcases_text = "Cumulative cases: " + cumcases + " - "
    rate_text = 'Rate of cumulative cases per 100k resident population: ' + rate

    return new_cases_text + cumcases_text + rate_text
