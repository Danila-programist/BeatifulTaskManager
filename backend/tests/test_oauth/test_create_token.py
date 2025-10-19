from app.oauth import ClientJWT


def test_create_new_token():
    client_jwt = ClientJWT(data={"important_data": "data"})
    string = client_jwt.create_token()

    assert isinstance(string, str)
    assert len(string) > 50
