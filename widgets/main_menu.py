import sys

from modules.ui_qol import register_button

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QApplication, QPushButton, QWidget, QVBoxLayout, QStackedWidget


class mainMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)

        register_button(self.main_layout, "start", self.start)
        register_button(self.main_layout, "quit", self.quit)


    def start(self):
        print("start pressed")

    def quit():
        sys.exit()