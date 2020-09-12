# Imperialism remake
# Copyright (C) 2014-16 Trilarion
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

"""
Generate the default rules.
"""

import os
import sys

from imperialism_remake.server.models.terrain_type import TerrainType
from imperialism_remake.server.models.workforce_type import WorkforceType

if __name__ == '__main__':

    # add source directory to path if needed
    source_directory = os.path.realpath(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir, 'source'))
    if source_directory not in sys.path:
        sys.path.insert(0, source_directory)

    from imperialism_remake.lib import utils
    from imperialism_remake.base import constants

    rules = {}

    # terrain names
    terrain_settings = {
        TerrainType.SEA.value: {'name': 'Sea', 'texture_filename': 'terrain.sea.png'},
        TerrainType.PLAIN.value: {'name': 'Plain', 'texture_filename': 'terrain.plains.png'},
        TerrainType.HILLS.value: {'name': 'Hills', 'texture_filename': 'terrain.hills.outer.png'},
        TerrainType.MOUNTAINS.value: {'name': 'Mountains', 'texture_filename': 'terrain.mountains.outer.png'},
        TerrainType.TUNDRA.value: {'name': 'Tundra', 'texture_filename': 'terrain.tundra.outer.png'},
        TerrainType.SWAMP.value: {'name': 'Swamp', 'texture_filename': 'terrain.swamp.outer.png'},
        TerrainType.DESERT.value: {'name': 'Desert', 'texture_filename': 'terrain.desert.outer.png'}
    }
    rules['terrain_settings'] = terrain_settings

    workforce_settings = {
        WorkforceType.ENGINEER.value: {'name': 'Engineer', 'texture_filename_stand': 'engineer.stand.png',
                                       'texture_filename_on_duty': 'engineer.on_duty.png'},
        WorkforceType.GEOLOGIST.value: {'name': 'Geologist', 'texture_filename_stand': 'geologist.stand.png',
                                        'texture_filename_on_duty': 'geologist.on_duty.png'}
    }
    rules['workforce_settings'] = workforce_settings

    workforce_action_cursors = {
        WorkforceType.ENGINEER: {'workforce_action_cursor_move': 'cursor.action.move.png',
                                 'workforce_action_cursor_duty_action': 'cursor.engineer.build.construction.png',
                                 'workforce_action_cursor_not_allowed': 'cursor.action.not.allowed.png'},
        WorkforceType.GEOLOGIST: {'workforce_action_cursor_move': 'cursor.action.move.png',
                                  'workforce_action_cursor_duty_action': 'cursor.geologist.explore.png',
                                  'workforce_action_cursor_not_allowed': 'cursor.action.not.allowed.png'}
    }
    rules['workforce_action_cursors'] = workforce_action_cursors

    # save
    file = constants.SCENARIO_RULESET_STANDARD_FILE
    print('write to {}'.format(file))
    utils.write_to_file(file, rules)
