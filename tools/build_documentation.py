#!/usr/bin/env python3
#
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
Builds the documentation.

See also sphinx.main(), sphinx.build_main(), cmdline.main()
"""

import os
import shutil
import glob

from sphinx.cmd.build import build_main
from sphinx.ext import apidoc


def sphinx_build(rst_directory):
    """
    Builds a sphinx project as html and latex.

    :param rst_directory:
    :return:
    """

    print('project directory {}'.format(rst_directory))

    # output directory and builder name
    build_directory = os.path.join(rst_directory, '_build')

    # delete files of old build
    if os.path.exists(build_directory):
        shutil.rmtree(build_directory)

    environment_file = os.path.join(rst_directory, 'environment.pickle')
    if os.path.exists(environment_file):
        os.remove(environment_file)

    for file_name in glob.glob(os.path.join(rst_directory, '*.doctree')):
        os.remove(file_name)

    # call to sphinx
    for builder_name in ('html', 'latex'):
        build_main(argv=['-b', builder_name, rst_directory, os.path.join(build_directory, builder_name)])

def sphinx_api_build(source_directory, out_directory):
    """

    :param source_directory:
    :param out_directory:
    :return:
    """

    # delete files of old build
    if os.path.exists(out_directory):
        shutil.rmtree(out_directory)

    apidoc.main(argv=['-o', out_directory, source_directory])

def copy_manual(source, target):
    """

    :param source:
    :param target:
    :return:
    """

    # delete target if existing
    if os.path.exists(target):
        shutil.rmtree(target)

    # copy manual
    shutil.copytree(source, target, ignore=shutil.ignore_patterns('.*'))

def build_documentation():
    """
    Builds all three documentation projects and copies the player manual to the sources/../data folder.
    """

    # get start directories
    tools_directory = os.path.abspath(os.path.dirname(__file__))
    source_directory = os.path.join(tools_directory, os.path.pardir, 'source')
    documentation_directory = os.path.join(tools_directory, os.path.pardir, 'documentation')

    # sphinx api build (python to rst)
    api_build_directory = os.path.join(documentation_directory, 'development', 'source')
    sphinx_api_build(source_directory, api_build_directory)

    # build manual (rst to html, latex)
    manual_rst_directory = os.path.join(documentation_directory, 'manual')
    sphinx_build(manual_rst_directory)

    # copy html manual to source/imperialism_remake/data/manual
    manual_data_directory = os.path.join(source_directory, 'imperialism_remake', 'data', 'manual')
    manual_build_directory = os.path.join(manual_rst_directory, '_build', 'html')
    copy_manual(manual_build_directory, manual_data_directory)

    # build definition
    definition_rst_directory = os.path.join(documentation_directory, 'definition')
    sphinx_build(definition_rst_directory)

    # build developer manual
    developer_rst_directory = os.path.join(documentation_directory, 'development')
    sphinx_build(developer_rst_directory)


if __name__ == '__main__':

    build_documentation()
