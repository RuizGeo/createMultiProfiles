# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_multi_profiles.ui'
#
# Created: Fri May 22 20:16:04 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

from ui_multi_profiles import Ui_multiProfilesWindow

#create the dialog 
class multiProfilesDialog (QtGui.QMainWindow,QtGui.QApplication):
    def __init__ (self):
        QtGui.QDialog.__init__(self)
        #set up the user interface from designer
        self.ui = Ui_multiProfilesWindow()
        
        self.ui.setupUi(self)

