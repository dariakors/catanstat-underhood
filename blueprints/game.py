from handlers import start_game
from flask import Blueprint, request, jsonify

game_blueprint = Blueprint('game_blueprint', __name__)


@game_blueprint.route('/game/start', methods=['POST'])
def start_game():
    """

    :return:
    """
    # {"players":
    #      {
    #          1: {"name": "Anton", "colour": "brown"},
    #          2: {"name": "Artem", "colour": "blue"},
    #          3: {"name": "Daria", "colour": "white"},
    #          4: {"name": "Julia", "colour": "red"}
    #      }
    #
    # }
    # game_id = game.create_()
    players = request.json.get("players")
    game_id = start_game.create_game(len(players))
    start_game.create_players(players, game_id)
    start_game.create_first_turn(game_id)
    return jsonify(id=game_id), 200



