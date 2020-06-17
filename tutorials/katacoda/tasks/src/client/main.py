import requests

def greet(server, api_key):
    res = requests.get(server, params={'api_key': api_key})
    return res.text
