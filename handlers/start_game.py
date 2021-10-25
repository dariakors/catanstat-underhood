import logging
from datetime import datetime

from handlers.exceptions import BadRequest
from handlers.utils import get_current_player_id
from models.game import GameModel
from models.player import PlayerModel
from models.turn import TurnModel
from models.turn_statuses_log import TurnStatusesModel

log = logging.getLogger(__name__)


def create_game(players_number):
    log.info('Starting to create the game')
    if 1 < players_number <= 6:
        game = GameModel(players_number, start_date=datetime.utcnow(), end_date=None)
        game.save_to_db()
        log.info('The game with id {game.id} is created')
        return game.id
    else:
        log.debug('The game was not created. Incorrect number of players')
        raise BadRequest("Amount of players is not correct. Should be between 2 and 6")


def create_first_turn(game_id):
    GameModel.increase_turns_number(game_id)
    log.debug('Identifying current player...')
    current_player_id = get_current_player_id(game_id)
    turn = TurnModel(game_id, current_player_id)
    turn.save_to_db()
    turn_status = TurnStatusesModel(turn.id, 'in_progress', start_date=datetime.utcnow())
    turn_status.save_to_db()
    log.info('First turn is successfully created')


def create_players(players, game_id):
    i = 1
    for player in players:
        player_db = PlayerModel(**player, order=i, game_id=game_id)
        player_db.save_to_db()
        i += 1
    log.info(f'{len(players)} players are successfully created and added to the game')
