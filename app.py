from flask import Flask
from db import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///postgres:postgres@localhost:5432/catangames.db'


if __name__ == '__main__':
    app.run(debug=True)
