# Imperialism remake
# Copyright (C) 2017 Trilarion
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
Generates an updated pynsist installer configuration to be used
to create a Windows installer with pynsist.
"""

import os, sys
from string import Template

if __name__ == '__main__':

    # add source directory to path if needed
    tools_directory = os.path.abspath(os.path.dirname(__file__))
    source_directory = os.path.realpath(os.path.join(tools_directory, os.path.pardir, 'source'))
    if source_directory not in sys.path:
        sys.path.insert(0, source_directory)

    # read the template
    template_file_path = os.path.join(tools_directory, 'pynsist_installer_cfg.template')
    with open(template_file_path, encoding='utf-8') as file:
        template_text = file.read()

    # create replacement dictionary
    from imperialism_remake import version
    substitution_dictionary = {
        'version': version.__version__
    }

    # replace
    t = Template(template_text)
    substituted_text = t.substitute(**substitution_dictionary)

    # save as pynsist_installer.cfg
    installer_cfg_path = os.path.join(tools_directory, 'pynsist_installer.cfg')
    with open(installer_cfg_path, mode='w', encoding='utf-8') as file:
        file.write(substituted_text)