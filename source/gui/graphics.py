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

class ExtendedGraphicsPixmapItem(QtGui.QGraphicsPixmapItem, QtCore.QObject):

    entered = QtCore.Signal()
    left = QtCore.Signal()
    clicked = QtCore.Signal()

    def __init__(self, pixmap):
        QtGui.QGraphicsPixmapItem.__init__(self, pixmap)
        QtCore.QObject.__init__(self)
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(QtCore.Qt.LeftButton)

    def hoverEnterEvent(self, event):
        self.entered.emit()

    def hoverLeaveEvent(self, event):
        self.left.emit()

    def mousePressEvent(self, event):
        self.clicked.emit()

Notification_Default_Style = 'border: 1px solid black; padding: 5px 10px 5px 10px; background-color: rgba(128, 128, 128, 128); color: white;'

def show_notification(parent, text, style=Notification_Default_Style, fade_duration=2000, stay_duration=2000, positioner=None, callback=None):
    """
        border_style example: "border: 1px solid black"
        Please only use a color that is fully opaque (alpha = 255) for bg_color, otherwise a black background will appear.
    """
    # create a clickable widget as standalone window and without a frame
    widget = ClickableWidget(parent, QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
    # connect the click event with closing of the widget and optional the callback action
    widget.clicked.connect(widget.close)
    if callback:
        widget.clicked.connect(callback)

    # widget must be translucent, otherwise when setting semi-transparent background colors
    widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    # create a label and set the text
    label = QtGui.QLabel(widget)
    label.setText(text)

    # set style (border, padding, background color, text color
    label.setStyleSheet(style)

    # we need to manually tell the widget that it should be exactly as big as the label it contains
    widget.resize(label.sizeHint())

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

    # if given, position
    if parent and positioner:
        position = positioner.calculate(parent.size(), widget.size())
        widget.move(position)

    # to avoid short blinking show transparent and start animation
    widget.setWindowOpacity(0)
    widget.show()
    widget.fade_in.start()

class Relative_Positioner():

    def __init__(self, ax = 0.5, bx = -0.5, cx = 0, ay = 0.5, by = -0.5, cy = 0):
        self.ax = ax
        self.bx = bx
        self.cx = cx
        self.ay = ay
        self.by = by
        self.cy = cy

    def calculate(self, parent_size, own_size):
        x = self.ax * parent_size.width() + self.bx * own_size.width() + self.cx
        y = self.ay * parent_size.height() + self.by * own_size.height() + self.cy
        return QtCore.QPoint(x, y)

def create_positioner_northwest(gap_x = 0, gap_y = 0):
    """
        Convenience method.
    """
    return Relative_Positioner(1, -1, -gap_x, 0, 0, gap_y)

def create_positioner_northeast(gap_x = 0, gap_y = 0):
    """
        Convenience method.
    """
    return Relative_Positioner(1, -1, -gap_x, 0, 0, gap_y)

def create_positioner_southwest(gap_x = 0, gap_y = 0):
    """
        Convenience method.
    """
    return Relative_Positioner(1, -1, -gap_x, 0, 0, gap_y)

def create_positioner_southeast(gap_x = 0, gap_y = 0):
    """
        Convenience method.
    """
    return Relative_Positioner(1, -1, -gap_x, 0, 0, gap_y)

class FadeAnimation():

    def __init__(self, graphics_item, duration):

        # create opacity effect
        self.effect = QtGui.QGraphicsOpacityEffect()
        self.effect.setOpacity(0)
        graphics_item.setGraphicsEffect(self.effect)

        # create animation
        self.animation = QtCore.QPropertyAnimation(self.effect, 'opacity')
        self.animation.setDuration(duration)  # in ms
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)

    def fade_in(self):
        self.animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self.animation.start()

    def fade_out(self):
        self.animation.setDirection(QtCore.QAbstractAnimation.Backward)
        self.animation.start()