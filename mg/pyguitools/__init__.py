# -*- coding: utf-8 -*-
"""
collection of some functions and classes to use with PyQt4

provides functionality to easily save and restore gui state (gui_save, gui_restore),
a class to wrap formlayout to provide some easily accessible and editable settings,
a simple window to display a matplotlib plot
and a class to provide a graphical logger
"""
#get ready for python 3
from __future__ import absolute_import

# import the public functions, should keep the gui_tools namespace relatively clean   
from .Log import QtDockLog
from .gui_save_and_load import gui_save, gui_restore
from .plot_window import SimplePlotWindow
from .easy_edit_settings import easy_edit_settings