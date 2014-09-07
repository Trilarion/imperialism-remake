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

"""
    Generates the default options.
"""

import os
os.chdir('..')

import constants as c

# options are stored as a dictionary
options = {
    c.O_VERSION: 'v0.2.0 (2014-09-07)', # to be displayed on the start screen
    c.O_OPTIONS_VERSION: 1, # version of options

    c.OG_MW_FULLSCREEN: True, # we start full screen (can be unset by the program for some linux desktop environments
    c.OG_FULLSCREEN_SUPPORTED: True, # is full screen supported

    c.OM_PHONON_SUPPORTED: True,
    c.OM_BG_MUTE: False
}

# save
import tools as t
print('write to {}'.format(c.Options_Default_File))
t.write_json(c.Options_Default_File, options)