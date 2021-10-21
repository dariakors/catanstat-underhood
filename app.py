import logging
import sys

from blueprints.game import game_blueprint
from db import db
from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(game_blueprint)


@app.before_first_request
def create_tables():
    db.create_all()


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
