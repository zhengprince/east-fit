from PyQt4 import QtCore, QtGui


class SpinBox(QtGui.QSpinBox):
    enterPressed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QSpinBox.__init__(self, parent)

    def keyPressEvent(self, event):
        super(SpinBox, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:   # Enter key
            self.enterPressed.emit()
