from flask import Flask, make_response, Response
from bulbs import Bulbs, BulbException


app = Flask(__name__)

definitions = """- all,All
-- liv,Salon
--- light_on-off,ON/OFF,/liv/on-off
-- bed,Sypialnia
--- light_on-off,ON/OFF,/bed/on-off
"""

bulbs = Bulbs()


@app.route("/")
def root():
    return "ok!"


@app.route("/endpoints")
def endpoints():
    response = make_response(definitions, 200)
    response.mimetype = "text/plain"
    return response


def create_response(msg: str, status: int) -> Response:
    response = make_response(msg, status)
    response.mimetype = "text/plain"
    return response


@app.route("/liv/on-off")
def liv_on_off():
    try:
        msg = bulbs.livingroom.on_off()
        response = create_response(msg, 200)
    except BulbException:
        response = create_response("ERROR", 500)
    return response


@app.route("/bed/on-off")
def bed_on_off():
    try:
        bulbs.bedroom.on_off()
        response = create_response("OK", 200)
    except BulbException:
        response = create_response("ERROR", 500)
    return response
