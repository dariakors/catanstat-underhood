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

    def __init__(self, game_id, player_id, red_cube=None, white_cube=None, event_cube=None):
        self.game_id = game_id
        self.player_id = player_id
        self.red_cube = red_cube
        self.white_cube = white_cube
        self.event_cube = event_cube

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
