import main


with open('/etc/credential/apiKey') as f:
    api_key = f.read()

def test_greet():
    server = 'http://localhost:8080/greet'
    res = main.greet(server, api_key)

    assert 'Hello, World!' in res
