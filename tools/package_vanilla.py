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

import os, shutil, zipfile

import manual_markdown_converter

"""
    Creates an OS independent package (as zip file) that contains the sources and the
    data but requires Python and PySide to be installed manually also saving space.
    It serves as generic non Windows distribution for the moment.
"""

# version string for file name encoding
version = '0.2.1'

# change to project root
os.chdir('..')

# run conversion of help files from markdown
manual_markdown_converter.convert()

# change to build directory
os.chdir('build')

# set names
folder_name = 'ImperialismRemake-{}'.format(version)
zip_name = 'ImperialismRemake-{}-allOS.zip'.format(version)
source_path = os.path.join('..', 'source')
data_path = os.path.join('..', 'data')

# delete directory and zip file if still existing
shutil.rmtree(folder_name, ignore_errors=True)
if os.path.isfile(zip_name):
    os.remove(zip_name)

# copy, first source and then data (copytree can only copy if destination folder is not existing)
shutil.copytree(source_path, folder_name, ignore=shutil.ignore_patterns('__pycache__'))
shutil.copytree(data_path, os.path.join(folder_name, 'data'))

# add some more files
shutil.copyfile(os.path.join('..', 'LICENSE'), os.path.join(folder_name, 'LICENSE'))
shutil.copyfile(os.path.join('..', 'resources', 'README-allOS'), os.path.join(folder_name, 'README'))

# zip the directory
def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))

zip = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
zipdir(folder_name, zip)
zip.close()