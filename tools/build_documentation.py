"""
Builds the documentation.

See also sphinx.main(), sphinx.build_main(), cmdline.main()
"""

import os
import shutil
import glob

import sphinx
from sphinx import apidoc

def sphinx_build(directory):
    """

    :param directory:
    :return:
    """

    print('build directory {}'.format(directory))

    # output directory and builder name
    out_directory = os.path.join(directory, '_build')
    builder_name = 'html'

    # delete files of old build
    if os.path.exists(out_directory):
        shutil.rmtree(out_directory)
    environment_file = os.path.join(directory, 'environment.pickle')
    if os.path.exists(environment_file):
        os.remove(environment_file)
    for file_name in glob.glob(os.path.join(directory, '*.doctree')):
        os.remove(file_name)

    # call to sphinx
    sphinx.build_main(argv=['', '-b', builder_name, directory, out_directory])

def sphinx_api_build(source_directory, out_directory):
    """

    :param source_directory:
    :param out_directory:
    :return:
    """

    # delete files of old build
    if os.path.exists(out_directory):
        shutil.rmtree(out_directory)

    apidoc.main(argv=['', '-o', out_directory, source_directory])

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


if __name__ == '__main__':

    # start with directory one down
    os.chdir('..')

    # sphinx api build
    source_directory = 'source'
    api_build_out_directory = os.path.join('documentation', 'development', 'source')
    sphinx_api_build(source_directory, api_build_out_directory)
    
    # build manual
    manual_rst_directory = os.path.join('documentation', 'manual')
    sphinx_build(manual_rst_directory)

    # copy manual to ./data
    manual_data_directory = os.path.join('source', 'imperialism_remake', 'data', 'manual')
    manual_build_directory = os.path.join(manual_rst_directory, '_build')
    copy_manual(manual_build_directory, manual_data_directory)
    
    # build definition
    definition_rst_directory = os.path.join('documentation', 'definition')
    sphinx_build(definition_rst_directory)
    
    # build developer manual
    developer_rst_directory = os.path.join('documentation', 'development')
    sphinx_build(developer_rst_directory)