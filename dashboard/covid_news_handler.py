"""Function(s) for proforming newsapi calls and handling the results"""

import json
import requests

def news_api_request(search_terms="Covid COVID-19 coronavirus"):
    """Proforms a search query for articles with the given search terms
    Defaults to covid search terms
    """
    api_key = "31c1a215c63d49fa9c3a65d259934575"
    url = f"https://newsapi.org/v2/everything?q={search_terms}&apiKey={api_key}"
    res = requests.get(url)
    assert res.status_code == 200

    data = json.loads(res.content)

    return data
