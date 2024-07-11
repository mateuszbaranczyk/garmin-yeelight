from yeelight import Bulb, discover_bulbs

from logs import file_logger


class BulbException(Exception):
    pass


class HomeBulb:
    def __init__(self, ip: str, name: str) -> None:
        self.bulb = Bulb(ip)
        self.bulb_name = name

    def on_off(self) -> str:
        power = self.check_state()
        try:
            msg = self.change_state(power)
            file_logger.info(f"Bulb ({self.bulb_name}) - State changed")
            return f"OK - {msg}"
        except Exception as err:
            file_logger.error(f"Bulb - {self.bulb_name} - {err}")
            raise BulbException(err)

    def change_state(self, power: str) -> None:
        match power:
            case "on":
                self.bulb.turn_off()
                return "Power off"
            case "off":
                self.bulb.turn_on()
                return "Power on"

    def check_state(self) -> str:
        '''-> "on" | "off"'''
        data = self.bulb.get_capabilities()
        return data["power"]


class Bulbs:
    liv_id = "0x0000000012ab31ea"
    bed_id = "0x0000000012bfc856"

    def __init__(self):
        self.discover_and_assign()

    def discover_and_assign(self):
        self.bulbs = discover_bulbs()

        for bulb in self.bulbs:
            id_ = bulb["capabilities"]["id"]
            ip = bulb["ip"]

            match id_:
                case self.bed_id:
                    self.bedroom = HomeBulb(ip, name="bed")
                case self.liv_id:
                    self.livingroom = HomeBulb(ip, name="liv")

    def refresh(self):
        self.discover_and_assign()
