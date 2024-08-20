import os

from yeelight import Bulb, discover_bulbs

from garlight.logs import gunicorn_logger
from garlight.models import BulbModel
from garlight.models import db


class BulbException(Exception):
    pass


class HomeBulb:
    def __init__(self, name: str) -> None:
        self.model = self.get_from_db(name)
        self.bulb = Bulb(ip=self.model.ip)

    def __repr__(self) -> str:
        return f"{self.model} - {self.check_state()}"

    def get_from_db(self, name: str) -> BulbModel:
        model = db.session.execute(
            db.select(BulbModel).filter_by(name=name)
        ).scalar_one()
        return model

    def on_off(self) -> str:
        power = self.check_state()
        try:
            msg = self.change_state(power)
            return f"{msg}"
        except Exception as err:
            gunicorn_logger.error(f"Bulb - {self.bulb_name} - {err}")
            raise BulbException(err)

    def change_state(self, power: str) -> None:
        match power:
            case "offline":
                return "Offline"
            case "on":
                self.bulb.turn_off()
                return "Power off"
            case "off":
                self.bulb.turn_on()
                return "Power on"

    def check_state(self) -> str:
        '''"on" | "off" | "offline"'''
        data = self.bulb.get_capabilities()
        state = data["power"] if data else "offline"
        return state


def discover_and_assign() -> None:
    devices = discover_bulbs()

    bulbs = [
        BulbModel(
            id=bulb["capabilities"]["id"],
            ip=bulb["ip"],
            name=bulb["capabilities"]["id"],
        )
        for bulb in devices
    ]
    db.session.add_all(bulbs)
    db.session.commit()
