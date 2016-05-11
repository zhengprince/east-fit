# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'profileselectwidget.ui'
#
# Created: Mon Apr 11 20:11:50 2016
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ProfileSelect(object):
    def setupUi(self, ProfileSelectWidget):
        ProfileSelectWidget.setObjectName(_fromUtf8("ProfileSelectWidget"))
        ProfileSelectWidget.resize(197, 546)
        self.gridLayout = QtGui.QGridLayout(ProfileSelectWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame_2 = QtGui.QFrame(ProfileSelectWidget)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 0, 0, 1, 1)
        self.lSelectProfile = QtGui.QLabel(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lSelectProfile.sizePolicy().hasHeightForWidth())
        self.lSelectProfile.setSizePolicy(sizePolicy)
        self.lSelectProfile.setAlignment(QtCore.Qt.AlignCenter)
        self.lSelectProfile.setObjectName(_fromUtf8("lSelectProfile"))
        self.gridLayout_3.addWidget(self.lSelectProfile, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 2, 0, 1, 1)
        self.frame = QtGui.QFrame(self.frame_2)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.bIonTemperature = QtGui.QPushButton(self.frame)
        self.bIonTemperature.setEnabled(True)
        self.bIonTemperature.setObjectName(_fromUtf8("bIonTemperature"))
        self.gridLayout_2.addWidget(self.bIonTemperature, 2, 0, 1, 1)
        self.bElectronDensity = QtGui.QPushButton(self.frame)
        self.bElectronDensity.setObjectName(_fromUtf8("bElectronDensity"))
        self.gridLayout_2.addWidget(self.bElectronDensity, 3, 0, 1, 1)
        self.bElectronTemperature = QtGui.QPushButton(self.frame)
        self.bElectronTemperature.setObjectName(_fromUtf8("bElectronTemperature"))
        self.gridLayout_2.addWidget(self.bElectronTemperature, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.frame, 3, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(17, 80, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 4, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 5, 0, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 57, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem4, 6, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 1)

        self.retranslateUi(ProfileSelectWidget)
        QtCore.QMetaObject.connectSlotsByName(ProfileSelectWidget)

    def retranslateUi(self, ProfileSelectWidget):
        ProfileSelectWidget.setWindowTitle(QtGui.QApplication.translate("ProfileSelectWidget", "Select Profile", None, QtGui.QApplication.UnicodeUTF8))
        self.lSelectProfile.setText(QtGui.QApplication.translate("ProfileSelectWidget", "Select a Profile to Fit", None, QtGui.QApplication.UnicodeUTF8))
        self.bIonTemperature.setText(QtGui.QApplication.translate("ProfileSelectWidget", "Ion Temperature", None, QtGui.QApplication.UnicodeUTF8))
        self.bElectronDensity.setText(QtGui.QApplication.translate("ProfileSelectWidget", "Electron Density", None, QtGui.QApplication.UnicodeUTF8))
        self.bElectronTemperature.setText(QtGui.QApplication.translate("ProfileSelectWidget", "Electron Temperature", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ProfileSelectWidget = QtGui.QWidget()
    ui = Ui_ProfileSelect()
    ui.setupUi(ProfileSelectWidget)
    ProfileSelectWidget.show()
    sys.exit(app.exec_())

