'''

    Start with working directory equals base directory of project.

    See also: http://cx-freeze.readthedocs.org/en/latest/index.html
'''

import os
import shutil
import sys

from cx_Freeze import setup, Executable


# TODO define icon

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

executables = [Executable(os.path.join('source', 'omnitux2.py'),
                          targetName='Omnitux2.exe',
                          base=base)]

# delete previous build directory completely
path = os.path.join('build', 'exe.win-amd64-3.3')
if os.path.isdir(path):
    shutil.rmtree(path)

# freeze
setup(name='Omnitux 2', version='0.1', description='description',
      options=options, executables=executables)

# delete some files we do not need
os.remove(os.path.join(path, 'data', 'sources_and_licenses.ods'))