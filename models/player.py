from db import db


class PlayerModel(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    colour = db.Column(db.String(20))
    order = db.Column(db.Integer)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    game = db.relationship('GameModel')

    def __init__(self, name, colour, order, game_id):
        self.name = name
        self.colour = colour
        self.order = order
        self.game_id = game_id

    def json(self):
        return {"id": self.id, "name": self.name, "colour": self.colour, "order": self.order}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_current_player_id(cls, order, game_id):
        return cls.query.filter_by(order=order, game_id=game_id).first().id
