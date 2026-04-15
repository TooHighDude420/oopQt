from PyQt6.QtCore import QRect, Qt
from PyQt6.QtWidgets import QLabel, QApplication, QPushButton, QWidget, QVBoxLayout, QStackedWidget
from modules.ui_qol import load_style
from typing import TYPE_CHECKING

# for type hinting
if TYPE_CHECKING:
    from modules.main_window import MainWindow

class PlayWindow(QWidget):
        def __init__(self, main_window:MainWindow):
            super().__init__()

            self.setAutoFillBackground(False)
            self.setStyleSheet(load_style("style/play.qss"))

            self.main_layout = QVBoxLayout(self)
            self.main_window_ref = main_window

            background = QWidget(self)
            background.setObjectName("play_window")
            self.main_layout.addWidget(background)

            

