from flask import Blueprint, Response, make_response

from garlight.bulbs import BulbException, HomeBulb
from garlight.endpoints_definitions import definitions
from garlight.logs import gunicorn_logger

bulb = Blueprint("liv", import_name=__name__, url_prefix="")
bed = Blueprint("bed", import_name=__name__, url_prefix="/bed")
root = Blueprint("root", import_name=__name__)


@root.route("/")
def smoke():
    return "ok!"


@bulb.route("/endpoints")
def endpoints():
    # get all from db
    # create endpoint definitions
    response = make_response(definitions)
    response.mimetype = "text/plain"
    return response


@bulb.route("/status")
def status():
    # get all from db
    # chack status
    response = make_response(status)
    return response


@bulb.route("/on-off/<str:name>")
def on_off(name: str):
    bulb = HomeBulb(name)
    response = change_request(bulb=bulb)
    return response


def change_request(bulb: HomeBulb) -> Response:
    try:
        msg = bulb.on_off()
        response = create_response(msg)
        gunicorn_logger.info(f"{bulb.bulb_name} - {msg}")
    except BulbException:
        response = create_response("ERROR", 500)
    return response


def create_response(msg: str, status: int = 200) -> Response:
    response = make_response(msg, status)
    response.mimetype = "text/plain"
    return response
