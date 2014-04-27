# Imperialism remake
# Copyright (C) 2014 Trilarion
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

import json
import constants

if __name__ == '__main__':

    # options are stored as a dictionary
    options = {}
    options['general.version'] = '0.2'

    # save
    print('write to {}'.format(constants.Options_Default))
    file = open(constants.Options_Default, 'w')
    json.dump(options, file, indent=2, separators=(',', ': '))
