from flask import Blueprint, request, jsonify
from handlers import start_game, make_turns, game
from handlers.exceptions import BadRequest

game_blueprint = Blueprint('game_blueprint', __name__)


@game_blueprint.route('/game/start', methods=['POST'])
def create_game():
    """
    Starting the game with creation of players and first turn
    ---
    tags:
      - game
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
                    enum:
                    - white
                    - red
                    - brown
                    - blue
                    - green
                    - yellow
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
    tags:
      - game
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
        description: previous turn was completed and new turn has started
      400:
        description: parameters are incorrect or not specified
      404:
        description: game was not found or is completed
      409:
        description: tha game is paused, making a turn is possible after resuming
      500:
        description: turn was not made by some reasons
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
    Pause the game
    ---
    tags:
      - game
    parameters:
      - name: game_id
        in: path
        description: id of current game
        required: true
        schema:
          type: integer
    responses:
      200:
        description: the game was successfully paused
      204:
        description: the game is already paused
      404:
        description: game was not found or is completed
      500:
        description: the game was not paused by some reasons
    """
    try:
        make_turns.pause_turn(game_id)
    except BadRequest:
        return '', 204
    return jsonify(message="OK"), 200


@game_blueprint.route('/game/<game_id>/resume', methods=['POST'])
def resume_game(game_id):
    """
    Resume the game
    ---
    tags:
      - game
    parameters:
      - name: game_id
        in: path
        description: id of current game
        required: true
        schema:
          type: integer
    responses:
      200:
        description: the game was successfully resumed
      204:
        description: the game is already resumed
      404:
        description: game was not found or is completed
      500:
        description: the game was not resumed by some reasons
    """
    try:
        make_turns.resume_turn(game_id)
    except BadRequest:
        return '', 204
    return jsonify(message="OK"), 200


@game_blueprint.route('/game/<game_id>/complete', methods=['POST'])
def complete_game(game_id):
    """
    Complete the game
    ---
    tags:
      - game
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
        description: game was successfully completed
      400:
        description: parameters are incorrect or not specified
      404:
        description: game was not found or is already completed
      409:
        description: tha game is paused, making a turn is possible after resuming
      500:
        description: game was not completed by some reasons
    """
    cubes = request.json.get("cubes")
    if not cubes:
        raise BadRequest("Parameter 'cubes' is not specified")
    turn_data = make_turns.complete_previous_turn(game_id, cubes)
    game.set_winner_and_end_date(game_id, **turn_data)
    return jsonify(message="OK"), 200
