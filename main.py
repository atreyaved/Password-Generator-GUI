#!/usr/bin/env python3
import sys
import os

# Libraries
from PyQt5.QtWidgets import *

from PyQt5.QtGui import QPixmap, QIcon, QFontDatabase, QKeySequence
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

import pyperclip
import PREFS

# Dependencies
import resources # .qrc file (Qt Resources)
import password_generator as password
from scrollable import ScrolLabel

class MainWindow(QMainWindow):
	resized = QtCore.pyqtSignal()
	def __init__(self, title, parent=None):
		super().__init__(parent)
		
		self.title = title
		
		# MainWidget icon
		self.scriptDir = os.path.dirname(os.path.realpath(__file__))
		self.setWindowIcon(QtGui.QIcon(':/icon.png'))
		
		self.resized.connect(self.on_resize)

		statusBar = QStatusBar()
		statusBar.setStyleSheet("background: #383838; color: white;")
		self.setStatusBar(statusBar)

		self.create_window()
		self.create_menu_bar()

	def resizeEvent(self, event):
		self.resized.emit()
		return super(MainWindow, self).resizeEvent(event)

	def on_resize(self):
		pass
	
	def create_window(self):
		# Window settings
		self.setWindowTitle(self.title)
		self.setMinimumSize(500, 470)
		self.setStyleSheet(
			"""
			QWidget {
				background: #323232;
			}
			"""
		)

		# creating MainWidget widget and setting it as central
		self.app_widget = MainWidget(parent=self)
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

		menu_stylesheet = (
			"QMenu {"
			"	background: #383838;"
			"	color: #ABABAB;"
			"	font-size: 15px;"
			"}"
			"QMenu::item:selected {"
			"	background: #4C4C4C;"
			"	color: #ffffff;"
			"}"
			"QMenu::item:pressed {"
			"	background: #595959;"
			"}"
		)

		# File menu
		file_menu = bar.addMenu('&File')
		file_menu.setStyleSheet(menu_stylesheet)
	
		settings_action = self.create_qaction(
			menu=file_menu, 
			text="Settings", 
			shortcut="Ctrl+S", 
			callback=self.app_widget.create_settings_dialog)

		close_action = self.create_qaction(
			menu=file_menu, 
			text="Close", 
			shortcut="Ctrl+Q", 
			callback=self.close_app)

		# Edit menu
		edit_menu = bar.addMenu('&Edit')
		edit_menu.setStyleSheet(menu_stylesheet)

		generate_action = self.create_qaction(
			menu=edit_menu, 
			text="Generate", 
			shortcut="Ctrl+G", 
			callback=self.app_widget.generate_password)

		copy_action = self.create_qaction(
			menu=edit_menu, 
			text="Copy", 
			shortcut="Ctrl+C", 
			callback=self.app_widget.copy_password)

		# About menu
		about_menu = bar.addMenu('&About')
		about_menu.setStyleSheet(menu_stylesheet)

		about_me_action = self.create_qaction(
			menu=about_menu, 
			text="About Password Generator GUI", 
			shortcut="Ctrl+P", 
			callback=self.app_widget.create_about_me_dialog)

	def create_qaction(self, menu, text: str, shortcut: str="", callback: callable=lambda: print("No callback")):
		action = QAction(self)

		if shortcut != "": # If the shortcut isn't empty
			key = shortcut.split("+")[0] # Split by + and get the modifier key (ctrl, shift, alt)
			mnemo = shortcut.split("+")[1] # Split by + and get the key (a, b, c)
			
			shortcut_text = text.replace(mnemo, f"&{mnemo}", 1) # Underline the shortut letter 

		action.setText(shortcut_text)
		action.setShortcut(shortcut)

		menu.addAction(action)
		
		action.triggered.connect(callback)

		return action

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

	def closeEvent(self, event):
		self.close_app()
		event.accept()

class MainWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__()

		self.parent = parent
		self.widgets = {
			"logo": [], 
			"generate_btn": [], 
			"copy_btn": [], 
			"label": [], 
		}

		self.init_prefs()

		self.create_window()

	def init_prefs(self):
		prefs = {"lowercase": True, "uppercase": True, "digits": True, "punctuation": True, "repeated_char": False, "consecutive_char": False, "length":15}

		self.settings = PREFS.PREFS(prefs, filename="Prefs/settings")
 
	def create_window(self):
		##### Creating window
		self.app = QApplication(sys.argv)

		# Setting grid
		self.setLayout(QGridLayout())

		# FONTS
		QFontDatabase.addApplicationFont(':/impact.ttf')

		# First frame
		self.main_frame()

	def clear_widgets(self):
		for key, val in self.widgets.items():
			if val != []:
				self.val[-1].hide()
			
			for i in range(len(val)):
				val.pop()

	def main_frame(self):
		# Logo
		logo = QLabel("&lt;<span style='color:#64a314'>/</span><span style='color:#ffffff'>P45w0rD<br/>G3n3R4t0r</span><span style='color:#64a314'>/</span>&gt;")
		logo.setStyleSheet("font-size: 80px; font-family: impact;")

		#logo.setPixmap(image)
		logo.setAlignment(QtCore.Qt.AlignCenter)
		self.widgets["logo"].append(logo)

		##### Buttons #####
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
			'''
		)
		
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
			'''
		) 

		copy_btn.clicked.connect(self.copy_password)
		self.widgets["copy_btn"].append(copy_btn)

		# Password label
		scrollable = ScrolLabel()		

		scrollable.label.setAlignment(QtCore.Qt.AlignCenter)
		
		scrollable.label.setCursor(QCursor(QtCore.Qt.IBeamCursor))
		
		scrollable.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
		scrollable.label.setContextMenuPolicy(Qt.CustomContextMenu)
		scrollable.label.customContextMenuRequested.connect(lambda *args, **kwargs: None)
	
		scrollable.label.setStyleSheet(
			"font-size: 25px;" + 
			"color: white;" +
			"padding: 10px 10px 10px 10px;" + 
			"background: '#64A314';" +
			"border-radius: 30px;" +
			"margin: 10px 0px 0px 0px;"
		)

		scrollable.setFixedHeight(120)

		self.widgets["label"].append(scrollable)
		self.generate_password()

		# Setting widgets in grid
		self.layout().addWidget(self.widgets["logo"][-1], 0, 0, 1, 0)
		self.layout().addWidget(self.widgets["generate_btn"][-1], 1, 0, 1, 0)
		self.layout().addWidget(self.widgets["copy_btn"][-1], 2, 2)
		self.layout().addWidget(self.widgets["label"][-1], 2, 0)

	def create_settings_dialog(self):
		def reset_settings():
			self.settings.overwrite_prefs()

			lower_check.setChecked(self.settings.file["lowercase"])
			upper_check.setChecked(self.settings.file["uppercase"])
			digits_check.setChecked(self.settings.file["digits"])
			punct_check.setChecked(self.settings.file["punctuation"])
			repeated_char_check.setChecked(self.settings.file["repeated_char"])
			consecutive_char_check.setChecked(self.settings.file["consecutive_char"])

			length_spinbox.setValue(self.settings.file["length"])

		######## SET UP DIALOG ########
		dialog = QDialog() # Creating dialog

		dialog.setWindowTitle("Settings") # Setting dialog title

		dialog.setWindowModality(Qt.ApplicationModal) # True blocks its parent window
		dialog.setLayout(QGridLayout())

		## Adding widgets ##
		dialog_stylesheet = """
			QDialog {
				background: #383838;
				color: #383838;
			}
			QSpinBox {
				background: #383838;
				color: white;
			}
			"""
		
		checkbox_stylesheet = '''
			*{
				color: #E1E1E1;
				padding: 2px 0px;
			}
			*:hover {
				color: #ffffff;
			}
			*::indicator{
				width: 15px;
				height: 15px;
			}
			*::indicator:checked {
				image: url(:/checkbox_checked.png);
			}
			'''

		button_stylesheet = '''
			*{
				color: white;
				background: #383838;
			}
			*:hover {
				background: #484848;
			}
			'''

		tooltip_stylesheet = (
			"QToolTip {"
			"	background: #383838;"
			"	border: 1px solid #BC006C;"
			"	border-radius: 5px;"
			"	color: #ffffff;"
			"	padding: 2px;"
			"}"
			)

		dialog.setStyleSheet(dialog_stylesheet + tooltip_stylesheet) # Setting dialog styling

		lower_check = self.create_checkbox("ASCII lowercase", 
			stylesheet=checkbox_stylesheet, 
			checked=self.settings.file["lowercase"], 
			callback=lambda: self.settings.write_prefs("lowercase", lower_check.isChecked()), 
			tooltip="Lowercase letters.")

		upper_check = self.create_checkbox("ASCII uppercase", 
			stylesheet=checkbox_stylesheet, 
			checked=self.settings.file["uppercase"], 
			callback=lambda: self.settings.write_prefs("uppercase", upper_check.isChecked()), 
			tooltip="Uppercase letters.")
		
		digits_check = self.create_checkbox("Digits (1, 2...)", 
			stylesheet=checkbox_stylesheet, 
			checked=self.settings.file["digits"], 
			callback=lambda: self.settings.write_prefs("digits", digits_check.isChecked()), 
			tooltip="Numbers from 0 to 9.")

		punct_check = self.create_checkbox("Punctuation", 
			stylesheet=checkbox_stylesheet, 
			checked=self.settings.file["punctuation"], 
			callback=lambda: self.settings.write_prefs("punctuation", punct_check.isChecked()), 
			tooltip="Punctuation marks.")

		repeated_char_check = self.create_checkbox("Repeated characters", 
			stylesheet=checkbox_stylesheet, 
			checked=self.settings.file["repeated_char"], 
			callback=lambda: self.settings.write_prefs("repeated_char", repeated_char_check.isChecked()), 
			tooltip="The password can include repeated characters.")

		consecutive_char_check = self.create_checkbox("Consecutive characters", 
			stylesheet=checkbox_stylesheet, 
			checked=self.settings.file["consecutive_char"], 
			callback=lambda: self.settings.write_prefs("consecutive_char", consecutive_char_check.isChecked()), 
			tooltip="Uppercase, lowercase, digits or punctuation can be consecutive (AB, ab, 01, !?).")

		length_spinbox = self.create_spinbox(
			minium=1, 
			maximum=10000, 
			prefix="Length: ",
			value=self.settings.file["length"], 
			callback=lambda: self.settings.write_prefs("length", length_spinbox.value()), 
			tooltip="The exact length of the password to generate."
		)

		save_btn = self.create_button(text="Close", 
			stylesheet=button_stylesheet, 
			callback=lambda: dialog.reject())
		save_btn.setDefault(True)

		reset_btn = self.create_button(text="Reset", 
			stylesheet=button_stylesheet, 
			callback=reset_settings)

		dialog.layout().addWidget(lower_check, 0, 0)
		dialog.layout().addWidget(upper_check, 1, 0)
		dialog.layout().addWidget(digits_check, 2, 0)
		dialog.layout().addWidget(punct_check, 3, 0)
		dialog.layout().addWidget(repeated_char_check, 4, 0)
		dialog.layout().addWidget(consecutive_char_check, 5, 0)
	
		dialog.layout().addWidget(length_spinbox, 6, 0)

		dialog.layout().addWidget(reset_btn, 7, 0)
		dialog.layout().addWidget(save_btn, 8, 0)

		self.settings_dialog = dialog

		dialog.exec_()

	def create_checkbox(self, 
		text: str, 
		stylesheet: str="", 
		checked: bool=True, 
		callback: callable=lambda x: print(f"No callback function {x}"), 
		tooltip: str=None):
		
		checkbox = QCheckBox(text)
		checkbox.setStyleSheet(stylesheet)
		checkbox.setChecked(checked)
		
		if not tooltip == None:
			checkbox.setToolTip(tooltip)

		checkbox.toggled.connect(callback)

		return checkbox

	def create_button(self, text: str, stylesheet: str="", callback: callable=lambda x: print(f"No callback function"), tooltip: str=None):
		button = QPushButton(text)
		button.setStyleSheet(stylesheet)
		button.clicked.connect(callback)

		if not tooltip == None:
			button.setToolTip(tooltip)

		return button

	def create_spinbox(self, 
		prefix: str="", 
		suffix: str="", 
		stylesheet: str="", 
		minium: int=0, 
		maximum: int=10000, 
		value: int=0, 
		callback: callable=lambda x: print(x), 
		tooltip: str=None):
		
		spinbox = QSpinBox()
		
		spinbox.setMinimum(minium)
		spinbox.setMaximum(maximum)
		
		spinbox.setPrefix(prefix)
		spinbox.setSuffix(suffix)

		spinbox.setValue(value)
		spinbox.setStyleSheet(stylesheet)

		if not tooltip == None:
			spinbox.setToolTip(tooltip)
	
		spinbox.valueChanged.connect(callback)

		return spinbox

	def create_about_me_dialog(self):
		######## SET UP DIALOG ########
		dialog = QDialog() # Creating dialog
		
		dialog.setWindowTitle("About me") # Setting dialog title
		dialog.setStyleSheet("background: #383838; color: #ffffff") # Setting dialog styling
		dialog.setWindowModality(True) # False blocks its parent window
		dialog.setLayout(QGridLayout())

		## Adding widgets ##
		about_label = QLabel("<strong>Password Generator <i>GUI</i></strong> is a simple app written in Python using PyQt5.<br/><br/>Contact me: <br/>&nbsp;&nbsp;&nbsp;&nbsp;Discord: patitotective#0127<br/>&nbsp;&nbsp;&nbsp;&nbsp;Mail: <a href='mailto:cristobalriaga@gmail.com' style='color: #8ebf42'>cristobalriaga@gmail.com</a>", dialog)
		about_label.setOpenExternalLinks(True)

		about_prefs_label = QLabel("<strong>Password Generator <i>GUI</i></strong> uses <a href='https://patitotective.github.io/PREFS' style='color: #8ebf42'>PREFS python library</a> to store the settings.")

		about_prefs_label.setStyleSheet("margin: 5px 0px 0px 0px;")
		about_prefs_label.setOpenExternalLinks(True)

		source_code_link = QLabel("<a href='https://github.com/Patitotective/password_generator_gui' style='color: #8ebf42'>Source code</a>", dialog)
		source_code_link.setOpenExternalLinks(True)

		dialog.layout().addWidget(about_label, 0, 0, 1, 1)
		dialog.layout().addWidget(about_prefs_label, 1, 0, 1, 1)
		dialog.layout().addWidget(QLabel(), 2, 0, 1, 1)
		dialog.layout().addWidget(source_code_link, 3, 1)
		dialog.layout().addWidget(QLabel("v0.1"), 3, 0)

		self.about_me_dialog = dialog

		dialog.exec_()

	def copy_password(self):
		# Get text from password label and copy it
		pyperclip.copy( self.widgets["label"][-1].label.text() )

		# Change copy button text from copy to copied
		self.widgets["copy_btn"][-1].setText("Copied!")

	def generate_password(self):
		# Generate a random password an set the password label text to it
		npassword = password.generate_password(
			chars=self.settings.file, 
			length=self.settings.file["length"], 
			repeated_char=self.settings.file["repeated_char"], 
			consecutive_char=self.settings.file["consecutive_char"])
		
		self.widgets["label"][-1].setText(npassword[0])

		self.parent.statusBar().showMessage(npassword[1])

		# Set copy button text to copy
		self.widgets["copy_btn"][-1].setText("Copy")

def init_app():
	app = QApplication(sys.argv)
	
	mainwindow = MainWindow("Password Generator")
	mainwindow.show()
	sys.exit(app.exec_())

def main():
	init_app()

if __name__ == '__main__':
	main()
