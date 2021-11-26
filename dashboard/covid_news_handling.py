import requests

def news_API_request(covid_terms="Covid COVID-19 coronavirus"):
    url = "https://newsapi.org/v2/everything?q={query}&apiKey={APIKey}".format(query=covid_terms, APIKey="31c1a215c63d49fa9c3a65d259934575")
    res = requests.get(url)
    assert res.status_code == 200
    return res.content