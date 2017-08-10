#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
easily editable settings: wrapper around formlayout
"""

from formlayout import fedit

class EasyEditSettings():
    """a class around formlayout to give easy to use settings
    
    initalized with a list of tuples that specifiy the settings it can return
    a dictionary with the settings to easily use in the application
    """
    def __init__(self, settings):
        """ initialize the advanced settings
        
        Parameters
        ----------
        setting : list of tuples
            each entry in the list is a setting with its name as the first 
            element and current value as second like for formlayout from fedit
        """
        self.settingsDict = {}
        self.settingsList = settings
        self.update_dict()

                
    def update_dict(self):
        for element in self.settingsList:
            if type(element[1]) == list:
                self.settingsDict[element[0]] = element[1][element[1][0]+1]
            else:
                self.settingsDict[element[0]] = element[1]
    
    def get_settings(self):
        return self.settingsDict
        
    def change_settings(self, title="Edit advanced settings" ):
        newSettings = fedit(self.settingsList, title=title)
        if newSettings != None:
            for i, newSetting in enumerate(newSettings):
                if type(self.settingsList[i][1]) == list:
                    tempList = self.settingsList[i][1]
                    tempList[0] = newSetting
                    self.settingsList[i] = (self.settingsList[i][0],tempList)
                else:
                    self.settingsList[i] = (self.settingsList[i][0],newSetting)
            self.update_dict()