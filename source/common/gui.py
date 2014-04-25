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

from PySide import QtCore, QtGui

class ClickableWidget(QtGui.QWidget):
    """

    """

    clicked = QtCore.Signal(QtGui.QMouseEvent)

    def __init__(self, *args, **kwargs):
        """

        """
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        """

        """
        self.clicked.emit(event)

def show_notification(parent, bg_color, text, fade_duration, stay_duration, callback=None):
    """
        Please only use a color that is fully opaque (alpha = 255) for bg_color, otherwise a black background will appear.
    """
    # create a clickable widget as standalone window and without a frame
    widget = ClickableWidget(parent, QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
    # connect the click event with closing of the widget and optional the callback action
    widget.clicked.connect(widget.close)
    if callback:
        widget.clicked.connect(callback)

    # if a background color is given, set it, otherwise set a translucent background
    if bg_color:
        palette = widget.palette()
        palette.setColor(widget.backgroundRole(), bg_color)
        widget.setPalette(palette)
    else:
        widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    # create a label and set the text
    label = QtGui.QLabel()
    label.setText(text)

    # any layout will do, just add the label
    layout = QtGui.QHBoxLayout()
    layout.addWidget(label)
    widget.setLayout(layout)

    # fade in animation
    widget.fade_in = QtCore.QPropertyAnimation(widget, 'windowOpacity')
    widget.fade_in.setDuration(fade_duration)
    widget.fade_in.setStartValue(0)
    widget.fade_in.setEndValue(1)

    # fading out and waiting for fading out makes only sense if a positive stay_duration has been given
    if stay_duration:

        # fade out animation
        widget.fade_out = QtCore.QPropertyAnimation(widget, 'windowOpacity')
        widget.fade_out.setDuration(fade_duration)
        widget.fade_out.setStartValue(1)
        widget.fade_out.setEndValue(0)
        widget.fade_out.finished.connect(widget.close)

        # timer for fading out animation
        widget.timer = QtCore.QTimer()
        widget.timer.setSingleShot(True)
        widget.timer.setInterval(stay_duration)
        widget.timer.timeout.connect(widget.fade_out.start)

        # start the timer as soon as the fading in animation has finished
        widget.fade_in.finished.connect(widget.timer.start)

    # to avoid short blinking show transparent and start animation
    widget.setWindowOpacity(0)
    widget.show()
    widget.fade_in.start()

    # widget.sizeHint()
