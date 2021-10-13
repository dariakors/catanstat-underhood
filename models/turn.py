from db import db


class TurnModel(db.Model):
    __tablename__ = 'turns'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    game = db.relationship('GameModel')
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    player = db.relationship('PlayerModel')

    red_cube = db.Column(db.Integer)
    white_cube = db.Column(db.Integer)
    event_cube = db.Column(db.String(10))
    duration = db.Column(db.DateTime)


