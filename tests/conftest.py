from garlight.run import create_app
from pytest import fixture
from flask.testing import FlaskClient


@fixture()
def app():
    app = create_app()
    app.config.update(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://"}
    )

    # other setup can go here

    yield app
    # clean up / reset resources here


@fixture()
def client(app) -> FlaskClient:
    return app.test_client()
