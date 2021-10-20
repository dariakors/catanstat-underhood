from db import db
from models.turn import TurnModel


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

    @classmethod
    def find_current_turn(cls, game_id):
        return cls.query.join(TurnModel, TurnModel.id == cls.turn_id).\
            filter(TurnModel.game_id == game_id).\
            filter(cls.end_date == None).first()

    @classmethod
    def find_all_statuses_by_turn_id(cls, turn_id):
        return cls.query.filter_by(turn_id=turn_id).all()
