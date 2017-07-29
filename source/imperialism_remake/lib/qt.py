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
Graphics (PyQt5) based objects and algorithms that do not depend specifically on the project but only on PyQt5.

Abstraction of the used elements in the project to achieve an intermediate layer and to minimize dependencies.
"""

from datetime import datetime
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

# some constant expressions

#: transparent pen
TRANSPARENT_PEN = QtGui.QPen(QtCore.Qt.transparent)


def exception_hook(type, value, traceback):
    """
    Use sys.__excepthook__, the standard hook.
    """
    sys.__excepthook__(type, value, traceback)


def fix_pyqt5_exception_eating():
    """
    PyQt5 by default eats exceptions (see http://stackoverflow.com/q/14493081/1536976)
    """
    sys.excepthook = exception_hook


class RelativeLayoutConstraint:
    """
    Defines a relative position. The position depends on our own size, the parent rectangle and a constant offset.
    """

    def __init__(self, x=(0, 0, 0), y=(0, 0, 0)):
        """
        Initialize so that the new object would be placed with the left-top corner exactly at the left-top-corner
        of the parent, regardless of parent frame or own size.

        See also calculate_relative_position()

        :param x: list of three factors (scaling of parents width, scaling of element width, horizontal offset)
        :param y: list of three factors (scaling of parents height, scaling of elements height, vertical offset)
        """
        self.x = x
        self.y = y

    def south(self, gap):
        """
        Aligns south (at the lower border) of the parent frame. Only affects the y position.

        :param gap: Distance between the bottom of the element and the bottom of the parent. Can be negative.
        :return: Returns itself for chained calls.
        """
        """

        """
        self.y = (1, -1, -gap)
        return self

    def north(self, gap):
        """
        Same as south, only towards the north (upper border). Only affects the y position.

        :param gap: Distance between the top of the element and the top of the parent. Can be negative.
        :return: Returns itself for chained calls.
        """
        self.y = (0, 0, gap)
        return self

    def west(self, gap):
        """
        Aligns west (to the left border) of the parent frame. Only affects the x position.

        :param gap: Distance between left edge of the element and left edge of the parent. Can be negative.
        :return: Returns itself for chained calls.
        """
        self.x = (0, 0, gap)
        return self

    def east(self, gap):
        """
        Same as west, only to the east (right border) of the parent frame. Only affects the x position.

        :param gap: Distance between right edge of the element and right edge of the parent. Can be negative.
        :return: Returns itself for chained calls.
        """
        """

        """
        self.x = (1, -1, -gap)
        return self

    def center_horizontal(self):
        """
        Centers the object horizontally, eg. the left upper corner of the element will be at the center of the
        parent frame horizontally and half the element size to the left, so the center of the element will exactly
        be at the center of the parent frame. Does not influence the vertical position.
        """
        self.x = (0.5, -0.5, 0)
        return self

    def center_vertical(self):
        """
        Same as center horizontally (centerH) but in the vertical direction.
        """
        self.y = (0.5, -0.5, 0)
        return self


def calculate_relative_position(parent_rect: QtCore.QRect, own_size: QtCore.QSize,
                                constraint: RelativeLayoutConstraint):
    """
    Calculates the position of the element, given its size, the position and size of the parent and a relative layout
    constraint. The position is the position of the parent plus the weighted size of the parent, the weighted size of
    the element and an offset. The weights and the offset are given by the constraint for each direction.

    :param parent_rect: parent coordinates and size as rectangle
    :param own_size: size of the element (width and height)
    :param constraint: relative layout constraint to apply
    :return: tuple of recommended x and y positions of the element
    """
    """
        Returns the left, upper corner of an object if the parent rectangle (QRect) is given and our own size (QSize)
        and a relative layout constraint (see RelativeLayoutConstraint).
    """
    x = (parent_rect.x()
         + constraint.x[0] * parent_rect.width()
         + constraint.x[1] * own_size.width()
         + constraint.x[2])
    y = (parent_rect.y()
         + constraint.y[0] * parent_rect.height()
         + constraint.y[1] * own_size.height()
         + constraint.y[2])
    return x, y


class RelativeLayout(QtWidgets.QLayout):
    """
        An implementation of QLayout working with RelativeLayoutConstraints so the position can be estimated by
        method calculate_relative_position()

        Note: No margins in this layout. The elements must have been set to their target size.
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.setContentsMargins(0, 0, 0, 0)
        self.items = []

    def addItem(self, item: QtWidgets.QLayoutItem):  # noqa: N802
        """
        Only add items that have a layout_constraint attribute.

        :param item: Item to be added, must have an attribute with name layout_constraint
        """

        if item.widget() is None or not hasattr(item.widget(), 'layout_constraint'):
            raise RuntimeError('Only add widgets (with attribute position_constraint).')
        self.items.append(item)

    def sizeHint(self):  # noqa: N802
        """
        In most cases the size is set externally, but we prefer at least the minimum size.
        """
        return self.minimumSize()

    def setGeometry(self, rect: QtCore.QRect):  # noqa: N802
        """
        Layout the elements by calculating their relative position inside the parent, given the parents coordinates
        and the sizes of the elements. The width and height are not changed but the offset is computed according to
        the layout constraint and the parent size.

        :param rect: Position and size of the parent.
        """
        for item in self.items:
            o_size = item.widget().size()

            c = item.widget().layout_constraint

            x, y = calculate_relative_position(rect, o_size, c)

            item.setGeometry(QtCore.QRect(x, y, o_size.width(), o_size.height()))

    def itemAt(self, index):  # noqa: N802
        """
        Returns an item (must be implemented).

        :param index: Index of the item to be returned.
        :return: Item to be returned.
        """
        if index < len(self.items):
            return self.items[index]
        else:
            return None

    def takeAt(self, index):  # noqa: N802
        """
        Pops an item (must be implemented).

        :param index: Index of the item to be returned.
        :return: Item to be returned.
        """
        return self.items.pop(index)

    def minimumSize(self):  # noqa: N802
        """
        Minimum size is the size so that every child is displayed in full with the offsets
        (see RelativeLayoutConstraint) however they could overlap.
        """
        min_width = 0
        min_height = 0

        for item in self.items:
            o_size = item.widget().size()

            c = item.widget().layout_constraint
            gap_x = abs(c.x[2])
            gap_y = abs(c.y[2])

            min_width = max(min_width, o_size.width() + gap_x)
            min_height = max(min_height, o_size.height() + gap_y)

        return QtCore.QSize(min_width, min_height)


class Notification(QtCore.QObject):
    """
    Holding a small widget (notification), the fading animations and a position specifier together.

    Also has signals, currently only when finished. Connect to if you want to be notified of the ending.
    """

    #: signal, emits when the notification has finished displaying
    finished = QtCore.pyqtSignal()
    #: signal, emits when the notification has been clicked
    clicked = QtCore.pyqtSignal(QtGui.QMouseEvent)

    def __init__(self, parent: QtWidgets.QWidget, content, fade_duration=2000, stay_duration=2000,
                 position_constraint: RelativeLayoutConstraint = None):
        """

        :param parent: parent widget (QWidget)
        :param content: either a widget or a string (is then placed into a QLabel widget) style it with stylesheet
        and modifier 'notification'
        :param fade_duration: duration of fade in/out in ms
        :param stay_duration: duration of stay in ms (if 0 stays forever)
        :param position_constraint: a RelativeLayoutConstraint to be used with method calculate_relative_position()
        """
        super().__init__()

        # create a clickable widget as standalone window and without a frame
        self.widget = ClickableWidget(parent, QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)

        # widget must be translucent, otherwise when setting semi-transparent background colors
        self.widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # connect widget clicked signal to our clicked signal
        self.widget.clicked.connect(self.clicked.emit)

        # replace content by QLabel if content is a string
        if isinstance(content, str):
            content = QtWidgets.QLabel(content)
            content.setObjectName('notification-label')

        # set background
        layout = QtWidgets.QVBoxLayout(self.widget)
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
        Show and start fade in
        """
        self.widget.show()
        self.fade.fadein()


class FadeAnimation(QtCore.QObject):
    """
    Fade animation on a QtWidgets.QGraphicsItem. As usual a reference to an instance must be stored.
    """

    #: signal, fade in is finished
    fadein_finished = QtCore.pyqtSignal()
    #: signal, fade out is finished
    fadeout_finished = QtCore.pyqtSignal()

    def __init__(self, parent):
        """
        Create property animations, sets the opacity to zero initially.

        :param parent:
        """
        super().__init__()
        if isinstance(parent, QtWidgets.QGraphicsItem):
            # create opacity effect
            self.effect = QtWidgets.QGraphicsOpacityEffect()
            self.effect.setOpacity(0)
            parent.setGraphicsEffect(self.effect)
            self.fade = QtCore.QPropertyAnimation(self.effect, 'opacity'.encode())  # encode is utf-8 by default
        elif isinstance(parent, QtWidgets.QWidget):
            parent.setWindowOpacity(0)
            self.fade = QtCore.QPropertyAnimation(parent, 'windowOpacity'.encode())  # encode is utf-8 by default
        else:
            raise RuntimeError('Type of parameter must be QtWidgets.QGraphicsItem or QtWidgets.QWidget.')

        # set start and stop value
        self.fade.setStartValue(0)
        self.fade.setEndValue(1)
        self.fade.finished.connect(self.finished)

        self.forward = True

    def set_duration(self, duration):
        """
        Sets the duration in ms.

        :param duration:
        :return:
        """
        self.fade.setDuration(duration)

    def fadein(self):
        """
        Starts to fade in.
        """
        self.fade.setDirection(QtCore.QAbstractAnimation.Forward)
        self.forward = True
        self.fade.start()

    def fadeout(self):
        """
        Starts to fade out.
        """
        self.fade.setDirection(QtCore.QAbstractAnimation.Backward)
        self.forward = False
        self.fade.start()

    def finished(self):
        """
        Depending on the direction emit the appropriate signal.
        """
        if self.forward:
            self.fadein_finished.emit()
        else:
            self.fadeout_finished.emit()


class GraphicsItemSet:
    """
    A set of QGraphicsItem elements.
    Some collective actions are possible like setting a Z-value to each of them.
    """

    def __init__(self):
        self._content = set()

    def add_item(self, item: QtWidgets.QGraphicsItem):
        """
        Adds an item to the content list. Should be

        :param item:
        """
        if not isinstance(item, QtWidgets.QGraphicsItem):
            raise RuntimeError('Expected instance of QGraphicsItem!')
        self._content.add(item)

    def set_zvalue(self, level):
        """
        Sets the z value of all items in the set.

        :param level:
        :return:
        """
        for item in self._content:
            item.setZValue(level)


class ZStackingManager:
    """
    Puts several QtWidgets.QGraphicsItem into different sets (floors) and in the end sets their z-value so that lower
    floors have lower z-value.
    """

    def __init__(self):
        """
        Start with empty list of floors.
        """
        self._floors = []

    def new_floor(self, floor: GraphicsItemSet = None, above=True):
        """
        Creates a new floor (set of items) and exposes it. Inserts the new floor either at the top (above is True)
        or at the bottom (above is False) or above or below a given floor.

        :param floor:
        :param above:
        :return:
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


class ZoomableGraphicsView(QtWidgets.QGraphicsView):
    """
    QtWidgets.QGraphicsView where you can zoom around the current mouse position with the mouse wheel.
    """

    #: Scaling increment/decrement factor
    ScaleDeltaFactor = 1.15
    #: Minimal scaling factor
    MinimalScaleFactor = 0.5
    #: Maximal scaling factor
    MaximalScaleFactor = 2

    def __init__(self, *args, **kwargs):
        """
        Set the transformation anchor to below the current mouse position.
        """
        super().__init__(*args, **kwargs)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    def wheelEvent(self, event):  # noqa: N802
        """
        Upon a wheel event, change the zoom.

        :param event:
        """
        current_scale = self.transform().m11()  # horizontal scaling factor = vertical scaling factor
        if event.delta() > 0:
            # we are zooming in
            f = ZoomableGraphicsView.ScaleDeltaFactor
            if current_scale * f > ZoomableGraphicsView.MaximalScaleFactor:
                return
        else:
            # we are zooming out
            f = 1 / ZoomableGraphicsView.ScaleDeltaFactor
            if current_scale * f < ZoomableGraphicsView.MinimalScaleFactor:
                return
        # scale
        self.scale(f, f)

        super().wheelEvent(event)


def make_widget_clickable(parent):
    """
    Takes any QtWidgets.QWidget derived class and emits a signal emitting on mousePressEvent.
    """

    # noinspection PyPep8Naming
    class ClickableWidgetSubclass(parent):
        """
            A widget that emits a clicked signal when the mouse is pressed.
        """

        #: signal
        clicked = QtCore.pyqtSignal(QtGui.QMouseEvent)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def mousePressEvent(self, event):  # noqa: N802
            """
            Mouse has been pressed, process the event, then emit the signal.

            :param event:
            """
            super().mousePressEvent(event)
            self.clicked.emit(event)

    return ClickableWidgetSubclass


def make_widget_draggable(parent):
    """
    Takes any QtWidgets.QWidget derived class and emits a signal on mouseMoveEvent emitting the position change since
    the last mousePressEvent. By default mouseMoveEvents are only invoked while the mouse is pressed. Therefore
    we can use it to listen to dragging or implement dragging.
    """

    # noinspection PyPep8Naming
    class DraggableWidgetSubclass(parent):
        """
        Draggable widget.
        """

        #: signal
        dragged = QtCore.pyqtSignal(QtCore.QPoint)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.position_on_click = None

        def mousePressEvent(self, event):  # noqa: N802
            """
            The mouse is now pressed. Store initial position on screen.

            :param event:
            """
            self.position_on_click = event.globalPos()
            super().mousePressEvent(event)

        def mouseMoveEvent(self, event):  # noqa: N802
            """
            The mouse has moved. Calculate difference to previous position and emit signal dragged. Update position.

            Note: This slot is only called if the mouse is also pressed (see documentation).

            :param event:
            """
            super().mouseMoveEvent(event)
            position_now = event.globalPos()
            self.dragged.emit(position_now - self.position_on_click)
            self.position_on_click = position_now

    return DraggableWidgetSubclass


class ClickableGraphicsItemSignaller(QtCore.QObject):
    """
    Clickable GraphicsItem, helper object.
    """

    #: signal
    entered = QtCore.pyqtSignal(QtWidgets.QGraphicsSceneHoverEvent)
    #: signal
    left = QtCore.pyqtSignal(QtWidgets.QGraphicsSceneHoverEvent)
    #: signal
    clicked = QtCore.pyqtSignal(QtWidgets.QGraphicsSceneMouseEvent)

    def __init__(self):
        super().__init__()


# noinspection PyPep8Naming
def make_GraphicsItem_clickable(parent):
    """
    Takes a QtWidgets.QGraphicsItem and adds signals for entering, leaving and clicking on the item. For this the item
    must have setAcceptHoverEvents and it must also inherit from QObject to have signals. Only use it when really
    needed because there is some performance hit attached.
    """

    # class ClickableGraphicsItem(parent, QtCore.QObject):
    # noinspection PyPep8Naming
    class ClickableGraphicsItem(parent):
        """
            Clickable GraphicsItem
        """

        def __init__(self, *args, **kwargs):
            """
            QGraphicsItems by default do not accept hover events or accept mouse buttons (for performance reasons).
            So we need to turn both on.
            """
            parent.__init__(self, *args, **kwargs)
#           QtCore.QObject.__init__(self)
            self.parent = parent
            self.setAcceptHoverEvents(True)
            self.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
            self.signaller = ClickableGraphicsItemSignaller()

        def hoverEnterEvent(self, event):  # noqa: N802
            """
            Emit the entered signal after default handling.

            :param event:
            """
            self.parent.hoverEnterEvent(self, event)
            self.signaller.entered.emit(event)

        def hoverLeaveEvent(self, event):  # noqa: N802
            """
            Emit the left signal after default handling.

            :param event:
            """
            self.parent.hoverLeaveEvent(self, event)
            self.signaller.left.emit(event)

        def mousePressEvent(self, event):  # noqa: N802
            """
            Emit the clicked signal after default handling.

            :param event:
            """
            self.parent.mousePressEvent(self, event)
            self.signaller.clicked.emit(event)

    return ClickableGraphicsItem


# noinspection PyPep8Naming
def make_GraphicsItem_draggable(parent):
    """
    Takes a QtWidgets.QGraphicsItem and adds signals for dragging the object around. For this the item must have the
    ItemIsMovable and ItemSendsScenePositionChanges flags set. Only use it when really needed because there is
    some performance hit attached.
    """

    # noinspection PyPep8Naming
    class DraggableGraphicsItem(parent, QtCore.QObject):
        """
        Draggable GraphicsItem.
        """
        changed = QtCore.pyqtSignal(object)

        def __init__(self, *args, **kwargs):
            """
            By default QGraphicsItems are not movable and also do not emit signals when the position is changed for
            performance reasons. We need to turn this on.
            """
            parent.__init__(self, *args, **kwargs)
            self.parent = parent
            QtCore.QObject.__init__(self)

            self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable
                          | QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges)

        def itemChange(self, change, value):  # noqa: N802
            """
            Catch all item position changes and emit the changed signal with the value (which will be the position).

            :param change:
            :param value:
            """
            if change == QtWidgets.QGraphicsItem.ItemPositionChange:
                self.changed.emit(value)

            return parent.itemChange(self, change, value)

    return DraggableGraphicsItem


# Some classes we need (just to make the naming clear), Name will be used in Stylesheet selectors

#: QToolBar made draggable
DraggableToolBar = make_widget_draggable(QtWidgets.QToolBar)
ClickableWidget = make_widget_clickable(QtWidgets.QWidget)
ClickablePixmapItem = make_GraphicsItem_clickable(QtWidgets.QGraphicsPixmapItem)
ClickablePathItem = make_GraphicsItem_clickable(QtWidgets.QGraphicsPathItem)
DraggableRectItem = make_GraphicsItem_draggable(QtWidgets.QGraphicsRectItem)


class ClockLabel(QtWidgets.QLabel):
    """
    Just a clock label that shows hour : minute and updates itself every minute for as long as it lives.
    """

    def __init__(self, *args, **kwargs):
        """
        We initialize the timer and set the update interval (one minute) and start it and update the clock at least
        once.
        """
        super().__init__(*args, **kwargs)

        # customize format if desired (https://docs.python.org/3.5/library/datetime.html#strftime-strptime-behavior)
        self.time_format = '%H:%M'

        # initial update
        self.update_clock()

        # create and start timer for all following updates
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.setInterval(60000)
        self.timer.start()

    def update_clock(self):
        """
        We get the time, format it and update the label text.
        """
        text = datetime.now().strftime(self.time_format)
        self.setText(text)


def create_action(icon: QtGui.QIcon, text, parent: QtWidgets.QWidget, trigger_connection=None, toggle_connection=None,
                  checkable=False) -> QtWidgets.QAction:
    """
    Shortcut for creation of an action and wiring.

    trigger_connection is the slot if the triggered signal of the QAction is fired
    toggle_connection is the slot if the toggled signal of the QAction is fired

    :param icon:
    :param text:
    :param parent:
    :param trigger_connection:
    :param toggle_connection:
    :param checkable:
    :return: The action
    """
    action = QtWidgets.QAction(icon, text, parent)
    if trigger_connection is not None:
        action.triggered.connect(trigger_connection)
    if toggle_connection is not None:
        action.toggled.connect(toggle_connection)
    action.setCheckable(checkable)
    return action


def wrap_in_boxlayout(items, horizontal=True, add_stretch=True) -> QtWidgets.QBoxLayout:
    """
    Wraps widgets or layouts in a horizontal or vertical QBoxLayout.

    :param items: Single widgets or list of widgets to wrap.
    :param horizontal: If True horizontal box layout, otherwise vertical.
    :param add_stretch: If True adds a stretch at the end.
    :return: The box layout.
    """
    if horizontal:
        layout = QtWidgets.QHBoxLayout()
    else:
        layout = QtWidgets.QVBoxLayout()
    if isinstance(items, (list, tuple)):
        for item in items:
            layout.addWidget(item)
    else:
        layout.addWidget(items)
    if add_stretch:
        layout.addStretch()
    return layout


def wrap_in_groupbox(item, title) -> QtWidgets.QGroupBox:
    """
    Shortcut for putting a widget or a layout into a QGroupBox (with a title). Returns the group box.

    :param item: Widget or Layout to wrap.
    :param title: Title string of the group box.
    :return: Group box
    """
    box = QtWidgets.QGroupBox(title)
    if isinstance(item, QtWidgets.QWidget):
        # we use a standard BoxLayout
        layout = QtWidgets.QVBoxLayout(box)
        layout.addWidget(item)
    elif isinstance(item, QtWidgets.QLayout):
        box.setLayout(item)
    return box


class FitSceneInViewGraphicsView(QtWidgets.QGraphicsView):
    """
    Extension of QGraphicsView that fits the scene rectangle of the scene into the view when the view is shown.
    This avoids problems with the size of the view different before any layout can take place and therefore
    fitInView failing.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def resizeEvent(self, event: QtGui.QResizeEvent):  # noqa: N802
        """
        The view is resized. We need to fit the scene rectangle into the view without distorting the scene proportions.
        We also need to center on the center in order to keep the scene centered.
        """
        super().resizeEvent(event)
        scene_rect = self.sceneRect()
        self.fitInView(scene_rect, QtCore.Qt.KeepAspectRatio)
        self.centerOn(scene_rect.center())


def local_url(relative_path):
    """
    Some things have problems with URLs with relative paths, that's why we convert to absolute paths before.
    """
    absolute_path = os.path.abspath(relative_path)
    url = QtCore.QUrl.fromLocalFile(absolute_path)
    return url
