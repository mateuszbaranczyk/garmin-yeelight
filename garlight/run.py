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

    from garlight.routing import bulbs_routes  # noqa
    from garlight.routing import manage_routes  # noqa

    app.register_blueprint(manage_routes.manage)
    app.register_blueprint(manage_routes.root)
    app.register_blueprint(bulbs_routes.bulb)

    return app


if __name__ == "__main__":
    app = create_app()
