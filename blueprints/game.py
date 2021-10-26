from flask import Blueprint, request, jsonify
from handlers import start_game, make_turns
from handlers.exceptions import BadRequest

game_blueprint = Blueprint('game_blueprint', __name__)


@game_blueprint.route('/game/start', methods=['POST'])
def create_game():
    """
    Starting the game with creation of players and first turn
    ---
    parameters:
      - name: body
        in: body
        description: list of players with names and colours
        required: true
        schema:
          type: object
          properties:
            players:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
                  colour:
                    type: string
    responses:
      200:
        description: game was successfully created
        schema:
          type: object
          properties:
            id:
              type: integer
              description: game id
      400:
        description: parameters are incorrect or not specified
      500:
        description: game was not created
    """
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
    Make next turn for the current game
    ---
    parameters:
      - name: game_id
        in: path
        description: id of current game
        required: true
        schema:
          type: integer
      - name: body
        in: body
        description: dictionary of dice with values on red, white and event cubes for previous turn
        required: true
        schema:
          type: object
          properties:
            cubes:
              type: object
              properties:
                red:
                  type: integer
                white:
                  type: integer
                event:
                  type: string
                  enum:
                    - sail
                    - yellow
                    - green
                    - blue
    responses:
      200:
        description: OK
    """
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
