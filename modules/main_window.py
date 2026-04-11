from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QApplication, QPushButton, QWidget, QVBoxLayout, QStackedWidget

from widgets.main_menu import mainMenu

class mainWindow():
    def __init__(self):
        self.app = QApplication([])
        self.screen = self.app.primaryScreen()

        SCREEN_HEIGHT = self.screen.size().height()
        SCREEN_WIDTH = self.screen.size().width()

        self.stack = QStackedWidget()

        self.window = QWidget()
        self.window.setMaximumHeight(SCREEN_HEIGHT)
        self.window.setMaximumWidth(SCREEN_WIDTH)
        self.window.showMaximized()
        self.window.setWindowTitle("Blackjack dealer training")

        self.layout = QVBoxLayout(self.window)
        self.layout.addWidget(self.stack)

        self.show_widget(mainMenu())

        self.window.show()

        self.app.exec()

    def show_widget(self, widget: QWidget):
        self.stack.addWidget(widget)
        self.stack.setCurrentWidget(widget)