# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selectefitti.ui'
#
# Created: Thu Jan 12 14:23:39 2017
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

class Ui_SelectEfitTi(object):
    def setupUi(self, SelectEfitTi):
        SelectEfitTi.setObjectName(_fromUtf8("SelectEfitTi"))
        SelectEfitTi.resize(505, 742)
        self.gridLayout_4 = QtGui.QGridLayout(SelectEfitTi)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.frame_6 = QtGui.QFrame(SelectEfitTi)
        self.frame_6.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_6.setObjectName(_fromUtf8("frame_6"))
        self.gridLayout_9 = QtGui.QGridLayout(self.frame_6)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.label_2 = QtGui.QLabel(self.frame_6)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_9.addWidget(self.label_2, 0, 0, 1, 1)
        self.rbFile_2 = QtGui.QRadioButton(self.frame_6)
        self.rbFile_2.setChecked(True)
        self.rbFile_2.setObjectName(_fromUtf8("rbFile_2"))
        self.gridLayout_9.addWidget(self.rbFile_2, 0, 1, 1, 1)
        self.rbMdsPlus_2 = QtGui.QRadioButton(self.frame_6)
        self.rbMdsPlus_2.setObjectName(_fromUtf8("rbMdsPlus_2"))
        self.gridLayout_9.addWidget(self.rbMdsPlus_2, 0, 2, 1, 1)
        self.gridLayout_4.addWidget(self.frame_6, 2, 0, 1, 1)
        self.frame_5 = QtGui.QFrame(SelectEfitTi)
        self.frame_5.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtGui.QFrame.Plain)
        self.frame_5.setObjectName(_fromUtf8("frame_5"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame_5)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(9, -1, 9, -1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lGFileDir = QtGui.QLabel(self.frame_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lGFileDir.sizePolicy().hasHeightForWidth())
        self.lGFileDir.setSizePolicy(sizePolicy)
        self.lGFileDir.setMinimumSize(QtCore.QSize(68, 0))
        self.lGFileDir.setObjectName(_fromUtf8("lGFileDir"))
        self.horizontalLayout_2.addWidget(self.lGFileDir)
        self.leGFileDir = QtGui.QLineEdit(self.frame_5)
        self.leGFileDir.setDragEnabled(True)
        self.leGFileDir.setObjectName(_fromUtf8("leGFileDir"))
        self.horizontalLayout_2.addWidget(self.leGFileDir)
        self.tbGFileDir = QtGui.QToolButton(self.frame_5)
        self.tbGFileDir.setObjectName(_fromUtf8("tbGFileDir"))
        self.horizontalLayout_2.addWidget(self.tbGFileDir)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.frame_5, 3, 0, 1, 1)
        self.frame_4 = QtGui.QFrame(SelectEfitTi)
        self.frame_4.setFrameShape(QtGui.QFrame.Panel)
        self.frame_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(self.frame_4)
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.spbShot = SpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spbShot.sizePolicy().hasHeightForWidth())
        self.spbShot.setSizePolicy(sizePolicy)
        self.spbShot.setMaximum(100000)
        self.spbShot.setObjectName(_fromUtf8("spbShot"))
        self.gridLayout.addWidget(self.spbShot, 0, 0, 1, 1)
        self.pbUpdate = QtGui.QPushButton(self.groupBox)
        self.pbUpdate.setObjectName(_fromUtf8("pbUpdate"))
        self.gridLayout.addWidget(self.pbUpdate, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox)
        self.treeLayout = QtGui.QVBoxLayout()
        self.treeLayout.setSpacing(0)
        self.treeLayout.setObjectName(_fromUtf8("treeLayout"))
        self.lTree = QtGui.QLabel(self.frame_4)
        self.lTree.setFrameShape(QtGui.QFrame.Panel)
        self.lTree.setFrameShadow(QtGui.QFrame.Raised)
        self.lTree.setAlignment(QtCore.Qt.AlignCenter)
        self.lTree.setObjectName(_fromUtf8("lTree"))
        self.treeLayout.addWidget(self.lTree)
        self.listTree = QtGui.QListWidget(self.frame_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listTree.sizePolicy().hasHeightForWidth())
        self.listTree.setSizePolicy(sizePolicy)
        self.listTree.setMaximumSize(QtCore.QSize(120, 16777215))
        self.listTree.setFrameShape(QtGui.QFrame.Panel)
        self.listTree.setObjectName(_fromUtf8("listTree"))
        self.treeLayout.addWidget(self.listTree)
        self.horizontalLayout.addLayout(self.treeLayout)
        self.timeLayout = QtGui.QVBoxLayout()
        self.timeLayout.setSpacing(0)
        self.timeLayout.setObjectName(_fromUtf8("timeLayout"))
        self.lTime = QtGui.QLabel(self.frame_4)
        self.lTime.setFrameShape(QtGui.QFrame.Panel)
        self.lTime.setFrameShadow(QtGui.QFrame.Raised)
        self.lTime.setAlignment(QtCore.Qt.AlignCenter)
        self.lTime.setObjectName(_fromUtf8("lTime"))
        self.timeLayout.addWidget(self.lTime)
        self.listTime = QtGui.QListWidget(self.frame_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listTime.sizePolicy().hasHeightForWidth())
        self.listTime.setSizePolicy(sizePolicy)
        self.listTime.setMaximumSize(QtCore.QSize(120, 16777215))
        self.listTime.setFrameShape(QtGui.QFrame.Panel)
        self.listTime.setObjectName(_fromUtf8("listTime"))
        self.timeLayout.addWidget(self.listTime)
        self.horizontalLayout.addLayout(self.timeLayout)
        spacerItem = QtGui.QSpacerItem(34, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout_4.addWidget(self.frame_4, 4, 0, 1, 1)
        self.frame = QtGui.QFrame(SelectEfitTi)
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
        self.gridLayout_4.addWidget(self.frame, 5, 0, 1, 1)
        self.frame_2 = QtGui.QFrame(SelectEfitTi)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(9, -1, 9, -1)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.rbRZMap = QtGui.QRadioButton(self.frame_2)
        self.rbRZMap.setChecked(True)
        self.rbRZMap.setObjectName(_fromUtf8("rbRZMap"))
        self.horizontalLayout_4.addWidget(self.rbRZMap)
        self.rbRhoMap = QtGui.QRadioButton(self.frame_2)
        self.rbRhoMap.setObjectName(_fromUtf8("rbRhoMap"))
        self.horizontalLayout_4.addWidget(self.rbRhoMap)
        self.rbPsiMap = QtGui.QRadioButton(self.frame_2)
        self.rbPsiMap.setObjectName(_fromUtf8("rbPsiMap"))
        self.horizontalLayout_4.addWidget(self.rbPsiMap)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(9, -1, 9, -1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.lDataDir = QtGui.QLabel(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lDataDir.sizePolicy().hasHeightForWidth())
        self.lDataDir.setSizePolicy(sizePolicy)
        self.lDataDir.setObjectName(_fromUtf8("lDataDir"))
        self.horizontalLayout_3.addWidget(self.lDataDir)
        self.leDataDir = QtGui.QLineEdit(self.frame_2)
        self.leDataDir.setDragEnabled(True)
        self.leDataDir.setObjectName(_fromUtf8("leDataDir"))
        self.horizontalLayout_3.addWidget(self.leDataDir)
        self.tbData = QtGui.QToolButton(self.frame_2)
        self.tbData.setObjectName(_fromUtf8("tbData"))
        self.horizontalLayout_3.addWidget(self.tbData)
        self.pbTemplates = QtGui.QPushButton(self.frame_2)
        self.pbTemplates.setMaximumSize(QtCore.QSize(77, 16777215))
        self.pbTemplates.setObjectName(_fromUtf8("pbTemplates"))
        self.horizontalLayout_3.addWidget(self.pbTemplates)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.frame_2, 6, 0, 1, 1)
        self.frame_3 = QtGui.QFrame(SelectEfitTi)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.gridLayout_5 = QtGui.QGridLayout(self.frame_3)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.diagnostics3 = QtGui.QCheckBox(self.frame_3)
        self.diagnostics3.setEnabled(False)
        self.diagnostics3.setObjectName(_fromUtf8("diagnostics3"))
        self.gridLayout_5.addWidget(self.diagnostics3, 2, 0, 1, 1)
        self.diagnostics1 = QtGui.QCheckBox(self.frame_3)
        self.diagnostics1.setEnabled(False)
        self.diagnostics1.setObjectName(_fromUtf8("diagnostics1"))
        self.gridLayout_5.addWidget(self.diagnostics1, 0, 0, 1, 1)
        self.diagnostics2 = QtGui.QCheckBox(self.frame_3)
        self.diagnostics2.setEnabled(False)
        self.diagnostics2.setObjectName(_fromUtf8("diagnostics2"))
        self.gridLayout_5.addWidget(self.diagnostics2, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.frame_3, 8, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 186, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem1, 9, 0, 1, 1)

        self.retranslateUi(SelectEfitTi)
        QtCore.QMetaObject.connectSlotsByName(SelectEfitTi)

    def retranslateUi(self, SelectEfitTi):
        SelectEfitTi.setWindowTitle(_translate("SelectEfitTi", "Form", None))
        self.label_2.setText(_translate("SelectEfitTi", "Select Efit From:", None))
        self.rbFile_2.setText(_translate("SelectEfitTi", "File", None))
        self.rbMdsPlus_2.setText(_translate("SelectEfitTi", "MDS+ Server", None))
        self.lGFileDir.setText(_translate("SelectEfitTi", "GFile Dir:", None))
        self.tbGFileDir.setText(_translate("SelectEfitTi", "Open", None))
        self.groupBox.setTitle(_translate("SelectEfitTi", "Shot", None))
        self.pbUpdate.setText(_translate("SelectEfitTi", "Update", None))
        self.lTree.setText(_translate("SelectEfitTi", "Tree", None))
        self.lTime.setText(_translate("SelectEfitTi", "Time (ms)", None))
        self.label.setText(_translate("SelectEfitTi", "Select Data From:", None))
        self.rbFile.setText(_translate("SelectEfitTi", "File", None))
        self.rbMdsPlus.setText(_translate("SelectEfitTi", "MDS+ Server", None))
        self.rbRZMap.setText(_translate("SelectEfitTi", "RZ Map", None))
        self.rbRhoMap.setText(_translate("SelectEfitTi", "Rho Map", None))
        self.rbPsiMap.setText(_translate("SelectEfitTi", "Psi Map", None))
        self.lDataDir.setText(_translate("SelectEfitTi", "Data  Dir:", None))
        self.tbData.setText(_translate("SelectEfitTi", "Open", None))
        self.pbTemplates.setText(_translate("SelectEfitTi", "Templates", None))
        self.diagnostics3.setText(_translate("SelectEfitTi", "TXCS", None))
        self.diagnostics1.setText(_translate("SelectEfitTi", "CXRS (Core)", None))
        self.diagnostics2.setText(_translate("SelectEfitTi", "CXRS (Edge)", None))

from spinbox import SpinBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SelectEfitTi = QtGui.QWidget()
    ui = Ui_SelectEfitTi()
    ui.setupUi(SelectEfitTi)
    SelectEfitTi.show()
    sys.exit(app.exec_())

