# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'profileselect.ui'
#
# Created: Fri Oct 27 01:34:01 2017
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

class Ui_ProfileSelectWidget(object):
    def setupUi(self, ProfileSelectWidget):
        ProfileSelectWidget.setObjectName(_fromUtf8("ProfileSelectWidget"))
        ProfileSelectWidget.resize(173, 546)
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
        self.bRotationVelocity = QtGui.QPushButton(self.frame)
        self.bRotationVelocity.setObjectName(_fromUtf8("bRotationVelocity"))
        self.gridLayout_2.addWidget(self.bRotationVelocity, 4, 0, 1, 1)
        self.gridLayout_3.addWidget(self.frame, 3, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 57, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 8, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(17, 80, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 1)

        self.retranslateUi(ProfileSelectWidget)
        QtCore.QMetaObject.connectSlotsByName(ProfileSelectWidget)

    def retranslateUi(self, ProfileSelectWidget):
        ProfileSelectWidget.setWindowTitle(_translate("ProfileSelectWidget", "Select Profile", None))
        self.lSelectProfile.setText(_translate("ProfileSelectWidget", "Select a Profile to Fit", None))
        self.bIonTemperature.setToolTip(_translate("ProfileSelectWidget", "Unit: keV", None))
        self.bIonTemperature.setText(_translate("ProfileSelectWidget", "Ion Temperature", None))
        self.bElectronDensity.setToolTip(_translate("ProfileSelectWidget", "Unit: 10^{19}m^{-3}", None))
        self.bElectronDensity.setText(_translate("ProfileSelectWidget", "Electron Density", None))
        self.bElectronTemperature.setToolTip(_translate("ProfileSelectWidget", "Unit: keV", None))
        self.bElectronTemperature.setText(_translate("ProfileSelectWidget", "Electron Temperature", None))
        self.bRotationVelocity.setToolTip(_translate("ProfileSelectWidget", "Unit: km/s", None))
        self.bRotationVelocity.setText(_translate("ProfileSelectWidget", "Rotation Velocity", None))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ProfileSelectWidget = QtGui.QWidget()
    ui = Ui_ProfileSelectWidget()
    ui.setupUi(ProfileSelectWidget)
    ProfileSelectWidget.show()
    sys.exit(app.exec_())

