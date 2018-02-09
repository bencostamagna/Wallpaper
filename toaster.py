from PyQt5.QtWidgets import (QMessageBox,QApplication, QWidget, QToolTip, QPushButton,
                             QDesktopWidget, QMainWindow, QAction, qApp, QToolBar, QVBoxLayout,
                             QComboBox,QLabel,QLineEdit,QGridLayout,QMenuBar,QMenu,QStatusBar,
                             QTextEdit,QDialog,QFrame,QProgressBar
                             )
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon,QFont,QPixmap,QPalette
from PyQt5.QtCore import QCoreApplication, Qt,QBasicTimer

import sys, threading, configparser, time
import ctypes

class RefreshScheduler(QtCore.QThread):
    refresh_signal = QtCore.pyqtSignal()

    def __init__(self, delay):
        QtCore.QThread.__init__(self)
        self.delay = delay

    def run(self):
        while 1:
            self.refresh_signal.emit()
            # display.loadText()
            print("sleeps " + str(self.delay))
            time.sleep(self.delay)

class Toaster(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mwidget = QMainWindow(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnBottomHint)

        self.lbl = QLabel(self)
        self.lbl.setFont(QFont('Times New Roman', 15, QFont.StyleItalic))
        self.lbl.setStyleSheet("background-color: #f5dfc9;"
                               "border: 1px solid gray;"
                               "color: #444444;")

        config = configparser.ConfigParser()
        config.read('wallpaper.ini')
        self.description_path = config["Files"]["description_path"];
        self.refresh_delay = int(config["Toaster"]["refresh_delay"]);
        if len(self.description_path) == 0:
            self.description_path="wallpaper.txt"

        scheduler = RefreshScheduler(self.refresh_delay)
        scheduler.refresh_signal.connect(self.loadText)
        scheduler.start()

        self.show()



    def loadText(self):
        with open(self.description_path) as f:
            description = f.read()
        if (len(description) == 0):
            description = "No description"

        screen_width=ctypes.windll.user32.GetSystemMetrics(0)
        # screen_height=ctypes.windll.user32.GetSystemMetrics(1)

        self.lbl.setText(description)

        width = self.lbl.fontMetrics().boundingRect(self.lbl.text()).width()+20
        height = self.lbl.fontMetrics().boundingRect(self.lbl.text()).height()+2
        self.lbl.setGeometry(0, 0,width,height)

        #size
        self.resize(width, height)
        self.move(screen_width - width, 0)


app = QApplication(sys.argv)
app.setStyleSheet("QMainWindow{background-color: transparent;border: 1px solid black}")

ex = Toaster()

sys.exit(app.exec_())
