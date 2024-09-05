# list_devices
# set_name
# discover


def test_smoke(client):
    response = client.get("/")
    assert response.status_code == 200
