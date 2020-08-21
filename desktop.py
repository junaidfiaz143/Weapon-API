import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MyApp(QWidget):

	def __init__(self):
		super().__init__()
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
		# QApplication.setStyleSheet(self, 'QMainWindow{background-color: darkgray;border: 1px solid black;}')
		self.initUI()

	def closeEvent(self, event):

		msg_box = QMessageBox()
		msg_box.setIcon(QMessageBox.Warning)
		msg_box.setWindowTitle("Alert")
		msg_box.setWindowIcon(QIcon("static/images/logo.png"))
		msg_box.setText("Are you sure you want to exit the program?")
		msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		btnExit = msg_box.button(QMessageBox.Yes)
		btnExit.setText("Exit")

		retval = msg_box.exec_()

		if retval == QMessageBox.Yes:
			subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=self.pro.pid))
			event.accept()
		else:
			event.ignore()

	def initUI(self):

		self.web = QWebEngineView()
		self.web.setWindowTitle("Weapon Detection")
		self.web.setWindowIcon(QIcon("static/images/logo.png"))
		self.web.load(QUrl("http://localhost:5000/"))
		self.web.showMaximized()
		self.web.setContextMenuPolicy(Qt.NoContextMenu)
		self.web.show()
		self.web.loadFinished.connect(self.webpageLoaded)

		# os.system("conda activate tensorflow1")
		process = "app.py"

		self.pro = subprocess.Popen(["python", "{}".format(process)])

		self.web.closeEvent = self.closeEvent

	def webpageLoaded(self):
		QApplication.restoreOverrideCursor()

if __name__ == "__main__":

	app = QApplication(sys.argv)
	my_app = MyApp()
	sys.exit(app.exec_())

# pip install PyQt5
# pip install PyQtWebEngine