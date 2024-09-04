from http import HTTPStatus

from flask import (
    Blueprint,
    redirect,
    request,
    url_for,
)

from garlight.bulbs import discover_and_assign
from garlight.database import db
from garlight.models import BulbModel


manage = Blueprint("manage", import_name=__name__)
root = Blueprint("root", import_name=__name__)


@root.route("/")
def smoke():
    return "ok!"


@manage.route("/list")
def list_devices():
    devices = db.session.execute(db.select(BulbModel)).scalars().all()
    result = {"devices": [device.name] for device in devices}
    return result


@manage.route("/set-name/<string:name>", methods=["POST"])
def set_name(name: str):
    new_name = request.json.get("name", None)
    if new_name:
        bulb = db.one_or_404(db.select(BulbModel).filter_by(name=name))
        bulb.name = new_name
        db.session.commit()
        return {"name": bulb.name}
    return {"msg": "provide name"}, HTTPStatus.BAD_REQUEST


@manage.route("/discover")
def discover():
    discover_and_assign()
    url = url_for("manage.list_devices")
    return redirect(url)
