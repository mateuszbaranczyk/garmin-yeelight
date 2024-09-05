from unittest.mock import patch
from tests.example import bulbs_single_discover, bulbs_multi_discover
from garlight.db.database import db
from garlight.db.models import BulbModel
import pytest


def test_smoke(client):
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "discover_result", [bulbs_multi_discover, bulbs_single_discover]
)
@patch("garlight.bulbs.discover_bulbs")
def test_discover(discover_bulbs_mock, discover_result, client):
    discover_bulbs_mock.return_value = discover_result
    with client:
        response = client.get("/discover")
        result = db.session.query(BulbModel).all()

    assert response.status_code == 302
    assert len(result) == len(discover_result)
def test_list_devices(app):
    num_of_devices = 2
    with app.app_context():
        client = app.test_client()
        create_bulbs(num_of_devices)
        response = client.get("/list")

    devices = response.json["devices"]
    assert len(devices) == num_of_devices
