"""
    see also sphinx.main(), sphinx.build_main(), cmdline.main()
"""
import os
import shutil
import glob

import sphinx
from sphinx import apidoc

def sphinx_build(directory):

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

    # delete files of old build
    if os.path.exists(out_directory):
        shutil.rmtree(out_directory)

    apidoc.main(argv=['', '-o', out_directory, source_directory])


if __name__ == '__main__':

    os.chdir('..')

    source_directory = os.path.join('source')
    out_directory = os.path.join('documentation', 'development', 'source')
    sphinx_api_build(source_directory, out_directory)
    
    # build manual
    directory = os.path.join('documentation', 'manual')
    outdir = os.path.join(directory, '_build')
    #sphinx_build(directory)

    # copy manual to ./data
    
    # build definition
    directory = os.path.join('documentation', 'definition')
    #sphinx_build(directory)
    
    # build developer manual
    directory = os.path.join('documentation', 'development')
    sphinx_build(directory)