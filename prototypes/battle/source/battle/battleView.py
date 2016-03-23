import math

from PyQt5.QtCore import QObject, QPointF
from PyQt5.QtWidgets import QMainWindow, QPushButton

from PyQt5.QtCore import QSize, Qt, QMetaObject
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QIcon
from PyQt5.QtWidgets import QMessageBox, QWidget, QGridLayout, QLabel, QSpacerItem, QSizePolicy, \
    QGraphicsScene, QGraphicsView

from prototypes.battle.source.base import constants


class MainBattleWindow(QMainWindow):
    def __init__(self, config, parent=None):
        super(MainBattleWindow, self).__init__(parent)
        self.config = config

    def resizeEvent(self, evt=None):
        self.ui.resize_event()

    def show(self):
        if self.config is None:
            self.showMaximized()
        elif self.config.show_fullscreen():
            self.showFullScreen()
        elif self.config.maximize():
            self.showMaximized()
        else:
            self.resize(self.config.get_resolution_qsize())
            self.showNormal()
        self.resizeEvent()

    def closeEvent(self, event):
        # noinspection PyTypeChecker,PyCallByClass
        result = QMessageBox.question(self,
                                      self.config.get_text('exit.window.title'),
                                      self.config.get_text('exit.window.content'),
                                      QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.No:
            event.ignore()


class MainQGraphicsScene(QGraphicsScene):
    def __init__(self):
        self.battleView = None
        super().__init__()

    def mousePressEvent(self, event):
        position = QPointF(event.scenePos())
        if self.battleView is not None:
            x, y = self.battleView.map.position_to_grid_position(position)
            if x >= 0 and y >= 0:
                print('TODO mouse click on grid ' + str(x) + ';' + str(y))
                # if ev.button() == Qt.LeftButton:
                #    item = QtGui.QGraphicsTextItem("CLICK")
                #    item.setPos(ev.scenePos())
                #    self.addItem(item)

    def set_battle_view(self, battle_view):
        self.battleView = battle_view


class BattleView(QObject):
    def __init__(self, battle_window, parent=None):
        super().__init__(parent)
        self.battleWindow = battle_window  # MainBattleWindow container

        if len(self.battleWindow.config.errors) != 0:
            # noinspection PyArgumentList
            QMessageBox.critical(battle_window, 'Configuration Error', self.battleWindow.config.get_error_str())
            exit(-1)

        # main elements
        self.centralWidget = QWidget(self.battleWindow)
        self.gridLayout = QGridLayout(self.centralWidget)

        # misc side elements
        self.graphicsView_coatOfArm = CustomScene()
        self.graphicsView_currentUnit = CustomScene()
        self.graphicsView_targetedUnit = CustomScene()

        for button in self.graphicsView_coatOfArm, self.graphicsView_currentUnit, self.graphicsView_targetedUnit:
            button.enter_functions.append(self.set_label_hint)
            button.leave_functions.append(self.clear_label_hint)

        # buttons
        self.autoCombatButton = CustomButton(self.centralWidget)
        self.helpButton = CustomButton(self.centralWidget)
        self.retreatButton = CustomButton(self.centralWidget)
        self.endUnitTurnButton = CustomButton(self.centralWidget)
        self.nextTargetButton = CustomButton(self.centralWidget)

        for button in self.autoCombatButton, self.helpButton, self.retreatButton, self.nextTargetButton, self.endUnitTurnButton:
            button.enter_functions.append(self.set_label_hint)
            button.leave_functions.append(self.clear_label_hint)
            button.click_functions.append(self.click_button)

        # info containers
        self.dateLabel = QLabel(self.centralWidget)  # display current turn in battle
        self.hintLabel = QLabel(self.centralWidget)  # display hint when hovering over an elemend

        # the actual battle scene
        self.mainScene = MainQGraphicsScene()
        self.graphicsView_main = QGraphicsView(self.mainScene)
        self.gridLayout.addWidget(self.graphicsView_main, 1, 0, 12, 1)

    def setup_ui(self):
        self.battleWindow.setWindowTitle(self.battleWindow.config.get_text('battle.window.title') + ' v' + str(self.battleWindow.config.version))
        background = self.battleWindow.config.theme_selected.get_background_pixmap()
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(background))
        self.battleWindow.setMinimumSize(constants.get_min_resolution_qsize())
        self.battleWindow.setAutoFillBackground(True)
        self.gridLayout.setVerticalSpacing(0)

        self.setup_hint_label()  # Labels
        self.setup_turn_label()  # Labels
        self.setup_space()  # Space item

        self.setup_help_button()  # Help Push Button
        self.setup_next_target_button()  # Next Target Button
        self.setup_end_unit_button()  # End Unit Button
        self.setup_retreat_button()  # Retreat Button
        self.setup_auto_combat_button()  # Automatic battle button

        self.setup_targeted_unit_view()  # Targeted Unit view
        self.setup_current_unit_view()  # Current Unit View
        self.setup_coat_of_arms_view()  # Coat of Arm view

        self.setup_map()  # Main view
        self.battleWindow.setPalette(palette)
        self.battleWindow.setCentralWidget(self.centralWidget)

        # noinspection PyArgumentList
        QMetaObject.connectSlotsByName(self.battleWindow)

    def setup_map(self):
        self.mainScene = MainQGraphicsScene()
        self.graphicsView_main.setScene(self.mainScene)
        self.mainScene.set_battle_view(self.battleView)
        width = 2 * self.graphicsView_main.height() / math.sqrt(3)
        height = self.graphicsView_main.height()
        if width > self.graphicsView_main.width():
            width = self.graphicsView_main.width()
            height = self.graphicsView_main.width() * math.sqrt(3) / 2
        item = self.mainScene.addRect(0, 0, width - 15, height - 15)
        item.hide()
        self.battleView.draw_battle_map(self.mainScene)

    def resize_event(self):
        self.setup_map()

    # misc elements
    def setup_hint_label(self):
        size_policy = constants.default_size_policy(self.hintLabel, QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.hintLabel.setSizePolicy(size_policy)
        self.hintLabel.setFont(constants.default_font())
        self.hintLabel.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.gridLayout.addWidget(self.hintLabel, 0, 0, 1, 1)

    def setup_turn_label(self):
        size_policy = constants.default_size_policy(self.dateLabel, QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.dateLabel.setSizePolicy(size_policy)
        self.dateLabel.setFont(constants.default_font())
        self.dateLabel.setText('Turn ' + str(self.battleView.turn))
        self.dateLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.gridLayout.addWidget(self.dateLabel, 0, 0, 1, 1)

    def setup_space(self):
        # Space between help Button and flag view
        spacer_item = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        self.gridLayout.addItem(spacer_item, 2, 1, 1, 1)
        # Space between flag view and next target Button
        spacer_item1 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        self.gridLayout.addItem(spacer_item1, 4, 1, 1, 1)
        # Space between retreat Button and targetted unit view
        spacer_item2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacer_item2, 8, 1, 1, 1)
        # Space between current unit view and auto Button
        spacer_item3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        self.gridLayout.addItem(spacer_item3, 11, 1, 1, 1)

    def setup_coat_of_arms_view(self):
        size = QSize(90, 120)
        self.battleView.draw_coat_of_arms(self.graphicsView_coatOfArm.scene(), size)
        self.graphicsView_coatOfArm.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        size_policy = constants.default_size_policy(self.graphicsView_coatOfArm, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.graphicsView_coatOfArm.setSizePolicy(size_policy)
        self.graphicsView_coatOfArm.setMinimumSize(size)
        self.graphicsView_coatOfArm.setMaximumSize(size)
        self.graphicsView_coatOfArm.setStyleSheet("border-style: none;background: transparent")
        self.graphicsView_coatOfArm.setCacheMode(QGraphicsView.CacheBackground)
        self.gridLayout.addWidget(self.graphicsView_coatOfArm, 3, 1, 1, 1)

    # unit views
    def setup_targeted_unit_view(self):
        size = QSize(60, 60)
        army = self.get_computer_army()
        defending = (army == self.battleView.defender)
        self.battleView.draw_targetted_unit(defending, self.graphicsView_targetedUnit.scene(), size)
        size_policy = constants.default_size_policy(self.graphicsView_targetedUnit, QSizePolicy.Fixed,
                                                    QSizePolicy.Fixed)
        self.graphicsView_targetedUnit.setSizePolicy(size_policy)
        self.graphicsView_targetedUnit.setMinimumSize(size)
        self.graphicsView_targetedUnit.setMaximumSize(size)
        self.gridLayout.addWidget(self.graphicsView_targetedUnit, 9, 1, 1, 1, Qt.AlignCenter)

    def setup_current_unit_view(self):
        size = QSize(60, 60)
        army = self.get_human_army()
        defending = (army == self.battleView.defender)
        self.battleView.draw_current_unit(defending, self.graphicsView_currentUnit.scene(), size)
        size_policy = constants.default_size_policy(self.graphicsView_currentUnit, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.graphicsView_currentUnit.setSizePolicy(size_policy)
        self.graphicsView_currentUnit.setMinimumSize(size)
        self.graphicsView_currentUnit.setMaximumSize(size)
        self.gridLayout.addWidget(self.graphicsView_currentUnit, 10, 1, 1, 1, Qt.AlignCenter)

    def get_human_army(self):
        if self.battleView.attacker.nation.computer:
            return self.battleView.defender
        return self.battleView.attacker

    def get_computer_army(self):
        if self.battleView.attacker.nation.computer:
            return self.battleView.attacker
        return self.battleView.defender

    # buttons
    def setup_next_target_button(self):
        size_policy = constants.default_size_policy(self.nextTargetButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.nextTargetButton.setSizePolicy(size_policy)
        self.nextTargetButton.setMinimumSize(QSize(45, 45))
        self.nextTargetButton.setMaximumSize(QSize(45, 45))
        self.nextTargetButton.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap(self.battleWindow.config.theme_selected.get_target_button_pixmap()), QIcon.Normal, QIcon.Off)
        self.nextTargetButton.setIcon(icon)
        self.nextTargetButton.setIconSize(QSize(40, 40))
        self.gridLayout.addWidget(self.nextTargetButton, 5, 1, 1, 1, Qt.AlignCenter)

    def setup_end_unit_button(self):
        size_policy = constants.default_size_policy(self.endUnitTurnButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.endUnitTurnButton.setSizePolicy(size_policy)
        self.endUnitTurnButton.setMinimumSize(QSize(45, 45))
        self.endUnitTurnButton.setMaximumSize(QSize(45, 45))
        self.endUnitTurnButton.setText("")
        icon1 = QIcon()
        icon1.addPixmap(self.battleWindow.config.theme_selected.get_end_button_pixmap(), QIcon.Normal, QIcon.Off)
        self.endUnitTurnButton.setIcon(icon1)
        self.endUnitTurnButton.setIconSize(QSize(40, 40))
        self.gridLayout.addWidget(self.endUnitTurnButton, 6, 1, 1, 1, Qt.AlignCenter)

    def setup_retreat_button(self):
        size_policy = constants.default_size_policy(self.retreatButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.retreatButton.setSizePolicy(size_policy)
        self.retreatButton.setMinimumSize(QSize(45, 45))
        self.retreatButton.setMaximumSize(QSize(45, 45))
        self.retreatButton.setToolTip("")
        self.retreatButton.setWhatsThis("")
        self.retreatButton.setText("")
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(self.battleWindow.config.theme_selected.get_retreat_button_pixmap()), QIcon.Normal, QIcon.Off)
        self.retreatButton.setIcon(icon2)
        self.retreatButton.setIconSize(QSize(42, 40))
        self.gridLayout.addWidget(self.retreatButton, 7, 1, 1, 1, Qt.AlignCenter)

    def setup_help_button(self):
        size_policy = constants.default_size_policy(self.helpButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.helpButton.setSizePolicy(size_policy)
        self.helpButton.setMinimumSize(QSize(80, 80))
        self.helpButton.setMaximumSize(QSize(80, 80))
        self.helpButton.setText("")
        icon3 = QIcon()
        icon3.addPixmap(QPixmap(self.battleWindow.config.theme_selected.get_help_button_pixmap()), QIcon.Normal, QIcon.Off)
        self.helpButton.setIcon(icon3)
        self.helpButton.setIconSize(QSize(75, 75))
        self.gridLayout.addWidget(self.helpButton, 0, 1, 2, 1)

    def setup_auto_combat_button(self):
        size_policy = constants.default_size_policy(self.autoCombatButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.autoCombatButton.setSizePolicy(size_policy)
        self.autoCombatButton.setMinimumSize(QSize(90, 90))
        self.autoCombatButton.setMaximumSize(QSize(90, 90))
        self.autoCombatButton.setText("")
        icon4 = QIcon()
        icon4.addPixmap(QPixmap(self.battleWindow.config.theme_selected.get_autocombat_button_pixmap()), QIcon.Normal, QIcon.Off)
        self.autoCombatButton.setIcon(icon4)
        self.autoCombatButton.setIconSize(QSize(80, 80))
        self.gridLayout.addWidget(self.autoCombatButton, 12, 1, 1, 1)

    # element interactions
    def clear_label_hint(self, generic_element):
        self.hintLabel.setText('')

    def set_label_hint(self, generic_element):
        text = ''
        if generic_element == self.graphicsView_currentUnit:
            text = str(self.battleView.currentUnit)
        elif generic_element == self.graphicsView_targetedUnit:
            text = str(self.battleView.targettedUnit)
        elif generic_element == self.autoCombatButton:
            text = self.battleWindow.config.get_text('auto.play.label')
        elif generic_element == self.helpButton:
            text = self.battleWindow.config.get_text('help.tacticalbattle.label')
        elif generic_element == self.retreatButton:
            text = self.battleWindow.config.get_text('retreat.all.label')
        elif generic_element == self.endUnitTurnButton:
            text = self.battleWindow.config.get_text('end.unit.label')
        elif generic_element == self.nextTargetButton:
            text = self.battleWindow.config.get_text('next.target.label')
        if text != '':
            self.hintLabel.setText(text)

    def click_button(self, button_element):
        if button_element == self.autoCombatButton:
            self.battleView.autoCombat = True
        elif button_element == self.helpButton:
            print('click helpButton')
        elif button_element == self.retreatButton:
            self.get_human_army().retreat = True
        elif button_element == self.endUnitTurnButton:
            print('click endUnitTurnButton')
        elif button_element == self.nextTargetButton:
            print('click nextTargetButton')


class CustomScene(QGraphicsView):
    enter_functions = []
    leave_functions = []

    def __init__(self):
        super().__init__(QGraphicsScene())

    def enterEvent(self, event):
        for f in self.enter_functions:
            f(self)
        super().enterEvent(event)

    def leaveEvent(self, event):
        for f in self.leave_functions:
            f(self)
        super().leaveEvent(event)


class CustomButton(QPushButton):
    enter_functions = []
    leave_functions = []
    click_functions = []

    def __init__(self, *__args):
        super().__init__(*__args)
        # noinspection PyUnresolvedReferences
        super().clicked.connect(self.click)

    def enterEvent(self, event):
        for f in self.enter_functions:
            f(self)
        super().enterEvent(event)

    def leaveEvent(self, event):
        for f in self.leave_functions:
            f(self)
        super().leaveEvent(event)

    def click(self):
        for f in self.click_functions:
            f(self)
