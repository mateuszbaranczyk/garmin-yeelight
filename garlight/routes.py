from flask import Blueprint, Response, make_response

from garlight.bulbs import BulbException
from garlight.endpoints_definitions import definitions
from garlight.logs import server_logger
from garlight.bulbs import Bulbs

liv = Blueprint("liv", import_name=__name__, url_prefix="/liv")
bed = Blueprint("bed", import_name=__name__, url_prefix="/bed")
root = Blueprint("root", import_name=__name__)
bulbs = Bulbs()


@root.route("/")
def smoke():
    return "ok!"


@root.route("/endpoints")
def endpoints():
    response = make_response(definitions, 200)
    response.mimetype = "text/plain"
    return response


@root.route("/status")
def status():
    bulbs = Bulbs()
    status = bulbs.status()
    response = make_response(status, 200)
    response.mimetype = "text/plain"
    return response


@liv.route("/on-off")
def liv_on_off():
    try:
        msg = bulbs.livingroom.on_off()
        response = create_response(msg, 200)
        server_logger.info(f"Livingroom - {msg}")
    except BulbException:
        response = create_response("ERROR", 500)
    return response


@bed.route("/on-off")
def bed_on_off():
    try:
        msg = bulbs.bedroom.on_off()
        response = create_response(msg, 200)
        server_logger.info(f"Bedroom - {msg}")
    except BulbException:
        response = create_response("ERROR", 500)
    return response


def create_response(msg: str, status: int) -> Response:
    response = make_response(msg, status)
    response.mimetype = "text/plain"
    return response
