from http import HTTPStatus

from flask import Blueprint, Response, make_response, request

from garlight.bulbs import BulbException, HomeBulb
from garlight.database import db
from garlight.endpoints_definitions import definitions, create_definitions
from garlight.logs import gunicorn_logger
from garlight.models import BulbModel

bulb = Blueprint("bulb", import_name=__name__)
manage = Blueprint("manage", import_name=__name__)
root = Blueprint("root", import_name=__name__)


@root.route("/")
def smoke():
    return "ok!"


@bulb.route("/endpoints")
def endpoints():
    devices = db.session.execute(db.select(BulbModel)).scalars()
    names = [device.name for device in devices]
    endpoints = create_definitions(devices=names)
    response = make_response(endpoints)
    response.mimetype = "text/plain"
    return response


@bulb.route("/status")
def status():
    # get all from db
    # chack status
    response = make_response(status)
    return response


@bulb.route("/on-off/<string:name>")
def on_off(name: str):
    bulb = HomeBulb(name)
    response = change_request(bulb)
    return response


@manage.route("/list")
def list_devices():
    devices = db.session.execute(db.select(BulbModel)).scalars()
    result = {"devices": devices}
    return result


@manage.route("/set-name/<string:id>")
def set_name(id: str):
    name = request.args.get("name", None)
    if name:
        bulb = db.one_or_404(db.select(BulbModel).filter_by(id=id))
        bulb.name = name
        db.session.commit()
        return bulb.as_dict()
    return {"msg": "provide name"}, HTTPStatus.BAD_REQUEST


def change_request(bulb: HomeBulb) -> Response:
    try:
        msg = bulb.on_off()
        response = create_response(msg)
        gunicorn_logger.info(f"{bulb.bulb_name} - {msg}")
    except BulbException:
        response = create_response("ERROR", HTTPStatus.INTERNAL_SERVER_ERROR)
    return response


def create_response(msg: str, status: int = HTTPStatus.OK) -> Response:
    response = make_response(msg, status)
    response.mimetype = "text/plain"
    return response
