# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from photoviewer import PhotoViewer
from pyqtconsole.console import PythonConsole

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1440, 800)
        MainWindow.setMinimumSize(QtCore.QSize(1440, 800))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color:whitesmoke;\n"
"font-size:20px;\n"
"font-weight:bold;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridFrame = QtWidgets.QFrame(self.centralwidget)
        self.gridFrame.setSizeIncrement(QtCore.QSize(0, 4))
        self.gridFrame.setObjectName("gridFrame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridFrame)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.symbol_table = QtWidgets.QListView(self.gridFrame)
        self.symbol_table.setMinimumSize(QtCore.QSize(250, 0))
        self.symbol_table.setMaximumSize(QtCore.QSize(250, 16777215))
        self.symbol_table.setStyleSheet("border: 2px solid silver;")
        self.symbol_table.setProperty("isWrapping", True)
        self.symbol_table.setObjectName("symbol_table")
        self.gridLayout_2.addWidget(self.symbol_table, 0, 0, 1, 1)
        self.graphicsView = PhotoViewer(self.gridFrame)
        self.graphicsView.setStyleSheet("border: 2px solid silver;")
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_2.addWidget(self.graphicsView, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.gridFrame, 0, 0, 1, 1)
        self.console = PythonConsole(self.centralwidget)
        self.console.setMinimumSize(QtCore.QSize(0, 200))
        self.console.setMaximumSize(QtCore.QSize(16777215, 200))
        self.console.setSizeIncrement(QtCore.QSize(0, 1))
        self.console.setStyleSheet("QFrame{\n"
"border: 2px solid silver;\n"
"}")
        self.console.setObjectName("console")
        self.gridLayout.addWidget(self.console, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Easy Paging"))
