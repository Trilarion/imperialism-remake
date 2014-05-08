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
    Start with working directory equals base directory of project and script parameter build.
    See also: http://cx-freeze.readthedocs.org/en/latest/index.html
"""

import os, shutil, sys
from cx_Freeze import setup, Executable

# TODO define icon

# run manual_markdown_converter to create newest help version


# set options
options = {'build_exe': {
    'optimize': 2,
    'compressed': True,
    'include_in_shared_zip': True,
    'include_msvcr': True,
    'include_files': [('data', 'data')],
    'excludes': ['Tkinter']
}}

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [Executable(os.path.join('source', 'start.py'), targetName='ImperialismRemake.exe', base=base)]

# delete previous build directory completely
path = os.path.join('build', 'exe.win-amd64-3.4')
if os.path.isdir(path):
    shutil.rmtree(path)

# freeze
setup(name='Imperialism Remake', version='0.2.0', description='Open Source remake of the classic SSI strategy game: Imperialism',
      options=options, executables=executables)

# delete some files we do not need
os.remove(os.path.join(path, 'data', 'sources_and_licenses.ods'))