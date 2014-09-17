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

from datetime import datetime
from PySide import QtCore, QtGui

"""
    Graphics (Qt) based objects and algorithms that do not depend specifically on the project but only on Qt.

    Abstraction of the used elements in the project to achieve an intermediate layer and to minimize dependencies.
"""


class RelativeLayoutConstraint():
    """
        Defines a relative position. The position depends on our own size, the parent rectangle and a constant offset.
    """

    def __init__(self, x=(0, 0, 0), y=(0, 0, 0)):
        """
            Initialize so that the new object would be placed with the left-top corner exactly at the left-top-corner
            of the parent, regardless of parent frame or own size.
        """
        self.x = x
        self.y = y

    def south(self, gap):
        """
            Aligns south (at the lower border) of the parent frame. A gap is a positive distance between the element
            and the lower border of the parent. Only affects the y axis. Returns itself for chained calls.
        """
        self.y = (1, -1, -gap)
        return self

    def north(self, gap):
        """
            Same as south, only towards the north (upper border).
        """
        self.y = (0, 0, gap)
        return self

    def west(self, gap):
        """
            Aligns west (to the left border) of the parent frame.
        """
        self.x = (0, 0, gap)
        return self

    def east(self, gap):
        """
            Same as west, only to the east (right border) of the parent frame.
        """
        self.x = (1, -1, -gap)
        return self

    def centerH(self):
        """
            Centers the object horizontally, eg. the left upper corner of the element will be at the center of the
            parent frame horizontally and half the element size to the left, so the center of the element will exactly
            be at the center of the parent frame. Does not influence the vertical position.
        """
        self.x = (0.5, -0.5, 0)
        return self

    def centerV(self):
        """
            Same as center horizontally (centerH) but in the vertical directiokn.
        """
        self.y = (0.5, -0.5, 0)
        return self


def calculate_relative_position(parent_rect, own_size, constraint):
    """
        Returns the left, upper corner of an object if the parent_rectangle is given and our own size and a relative
        position constraint.
    """
    x = parent_rect.x() + constraint.x[0] * parent_rect.width() + constraint.x[1] * own_size.width() + constraint.x[2]
    y = parent_rect.y() + constraint.y[0] * parent_rect.height() + constraint.y[1] * own_size.height() + constraint.y[2]
    return x, y


class Notification(QtCore.QObject):
    """
        Holding a small widget (notification), the fading animations and a position specifier together.

        Also has signals, currently only when finished. Connect to if you want to be notified of the ending.
        TODO add signal clicked to listen for clicks
    """
    finished = QtCore.Signal()

    def __init__(self, parent, content, fade_duration=2000, stay_duration=2000, position_constraint=None):
        """
            parent - parent widget (QWidget)
            content - either a widget or a string (is then placed into a QLabel widget)
                style it with stylesheet and modifier 'notification'
            fade_duration - duration of fade in/out in ms
            stay_duration - duration of stay in ms (if 0 stays forever)
            position_constraint - a RelativeLayoutConstraint to be used with method calculate_relative_position()
        """
        super().__init__()

        # create a clickable widget as standalone window and without a frame
        self.widget = QtGui.QWidget(parent, QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)

        # widget must be translucent, otherwise when setting semi-transparent background colors
        self.widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # replace content by QLabel if content is a string
        if isinstance(content, str):
            content = QtGui.QLabel(content)
            content.setObjectName('notification')

        # set background
        layout = QtGui.QVBoxLayout(self.widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(content)

        # fade animation
        self.fade = FadeAnimation(self.widget)
        self.fade.set_duration(fade_duration)

        # fading out and waiting for fading out makes only sense if a positive stay_duration has been given
        if stay_duration > 0:
            # when fade out has finished, emit finished
            self.fade.fadeout_finished.connect(self.finished.emit)

            # timer for fading out animation
            self.timer = QtCore.QTimer()
            self.timer.setSingleShot(True)
            self.timer.setInterval(stay_duration)
            self.timer.timeout.connect(self.fade.fadeout)

            # start the timer as soon as the fading in animation has finished
            self.fade.fadein_finished.connect(self.timer.start)

        # if given, set a position
        if parent is not None and position_constraint is not None:
            x, y = calculate_relative_position(parent.geometry(), content.sizeHint(), position_constraint)
            self.widget.move(QtCore.QPoint(x, y))

    def show(self):
        """
            show and start fade in
        """
        self.widget.show()
        self.fade.fadein()


class RelativeLayout(QtGui.QLayout):
    """
        An implementation of QLayout working with RelativeLayoutConstraints so the position can be estimated by
        method calculate_relative_position()
    """

    def __init__(self, *args):
        """
            No margins in this layout.
        """
        super().__init__(*args)
        self.setContentsMargins(0, 0, 0, 0)
        self.items = []

    def addItem(self, item):
        """
            Only add items that have a layout_constraint attribute.
        """
        if item.widget() is None or not hasattr(item.widget(), 'layout_constraint'):
            raise RuntimeError('Only add widgets (with attribute position_constraint).')
        self.items.append(item)

    def sizeHint(self):
        """
            In most cases the size is set externally, but we prefer at least the minimum size
        """
        return self.minimumSize()

    def setGeometry(self, rect):
        """
            Layout the elements by calculating their relative position.
        """
        for item in self.items:
            o_size = item.sizeHint()

            c = item.widget().layout_constraint

            x, y = calculate_relative_position(rect, o_size, c)

            item.setGeometry(QtCore.QRect(x, y, o_size.width(), o_size.height()))

    def itemAt(self, index):
        """
            Return an item (must be implemented)
        """
        if index < len(self.items):
            return self.items[index]
        else:
            return None

    def takeAt(self, index):
        """
            Pop an item (must be implemented)
        """
        return self.items.pop(index)

    def minimumSize(self):
        """
            Minimum size is the size so that every child is displayed in full with the offsets (see RelativeLayoutConstraint)
            however they could overlap.
        """
        min_width = 0
        min_height = 0

        for item in self.items:
            o_size = item.sizeHint()

            c = item.widget().layout_constraint
            gap_x = abs(c.x[2])
            gap_y = abs(c.y[2])

            min_width = max(min_width, o_size.width() + gap_x)
            min_height = max(min_height, o_size.height() + gap_y)

        return QtCore.QSize(min_width, min_height)


# TODO make this more flexible to work with widget and graphicsitem as well as override duration
class FadeAnimation(QtCore.QObject):
    """
        Fade animation on a QtGui.QGraphicsItem. As usual a reference to an instance must be stored.
    """

    fadein_finished = QtCore.Signal()
    fadeout_finished = QtCore.Signal()

    def __init__(self, parent):
        """
            Create property animations, sets the opacity to zero initially.
        """
        super().__init__()
        if isinstance(parent, QtGui.QGraphicsItem):
            # create opacity effect
            self.effect = QtGui.QGraphicsOpacityEffect()
            self.effect.setOpacity(0)
            parent.setGraphicsEffect(self.effect)
            self.fade = QtCore.QPropertyAnimation(self.effect, 'opacity')
        elif isinstance(parent, QtGui.QWidget):
            parent.setWindowOpacity(0)
            self.fade = QtCore.QPropertyAnimation(parent, 'windowOpacity')
        else:
            raise RuntimeError('Type of parameter must be QtGui.QGraphicsItem or QtGui.QWidget.')

        # set start and stop value
        self.fade.setStartValue(0)
        self.fade.setEndValue(1)
        self.fade.finished.connect(self.finished)

        self.forward = True

    def set_duration(self, duration):
        """
            Sets the duration in ms.
        """
        self.fade.setDuration(duration)

    def fadein(self):
        """
            Starts a fade in.
        """
        self.fade.setDirection(QtCore.QAbstractAnimation.Forward)
        self.forward = True
        self.fade.start()

    def fadeout(self):
        """
            Starts a fade out.
        """
        self.fade.setDirection(QtCore.QAbstractAnimation.Backward)
        self.forward = False
        self.fade.start()

    def finished(self):
        """
            Depending on the direction emit the appropriate signal.
        """
        if self.forward is True:
            self.fadein_finished.emit()
        else:
            self.fadeout_finished.emit()


class GraphicsItemSet():
    """
        A set of QGraphicsItem elements.
        Some collective actions are possible like setting a Z-value to each of them.
    """

    def __init__(self):
        self._content = set()

    def add_item(self, item):
        """
            Adds an item to the content list. Should be
            item -- QtGui.QGraphicsItem
        """
        if not isinstance(item, QtGui.QGraphicsItem):
            raise RuntimeError('Expected instance of QGraphicsItem!')
        self._content.add(item)

    def set_zvalue(self, level):
        """
            Sets the z value of all items in the set.
        """
        for item in self._content:
            item.setZValue(level)


class ZStackingManager():
    """
        Puts several QtGui.QGraphicsItem into different sets (floors) and in the end sets their z-value so that lower
        floors have lower z-value.
    """

    def __init__(self):
        """
            Start with empty list of floors.
        """
        self._floors = []

    def new_floor(self, floor=None, above=True):
        """
            Creates a new floor (set of items) and exposes it. Inserts the new floor either at the top (above is True)
            or at the bottom (above is False) or above or below a given floor.

            floor - GraphicsItemSet
        """

        # if a floor is given, it should exist
        if floor and floor not in self._floors:
            raise RuntimeError('Specified floor unknown!')
        if floor:
            # insert above or below the given floor
            insert_position = self._floors.index(floor) + (1 if above else 0)
        else:
            # insert at the end or the beginning of the floors
            insert_position = len(self._floors) if above else 0
        # create new floor, insert in list and return it
        new_floor = GraphicsItemSet()
        self._floors.insert(insert_position, new_floor)
        return new_floor

    def stack(self):
        """
            Set all items in the i-th floor to i (starting at 0).
        """
        for z in range(0, len(self._floors)):
            self._floors[z].set_zvalue(z)


class ZoomableGraphicsView(QtGui.QGraphicsView):
    """
        QtGui.QGraphicsView where you can zoom around the current mouse position with the mouse wheel.
    """
    ScaleFactor = 1.15
    MinScaling = 0.5
    MaxScaling = 2

    def __init__(self, *args, **kwargs):
        """
            Set the transformation anchor to below the current mouse position.
        """
        super().__init__(*args, **kwargs)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.standard_scale = 1

    def wheelEvent(self, event):
        """
            Upon a wheel event, change the zoom.
        """
        current_scale = self.transform().m11()  # horizontal scaling factor = vertical scaling factor
        if event.delta() > 0:
            # we are zooming in
            f = ZoomableGraphicsView.ScaleFactor
            if current_scale * f > ZoomableGraphicsView.MaxScaling * self.standard_scale:
                return
        else:
            # we are zooming out
            f = 1 / ZoomableGraphicsView.ScaleFactor
            if current_scale * f < ZoomableGraphicsView.MinScaling * self.standard_scale:
                return
        # scale
        self.scale(f, f)

        super().wheelEvent(event)


def makeWidgetClickable(parent):
    """
        Takes any QtGui.QWidget derived class and emits a signal emitting on mousePressEvent.
    """

    class ClickableWidgetSubclass(parent):
        clicked = QtCore.Signal(QtGui.QMouseEvent)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def mousePressEvent(self, event):
            super().mousePressEvent(event)
            self.clicked.emit(event)

    return ClickableWidgetSubclass


def makeDraggableWidget(parent):
    """
        Takes any QtGui.QWidget derived class and emits a signal on mouseMoveEvent emitting the position change since
        the last mousePressEvent. By default mouseMoveEvents are only invoked while the mouse is pressed. Therefore
        we can use it to listen to dragging or implement dragging.
    """

    class DraggableWidgetSubclass(parent):
        dragged = QtCore.Signal(QtCore.QPoint)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


        def mousePressEvent(self, event):
            self.position_on_click = event.globalPos()
            super().mousePressEvent(event)

        def mouseMoveEvent(self, event):
            super().mouseMoveEvent(event)
            position_now = event.globalPos()
            self.dragged.emit(position_now - self.position_on_click)
            self.position_on_click = position_now

    return DraggableWidgetSubclass


def makeClickableGraphicsItem(parent):
    """
        Takes a QtGui.QGraphicsItem and adds signals for entering, leaving and clicking on the item. For this the item
        must have setAcceptHoverEvents and it must also inherit from QObject to have signals. Only use it when really
        needed because there is some performance hit attached.
    """

    class ClickableGraphicsItem(parent, QtCore.QObject):
        entered = QtCore.Signal(QtGui.QGraphicsSceneHoverEvent)
        left = QtCore.Signal(QtGui.QGraphicsSceneHoverEvent)
        clicked = QtCore.Signal(QtGui.QGraphicsSceneMouseEvent)

        def __init__(self, *args, **kwargs):
            parent.__init__(self, *args, **kwargs)
            QtCore.QObject.__init__(self)
            self.parent = parent
            self.setAcceptHoverEvents(True)
            self.setAcceptedMouseButtons(QtCore.Qt.LeftButton)

        def hoverEnterEvent(self, event):
            self.entered.emit(event)
            self.parent.hoverEnterEvent(self, event)

        def hoverLeaveEvent(self, event):
            self.left.emit(event)
            self.parent.hoverLeaveEvent(self, event)

        def mousePressEvent(self, event):
            self.clicked.emit(event)
            self.parent.mousePressEvent(self, event)

    return ClickableGraphicsItem

def makeDraggableGraphicsItem(parent):
    """

    """

    class DraggableGraphicsRectItem(parent, QtCore.QObject):

        changed = QtCore.Signal(object)

        def __init__(self, *args, **kwargs):
            parent.__init__(self, *args, **kwargs)
            self.parent = parent
            QtCore.QObject.__init__(self)

            self.setFlags(QtGui.QGraphicsItem.ItemIsMovable | QtGui.QGraphicsItem.ItemSendsScenePositionChanges)

        def itemChange(self, change, value):
            if change == QtGui.QGraphicsItem.ItemPositionChange:
                self.changed.emit(value)

            return parent.itemChange(self, change, value)

    return DraggableGraphicsRectItem

# Some classes we need (just to make the naming clear), Name will be used in Stylesheet selectors
DraggableToolBar = makeDraggableWidget(QtGui.QToolBar)
ClickableWidget = makeWidgetClickable(QtGui.QWidget)
ClickablePixmapItem = makeClickableGraphicsItem(QtGui.QGraphicsPixmapItem)
DraggableRectItem = makeDraggableGraphicsItem(QtGui.QGraphicsRectItem)

class ClockLabel(QtGui.QLabel):
    """
        Just a clock label that shows hour : minute and updates itself every minute for as long as it lives.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.setInterval(60000)
        self.timer.start()
        self.update_clock()

    def update_clock(self):
        text = datetime.now().strftime('%H:%M')
        self.setText(text)

# some constant expressions
TRANSPARENT_PEN = QtGui.QPen(QtCore.Qt.transparent)