'''
Developed by Brian Brogan
TOP-LEVEL run script for KnitKit
For knitkit functions see knitkit.py
November 2026
'''

import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QStatusBar, QToolBar

sys.path.append("../../frameworks/_pyqt/framework")

from layout_objects import Window, ImageWindow
from knitkit import KnitKit


if __name__ == "__main__":

	app = QApplication([])

	window = KnitKit()
	# window = ImageWindow()
	
	window.show()
	sys.exit(app.exec())
