# -*- coding: utf-8 -*-
"""
Created on Fri May 08 18:37:15 2015

@author: egor
"""

import sys

from mapnWindow import Ui_mapnWindow
from PyQt4 import QtGui 

class Mapn (QtGui.QMainWindow, Ui_mapnWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
    
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    m = Mapn()
    m.show()
    app.exec_()