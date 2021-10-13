from db import db


class TurnStatusesModel(db.Model):
    __tablename__ = 'turnstatuses'
    id = db.Column(db.Integer, primary_key=True)
    turn_id = db.Column(db.Integer, db.ForeignKey('turns.id'))
    turn = db.relationship('TurnsModel')
    status = db.Column(db.String(20))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
