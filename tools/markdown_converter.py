# Markdown converter for our help files
# Copyright (C) 2012 Trilarion
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

import os, fnmatch, sys, shutil, codecs
from datetime import datetime

import markdown # https://pypi.python.org/pypi/Markdown
import tools


# parameters
lookup_dir = 'C:/Users/Jan/Dropbox/remake/documentation' # relative to this files location
# all following dirs are relative to the lookup dir
install_dir = lookup_dir + '/help'
template_dir = 'templates'

lookup_files = '*.md'
header_file = 'header.tpl'
style_file = "style.css"

encoding = "utf-8"

# change to lookup directory, everything relative to lookup directory
os.chdir(lookup_dir)

# print welcome message
print 'markdown to html conversion for all txt files in this directory'
print 'and all subdirectories - for usage see comments in the python source'
print 'start: ' + str(datetime.time(datetime.now()))

# clean and recreate install directory
if os.path.isdir(install_dir):
    shutil.rmtree(install_dir)
os.mkdir(install_dir)

# load header
header = template_dir + os.sep + header_file
if os.path.exists(header) and os.path.isfile(header):
    header = tools.read(header)
else:
    header = u''

# copy stylesheet if existing
css = template_dir + os.sep + style_file
if os.path.exists(css) and os.path.isfile(css):
    text = tools.read(css)
    tools.write(install_dir + os.sep + style_file, text, 'ascii')
    # must save as ascii because Jave CSS import in JEditorPane does not read utf-8

# locate all lookup files
print "locating markdown files"
folders, files = tools.locate(lookup_files)
number = len(files)
print "found %d files" %number

# create new Markdown parser object
md = markdown.Markdown(extensions = ['footnotes'], output_format = 'html4')

# loop over files
for k in range(number):
    f = files[k]
    d = folders[k]
    print 'processing: ' + f

    # need to insert the install_dir in the path at first position
    o = install_dir + os.sep + d

    # if a subfolder needs to be created do it
    if not os.path.exists(o):
        os.makedirs(o)

    # construct input and output file paths (output file ending on html, input file having a 3 character extension)
    inf = d + os.sep + f;
    outf = o + os.sep + f.rsplit(".", 1)[0] + '.html'

    # read input file content
    text = tools.read(inf)

    # convert and add header and body tag (\n as newline)
    html = md.convert(text)
    html = header + u'<body>\n' + html + u'\n</body>\n</html>\n'

    # write to output
    tools.write(outf, html)

    # reset state of converter
    md.reset