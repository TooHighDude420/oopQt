import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QApplication, QPushButton, QWidget, QVBoxLayout, QStackedWidget
from modules.ui_qol import register_button
from .play_window import PlayWindow
from typing import TYPE_CHECKING

# for type hinting
if TYPE_CHECKING:
    from modules.main_window import MainWindow

class MainMenu(QWidget):
    def __init__(self, main_window:MainWindow):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.main_window_ref = main_window

        register_button(self.main_layout, "start", self.start)
        register_button(self.main_layout, "quit", self.quit)


    def start(self):
        self.main_window_ref.show_widget(PlayWindow(self.main_window_ref))
        self.main_window_ref.remove_widget(self)

    def quit(self):
        sys.exit()