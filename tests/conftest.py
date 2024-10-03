from dataclasses import asdict, dataclass

from flask import Flask
from flask.testing import FlaskClient
from pytest import fixture

from garlight.db.database import db
from garlight.db.models import BulbModel


@fixture()
def app():
    app = Flask("test_app")

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from garlight.routing import bulbs_routes  # noqa
    from garlight.routing import manage_routes  # noqa

    app.register_blueprint(manage_routes.manage)
    app.register_blueprint(manage_routes.root)
    app.register_blueprint(bulbs_routes.bulb)

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all


@fixture()
def client(app) -> FlaskClient:
    return app.test_client()


@dataclass(frozen=True)
class BulbData:
    id: str
    ip: str
    name: str


@fixture()
def bulb_data():
    data = {"id": "test_id", "ip": "10.5.0.1", "name": "test_name"}
    return BulbData(**data)


@fixture()
def bulb(app, bulb_data) -> BulbModel:
    with app.app_context():
        db_bulb = BulbModel(**asdict(bulb_data))
        db.session.add(db_bulb)
        db.session.commit()
    return bulb_data
