# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'profileselectwidget.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_ProfileSelectWidget(object):
    def setupUi(self, ProfileSelectWidget):
        ProfileSelectWidget.setObjectName(_fromUtf8("ProfileSelectWidget"))
        ProfileSelectWidget.resize(189, 363)
        self.gridLayout = QtGui.QGridLayout(ProfileSelectWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 57, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 6, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 5, 0, 1, 1)
        self.lSelectProfile = QtGui.QLabel(ProfileSelectWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lSelectProfile.sizePolicy().hasHeightForWidth())
        self.lSelectProfile.setSizePolicy(sizePolicy)
        self.lSelectProfile.setAlignment(QtCore.Qt.AlignCenter)
        self.lSelectProfile.setObjectName(_fromUtf8("lSelectProfile"))
        self.gridLayout.addWidget(self.lSelectProfile, 1, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 61, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 4, 0, 1, 1)
        self.frame = QtGui.QFrame(ProfileSelectWidget)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.bIonTemperature = QtGui.QPushButton(self.frame)
        self.bIonTemperature.setEnabled(False)
        self.bIonTemperature.setObjectName(_fromUtf8("bIonTemperature"))
        self.gridLayout_2.addWidget(self.bIonTemperature, 2, 0, 1, 1)
        self.bElectronDensity = QtGui.QPushButton(self.frame)
        self.bElectronDensity.setObjectName(_fromUtf8("bElectronDensity"))
        self.gridLayout_2.addWidget(self.bElectronDensity, 3, 0, 1, 1)
        self.bElectronTemperature = QtGui.QPushButton(self.frame)
        self.bElectronTemperature.setObjectName(_fromUtf8("bElectronTemperature"))
        self.gridLayout_2.addWidget(self.bElectronTemperature, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 3, 0, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 0, 0, 1, 1)

        self.retranslateUi(ProfileSelectWidget)
        QtCore.QMetaObject.connectSlotsByName(ProfileSelectWidget)

    def retranslateUi(self, ProfileSelectWidget):
        ProfileSelectWidget.setWindowTitle(_translate("ProfileSelectWidget", "Select Profile", None))
        self.lSelectProfile.setText(_translate("ProfileSelectWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Select a Profile to Fit</span></p></body></html>", None))
        self.bIonTemperature.setText(_translate("ProfileSelectWidget", "Ion Temperature", None))
        self.bElectronDensity.setText(_translate("ProfileSelectWidget", "Electron Density", None))
        self.bElectronTemperature.setText(_translate("ProfileSelectWidget", "Electron Temperature", None))

import res_rc
