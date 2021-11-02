from db import db


class GameModel(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    players_number = db.Column(db.Integer, default=0)
    turns_number = db.Column(db.Integer, default=0)
    start_date = db.Column(db.DateTime, default=None)
    end_date = db.Column(db.DateTime, default=None)
    winner = db.Column(db.Integer, db.ForeignKey('players.id'), default=None)
    player = db.relationship('PlayerModel', foreign_keys=[winner])

    def __init__(self, players_number, start_date, end_date):
        self.players_number = players_number
        self.start_date = start_date
        self.end_date = end_date

    def json(self):
        return {"id": self.id, "start_date": self.start_date, "end_date": self.end_date}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def increase_turns_number(cls, id):
        game = cls.find_by_id(id)
        game.turns_number += 1
        game.save_to_db()

    @classmethod
    def get_current_player_order(cls, game_id):
        game = cls.query.filter_by(id=game_id).first()
        result = game.turns_number % game.players_number
        return result if result != 0 else game.players_number

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
