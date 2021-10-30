import logging
from datetime import timedelta
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
    turn_parts = TurnStatusesModel.find_all_statuses_by_turn_id(turn_id)
    in_progress_parts = list(filter(lambda x: x.status == 'in_progress', turn_parts))
    is_paused_parts = list(filter(lambda x: x.status == 'is_paused', turn_parts))
    in_progress_duration = timedelta()
    is_paused_duration = timedelta()
    for pr_part in in_progress_parts:
        in_progress_duration += (pr_part.end_date - pr_part.start_date)
    actual_duration = in_progress_duration.total_seconds() * 1000  # in ms
    for p_part in is_paused_parts:
        is_paused_duration += (p_part.end_date - p_part.start_date)
    procrastination_duration = is_paused_duration.total_seconds() * 1000  # in ms
    total_duration = actual_duration + procrastination_duration
    return {"actual_duration": actual_duration,
            "procrastination_duration": procrastination_duration,
            "total_duration": total_duration}


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
