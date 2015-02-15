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

import os
os.chdir('..')

from lib import utils as u
from base import constants as c

"""
    Generates the default options.
"""

# options are stored as a dictionary
options = {
    c.O_Version: 'v0.2.1 (2015-02-15)', # to be displayed on the start screen
    # TODO this options version does not work
    c.O_Options_Version: 2, # version of options

    c.OG_MW_Fullscreen: True, # we start full screen (can be unset by the program for some linux desktop environments
    c.OG_Fullscreen_Supported: True, # is full screen supported

    c.OM_Phonon_Supported: True,
    c.OM_BG_Mute: False
}

# save
print('write to {}'.format(c.Options_Default_File))
u.write_as_yaml(c.Options_Default_File, options)