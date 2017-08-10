#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
a simple pyqt window with a matplotlib plot
"""

from PyQt4 import QtCore, QtGui

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg \
  import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class SimplePlotWindow(QtGui.QMainWindow):
    """a window with a matplotlib plot
    """
    def __init__(self,parent=None,name="plot window"):
        QtGui.QMainWindow.__init__(self, parent)
        
        self.setWindowTitle(name)
        self.setObjectName(name)
        self.resize(800, 600)
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.imageLayout = QtGui.QVBoxLayout()
        self.imageLayout.setObjectName(_fromUtf8("imageLayout"))
        self.gridLayout.addLayout(self.imageLayout, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 550, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(self)
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
    
    app = QtGui.QApplication(sys.argv)
    gui = SimplePlotWindow()
    x = np.linspace(0,4*np.pi,100)
    y = np.sin(x)
    gui.ax1.plot(x,y)
    gui.show()
    sys.exit(app.exec_())
