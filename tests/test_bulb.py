from unittest.mock import patch


def test_endpoints(bulb, client):
    endpoint = "/endpoints"
    result = client.get(endpoint)

    assert result.status_code == 200
    assert bulb.name in result.text


def test_status(bulb, client):
    endpoint = "/status"
    expected_result = ["test_name - offline"]

    response = client.get(endpoint)
    result = response.json

    assert response.status_code == 200
    assert result["statuses"] == expected_result


def test_on_off(bulb, client):
    name = bulb.name
    endpoint = f"/on-off/{name}"
    expected_result = "Offline"

    response = client.get(endpoint)
    result = response.text
    assert response.status_code == 200
    assert result == expected_result


@patch("garlight.bulbs.Bulb.set_scene")
def test_set_warm(scene_mock, bulb, client):
    scene_mock.return_value = "ok"
    name = bulb.name
    endpoint = f"/set-warm/{name}"
    expected_result = "Ok"

    response = client.get(endpoint)
    result = response.text
    assert response.status_code == 200
    assert result == expected_result


@patch("garlight.bulbs.Bulb.set_scene")
def test_set_color(scene_mock, bulb, client):
    scene_mock.return_value = "ok"
    name = bulb.name
    endpoint = f"/set-color/{name}"
    expected_result = "Ok"

    response = client.get(endpoint)
    result = response.text
    assert response.status_code == 200
    assert result == expected_result


@patch("garlight.bulbs.Bulb.cron_add")
def test_set_timer(cron_mock, bulb, client):
    cron_mock.return_value = "ok"
    name = bulb.name
    endpoint = f"/set-timer/{name}"
    expected_result = "Timer to 15 min."

    response = client.get(endpoint)
    result = response.text
    assert response.status_code == 200
    assert result == expected_result
