"""
    see also sphinx.main(), sphinx.build_main(), cmdline.main()
"""
import os
import shutil
import glob

from sphinx.application import Sphinx

from sphinx import apidoc

def sphinx_build(directory):

    print('build directory {}'.format(directory))

    srcdir = directory
    confdir = directory
    doctreedir = directory
    outdir = os.path.join(directory, '_build')
    buildername = 'html'

    # delete files of old build
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    environment_file = os.path.join(directory, 'environment.pickle')
    if os.path.exists(environment_file):
        os.remove(environment_file)
    for file_name in glob.glob(os.path.join(directory, '*.doctree')):
        os.remove(file_name)
    
    app = Sphinx(srcdir, confdir, outdir, doctreedir, buildername)
    app.build()

if __name__ == '__main__':

    #source_directory = os.path.join('..', 'source')
    #out_directory = os.path.join('..', 'documentation', 'development', 'source')
    #apidoc.main(argv=['', '-o', out_directory, source_directory])
    
    # build manual
    directory = os.path.join('..', 'documentation', 'manual')
    #sphinx_build(directory)
    
    # build definition
    directory = os.path.join('..', 'documentation', 'definition')
    #sphinx_build(directory)
    
    # build developer manual
    directory = os.path.join('..', 'documentation', 'development')
    sphinx_build(directory)