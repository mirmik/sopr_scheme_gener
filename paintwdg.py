from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import common

class PaintWidgetSetter(QWidget):
	def __init__(self, container):
		super().__init__()
		self.container = container

		self.vlayout = QVBoxLayout()
		self.hlayout = QHBoxLayout()

		self.warr = QWidget(), QWidget(), QWidget(), QWidget()
		
		for w in self.warr[0:2]:
			w.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
			w.setAutoFillBackground(True);

		for w in self.warr[2:4]:
			w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
			w.setAutoFillBackground(True);

		pal = QPalette();

		#pal.setColor(QPalette.Background, Qt.black);
		pal.setColor(QPalette.Background, Qt.gray);
		self.warr[0].setPalette(pal);		
		
		#pal.setColor(QPalette.Background, Qt.red);
		pal.setColor(QPalette.Background, Qt.gray);
		self.warr[1].setPalette(pal);		
		
		#pal.setColor(QPalette.Background, Qt.green);
		pal.setColor(QPalette.Background, Qt.gray);
		self.warr[2].setPalette(pal);		
		
		#pal.setColor(QPalette.Background, Qt.blue);
		pal.setColor(QPalette.Background, Qt.gray);
		self.warr[3].setPalette(pal);		
		
		self.vlayout.addWidget(self.warr[0])
		self.vlayout.addLayout(self.hlayout)
		self.vlayout.addWidget(self.warr[1])

		self.hlayout.addWidget(self.warr[2])
		self.hlayout.addWidget(self.container)		
		self.hlayout.addWidget(self.warr[3])

		self.vlayout.setSpacing(0)
		self.hlayout.setSpacing(0)
		#self.vlayout.setContentsMargins(0,0,0,0)
		#self.hlayout.setContentsMargins(0,0,0,0)

		self.setLayout(self.vlayout)


class PaintPreDialog(QDialog):
	def __init__(self, main):
		super().__init__()
		self.layout = QVBoxLayout()
		self.label = QLabel()
		self.pix = QPixmap(main.make_image())
		self.label.setPixmap(self.pix)
		self.layout.addWidget(self.label)
		self.layout.setContentsMargins(0,0,0,0)
		self.setLayout(self.layout)
		self.window().setFixedSize( self.window().sizeHint() );

class PaintWidget(QWidget):
	def __init__(self):
		super().__init__()

	def resizeEvent(self, ev):
		self.shemetype.datasettings.width = self.width()
		self.shemetype.datasettings.height = self.height()

		self.shemetype.updateDataSettingsVM()

	def make_image(self):
		img = QImage(self.size(), QImage.Format_ARGB32)
		
		with QPainter(img) as painter:
			self.render(painter)

		return img

	def predraw_dialog(self):
		PaintPreDialog(self).exec()

	def save_image(self, path):
		self.make_image().save(path)
		