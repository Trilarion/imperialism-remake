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

"""
    Converts the help files written in Markdown syntax to html using the markdown
    converter.
"""

import os, shutil
import markdown  # https://pypi.python.org/pypi/Markdown

def convert():
    """

    """

    # set input and output directory
    lookup_dir = os.path.join('resources', 'manual')
    install_dir = os.path.join('data', 'manual')

    # clean and re-create install directory
    if os.path.isdir(install_dir):
        shutil.rmtree(install_dir)
    os.mkdir(install_dir)

    # load header
    header_file = os.path.join(lookup_dir, 'header.tpl')
    with open(header_file, 'rt') as file:
        header = file.read()

    # load footer
    footer_file = os.path.join(lookup_dir, 'footer.tpl')
    with open(footer_file, 'rt') as file:
        footer = file.read()

    # copy style files
    shutil.copytree(os.path.join(lookup_dir, 'css'), os.path.join(install_dir, 'css'))

    # search for all markdown files
    md_files = [x for x in os.listdir(lookup_dir) if x.endswith('.md') and not x.startswith('README')]
    print('convert {} files'.format(len(md_files)))

    # create new Markdown parser
    md = markdown.Markdown(extensions=['footnotes'], output_format='html4')

    # loop over files
    for md_file in md_files:
        print('processing {}'.format(md_file))

        # read it
        with open(os.path.join(lookup_dir, md_file), 'rt') as file:
            text = file.read()

        # convert and add header and body tag (\n as newline)
        body = md.convert(text)
        html = header + body + footer

        # output file name is with html extension instead of md
        out_file = os.path.join(install_dir, md_file.rsplit(".", 1)[0] + '.html')

        # write to output
        with open(out_file, 'wt') as file:
            file.write(html)

        # reset state of converter
        md.reset()

if __name__ == '__main__':
    # change to project root
    os.chdir('..')
    convert()