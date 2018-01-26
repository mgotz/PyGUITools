#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
a simple pyqt window with a matplotlib plot
"""
#get compatible to python3
from __future__ import absolute_import, division, print_function

import os

#enable compatibility to both pyqt4 and pyqt5
_modname = os.environ.setdefault('QT_API', 'pyqt')
assert _modname in ('pyqt', 'pyqt5')

if os.environ['QT_API'].startswith('pyqt'):
    try:
        if os.environ['QT_API'] == 'pyqt5':
            from PyQt5.QtWidgets import (QMainWindow, QWidget, QGridLayout, 
                                         QVBoxLayout, QStatusBar, QMenuBar, 
                                         QApplication)
            
            from PyQt5 import QtCore
            from matplotlib.backends.backend_qt5agg import (FigureCanvas, 
                                                            NavigationToolbar2QT)
        else:
            from PyQt4.QtGui import (QMainWindow, QWidget, QGridLayout, 
                                         QVBoxLayout, QStatusBar, QMenuBar, 
                                         QApplication)            
            from PyQt4 import QtCore
            from matplotlib.backends.backend_qt4agg import (FigureCanvas, 
                                                            NavigationToolbar2QT)
    except ImportError:
        raise ImportError("plot_window requires PyQt4 or PyQt5. " 
                          "QT_API: {!s}".format(os.environ['QT_API']))


from matplotlib.figure import Figure



# this should work for both API versions. If QStrings are used it will translate
# Strings to QString, if not it will do nothing
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class SimplePlotWindow(QMainWindow):
    """a window with a matplotlib plot
    """
    def __init__(self,parent=None,name="plot window"):
        QMainWindow.__init__(self, parent)
        
        self.setWindowTitle(name)
        self.setObjectName(name)
        self.resize(800, 600)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.imageLayout = QVBoxLayout()
        self.imageLayout.setObjectName(_fromUtf8("imageLayout"))
        self.gridLayout.addLayout(self.imageLayout, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 550, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        self.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(self)

        ###
        #matplotlib setup
        
        self.fig1 = Figure()
        self.ax1 = self.fig1.add_subplot(111)

        self.canvas = FigureCanvas(self.fig1)
        self.toolbar = NavigationToolbar2QT(self.canvas, None)

        self.imageLayout.addWidget(self.canvas)
        self.imageLayout.addWidget(self.toolbar)
        
################################################################

if __name__ == "__main__":

    # execute when run directly, but not when called as a module.
    
    import numpy as np    
    import sys
    
    app = QApplication(sys.argv)
    gui = SimplePlotWindow()
    x = np.linspace(0,4*np.pi,100)
    y = np.sin(x)
    gui.ax1.plot(x,y)
    gui.show()
    sys.exit(app.exec_())
