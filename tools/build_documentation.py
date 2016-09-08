import os
from sphinx.application import Sphinx

# base_directory = os.path.join('..', 'documentation', 'development')
# base_directory = os.path.join('..', 'documentation', 'manual')
base_directory = os.path.join('..', 'documentation', 'definition')

srcdir = base_directory
confdir = base_directory
doctreedir = base_directory
outdir = os.path.join(base_directory, '_build')
buildername = 'html'

app = Sphinx(srcdir, confdir, outdir, doctreedir, buildername)
app.build()

# see sphinx.main(), sphinx.build_main(), cmdline.main()