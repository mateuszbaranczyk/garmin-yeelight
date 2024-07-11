from garlight import app, bulbs
from flask import make_response, Response
from bulbs import BulbException
from endpoints_definitions import definitions


@app.route("/endpoints")
def endpoints():
    response = make_response(definitions, 200)
    response.mimetype = "text/plain"
    return response


@app.route("/liv/on-off")
def liv_on_off():
    try:
        msg = bulbs.livingroom.on_off()
        response = create_response(msg, 200)
        app.logger.info(f"Livingroom - {msg}")
    except BulbException:
        response = create_response("ERROR", 500)
    return response


@app.route("/bed/on-off")
def bed_on_off():
    try:
        msg = bulbs.bedroom.on_off()
        response = create_response(msg, 200)
        app.logger.info(f"Bedroom - {msg}")
    except BulbException:
        response = create_response("ERROR", 500)
    return response


def create_response(msg: str, status: int) -> Response:
    response = make_response(msg, status)
    response.mimetype = "text/plain"
    return response
