import logging
from datetime import datetime
from handlers import utils
from handlers.utils import get_current_player_id
from models.game import GameModel
from models.turn import TurnModel
from models.turn_statuses_log import TurnStatusesModel

log = logging.getLogger(__name__)


def complete_previous_turn(game_id, cubes):
    log.debug('Identifying current turn...')
    turn = TurnStatusesModel.find_current_turn(game_id)
    log.debug(f'Found turn {turn.turn_id} in game {game_id} with status {turn.status}')

    if turn.status == 'in_progress':
        turn_with_cubes = TurnModel.find_by_id(turn.turn_id)
        turn_with_cubes.red_cube = cubes["red"]
        turn_with_cubes.white_cube = cubes["white"]
        turn_with_cubes.event_cube = cubes["event"]
        turn.end_date = datetime.utcnow()
        turn.save_to_db()
        # turn_with_cubes.duration = utils.count_turn_duration(turn.turn_id)
        turn_with_cubes.save_to_db()
        log.debug(f'Dice {cubes} are saved')
        log.info('Previous turn is completed')


def make_next_turn(game_id,):
    GameModel.increase_turns_number(game_id)
    log.debug('Identifying current player...')
    current_player_id = get_current_player_id(game_id)
    turn = TurnModel(game_id, current_player_id)
    turn.save_to_db()
    log.info('New turn is created')
    turn_status = TurnStatusesModel(turn.id, 'in_progress', start_date=datetime.utcnow())
    turn_status.save_to_db()


def pause_turn(game_id):
    log.debug('Identifying current turn...')
    turn = TurnStatusesModel.find_current_turn(game_id)
    log.debug(f'Found turn {turn.turn_id} in game {game_id} with status {turn.status}')
    if turn.status == 'in_progress':
        turn.end_date = datetime.utcnow()
        turn.save_to_db()
        paused_turn = TurnStatusesModel(turn.turn_id, 'is_paused', start_date=datetime.utcnow())
        paused_turn.save_to_db()
        log.info('The game is paused')


def resume_turn(game_id):
    log.debug('Identifying current turn...')
    turn = TurnStatusesModel.find_current_turn(game_id)
    log.debug(f'Found turn {turn.turn_id} in game {game_id} with status {turn.status}')
    if turn.status == 'is_paused':
        turn.end_date = datetime.utcnow()
        turn.save_to_db()
        resumed_turn = TurnStatusesModel(turn.turn_id, 'in_progress', start_date=datetime.utcnow())
        resumed_turn.save_to_db()
        log.info('The game is resumed')
