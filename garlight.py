from flask import Flask
import time
import threading
from bulbs import Bulbs


bulbs = Bulbs()


def update_bulbs():
    global bulbs
    while True:
        bulbs.refresh()
        time.sleep(300)


def start_update_thread():
    thread = threading.Thread(target=update_bulbs)
    thread.daemon = True
    thread.start()


app = Flask(__name__)
start_update_thread()


@app.route("/")
def root():
    return "ok!"
