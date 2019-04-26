# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting.ui'
#
# Created: Thu Dec 29 09:21:03 2016
#      by: PyQt4 UI code generator 4.9.6
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

class Ui_Setting(object):
    def setupUi(self, Setting):
        Setting.setObjectName(_fromUtf8("Setting"))
        Setting.resize(408, 169)
        self.gridLayout = QtGui.QGridLayout(Setting)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Setting)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.label_2 = QtGui.QLabel(Setting)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.label_3 = QtGui.QLabel(Setting)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 3, 1, 1)
        self.cbFittingRange = QtGui.QComboBox(Setting)
        self.cbFittingRange.setObjectName(_fromUtf8("cbFittingRange"))
        self.cbFittingRange.addItem(_fromUtf8(""))
        self.cbFittingRange.addItem(_fromUtf8(""))
        self.cbFittingRange.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cbFittingRange, 0, 4, 1, 1)
        self.line = QtGui.QFrame(Setting)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 1, 0, 1, 5)
        self.label1 = QtGui.QLabel(Setting)
        self.label1.setObjectName(_fromUtf8("label1"))
        self.gridLayout.addWidget(self.label1, 2, 0, 1, 1)
        self.cbGridSize = QtGui.QComboBox(Setting)
        self.cbGridSize.setObjectName(_fromUtf8("cbGridSize"))
        self.cbGridSize.addItem(_fromUtf8(""))
        self.cbGridSize.addItem(_fromUtf8(""))
        self.cbGridSize.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cbGridSize, 2, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Setting)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 2, 1, 3)

        self.retranslateUi(Setting)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Setting.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Setting.reject)
        QtCore.QMetaObject.connectSlotsByName(Setting)

    def retranslateUi(self, Setting):
        Setting.setWindowTitle(_translate("Setting", "Setting", None))
        self.label.setText(_translate("Setting", "Fitting Range:", None))
        self.label_2.setText(_translate("Setting", "0", None))
        self.label_3.setText(_translate("Setting", "~", None))
        self.cbFittingRange.setItemText(0, _translate("Setting", "1.0", None))
        self.cbFittingRange.setItemText(1, _translate("Setting", "1.1", None))
        self.cbFittingRange.setItemText(2, _translate("Setting", "1.2", None))
        self.label1.setText(_translate("Setting", "Grid Size:", None))
        self.cbGridSize.setItemText(0, _translate("Setting", "51", None))
        self.cbGridSize.setItemText(1, _translate("Setting", "101", None))
        self.cbGridSize.setItemText(2, _translate("Setting", "201", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Setting = QtGui.QDialog()
    ui = Ui_Setting()
    ui.setupUi(Setting)
    Setting.show()
    sys.exit(app.exec_())

