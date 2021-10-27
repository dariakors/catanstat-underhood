import logging
from functools import wraps
from handlers.exceptions import NotFound
from models.game import GameModel
from models.player import PlayerModel
from models.turn_statuses_log import TurnStatusesModel

log = logging.getLogger(__name__)


def get_current_player_id(game_id):
    order = GameModel.get_current_player_order(game_id)
    return PlayerModel.find_current_player_id(order, game_id)


def count_turn_duration(turn_id):
    pass


def determine_current_turn(game_id):
    log.debug('Identifying current turn...')
    turn = TurnStatusesModel.find_current_turn(game_id)
    if turn:
        log.debug(f'Found turn {turn.turn_id} in game id={game_id} with status {turn.status}')
        return turn
    else:
        raise NotFound(f"The game with id={game_id} was completed. You couldn't make turns anymore")


def check_game(decorated_func):
    @wraps(decorated_func)
    def wrapper(game_id, *args, **kwargs):
        if not GameModel.find_by_id(game_id):
            raise NotFound(f"The game with id={game_id} is not found")
        decorated_func(game_id, *args, **kwargs)
    return wrapper
