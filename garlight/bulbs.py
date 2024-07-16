import os

from yeelight import Bulb, discover_bulbs

from garlight.logs import gunicorn_logger


class BulbException(Exception):
    pass


class HomeBulb:
    def __init__(self, ip: str, name: str) -> None:
        self.bulb = Bulb(ip)
        self.bulb_name = name

    def __repr__(self) -> str:
        return f"{self.bulb_name} - {self.check_state()}"

    def on_off(self) -> str:
        power = self.check_state()
        try:
            msg = self.change_state(power)
            return f"OK - {msg}"
        except Exception as err:
            gunicorn_logger.error(f"Bulb - {self.bulb_name} - {err}")
            raise BulbException(err)

    def change_state(self, power: str) -> None:
        match power:
            case "on":
                self.bulb.turn_off()
                return "Power off"
            case "off":
                self.bulb.turn_on()
                return "Power on"

    def check_state(self) -> str | None:
        '''"on" | "off"'''
        data = self.bulb.get_capabilities()
        return data["power"]


class Bulbs:
    _instance = None
    index = 0

    liv_id = os.getenv("LIV_ID")
    bed_id = os.getenv("BED_ID")
    bedroom = "Bedroom - offline"
    livingroom = "Livingroom - offline"
    devices = []

    def __new__(cls) -> "Bulbs":
        if cls._instance is None:
            cls._instance = super(Bulbs, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.discover_and_assign()

    def __iter__(self) -> HomeBulb | str:
        for bulb in self.devices:
            yield bulb

    def __getitem__(self, index) -> HomeBulb | str:
        return self.devices[index]

    def __repr__(self) -> str:
        return str(self.devices)

    def discover_and_assign(self) -> None:
        self.bulbs = discover_bulbs()

        for bulb in self.bulbs:
            id_ = bulb["capabilities"]["id"]
            ip = bulb["ip"]

            match id_:
                case self.bed_id:
                    self.bedroom = HomeBulb(ip, name="bed")
                case self.liv_id:
                    self.livingroom = HomeBulb(ip, name="liv")

        self.devices = [
            self.bedroom,
            self.livingroom,
        ]

    def status(self) -> str:
        return str(self.devices)
