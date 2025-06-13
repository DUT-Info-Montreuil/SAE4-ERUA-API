from flask import Flask, jsonify, request, Blueprint
from controllers.artist_controller import artist_controller
from controllers.artwork_controller import artwork_controller
from utils.function import send_error
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CORS(app)

app.register_blueprint(artist_controller)
app.register_blueprint(artwork_controller)


@app.errorhandler(500)
def internal_error(error):
    return send_error(500, "Internal Server Error")


@app.errorhandler(404)
def not_found(error):
    return send_error(404, "Endpoint not found")


@app.errorhandler(400)
def bad_request(error):
    return send_error(400, "Bad Request")


@app.errorhandler(405)
def bad_request(error):
    return send_error(405, "Method not Allowed")


if __name__ == '__main__':
    app.run()