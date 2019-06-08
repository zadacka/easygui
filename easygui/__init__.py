"""
Hello from easygui/__init__.py

"""

# __all__ must be defined in order for Sphinx to generate the API automatically.
__all__ = ['buttonbox',
           'diropenbox',
           'fileopenbox',
           'filesavebox',
           'textbox',
           'integerbox',
           'multenterbox',
           'enterbox',
           'choicebox',
           'passwordbox',
           'multpasswordbox',
           'multchoicebox',
           'EgStore',
           'eg_version',
           'egversion',
           'abouteasygui',
           'egdemo',
]

from demos.demo import easygui_demo as egdemo
# Import all functions that form the API
from .boxes.button_box import buttonbox
from .boxes.choice_box import choicebox
from .boxes.choice_box import multchoicebox
from easygui.boxes.text_box import codebox, exceptionbox
from easygui.boxes.fillable_box import integerbox, enterbox, passwordbox
from easygui.boxes.button_box import ynbox, ccbox, boolbox, indexbox, msgbox
from .boxes.diropen_box import diropenbox
from .boxes.egstore import EgStore, read_or_create_settings
from .boxes.fileopen_box import fileopenbox
from .boxes.filesave_box import filesavebox
from .boxes.multi_fillable_box import multenterbox
from .boxes.multi_fillable_box import multpasswordbox
from .boxes.text_box import textbox

