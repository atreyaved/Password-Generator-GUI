import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QAction
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

import password_generator as password
import pyperclip

class MainWindow(QWidget):
	def __init__(self, title):
		super(MainWindow, self).__init__()
		
		self.title = title
		
		self.widgets = {
			"logo": [], 
			"generate_btn": [], 
			"copy_btn": [], 
			"label": []
		}

		self.window()

	def window(self):
		##### Creating window
		self.app = QApplication(sys.argv)

		# Window settings
		self.setWindowTitle(self.title)
		self.setMinimumSize(500, 400)
		self.move(0, 0)
		self.setStyleSheet("background: #323232")

		# Setting grid
		self.setLayout(QGridLayout())

		# First frame
		self.frame1()

		# Showing window
		self.show()
		
		# print(f"window: {self.window.size()}")
		sys.exit(self.app.exec()) # Quiting window

	def clear_widgets(self):
		for key, val in self.widgets.items():
			if val != []:
				self.val[-1].hide()
			
			for i in range(len(val)):
				val.pop()

	def frame1(self):
		# Logo
		image = QPixmap("Images/logo.png")
		logo = QLabel()
		logo.setPixmap(image)
		logo.setAlignment(QtCore.Qt.AlignCenter)

		# print(f"logo: {logo.size()}")

		self.widgets["logo"].append(logo)

		##### Buttons
		
		# Generate button
		generate_btn = QPushButton("GENERATE")
		generate_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		generate_btn.setStyleSheet('''
			*{
				border: 4px solid '#BC006C';
				border-radius: 30px;
				font-size: 30px;
				color: white;
				padding: 25px 10px;
				margin: 30px 0px 0px 0px;
			}
			*:hover {
				background: '#BC006C';
			}
			'''#transition: background-color 500ms;
		) 

		# print(f"generate_btn: {generate_btn.size()}")

		generate_btn.clicked.connect(self.generate_password)
		self.widgets["generate_btn"].append(generate_btn)

		# Copy button

		copy_btn = QPushButton("Copy")
		copy_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		copy_btn.setStyleSheet('''
			*{
				border: 4px solid '#BC006C';
				border-radius: 30px;
				font-size: 30px;
				color: white;
				padding: 25px 10px; 
				margin: 10px 0px 0px 0px;

			}
			*:hover {
				background: '#BC006C';
			}
			'''#transition: background-color 500ms;
		) 

		# print(f"copy_btn: {copy_btn.size()}")

		copy_btn.clicked.connect(self.copy_password)
		self.widgets["copy_btn"].append(copy_btn)

		# Password label
		label = QLabel(password.generate_password())
		label.setAlignment(QtCore.Qt.AlignCenter)
		#label.setFixedHeight(150)
		label.setTextInteractionFlags(Qt.TextSelectableByMouse)
		label.setStyleSheet(
			"font-size: 25px;" + 
			"color: white;" +
			"padding: 10px 10px 10px 10px;" + 
			"background: '#64A314';" +
			"border-radius: 30px;" +
			"margin: 10px 0px 0px 0px;"

		)

		# print(f"label: {label.size()}")

		self.widgets["label"].append(label)

		# Setting widgets in grid
		self.layout().addWidget(self.widgets["logo"][-1], 0, 0, 1, 0)
		self.layout().addWidget(self.widgets["generate_btn"][-1], 1, 0, 1, 0)
		self.layout().addWidget(self.widgets["copy_btn"][-1], 2, 1)
		self.layout().addWidget(self.widgets["label"][-1], 2, 0)

	def copy_password(self):
		# Get text from password label and copy it
		pyperclip.copy( self.widgets["label"][-1].text() )

		# Change copy button text from copy to copied
		self.widgets["copy_btn"][-1].setText("Copied!")

	def generate_password(self):
		# Generate a random password an set the password label text to it
		npassword = password.generate_password(chars={"lowercase": True, "uppercase": True, "digits": True, "punctuation": False, "whitespace": False}, length=15)
		self.widgets["label"][-1].setText(npassword)

		# Set copy button text to copy
		self.widgets["copy_btn"][-1].setText("Copy")

def main():
	app = QApplication(sys.argv)

	main_window = MainWindow("Password Generator")

	sys.exit(self.app.exec_()) # Quiting window


if __name__ == "__main__":
	main()
