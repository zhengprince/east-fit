# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(480, 289)
        self.frame_4 = QtGui.QFrame(Form)
        self.frame_4.setGeometry(QtCore.QRect(10, 20, 451, 228))
        self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.gridLayout = QtGui.QGridLayout(self.frame_4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.treeLayout = QtGui.QVBoxLayout()
        self.treeLayout.setSpacing(0)
        self.treeLayout.setObjectName(_fromUtf8("treeLayout"))
        self.label_4 = QtGui.QLabel(self.frame_4)
        self.label_4.setFrameShape(QtGui.QFrame.Panel)
        self.label_4.setFrameShadow(QtGui.QFrame.Raised)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.treeLayout.addWidget(self.label_4)
        self.listTree = QtGui.QListView(self.frame_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listTree.sizePolicy().hasHeightForWidth())
        self.listTree.setSizePolicy(sizePolicy)
        self.listTree.setMaximumSize(QtCore.QSize(100, 16777215))
        self.listTree.setFrameShape(QtGui.QFrame.Panel)
        self.listTree.setObjectName(_fromUtf8("listTree"))
        self.treeLayout.addWidget(self.listTree)
        self.gridLayout.addLayout(self.treeLayout, 0, 0, 1, 1)
        self.timeLayout = QtGui.QVBoxLayout()
        self.timeLayout.setSpacing(0)
        self.timeLayout.setObjectName(_fromUtf8("timeLayout"))
        self.label_5 = QtGui.QLabel(self.frame_4)
        self.label_5.setFrameShape(QtGui.QFrame.Panel)
        self.label_5.setFrameShadow(QtGui.QFrame.Raised)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.timeLayout.addWidget(self.label_5)
        self.listTime = QtGui.QListWidget(self.frame_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listTime.sizePolicy().hasHeightForWidth())
        self.listTime.setSizePolicy(sizePolicy)
        self.listTime.setMaximumSize(QtCore.QSize(100, 16777215))
        self.listTime.setFrameShape(QtGui.QFrame.Panel)
        self.listTime.setObjectName(_fromUtf8("listTime"))
        self.timeLayout.addWidget(self.listTime)
        self.gridLayout.addLayout(self.timeLayout, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(34, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_4.setText(_translate("Form", "Tree", None))
        self.label_5.setText(_translate("Form", "Time", None))

