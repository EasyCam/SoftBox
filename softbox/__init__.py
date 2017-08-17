# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'soft.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

import sys
import re
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QFrame, QApplication)
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout,QHBoxLayout, QSizePolicy, QMessageBox, QWidget
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SoftBox(QMainWindow,QFrame):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('SoftBox')
        self.create_main_frame()

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 100
        self.col = QColor(255, 255, 255, 0)

        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

        self.square = QFrame(self)
        #self.square.setGeometry(20, 20, 100, 100)
        #self.square.setStyleSheet("QWidget { background-color: %s }" %self.col.name())

        self.setStyleSheet("QWidget { background-color: %s }" % self.col.name())

        self.Slider_R = QtWidgets.QSlider()
        self.Slider_R.setOrientation(QtCore.Qt.Horizontal)
        self.Slider_R.setObjectName("Slider_R")

        self.Slider_R.setRange(0,255)
        self.Slider_R.setValue(255)
        self.Slider_R.setTracking(True)
        self.Slider_R.valueChanged.connect(self.setColor)

        self.Slider_G = QtWidgets.QSlider()
        self.Slider_G.setOrientation(QtCore.Qt.Horizontal)
        self.Slider_G.setObjectName("Slider_G")

        self.Slider_G.setRange(0,255)
        self.Slider_G.setValue(255)
        self.Slider_G.setTracking(True)
        self.Slider_G.valueChanged.connect(self.setColor)

        self.Slider_B = QtWidgets.QSlider()
        self.Slider_B.setOrientation(QtCore.Qt.Horizontal)
        self.Slider_B.setObjectName("Slider_B")

        self.Slider_B.setRange(0,255)
        self.Slider_B.setValue(255)
        self.Slider_B.setTracking(True)
        self.Slider_B.valueChanged.connect(self.setColor)


        self.label_R = QtWidgets.QLabel()
        self.label_R.setObjectName("R")
        self.label_R.setText('R')

        self.label_G = QtWidgets.QLabel()
        self.label_G.setObjectName("G")
        self.label_G.setText('G')

        self.label_B = QtWidgets.QLabel()
        self.label_B.setObjectName("B")
        self.label_B.setText('B')


        self.label_R.setText("R " + "%03d" %(self.Slider_R.value()))
        self.label_G.setText("G " + "%03d" %(self.Slider_G.value()))
        self.label_B.setText("B " + "%03d" %(self.Slider_B.value()))

        for w in [self.label_R,self.Slider_R,self.label_G,self.Slider_G,self.label_B,self.Slider_B]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox.addWidget(self.square)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)


        self.show()



    def setColor(self):



        Rval = int(self.Slider_R.value())
        Gval = int(self.Slider_G.value())
        Bval = int(self.Slider_B.value())


        self.label_R.setText("R " + "%03d" %(self.Slider_R.value()))
        self.label_G.setText("G " + "%03d" %(self.Slider_G.value()))
        self.label_B.setText("B " + "%03d" %(self.Slider_B.value()))


        self.col.setRed(Rval)

        self.Rcol = QColor(0, 0, 0, 0)
        self.Rcol.setRed(Rval)

        #self.label_R.setStyleSheet("QWidget { background-color: %s }" %self.Rcol.name())

        #self.Slider_R.setStyleSheet("QWidget { background-color: %s }" %self.Rcol.name())


        self.col.setGreen(Gval)

        self.Gcol = QColor(0, 0, 0, 0)
        self.Gcol.setGreen(Gval)
        #self.label_G.setStyleSheet("QWidget { background-color: %s }" %self.Gcol.name())

        #self.Slider_G.setStyleSheet("QWidget { background-color: %s }" %self.Gcol.name())



        self.col.setBlue(Bval)
        self.Bcol = QColor(0, 0, 0, 0)
        self.Bcol.setBlue(Bval)
        #self.label_B.setStyleSheet("QWidget { background-color: %s }" %self.Bcol.name())

        #self.Slider_B.setStyleSheet("QWidget { background-color: %s }" %self.Bcol.name())

        #self.square.setStyleSheet("QWidget { background-color: %s }" % self.col.name())

        self.setStyleSheet("QWidget { background-color: %s }" % self.col.name())
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = SoftBox()
    sys.exit(app.exec_())

def begin():
    app = QApplication(sys.argv)
    ex = SoftBox()
    sys.exit(app.exec_())



if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())