from db import db


class GameModel(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, default=None)
    end_date = db.Column(db.DateTime, default=None)



