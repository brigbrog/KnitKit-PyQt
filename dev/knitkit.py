'''
Developed by Brian Brogan
app construction for KnitKit
For knitkit run see KnitKitApp.py
November 2026
'''

import sys
import os
from pathlib import Path

import numpy as np
from PIL import Image

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QPixmap, QImage
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (
	QApplication,
	QLabel,
	QMainWindow,
	QStatusBar,
	QToolBar,
	QGraphicsView,
	QPushButton,
	QFileDialog,
	QGraphicsScene,
	QGraphicsPixmapItem
	)

sys.path.append("../../frameworks/_pyqt/framework")

from layout_objects import Window, ImageWindow


"""
NOTES :
------------------------------------------------------------------------------------------------

- Put Load, Export (change to Download ? ) in menu bar, leave image tool bar for transformation
	widgets and convert button

- create transformation widgets 
	(
		integer text entry : number of rows (nrows)
		checkbox : invert image
		slider : grid resolution (use automatic ranging for bounds around squareness)
		slider : grid shift, x & y
		slider : contrast threshold
	)

- Add multi channel support for image import

- Add multi format support for image export

- Update StatusBar functionality to display helpful messages when actions are completed

- automatic center detection ? 

- drag box ROI cropping ? :[]

"""

class KnitKit(ImageWindow):
# Initialization
	def __init__(self):
		super().__init__()
			
	def _init_ui(self):

		# create the graphics viewer
		self.graphicsView = QGraphicsView()
		self.setCentralWidget(self.graphicsView)
		self._createImageToolBar()
		self._createStatusBar()

		# create menu bar for file i/o


# Features
	def _createImageToolBar(self):
		# should include conversion widgets and convert button ONLY

		functions = QToolBar()

		# ToolBar Buttons
		load_button = self._getLoadImageButton()
		convert_button = self._getConvertImageButton() 
		export_button = self._getExportImageButton()
		
		# functions.addAction("CONVERT", self._convertImage)

		# Add Widgets to ToolBar
		functions.addWidget(load_button)
		functions.addWidget(convert_button)
		functions.addWidget(export_button)
		self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, functions)


	def _getLoadImageButton(self):

		# will be moved to menu bar

		load_button = QPushButton("Load")
		load_button.clicked.connect(self._loadImage)

		return load_button


	def _getConvertImageButton(self):

		convert_button = QPushButton("Convert")
		convert_button.clicked.connect(self._convertImage)

		return convert_button

	def _getExportImageButton(self):

		# will be moved to menu bar

		export_button = QPushButton("Export")
		export_button.clicked.connect(self._exportImage)

		return export_button


# TRANSFORMERS :
# ------------------------------------------------------------------------------------------------


	def _convertImage(self):

		if not self.scene:
			print("VOID SCENE") # <----------------------- SEND TO STATUS
			return None
		else:
			image_q = self._getImageDataFromViewer()
			image_pil = self._qImage2Pil(image_q)
			# apply pillow conversions here
			print("image converted to pillow type successfully !") # <- gay


	def _getImageDataFromViewer(self):
		pixmap_item = None
		for item in self.scene.items():
			if isinstance(item, QGraphicsPixmapItem):
				pixmap_item = item
				break

		if not pixmap_item:
			print("VOID SCENE") # <----------------------- SEND TO STATUS
			return None

		pixmap = pixmap_item.pixmap()
		qimage = pixmap.toImage()

		return qimage


	def _qImage2Pil(self, qimage: QImage):
		if qimage is not None:
			arr = self.qImage2Ndarray(qimage)
			pilimage = Image.fromarray(arr)

			return pilimage


	def qImage2Ndarray(self, qimage: QImage):
		if qimage is not None:
			qimage = qimage.convertToFormat(QImage.Format.Format_RGBA8888)
			width = qimage.width()
			height = qimage.height()

			ptr = qimage.bits()
			ptr.setsize(qimage.sizeInBytes())
			arr = np.array(ptr).reshape((height, width, 4))

			return arr

	# def _pil2QImage(self, pilimage: Image):


# FILE I / O :
# ------------------------------------------------------------------------------------------------


	def _loadImage(self):
		'''
		add multi channel support
		'''
		fpath, _ = QFileDialog.getOpenFileName(
				self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
			)
		if not fpath:
			return

		image_pil = Image.open(fpath)
		image_pil = image_pil.convert("L")

		im_data = image_pil.tobytes("raw", "L")
		qimage = QImage(
			im_data, 
			image_pil.width,
			image_pil.height, 
			image_pil.width, 
			QImage.Format.Format_Grayscale8
		)

		pixmap = QPixmap.fromImage(qimage)
		self._reload_canvas(pixmap)

	def _exportImage(self):

		if not self.scene:
			print("VOID SCENE") # <----------------------- SEND TO STATUS
			return None
		
		fpath, _ = QFileDialog.getSaveFileName(
				self, "Select Save Location", "", "PNG Files (*.png)"
			)
		if not fpath:
			return

		image_q = self._getImageDataFromViewer()
		image_pil = self._qImage2Pil(image_q)

		image_pil.save(fpath, "PNG")




		











