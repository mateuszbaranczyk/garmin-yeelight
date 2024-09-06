from pytest import fixture
from flask.testing import FlaskClient
from flask import Flask
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



