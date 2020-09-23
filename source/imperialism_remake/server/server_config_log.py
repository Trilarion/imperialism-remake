# Imperialism remake
# Copyright (C) 2020 amtyurin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
import logging
import os

from imperialism_remake.base import constants

LOG_LEVEL = logging.DEBUG
LOG_FILE_SIZE = 100 * 1024 ** 2  # 100 MB
LOG_BACKUP_COUNT = 5

LOG_CONFIG = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'detailed': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s [%(levelname)-8s] [%(name)-10s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': LOG_LEVEL,
            'formatter': 'detailed',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': LOG_LEVEL,
            'formatter': 'detailed',
            'filename': os.path.join(constants.get_user_directory(), 'remake_server.log'),
            'mode': 'a',
            'maxBytes': LOG_FILE_SIZE,
            'backupCount': LOG_BACKUP_COUNT,
        },
        'file_error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': logging.ERROR,
            'formatter': 'detailed',
            'filename': os.path.join(constants.get_user_directory(), 'remake_server_error.log'),
            'mode': 'a',
            'maxBytes': LOG_FILE_SIZE,
            'backupCount': LOG_BACKUP_COUNT,
        }
    },
    'root': {
        'level': LOG_LEVEL,
        'handlers': ['console', 'file', 'file_error']
    }
}
