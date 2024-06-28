from yeelight import Bulb, discover_bulbs


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
                    self.bedroom = Bulb(ip)
                case self.liv_id:
                    self.livingroom = Bulb(ip)
