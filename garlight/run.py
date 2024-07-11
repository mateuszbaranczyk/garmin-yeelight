import threading
import time

from flask import Flask

from garlight.bulbs import Bulbs
from garlight.logs import server_logger

bulbs = Bulbs()


def update_bulbs():
    global bulbs
    while True:
        bulbs.refresh()
        time.sleep(60)


def start_update_thread():
    thread = threading.Thread(target=update_bulbs)
    thread.daemon = True
    thread.start()


def create_app():
    app = Flask(__name__)
    start_update_thread()
    app.logger.handlers = server_logger.handlers

    from . import routes  # noqa

    app.register_blueprint(routes.bed)
    app.register_blueprint(routes.liv)
    app.register_blueprint(routes.root)

    return app


if __name__ == "__main__":
    app = create_app()
