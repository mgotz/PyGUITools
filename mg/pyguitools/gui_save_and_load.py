#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
functions to save and restore pyqt gui contents
"""

#get compatible to python3
from __future__ import absolute_import, division, print_function
from builtins import str #use instead of pyhton2 unicode()

import os

#enable compatibility to both pyqt4 and pyqt5
_modname = os.environ.setdefault('QT_API', 'pyqt')
assert _modname in ('pyqt', 'pyqt5')

if os.environ['QT_API'].startswith('pyqt'):
    try:
        if os.environ['QT_API'] == 'pyqt5':
            from PyQt5.QtWidgets import (QComboBox, QLineEdit, QCheckBox, 
                                         QSpinBox, QDoubleSpinBox)
        else:
            from PyQt4.QtGui import (QComboBox, QLineEdit, QCheckBox, 
                                         QSpinBox, QDoubleSpinBox)
    except ImportError:
        raise ImportError("plot_window requires PyQt4 or PyQt5. " 
                          "QT_API: {!s}".format(os.environ['QT_API']))

import inspect

def gui_save(ui, settings):
    """Saves the content of the ui elements into settings.
    
    Currently handles comboboxes, line-edits, check-boxes and spin-boxes
    all other elements are ignored.
    
    Parameters
    ---------------
    ui : pyqt UI
        The object should contain the ui elements to save as children
    settings : QtCore.QSettings object
        The settings object to save the information to, should be an instance
        of QtCore.QSettings
    """

    #get all the children of the ui
    for name, obj in inspect.getmembers(ui):
        #different fields need slightly different things to be saved
        if isinstance(obj, QComboBox):
            name   = obj.objectName()      # get combobox name
            index  = obj.currentIndex()    # get current index from combobox
            text   = obj.itemText(index)   # get the text for current index
            settings.setValue(name, text)   # save combobox selection to settings
        if isinstance(obj, QLineEdit):
            name = obj.objectName()
            value = str(obj.text())
            settings.setValue(name, value)
        if isinstance(obj, QCheckBox):
            name = obj.objectName()
            state = obj.checkState()
            settings.setValue(name, state)
        if isinstance(obj, QSpinBox) or isinstance(obj, QDoubleSpinBox):
            name = obj.objectName()
            value = obj.value()
            settings.setValue(name,value)
            
def gui_restore(ui, settings):
    """Restores the content of the ui elements from settings.
    
    Currently handles comboboxes, line-edits, check-boxes and spin-boxes
    all other elements are ignored.
    
    Parameters
    ---------------
    ui : pyqt UI
        The object should contain the ui elements to restore as children
    settings : QtCore.QSettings object
        The settings object containing the information to restore, 
        should be an instance of QtCore.QSettings
    """
    
    #iterate over the child items and try to load something for each item
    for name, obj in inspect.getmembers(ui):
        if isinstance(obj, QComboBox):
            name   = obj.objectName()
            value = str(settings.value(name))  

            if value == "":
                continue

            index = obj.findText(value)   #determine the index of the loaded text

            if index == -1:  # add to list if not found
                obj.insertItems(0,[value])
                index = obj.findText(value)
                obj.setCurrentIndex(index)
            else:
                obj.setCurrentIndex(index)   # set the correct index otherwise

        if isinstance(obj, QLineEdit):
            name = obj.objectName()
            try:
                value = settings.value(name,type=str)  # get stored value from registry
            except TypeError:
                value = None
            if value != None:
                obj.setText(str(value))  # restore lineEditFile

        if isinstance(obj, QCheckBox):
            name = obj.objectName()
            try:
                value = settings.value(name,type=bool)   # get stored value from registry
            except TypeError:
                value = None
            if value != None:
                obj.setChecked(value)   # restore checkbox
                
        if isinstance(obj, QSpinBox):
            name = obj.objectName()
            try:
                value = settings.value(name,type=int)
            except TypeError:
                value = None
            if value != None:
                obj.setValue(value)

        if isinstance(obj, QDoubleSpinBox):
            name = obj.objectName()
            try:
                value = settings.value(name,type=float)
            except TypeError:
                value = None
            if value != None:
                obj.setValue(value)