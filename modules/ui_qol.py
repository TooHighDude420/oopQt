from PyQt6.QtWidgets import QPushButton, QLayout
from collections.abc import Callable


def register_button(layout: QLayout, text:str, function: Callable, qss_name:str | None = None, **kwargs):
    tmpbutton = QPushButton(f"{text}")
    
    # if function an kwargs passed use lamda to pass function with kwargs
    # lambda is the same as javascript:
    # () => ({})?
    # (i think)
    if function and len(kwargs) > 0:
        tmpbutton.clicked.connect(lambda: function(**kwargs))
    elif function:
        tmpbutton.clicked.connect(function)
        
    if qss_name:
        tmpbutton.setObjectName(f"{qss_name}")
        
    layout.addWidget(tmpbutton)  