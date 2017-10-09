from PyQt4 import QtGui, QtCore

from Ui_setting import Ui_Setting


class Setting(QtGui.QDialog, Ui_Setting):
    def __init__(self, par, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.move(700, 350)
        if par['FittingRange'] == 1.0:
            self.cbFittingRange.setCurrentIndex(0)
        elif par['FittingRange'] == 1.1:
            self.cbFittingRange.setCurrentIndex(1)
        elif par['FittingRange'] == 1.2:
            self.cbFittingRange.setCurrentIndex(2)
        if par['GridSize'] == 51:
            self.cbGridSize.setCurrentIndex(0)
        elif par['GridSize'] == 101:
            self.cbGridSize.setCurrentIndex(1)
        elif par['GridSize'] == 201:
            self.cbGridSize.setCurrentIndex(2)
