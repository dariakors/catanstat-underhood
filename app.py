import logging
import sys
from blueprints.game import game_blueprint
from db import db
from flasgger import Swagger
from flask import Flask, jsonify
from handlers.exceptions import CommonApplicationException
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(game_blueprint)
swagger = Swagger(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, CommonApplicationException):
        return jsonify(e.to_dict()), e.status_code
    elif isinstance(e, HTTPException):
        return jsonify(error=e.description), e.code
    else:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    string_format = u"%(asctime)s logger:%(name)s: module:%(module)s:%(lineno)d [%(levelname)s] %(message)s"
    formatter = logging.Formatter(string_format, "%Y-%m-%d %H:%M:%S")
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    db.init_app(app)
    app.run(debug=True)
