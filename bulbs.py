from yeelight import Bulb, discover_bulbs
import logging

logging.basicConfig(
    filename="bulbs",
    filemode="a",
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger("Bulbs")


class BulbException(Exception):
    pass


class HomeBulb:
    def __init__(self, ip: str, name: str) -> None:
        self.bulb = Bulb(ip)
        self.bulb_name = name

    def on_off(self) -> str:
        power = self.check_state()
        try:
            self.change_state(power)
            logger.info(f"Bulb ({self.bulb_name}) - State changed")
            return "OK"
        except Exception as err:
            logger.error(f"Bulb - {self.bulb_name} - {err}")
            raise BulbException(err)

    def change_state(self, power: str) -> None:
        match power:
            case "on":
                self.bulb.turn_off()
            case "off":
                self.bulb.turn_on()

    def check_state(self) -> str:
        '''-> "on" | "off"'''
        data = self.bulb.get_capabilities()
        return data["power"]


class Bulbs:
    liv_id = "0x0000000012ab31ea"
    bed_id = "0x0000000012bfc856"

    def __init__(self):
        bulbs = discover_bulbs()

        for bulb in bulbs:
            id_ = bulb["capabilities"]["id"]
            ip = bulb["ip"]

            match id_:
                case self.bed_id:
                    self.bedroom = HomeBulb(ip, name="bed")
                case self.liv_id:
                    self.livingroom = HomeBulb(ip, name="liv")
