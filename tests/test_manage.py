from unittest.mock import patch

import pytest

from garlight.db.database import db
from garlight.db.models import BulbModel
from tests.example import bulbs_multi_discover, bulbs_single_discover


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


def test_set_name(client, bulb):
    old_name = bulb.name
    new_name = "new_name"
    request_data = {"name": new_name}
    expected = {"name": new_name}

    response = client.post(f"/set-name/{old_name}", json=request_data)

    assert response.json == expected


def create_bulbs(num: int, name: str = "test") -> list[dict[str:str]]:
    bulbs = []
    for bulb in range(num):
        bulb_data = {
            "id": f"id_bulb{bulb}",
            "ip": f"10.5.0.{bulb}",
            "name": f"{name}_{bulb}",
        }
        db_bulb = BulbModel(**bulb_data)
        bulbs.append(bulb_data)
        db.session.add(db_bulb)
        db.session.commit()
    return bulbs
