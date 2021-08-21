import sys

from PyQt5.QtWidgets import (QApplication, QLabel, 
	QVBoxLayout, QWidget, QMainWindow,  
	QGridLayout, QDialog, QScrollBar, 
	QScrollArea, qApp)

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QCoreApplication, QEvent

class ScrolLabel(QScrollArea):

	# constructor
	def __init__(self, *args, **kwargs):
		QScrollArea.__init__(self, *args, **kwargs)

		self.horizontalScrollBar().setSingleStep(5)

		content = QWidget(self)

		self.setWidget(content)

		self.label = QLabel(content)
		self.label.setContentsMargins(0, 0, 0, self.horizontalScrollBar().height())
		self.label.setAlignment(Qt.AlignCenter)

		lay = QVBoxLayout(content)
		lay.addWidget(self.label)

		self.setScrollStyleSheet()

		self.setWidgetResizable(True)

		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		self.label.installEventFilter(self)


	# the setText method
	def setText(self, text):
		self.label.setText(text)

	def setLabelStyleSheet(self, stylesheet: str):
		self.label.setStyleSheet(stylesheet)

	def setScrollStyleSheet(self):
		self.setStyleSheet("""
			 /* --------------------------------------- QScrollBar  -----------------------------------*/
			QScrollArea  {
				border: none;    
			}
			 
			QScrollBar:horizontal
			{
				height: 15px;
				margin: 3px 15px 3px 15px;
				border: 1px transparent #2A2929;
				border-radius: 4px;
				background-color: #C4C4C4;
			}

			QScrollBar::handle:horizontal
			{
				background-color: #807E7E;
				min-width: 5px;
				border-radius: 4px;
			}

			QScrollBar::handle:hover
			{
				background-color: #605F5F;
			}

			QScrollBar::add-line:horizontal
			{
				margin: 0px 3px 0px 3px;
				border-image: url(:/qss_icons/rc/right_arrow_disabled.png);
				width: 10px;
				height: 10px;
				subcontrol-position: right;
				subcontrol-origin: margin;
			}

			QScrollBar::sub-line:horizontal
			{
				margin: 0px 3px 0px 3px;
				border-image: url(:/qss_icons/rc/left_arrow_disabled.png);
				height: 10px;
				width: 10px;
				subcontrol-position: left;
				subcontrol-origin: margin;
			}

			QScrollBar::add-line:horizontal:hover,QScrollBar::add-line:horizontal:on
			{
				border-image: url(:/qss_icons/rc/right_arrow.png);
				height: 10px;
				width: 10px;
				subcontrol-position: right;
				subcontrol-origin: margin;
			}


			QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on
			{
				border-image: url(:/qss_icons/rc/left_arrow.png);
				height: 10px;
				width: 10px;
				subcontrol-position: left;
				subcontrol-origin: margin;
			}

			QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal
			{
				background: none;
			}


			QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
			{
				background: none;
			}

			""")

	def eventFilter(self, obj, event):
		try: # Without try and except raises three errors when begin run code
			if self.label is obj and event.type() == QEvent.Wheel:
				QCoreApplication.sendEvent(self.horizontalScrollBar(), event)
			return super().eventFilter(obj, event)
		except:
			return True

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.create_widgets()

	def create_widgets(self):

		scrollable = ScrolLabel()
		scrollable.setText(r"sO+Yu_b>P*vG1F3W@X\hU/J]o=HaE4M2&9f6m\"j0r<z:e!DlL}q^8")
		
		scrollable.setLabelStyleSheet(
			"font-size: 25px;" + 
			"color: white;" + 
			"padding: 10px 10px 10px 10px;" + 
			"background: '#64A314';" +
			"border-radius: 30px;" 
		)

		scrollable.setFixedHeight(100)

		self.setCentralWidget(scrollable)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	main_window = MainWindow()
	
	main_window.setStyleSheet("background: black;")
	
	main_window.show()
	sys.exit(app.exec_())
