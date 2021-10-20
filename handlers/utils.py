from models.game import GameModel
from models.player import PlayerModel


def get_current_player_id(game_id):
    order = GameModel.get_current_player_order(game_id)
    return PlayerModel.find_current_player_id(order, game_id)


def count_turn_duration(turn_id):
    pass