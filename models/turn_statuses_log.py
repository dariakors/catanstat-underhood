from db import db


class TurnStatusesModel(db.Model):
    __tablename__ = 'turnstatuses'
    id = db.Column(db.Integer, primary_key=True)
    turn_id = db.Column(db.Integer, db.ForeignKey('turns.id'))
    turn = db.relationship('TurnModel')
    status = db.Column(db.String(20))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    def __init__(self, turn_id, status, start_date):
        self.turn_id = turn_id
        self.status = status
        self.start_date = start_date

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
