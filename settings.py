import os
from logging import config

import coloredlogs

if os.environ.get("TESTING") is not None:
    from settings_local_tests import *

    TESTING = True
else:
    from settings_local import *

    TESTING = False

BLUEPRINTS_DIR = 'src/api/blueprints/'

coloredlogs.install()
LOGGERS = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'colored': {
            '()': 'coloredlogs.ColoredFormatter',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'consoleDebug': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'colored',
            'stream': 'ext://sys.stdout'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'formatter': 'colored',
            'stream': 'ext://sys.stdout'
        },
        'fileDebug': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'filename': os.path.join(LOGGING_DIR, 'common.log'),
            'mode': 'a'
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'WARNING',
            'formatter': 'simple',
            'filename': os.path.join(LOGGING_DIR, 'common.log'),
            'mode': 'a'
        },
    },
    'loggers': {
        'src': {
            'level': 'DEBUG',
            'handlers': [logging_type + ['', 'Debug'][DEBUG] for logging_type in LOGGING_TYPES]
        }
    }
}
config.dictConfig(LOGGERS)
