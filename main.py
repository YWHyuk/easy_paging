#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from gui import Ui_MainWindow
from memory import VirtualMachine

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.vm = VirtualMachine()
        self.ui.console.push_local_ns('vm', self.vm)
        #self.ui.console.setStyleSheet("color:#F8F8F2;")
        self.ui.console.eval_queued()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
