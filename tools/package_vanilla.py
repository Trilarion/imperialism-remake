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

version = '0.2.0'

# change directory to build (we assume we start in project/tools)
os.chdir(os.path.join('..', 'build'))

# set names
folder_name = 'ImperialismRemake-{}'.format(version)
zip_name = 'ImperialismRemake-{}-vanilla.zip'.format(version)
source_path = os.path.join('..', 'source')
data_path = os.path.join('..', 'data')

# delete directory and zip file
shutil.rmtree(folder_name, ignore_errors=True)
if os.path.isfile(zip_name):
    os.remove(zip_name)

# copy, first source and then data
shutil.copytree(source_path, folder_name, ignore=shutil.ignore_patterns('__pycache__'))
shutil.copytree(data_path, os.path.join(folder_name, 'data'))

# delete some files we do not need
os.remove(os.path.join(folder_name, 'data', 'sources_and_licenses.ods'))

# add some more files
shutil.copyfile(os.path.join('..', 'resources', 'vanilla_instructions.txt'), os.path.join(folder_name, 'vanilla_instructions.txt'))

# zip the directory
def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))

zip = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
zipdir(folder_name, zip)
zip.close()