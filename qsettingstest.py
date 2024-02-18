import sys
from random import shuffle
from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import *
from PySide6.QtCharts import *
from PySide6.QtWidgets import QWidget
from functools import partial



settings = QSettings("AjSpeed Dev", "FlashcardApp")
settings.setValue("editor/wrapMargin", 68)

margin = settings.value("editor/wrapMargin", 80)
print(margin)