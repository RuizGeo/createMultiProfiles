# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'multi_profiles_dialog_base.ui'
#
# Created: Wed May 27 18:51:57 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_multiProfilesWindow(object):
    def setupUi(self, multiProfilesWindow):
        multiProfilesWindow.setObjectName(_fromUtf8("multiProfilesWindow"))
        multiProfilesWindow.resize(488, 395)
        self.centralwidget = QtGui.QWidget(multiProfilesWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 11, 466, 351))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labelDrainNet = QtGui.QLabel(self.layoutWidget)
        self.labelDrainNet.setObjectName(_fromUtf8("labelDrainNet"))
        self.gridLayout.addWidget(self.labelDrainNet, 0, 0, 1, 1)
        self.labelRidge = QtGui.QLabel(self.layoutWidget)
        self.labelRidge.setObjectName(_fromUtf8("labelRidge"))
        self.gridLayout.addWidget(self.labelRidge, 2, 0, 1, 1)
        self.labelNearNeigh = QtGui.QLabel(self.layoutWidget)
        self.labelNearNeigh.setObjectName(_fromUtf8("labelNearNeigh"))
        self.gridLayout.addWidget(self.labelNearNeigh, 4, 0, 1, 1)
        self.lineEditNeaNeigh = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditNeaNeigh.setObjectName(_fromUtf8("lineEditNeaNeigh"))
        self.gridLayout.addWidget(self.lineEditNeaNeigh, 4, 1, 1, 1)
        self.labelLeafSize = QtGui.QLabel(self.layoutWidget)
        self.labelLeafSize.setObjectName(_fromUtf8("labelLeafSize"))
        self.gridLayout.addWidget(self.labelLeafSize, 4, 2, 1, 1)
        self.lineEditLeafSize = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditLeafSize.setObjectName(_fromUtf8("lineEditLeafSize"))
        self.gridLayout.addWidget(self.lineEditLeafSize, 4, 3, 1, 1)
        self.labelOutShp = QtGui.QLabel(self.layoutWidget)
        self.labelOutShp.setObjectName(_fromUtf8("labelOutShp"))
        self.gridLayout.addWidget(self.labelOutShp, 5, 0, 1, 1)
        self.pushButtonOutShp = QtGui.QPushButton(self.layoutWidget)
        self.pushButtonOutShp.setObjectName(_fromUtf8("pushButtonOutShp"))
        self.gridLayout.addWidget(self.pushButtonOutShp, 6, 3, 1, 1)
        self.pushButtonProcess = QtGui.QPushButton(self.layoutWidget)
        self.pushButtonProcess.setObjectName(_fromUtf8("pushButtonProcess"))
        self.gridLayout.addWidget(self.pushButtonProcess, 7, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(self.layoutWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 9, 0, 1, 4)
        self.pushButtonQuit = QtGui.QPushButton(self.layoutWidget)
        self.pushButtonQuit.setObjectName(_fromUtf8("pushButtonQuit"))
        self.gridLayout.addWidget(self.pushButtonQuit, 7, 3, 1, 1)
        self.comboBoxDrainNet = QtGui.QComboBox(self.layoutWidget)
        self.comboBoxDrainNet.setMinimumSize(QtCore.QSize(0, 0))
        self.comboBoxDrainNet.setObjectName(_fromUtf8("comboBoxDrainNet"))
        self.gridLayout.addWidget(self.comboBoxDrainNet, 1, 0, 1, 4)
        self.comboBoxRidge = QtGui.QComboBox(self.layoutWidget)
        self.comboBoxRidge.setMinimumSize(QtCore.QSize(0, 0))
        self.comboBoxRidge.setObjectName(_fromUtf8("comboBoxRidge"))
        self.gridLayout.addWidget(self.comboBoxRidge, 3, 0, 1, 4)
        self.lineEditOutShp = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditOutShp.setObjectName(_fromUtf8("lineEditOutShp"))
        self.gridLayout.addWidget(self.lineEditOutShp, 6, 0, 1, 3)
        self.labelNumVert = QtGui.QLabel(self.layoutWidget)
        self.labelNumVert.setText(_fromUtf8(""))
        self.labelNumVert.setObjectName(_fromUtf8("labelNumVert"))
        self.gridLayout.addWidget(self.labelNumVert, 8, 0, 1, 2)
        self.labelNumVertIter = QtGui.QLabel(self.layoutWidget)
        self.labelNumVertIter.setText(_fromUtf8(""))
        self.labelNumVertIter.setObjectName(_fromUtf8("labelNumVertIter"))
        self.gridLayout.addWidget(self.labelNumVertIter, 8, 2, 1, 1)
        multiProfilesWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(multiProfilesWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        multiProfilesWindow.setStatusBar(self.statusbar)

        self.retranslateUi(multiProfilesWindow)
        QtCore.QMetaObject.connectSlotsByName(multiProfilesWindow)

    def retranslateUi(self, multiProfilesWindow):
        multiProfilesWindow.setWindowTitle(_translate("multiProfilesWindow", "Create Multi Profiles", None))
        self.labelDrainNet.setText(_translate("multiProfilesWindow", "Drainage network", None))
        self.labelRidge.setText(_translate("multiProfilesWindow", "Ridge", None))
        self.labelNearNeigh.setText(_translate("multiProfilesWindow", "Nearest neighbors", None))
        self.labelLeafSize.setText(_translate("multiProfilesWindow", "Leaf size", None))
        self.labelOutShp.setText(_translate("multiProfilesWindow", "Output profiles", None))
        self.pushButtonOutShp.setText(_translate("multiProfilesWindow", "...", None))
        self.pushButtonProcess.setText(_translate("multiProfilesWindow", "Process", None))
        self.pushButtonQuit.setText(_translate("multiProfilesWindow", "Quit", None))

