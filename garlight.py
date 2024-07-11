from flask import Flask
from datetime import time
import threading
from bulbs import Bulbs

app = Flask(__name__)
bulbs = Bulbs()


def update_bulbs():
    global bulbs
    while True:
        bulbs.refresh()
        time.sleep(300)


@app.before_first_request
def start_update_thread():
    thread = threading.Thread(target=update_bulbs)
    thread.daemon = True
    thread.start()


@app.route("/")
def root():
    return "ok!"
