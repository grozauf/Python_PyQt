import logging
import sys

logger = logging.getLogger('decorators')


def logged(func):
    def wrapper(*args, **kwargs):
        logger.debug(f'{ func.__name__ } - with args:{ args }, { kwargs }')
        caller = sys._getframe(1).f_code.co_name
        logger.debug(f'{func.__name__} called from function: {caller}')
        return func(*args, **kwargs)

    return wrapper
