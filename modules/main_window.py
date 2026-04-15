from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QApplication, QPushButton, QWidget, QVBoxLayout, QStackedWidget

from widgets.main_menu import MainMenu

class MainWindow():
    def __init__(self):
        self.app = QApplication([])
        self.screen = self.app.primaryScreen()

        self.screen_height = self.screen.size().height()
        self.screen_width = self.screen.size().width()

        self.stack = QStackedWidget()

        self.window = QWidget()
        self.window.setMaximumHeight(self.screen_height)
        self.window.setMaximumWidth(self.screen_width)
        self.window.showMaximized()
        self.window.setWindowTitle("Blackjack dealer training")

        self.layout = QVBoxLayout(self.window)
        self.layout.addWidget(self.stack)

        self.show_widget(MainMenu(self))

        self.window.show()

        self.app.exec()

    def show_widget(self, widget: QWidget):
        self.stack.addWidget(widget)
        self.stack.setCurrentWidget(widget)

    def remove_widget(self, widget: QWidget):
        self.stack.removeWidget(widget)