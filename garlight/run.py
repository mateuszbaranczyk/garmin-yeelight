from flask import Flask

from garlight.logs import gunicorn_logger
from garlight.models import db


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///garlight.db"

    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from garlight import routes  # noqa

    app.register_blueprint(routes.manage)
    app.register_blueprint(routes.bulb)
    app.register_blueprint(routes.root)

    return app


if __name__ == "__main__":
    app = create_app()
