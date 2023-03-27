import requests


def make_api_call(url):
    # Make API call to get some data
    response = requests.get(url)
    data = response.json()