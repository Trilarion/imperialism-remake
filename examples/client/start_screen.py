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
Extraction of the start screen only from the client.
"""

import os
import sys

from PyQt5 import QtWidgets, QtCore

if __name__ == '__main__':

    # add source directory to path if needed
    source_directory = os.path.realpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir, os.path.pardir, 'source'))
    if source_directory not in sys.path:
        sys.path.insert(0, source_directory)

    # imperialism remake imports
    from imperialism_remake.lib import qt
    from imperialism_remake.base import tools, constants
    from imperialism_remake.client import client

    qt.fix_pyqt5_exception_eating()

    # get user folder
    user_folder = constants.get_user_directory()

    # read options
    options_file = os.path.join(user_folder, 'options.info')
    if not os.path.exists(options_file):
        raise RuntimeError('Preferences file does not exist:')
    tools.load_options(options_file)

    app = QtWidgets.QApplication([])

    # test for desktop availability
    desktop = app.desktop()
    rect = desktop.screenGeometry()
    print('desktop geometry', rect, 'minimal required screen size', constants.MINIMAL_SCREEN_SIZE)

    # load global stylesheet to app
    with open(constants.GLOBAL_STYLESHEET_FILE, encoding='utf-8') as file:
        style_sheet = file.read()
    app.setStyleSheet(style_sheet)

    # set icon
    app.setWindowIcon(tools.load_ui_icon('window.icon.ico'))

    # main window
    main_window = QtWidgets.QWidget()
    # set geometry
    main_window.setGeometry(tools.get_option(constants.Option.MAINWINDOW_BOUNDS))
    # set title
    main_window.setWindowTitle('Imperialism Remake')
    # show in full screen, maximized or normal
    if tools.get_option(constants.Option.MAINWINDOW_FULLSCREEN):
        main_window.setWindowFlags(main_window.windowFlags() | QtCore.Qt.FramelessWindowHint)
        main_window.showFullScreen()
    elif tools.get_option(constants.Option.MAINWINDOW_MAXIMIZED):
        main_window.showMaximized()
    else:
        main_window.show()

    # widget switcher
    widget_switcher = qt.WidgetSwitcher(main_window)

    do_nothing = lambda *args: None
    actions = {'exit': main_window.close,
               'help': do_nothing,
               'lobby': do_nothing,
               'editor': do_nothing,
               'options': do_nothing}
    widget = client.create_start_screen_widget(actions)
    widget_switcher.switch(widget)

    app.exec_()