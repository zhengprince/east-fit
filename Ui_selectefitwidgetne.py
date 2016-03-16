# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selectefitwidgetne.ui'
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

class Ui_SelectEfitNe(object):
    def setupUi(self, SelectEfitNe):
        SelectEfitNe.setObjectName(_fromUtf8("SelectEfitNe"))
        SelectEfitNe.resize(471, 516)
        self.gridLayout_2 = QtGui.QGridLayout(SelectEfitNe)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.frame = QtGui.QFrame(SelectEfitNe)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_7 = QtGui.QGridLayout(self.frame)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_7.addWidget(self.label, 0, 0, 1, 1)
        self.rbFile = QtGui.QRadioButton(self.frame)
        self.rbFile.setChecked(True)
        self.rbFile.setObjectName(_fromUtf8("rbFile"))
        self.gridLayout_7.addWidget(self.rbFile, 0, 1, 1, 1)
        self.rbMdsPlus = QtGui.QRadioButton(self.frame)
        self.rbMdsPlus.setObjectName(_fromUtf8("rbMdsPlus"))
        self.gridLayout_7.addWidget(self.rbMdsPlus, 0, 2, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        self.frame_2 = QtGui.QFrame(SelectEfitNe)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_2 = QtGui.QLabel(self.frame_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.leGFileDir = QtGui.QLineEdit(self.frame_2)
        self.leGFileDir.setDragEnabled(True)
        self.leGFileDir.setObjectName(_fromUtf8("leGFileDir"))
        self.gridLayout_3.addWidget(self.leGFileDir, 0, 1, 1, 1)
        self.tbGFileDir = QtGui.QToolButton(self.frame_2)
        self.tbGFileDir.setObjectName(_fromUtf8("tbGFileDir"))
        self.gridLayout_3.addWidget(self.tbGFileDir, 0, 2, 1, 1)
        self.leDataDir = QtGui.QLineEdit(self.frame_2)
        self.leDataDir.setDragEnabled(True)
        self.leDataDir.setObjectName(_fromUtf8("leDataDir"))
        self.gridLayout_3.addWidget(self.leDataDir, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.frame_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)
        self.tbData = QtGui.QToolButton(self.frame_2)
        self.tbData.setObjectName(_fromUtf8("tbData"))
        self.gridLayout_3.addWidget(self.tbData, 1, 2, 1, 1)
        self.gridLayout_2.addWidget(self.frame_2, 1, 0, 1, 1)
        self.frame_4 = QtGui.QFrame(SelectEfitNe)
        self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.gridLayout = QtGui.QGridLayout(self.frame_4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.radioButton_2 = QtGui.QRadioButton(self.frame_4)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.gridLayout.addWidget(self.radioButton_2, 0, 0, 1, 1)
        self.radioButton = QtGui.QRadioButton(self.frame_4)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.gridLayout.addWidget(self.radioButton, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_4, 2, 0, 1, 1)
        self.frame_3 = QtGui.QFrame(SelectEfitNe)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.gridLayout_5 = QtGui.QGridLayout(self.frame_3)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.diagnostics2 = QtGui.QCheckBox(self.frame_3)
        self.diagnostics2.setObjectName(_fromUtf8("diagnostics2"))
        self.gridLayout_5.addWidget(self.diagnostics2, 2, 0, 1, 1)
        self.diagnostics1 = QtGui.QCheckBox(self.frame_3)
        self.diagnostics1.setObjectName(_fromUtf8("diagnostics1"))
        self.gridLayout_5.addWidget(self.diagnostics1, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_3, 3, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 257, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 4, 0, 1, 1)

        self.retranslateUi(SelectEfitNe)
        QtCore.QObject.connect(self.rbFile, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.frame_2.show)
        QtCore.QObject.connect(self.rbFile, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.frame_3.hide)
        QtCore.QObject.connect(self.rbMdsPlus, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.frame_2.hide)
        QtCore.QObject.connect(self.rbMdsPlus, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.frame_3.show)
        QtCore.QObject.connect(self.rbFile, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.frame_4.hide)
        QtCore.QObject.connect(self.rbMdsPlus, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.frame_4.show)
        QtCore.QMetaObject.connectSlotsByName(SelectEfitNe)

    def retranslateUi(self, SelectEfitNe):
        self.label.setText(_translate("SelectEfitNe", "Select Efit From:", None))
        self.rbFile.setText(_translate("SelectEfitNe", "File", None))
        self.rbMdsPlus.setText(_translate("SelectEfitNe", "MDS+ Server", None))
        self.label_2.setText(_translate("SelectEfitNe", "Gfile Dir:", None))
        self.tbGFileDir.setText(_translate("SelectEfitNe", "...", None))
        self.label_3.setText(_translate("SelectEfitNe", "Data Dir:", None))
        self.tbData.setText(_translate("SelectEfitNe", "...", None))
        self.radioButton_2.setText(_translate("SelectEfitNe", "efit_east", None))
        self.radioButton.setText(_translate("SelectEfitNe", "efitrt_east", None))
        self.diagnostics2.setText(_translate("SelectEfitNe", "Thomson scattering(TS)", None))
        self.diagnostics1.setText(_translate("SelectEfitNe", "Reflectometry(ReflJ)", None))

