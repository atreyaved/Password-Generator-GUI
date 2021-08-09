#!/usr/bin/env python3
import sys
import os
from PyQt5.QtWidgets import (QApplication, QLabel, QPushButton, 
	QVBoxLayout, QWidget, QFileDialog, 
	QGridLayout, QCheckBox, QDialog, 
	QAction, QMainWindow, QWidgetAction, 
	QSpinBox, QScrollArea, qApp)

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

import password_generator as password
import pyperclip
import PREFS
import webbrowser

class MainWindow(QMainWindow):
	resized = QtCore.pyqtSignal()
	def __init__(self, title, parent=None):
		super().__init__(parent)
		
		self.title = title
		
		# App icon
		self.scriptDir = os.path.dirname(os.path.realpath(__file__))
		self.setWindowIcon(QtGui.QIcon(self.scriptDir + os.path.sep + 'Images/icon.png'))
		
		self.resized.connect(self.on_resize)

		self.window()
		self.create_menu_bar()

	def resizeEvent(self, event):
		self.resized.emit()
		return super(MainWindow, self).resizeEvent(event)

	def on_resize(self):
		w, h = self.size().width(), self.size().height()
		logo_css = css_to_dict(self.app_widget.widgets["logo"][-1].styleSheet())
		proportion = h / w
			
		#print("Window: ", w, h)
		#print("Logo: ", logo_css["font-size"])
		
		#print(77.777777778*proportion)
		
		print("\n")

	def window(self):
		# Window settings
		self.setWindowTitle(self.title)
		self.setMinimumSize(500, 450)
		self.setStyleSheet("background: #323232")

		# creating App widget and setting it as central
		self.app_widget = App(parent=self)
		self.setCentralWidget(self.app_widget)

	def create_menu_bar(self):
		# filling up a menu bar
		bar = self.menuBar()
		bar.setStyleSheet(
			"""
			QMenuBar {
				background-color: #383838;
			}

			QMenuBar::item {
				padding: 1px 4px;
				background: transparent;
				border-radius: 4px;
				color: #ffffff
			}

			QMenuBar::item:selected { /* when selected using mouse or keyboard */
				background: #4C4C4C;
			}

			QMenuBar::item:pressed {
				background: #595959;
			}
			""")

		widget_action_stylesheet = """
			*{
				background: #383838;
				color: #ABABAB;
				padding: 4px 4px;
				font-size: 15px;
				}

			*:hover{
				background: #4C4C4C;
				color: #ffffff;
			}
			*:pressed {
				background: #595959;
			}
		"""
		
		# File menu
		file_menu = bar.addMenu('&File')
		
		
		# Adding actions to file menu
		settings_action = self.create_action_widget("Settings", 
			file_menu, 
			stylesheet=widget_action_stylesheet, 
			callback=self.app_widget.create_settings_dialog, 
			shortcut="Ctrl+S")
		
		close_action = self.create_action_widget("Close", 
			file_menu, 
			stylesheet=widget_action_stylesheet, 
			callback=self.close_app, 
			shortcut="Ctrl+Q")

		# Edit menu
		edit_menu = bar.addMenu('&Edit')
		
		# Adding actions to edit menu
		generate_action = self.create_action_widget('Generate', 
			edit_menu, 
			stylesheet=widget_action_stylesheet, 
			callback=self.app_widget.generate_password, 
			shortcut="Ctrl+G")
		
		copy_action = self.create_action_widget('Copy', 
			edit_menu, 
			stylesheet=widget_action_stylesheet, 
			callback=self.app_widget.copy_password, 
			shortcut="Ctrl+C")

		# Edit menu
		about_menu = bar.addMenu('&About')
		
		# Adding actions to edit menu
		about_app_action = self.create_action_widget('About me', 
			about_menu, 
			stylesheet=widget_action_stylesheet, 
			callback=self.app_widget.create_about_me_dialog, 
			shortcut="Ctrl+m")

	def create_action_widget(self, text: str, menu, stylesheet: str="", callback: callable=lambda: print("No callback"), shortcut: str=""):
		"""
		Args:
			text (str): The text to be displayed in the QWidgetAction.
			menu (menuBar.addMenu): The menu to append the QWidgetAction.
			stylesheet (str, optional=""): The stylesheet of the QWidgetAction (really the stylesheet of the Label).
			callback (callable, optional=lambda: print("No callback")): The callback function to the QWidgetAction.
			shortcut (str, optional=""): The shortcut to acces to the QWidgetAction
		"""
		action = QWidgetAction(self) # Create a QWidget action in QMainWindow
		
		if shortcut != "": # If the shortcut isn't empty
			key = shortcut.split("+")[0] # Split by + and get the modifier key (ctrl, shift, alt)
			mnemo = shortcut.split("+")[1] # Split by + and get the key (a, b, c)
			
			### IF I COMMENT THESE THREE LINES THE QWIDGETACTIONS WORKS ###
			text = text.replace(mnemo, f"<u>{mnemo}</u>", 1) # Underline the shortut letter 
			text += f"{'&nbsp;'*3}" # Spacing between given text and shortcut
			text += f"<span style='color: #ABABAB; font-size: 14px;'>{key}+{mnemo.capitalize()}</span>" # Add different color and font-size to the shortcut

		label = QLabel(text) # Create a QLabel with the text
		label.setStyleSheet(stylesheet) # Set the given stylesheet to the QLabel
		action.setDefaultWidget(label); # Set QLabel as default widget to QWidget
		action.setShortcut(shortcut) # Set shortcut to QWidgetAction

		menu.addAction(action) # Add action to given menu (menuBar.addMenu)
		action.triggered.connect(callback) # Connect the QWidgetAction with the given callback

		return action # Return the QWidgetAction

	def close_app(self):
		self.close()
		try:
			self.app_widget.settings_dialog.close()
		except:
			pass
		try:
			self.app_widget.about_me_dialog.close()
		except:
			pass

class App(QWidget):
	def __init__(self, parent=None):
		super(App, self).__init__()

		
		self.widgets = {
			"logo": [], 
			"generate_btn": [], 
			"copy_btn": [], 
			"label": []
		}

		self.init_prefs()

		self.window()

	def init_prefs(self):
		# prefs = {"lowercase": True, "uppercase": True, "digits": True, "punctuation": False, "whitespace":False, "length":15}

		self.settings = PREFS.PREFS(PREFS.read_prefs_file("Prefs/default_settings"), filename="Prefs/settings")
 
	def window(self):
		##### Creating window
		self.app = QApplication(sys.argv)

		# Setting grid
		self.setLayout(QGridLayout())

		# First frame
		self.frame1()

		# Showing window
		#self.show()
		
		# print(f"window: {self.window.size()}")
		#sys.exit(self.app.exec()) # Quiting window

	def clear_widgets(self):
		for key, val in self.widgets.items():
			if val != []:
				self.val[-1].hide()
			
			for i in range(len(val)):
				val.pop()

	def frame1(self):
		# Logo
		# image = QPixmap("Images/logo.png")
		logo = QLabel("&lt;<span style='color:#64a314'>/</span><span style='color:#ffffff'>P45w0rD<br/>G3n3R4t0r</span><span style='color:#64a314'>/</span>&gt;")
		logo.setStyleSheet("font-size: 70px; font-family: impact;")

		#logo.setPixmap(image)
		logo.setAlignment(QtCore.Qt.AlignCenter)

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
		label = QLabel(password.generate_password(chars=self.settings.file, length=self.settings.file["length"]))
		label.setAlignment(QtCore.Qt.AlignCenter)
		
		label.setCursor(QCursor(QtCore.Qt.IBeamCursor))
		
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

	def create_settings_dialog(self):
		######## SET UP DIALOG ########
		dialog = QDialog() # Creating dialog
		
		dialog.setWindowTitle("Settings") # Setting dialog tittle
		dialog.setStyleSheet("background: #383838; color: #ffffff") # Setting dialog styling
		dialog.setWindowModality(Qt.ApplicationModal) # True blocks its parent window
		dialog.setLayout(QGridLayout())

		## Adding widgets ##

		lower_check = QCheckBox("ASCII lowercase")
		lower_check.setStyleSheet(
			'''
			*{
				color: #E1E1E1;
			}
			*:hover {
				color: #ffffff;
			}
			''')

		lower_check.setChecked(self.settings.file["lowercase"])
		lower_check.toggled.connect( lambda: self.settings.write_prefs("lowercase", lower_check.isChecked()) )

		upper_check = QCheckBox("ASCII uppercase")
		upper_check.setStyleSheet(
			'''
			*{
				color: #E1E1E1;
			}
			*:hover {
				color: #ffffff;
			}
			''')

		upper_check.setChecked(self.settings.file["uppercase"])
		upper_check.toggled.connect( lambda: self.settings.write_prefs("uppercase", upper_check.isChecked()) )

		digits_check = QCheckBox("Digits (1, 2...)")
		digits_check.setStyleSheet(
			'''
			*{
				color: #E1E1E1;
			}
			*:hover {
				color: #ffffff;
			}
			''')

		digits_check.setChecked(self.settings.file["digits"])
		digits_check.toggled.connect( lambda: self.settings.write_prefs("digits", digits_check.isChecked()) )

		punct_check = QCheckBox("Punctuation")
		punct_check.setStyleSheet(
			'''
			*{
				color: #E1E1E1;
			}
			*:hover {
				color: #ffffff;
			}
			''')
		
		punct_check.setChecked(self.settings.file["punctuation"])
		punct_check.toggled.connect( lambda: self.settings.write_prefs("punctuation", punct_check.isChecked()) )


		length_spinbox = QSpinBox()
		length_spinbox.setMinimum(1)
		length_spinbox.setMaximum(10000)
		length_spinbox.setPrefix("Length: ")
		length_spinbox.setValue(self.settings.file["length"])
		length_spinbox.valueChanged.connect( lambda: self.settings.write_prefs("length", length_spinbox.value()) )

		save_btn = QPushButton("Close", dialog)
		save_btn.setStyleSheet('''
			*{
				color: white;
				background: #383838;
			}
			*:hover {
				background: #484848;
			}
			'''#transition: background-color 500ms;
		)

		save_btn.clicked.connect(lambda: dialog.reject())

		dialog.layout().addWidget(lower_check, 0, 0)
		dialog.layout().addWidget(upper_check, 1, 0)
		dialog.layout().addWidget(digits_check, 2, 0)
		dialog.layout().addWidget(punct_check, 3, 0)
	
		dialog.layout().addWidget(length_spinbox, 4, 0)

		dialog.layout().addWidget(save_btn, 5, 0)

		self.settings_dialog = dialog

		dialog.exec_()
	
	def create_about_me_dialog(self):
		######## SET UP DIALOG ########
		dialog = QDialog() # Creating dialog
		
		dialog.setWindowTitle("About me") # Setting dialog tittle
		dialog.setStyleSheet("background: #383838; color: #ffffff") # Setting dialog styling
		dialog.setWindowModality(True) # False blocks its parent window
		dialog.setLayout(QGridLayout())

		## Adding widgets ##
		about_label = QLabel("This is a simple GUI app written in Python using PyQt5.<br/><br/>Contact me: <br/>&nbsp;&nbsp;&nbsp;&nbsp;Discord: patitotective#0127<br/>&nbsp;&nbsp;&nbsp;&nbsp;Mail: <a href='mailto:cristobalriaga@gmail.com' style='color: #8ebf42'>cristobalriaga@gmail.com</a>")
		about_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
		about_label.setOpenExternalLinks(True)

		source_code_link = QLabel("<a href='https://github.com/Patitotective/password_generator_gui' style='color: #8ebf42'>Source code</a>", dialog)
		source_code_link.setOpenExternalLinks(True)

		dialog.layout().addWidget(about_label, 0, 0, 1, 1)
		dialog.layout().addWidget(QLabel(), 1, 0, 1, 1)
		dialog.layout().addWidget(source_code_link, 2, 1)
		dialog.layout().addWidget(QLabel("v0.1"), 2, 0)

		self.about_me_dialog = dialog

		dialog.exec_()

	def copy_password(self):
		# Get text from password label and copy it
		pyperclip.copy( self.widgets["label"][-1].text() )

		# Change copy button text from copy to copied
		self.widgets["copy_btn"][-1].setText("Copied!")

	def generate_password(self):
		# Generate a random password an set the password label text to it
		npassword = password.generate_password(chars=self.settings.file, length=self.settings.file["length"])
		self.widgets["label"][-1].setText(npassword)

		# Set copy button text to copy
		self.widgets["copy_btn"][-1].setText("Copy")

def css_to_dict(string: str, ender: str=";", separator: str=": "):
	props = filter(lambda x: True if separator in x else False, string.split(ender))
	result = {}

	for prop in props:
		key, val = prop.split(separator)
		result[key.strip()] = val.strip()

	return result

def dict_to_css(css_dict: dict, ender: str=";", separator: str=": "):
	result = ""

	for k, v in css_dict.items():
		result += f"{k}{separator}{v}{ender}"

	return result

def init_app():
	app = QApplication(sys.argv)
	# creating main window
	mw = MainWindow("Password Generator")
	mw.show()
	sys.exit(app.exec_())

def main():
	init_app()

if __name__ == '__main__':
	main()
