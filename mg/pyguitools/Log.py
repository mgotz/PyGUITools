"""
FilterGui module of the Gui utility package MyGui

Naturally used within MainGui
stand-alone also possible with certain limitations

usage:
    from MyGui import Log
    Log.run()
"""

from PyQt4 import QtCore, QtGui

import os
import logging


### dummy class to define logging signal
class LogSignal(QtCore.QObject):
    """
        Dummy class to define customized logging signals
        
        usage:
            logSig = LogSignal()
            ### connect
            logSig.log.connect(SLOT)
            ...
            ### emit
            logSig.log.emit_log(str)
   """
    ### the signal
    log = QtCore.pyqtSignal(str)
    ### emit the signal
    def emit_log(self, text):
        self.log.emit(text)

        
class LogHandler(logging.Handler):
    """
        Customized logging.Handler class with color scheme own emit method
        
        usage (within Qt4 widget):
            self.logger = logging.getLogger()
            self.handler = LogHandler(self) ### pass Qt4 widget here!
            self.logger.addHandler(self.handler)      
   """
    
    def __init__(self, parent=None):
        ### run regular Handler __init__
        logging.Handler.__init__(self)
        
        self.parent = None
        ### create SIGNAL and connect to parent SLOT if parent widget was passed
        ### parent widget must have SLOT method defined
        if parent:
            self.parent = parent
            self.logSig = LogSignal()
            self.logSig.log.connect(parent.printLog)
        
    _use_colors = True
        
    COLORS = {
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'orange',
        'ERROR': 'red',
        'CRITICAL': 'red'
    }
    
    def emit(self, record):
        
        text = str(self.format(record))
        ### emit signal if parent was passed
        if self.parent:
            ### color text 
            if LogHandler._use_colors:
                text = "<font color='%s'> %s </font>" \
                        % ( LogHandler.COLORS[record.levelname], text)
            self.logSig.emit_log(text)
        ### otherwise just print log message
        else:
            print text


class LogFormat(logging.Formatter):
    """
        Customized logging.Formatter with different formatting for the levels
        
        usage (within Qt4 widget):
            self.logger = logging.getLogger()
            self.handler = LogHandler(self) ### pass Qt4 widget here!
            self.handler.setFormatter(LogFormat())
            self.logger.addHandler(self.handler)           
   """    
#Andreas's Formatters:   
#    dbg_fmt  = "[DEBUG] %(module)s:%(funcName)s line:%(lineno)d >> %(msg)s"
#    info_fmt = "[INFO] %(module)s:%(funcName)s >> %(msg)s"
#    warn_fmt = "[WARNING] %(module)s:%(funcName)s >> %(msg)s"
#    err_fmt  = "[ERROR] %(module)s:%(funcName)s >> %(msg)s"
#My Formattes (prints just the messages):
#   
    dbg_fmt  = "[DEBUG]%(asctime)s %(msg)s"
    info_fmt = "[INFO]%(asctime)s %(msg)s"
    warn_fmt = "[WARNING]%(asctime)s %(msg)s"
    err_fmt  = "[ERROR]%(asctime)s %(msg)s"
    crit_fmt = "[CRITICAL]%(asctime)s %(msg)s"
    datefmt = ""

    def __init__(self, fmt="%(levelno)s: %(msg)s",datefmt=None,infoString=True):
        logging.Formatter.__init__(self, fmt,datefmt)
        self.datefmt = datefmt
        
        if not infoString:
            self.info_fmt = "%(asctime)s %(msg)s"

    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == 10:   # DEBUG
            self._fmt = self.dbg_fmt

        elif record.levelno == 20: # INFO
            self._fmt = self.info_fmt

        elif record.levelno == 30: # WARNING
            self._fmt = self.warn_fmt

        elif record.levelno == 40: # ERROR
            self._fmt = self.err_fmt
            
        elif record.levelno == 50: # CRITICAL
            self._fmt = self.crit_fmt


        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._fmt = format_orig

        return result
    
        
        
### import ui created with qtdesigner
### create python file with: 
### pyuic4 Log.ui > ui_Log.py
from ui_Log import Ui_DockWidget

class QtDockLog(QtGui.QDockWidget):
    """
    Log Dock Widget to use in a PyQt GUI 
    Will output all the logging.info(), logging.debug() etc. info
    
    usage:
        log_dock = QtDockLog()
        addDockWidget(QtCore.Qt.BottomDockWidgetArea, log_dock)
    """    

    def __init__(self,datefmt=None,infoString = True):
        """Constructor of the QtDockLog
        
        Log Dock Widget to use in a PyQt GUI.
        Will output all info written to logging.info(), logging..debug() etc.
    
        usage:
            log_dock = QtDockLog()
            addDockWidget(QtCore.Qt.BottomDockWidgetArea, log_dock)
        
            
        Parameters
        ---------
        datefmt : format string, optional
            format string for date time in log messages
        
        infoString : bool, optional
            if false info messages are not prefixed with the log level string
        """
        
        QtGui.QDockWidget.__init__(self)
        
        # Set up the user interface from Designer.
        self.ui =  Ui_DockWidget()
        self.ui.setupUi(self)
        
        ### define logger and handler
        self.logger = logging.getLogger()
        self.handler = LogHandler(self)
        self.handler.setFormatter(LogFormat(datefmt=datefmt,infoString=infoString))
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.handler)
        
        # define file for the second handler, saving the complete log to file
        self.filename = "log.out"
        # remove possibly existing log file (otherwise it appends to it)
        try:
            os.remove(self.filename) 
        except:
            pass
        
        # define second file handler, saving all of the log to self.filename
        self.filehandler = logging.FileHandler(self.filename)
        self.filehandler.setLevel(logging.DEBUG)   # set to DEBUG --> saves all
        self.filehandler.setFormatter(LogFormat(datefmt=datefmt,infoString=infoString)) # use the same format
        self.logger.addHandler(self.filehandler)   # attach to logger
             
        ### connections
        self.ui.comboBox.currentIndexChanged.connect(
                        lambda: self.setLevel(self.ui.comboBox.currentText()))
        self.ui.pushButtonSave.clicked.connect(self.saveLog) 


    def saveLog(self):
        """
        Saves the shown log to file 'filename'
        """
        savePath =QtGui.QFileDialog.getSaveFileName(self,'select save file')
        if savePath != '':
            text = str(self.ui.textBrowser.toPlainText())   # get log text 
            f = open(savePath, 'w')                   # open file
            f.writelines(text)                              # write text to file
            f.close()                                       # close file


    def setLevel(self, level):
        """
        Sets the the widget to show only log entries above and equal to
        the given level.
        """
        level = str(level).upper()
        level_int = eval("logging.%s" %(level))
        # clear the text window
        self.ui.textBrowser.clear()
        # open the log file
        f = open(self.filename, 'r')
        # go through lines in log file
        for line in f:
            line = line.strip()                      # delete end of line
            try:
                level_line = line.split('[')[1].split(']')[0]      # get level of line
            except IndexError:
                level_line = "INFO"                                 #default to info
                
            level_line_int = eval("logging.%s" %(level_line))
            # if number of line level is greater equal to number of 
            #  the global level, append to text in color
            if level_line_int >= level_int:
                text = "<font color='%s'> %s </font>" \
                            % ( self.handler.COLORS[level_line], line)
                self.ui.textBrowser.append(text)
        # close file        
        f.close()
              
        cmd = "self.handler.setLevel(logging.%s)" % (level)
        eval(cmd)
        ### print new level
        self.logger.debug("Logging level set to %s." %(level))
        
    ### pyQt SLOT used to receive emitted SIGNAL from LogHandler()
    ### pass self to LogHandler to make this work   
    @QtCore.pyqtSlot(str)
    def printLog(self, text):
        self.ui.textBrowser.append(text)
  
  
        
def run():
    import sys
    
    app = QtGui.QApplication(sys.argv)
    win = QtGui.QMainWindow()
    win.addDockWidget(QtCore.Qt.TopDockWidgetArea, QtDockLog())
    win.show()
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
    run()
