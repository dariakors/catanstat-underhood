from flask import Blueprint, request, jsonify
from handlers import start_game, make_turns
from handlers.exceptions import BadRequest

game_blueprint = Blueprint('game_blueprint', __name__)


@game_blueprint.route('/game/start', methods=['POST'])
def create_game():
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
    players = request.json.get("players")
    if not players:
        raise BadRequest("Parameter 'players' is not specified")
    game_id = start_game.create_game(len(players))
    start_game.create_players(players, game_id)
    start_game.create_first_turn(game_id)
    return jsonify(id=game_id), 200


@game_blueprint.route('/game/<game_id>/next', methods=['POST'])
def make_next_turn(game_id):
    """

    :return:
    """
    # {
    #     "cubes":
    #         {
    #             "red": 3,
    #             "white": 5,
    #             "event": "sail"/"yellow"/"green"/"blue"
    #         }
    # }
    cubes = request.json.get("cubes")
    if not cubes:
        raise BadRequest("Parameter 'cubes' is not specified")
    make_turns.complete_previous_turn(game_id, cubes)
    make_turns.make_next_turn(game_id)
    return jsonify(message="OK"), 200


@game_blueprint.route('/game/<game_id>/pause', methods=['POST'])
def pause_game(game_id):
    """

    :return:
    """
    try:
        make_turns.pause_turn(game_id)
    except BadRequest:
        return '', 204
    return jsonify(message="OK"), 200


@game_blueprint.route('/game/<game_id>/resume', methods=['POST'])
def resume_game(game_id):
    """

    :return:
    """
    try:
        make_turns.resume_turn(game_id)
    except BadRequest:
        return '', 204
    return jsonify(message="OK"), 200
