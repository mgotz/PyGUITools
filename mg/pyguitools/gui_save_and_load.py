#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
functions to save and restore pyqt gui contents
"""

from PyQt4 import QtGui
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
        if isinstance(obj, QtGui.QComboBox):
            name   = obj.objectName()      # get combobox name
            index  = obj.currentIndex()    # get current index from combobox
            text   = obj.itemText(index)   # get the text for current index
            settings.setValue(name, text)   # save combobox selection to settings
        if isinstance(obj, QtGui.QLineEdit):
            name = obj.objectName()
            value = str(obj.text())
            settings.setValue(name, value)
        if isinstance(obj, QtGui.QCheckBox):
            name = obj.objectName()
            state = obj.checkState()
            settings.setValue(name, state)
        if isinstance(obj, QtGui.QSpinBox) or isinstance(obj, QtGui.QDoubleSpinBox):
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
        if isinstance(obj, QtGui.QComboBox):
            name   = obj.objectName()
            value = unicode(settings.value(name))  

            if value == "":
                continue

            index = obj.findText(value)   #determine the index of the loaded text

            if index == -1:  # add to list if not found
                obj.insertItems(0,[value])
                index = obj.findText(value)
                obj.setCurrentIndex(index)
            else:
                obj.setCurrentIndex(index)   # set the correct index otherwise

        if isinstance(obj, QtGui.QLineEdit):
            name = obj.objectName()
            try:
                value = settings.value(name,type=str)  # get stored value from registry
            except TypeError:
                value = None
            if value != None:
                obj.setText(unicode(value))  # restore lineEditFile

        if isinstance(obj, QtGui.QCheckBox):
            name = obj.objectName()
            try:
                value = settings.value(name,type=bool)   # get stored value from registry
            except TypeError:
                value = None
            if value != None:
                obj.setChecked(value)   # restore checkbox
                
        if isinstance(obj, QtGui.QSpinBox):
            name = obj.objectName()
            try:
                value = settings.value(name,type=int)
            except TypeError:
                value = None
            if value != None:
                obj.setValue(value)

        if isinstance(obj, QtGui.QDoubleSpinBox):
            name = obj.objectName()
            try:
                value = settings.value(name,type=float)
            except TypeError:
                value = None
            if value != None:
                obj.setValue(value)