from flask import Flask, make_response, Response
from bulbs import Bulbs

app = Flask(__name__)

definitions = """- all,All
-- liv,Salon
--- light_on,Włącz,/liv/on
--- light-off,Wyłącz,/liv/off
-- bed,Sypialnia
--- light_on,Włącz,/bed/on
--- light-off,Wyłącz,/bed/off
"""

bulbs = Bulbs()


@app.route("/endpoints")
def endpoints():
    response = make_response(definitions, 200)
    response.mimetype = "text/plain"
    return response


def create_response(msg: str, status: int) -> Response:
    response = make_response(msg, status)
    response.mimetype = "text/plain"
    return response


@app.route("/liv/on")
def liv_on():
    try:
        bulbs.livingroom.turn_on()
        response = create_response("OK", 200)
    except:
        response = create_response("ERROR", 500)
    return response


@app.route("/liv/off")
def liv_off():
    try:
        bulbs.livingroom.turn_off()
        response = create_response("OK", 200)
    except:
        response = create_response("ERROR", 500)
    return response


@app.route("/bed/on")
def bed_on():
    try:
        bulbs.bedroom.turn_on()
        response = create_response("OK", 200)
    except:
        response = create_response("ERROR", 500)
    return response


@app.route("/bed/off")
def bed_off():
    try:
        bulbs.bedroom.turn_off()
        response = create_response("OK", 200)
    except:
        response = create_response("ERROR", 500)
    return response
