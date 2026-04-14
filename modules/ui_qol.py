from PyQt6.QtWidgets import QPushButton, QLayout
from collections.abc import Callable
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def register_button(layout: QLayout, text:str, function: Callable, qss_name:str | None = None, **kwargs):
    tmpbutton = QPushButton(f"{text}")
    
    # iuse lambda to pass function with unpacked keyword arguments
    if function and len(kwargs) > 0:
        tmpbutton.clicked.connect(lambda: function(**kwargs))
    elif function:
        tmpbutton.clicked.connect(function)
        
    if qss_name:
        tmpbutton.setObjectName(f"{qss_name}")
        
    layout.addWidget(tmpbutton)

def load_style(filepath: str) -> str:
    return open(BASE_DIR / filepath).read()