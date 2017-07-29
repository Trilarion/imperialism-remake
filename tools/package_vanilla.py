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
Creates an OS independent package (as zip file) that contains the sources and the
data but requires Python and Python modules to be installed manually before.
It serves as generic non Windows distribution for the moment.
"""

import os, sys, shutil, zipfile

if __name__ == '__main__':

    # first build the documentation
    from build_documentation import build_documentation
    build_documentation()

    # add source directory to path if needed
    root_directory = os.path.realpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir))
    source_directory = os.path.join(root_directory, 'source')
    if source_directory not in sys.path:
        sys.path.insert(0, source_directory)

    # create build directory if not existing
    build_directory = os.path.join(root_directory, 'build')
    if not os.path.exists(build_directory):
        os.mkdir(build_directory)

    # get build folder name
    from imperialism_remake import version
    target_directory_name = 'ImperialismRemake-{}'.format(version.__version__)
    target_zip_name = 'ImperialismRemake-{}-allOS.zip'.format(version.__version__)
    target_directory = os.path.join(build_directory, target_directory_name)
    target_zip = os.path.join(build_directory, target_zip_name)

    # delete target directory and zip file if still existing
    shutil.rmtree(target_directory, ignore_errors=True)
    if os.path.isfile(target_zip):
        os.remove(target_zip)

    # copy source (copytree can only copy if destination folder is not existing!)
    shutil.copytree(source_directory, target_directory, ignore=shutil.ignore_patterns('__pycache__'))

    # add some more files
    shutil.copyfile(os.path.join(root_directory, 'LICENSE'), os.path.join(target_directory, 'LICENSE'))
    shutil.copyfile(os.path.join(root_directory, 'documentation', 'README-allOS.txt'), os.path.join(target_directory, 'README.txt'))

    # zip the directory
    def zipdir(path, zip):
        for root, dirs, files in os.walk(path):
            for file in files:
                zip.write(os.path.join(root, file))

    zip = zipfile.ZipFile(target_zip, 'w', zipfile.ZIP_DEFLATED)
    zipdir(target_directory, zip)
    zip.close()