import main

def test_main():
    main.app.testing = True
    client = main.app.test_client()

    r = client.get('/')
    assert r.status_code == 200
    assert 'Your app is up and running' in r.data.decode('utf-8')
