from PyQt4 import QtGui, QtCore

from Ui_dialog5 import Ui_Dialog5


class Dialog5(QtGui.QDialog, Ui_Dialog5):
    """
    c includes three parts, sliders' value, spin boxes' value, check buttons' value
    """
    c = dict(Params=[0, 0, 0, 0, 0])

    def __init__(self, _in, _range=1000, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.g = _in
        self.range = _range
        for btn in self.buttonBox.buttons():
            if self.buttonBox.buttonRole(btn) == QtGui.QDialogButtonBox.ResetRole:
                btn.clicked.connect(self.reset)
        self._initial()
        for x in self.findChildren(QtGui.QDialogButtonBox):
            x.setFocusPolicy(QtCore.Qt.NoFocus)

    def reset(self):
        """
        reset values
        """
        self.sld1.setMinimum(0)
        self.sld2.setMinimum(0)
        self.sld3.setMinimum(0)
        self.sld4.setMinimum(0)
        self.sld5.setMinimum(0)
        self.sld1.setMaximum(self.range)
        self.sld2.setMaximum(self.range)
        self.sld3.setMaximum(self.range)
        self.sld4.setMaximum(self.range)
        self.sld5.setMaximum(self.range)
        self.sld5.setValue(self.range)
        self.sld4.setValue(950)
        self.sld3.setValue(900)
        self.sld2.setValue(500)
        self.sld1.setValue(0)
        self.lDig1.setNum(self.sld1.value())
        self.lDig2.setNum(self.sld2.value())
        self.lDig3.setNum(self.sld3.value())
        self.lDig4.setNum(self.sld4.value())
        self.lDig5.setNum(self.sld5.value())
        self.save()

    @QtCore.pyqtSignature("")
    def on_buttonBox_rejected(self):
        self.save()
        self.reject()

    @QtCore.pyqtSignature("")
    def on_buttonBox_accepted(self):
        self.save()
        self.accept()

    def _initial(self):
        for sld in self.findChildren(QtGui.QSlider):
            sld.setPageStep(1)
        if len(self.g.value['Params']) == 0:
            self.reset()
        else:
            self.sld1.setMinimum(0)
            self.sld2.setMinimum(0)
            self.sld3.setMinimum(0)
            self.sld4.setMinimum(0)
            self.sld5.setMinimum(0)
            self.sld1.setMaximum(self.range)
            self.sld2.setMaximum(self.range)
            self.sld3.setMaximum(self.range)
            self.sld4.setMaximum(self.range)
            self.sld5.setMaximum(self.range)
            self.sld5.setValue(self.g.value['Params'][4])
            self.sld4.setValue(self.g.value['Params'][3])
            self.sld3.setValue(self.g.value['Params'][2])
            self.sld2.setValue(self.g.value['Params'][1])
            self.sld1.setValue(self.g.value['Params'][0])
            self.lDig1.setNum(self.sld1.value())
            self.lDig2.setNum(self.sld2.value())
            self.lDig3.setNum(self.sld3.value())
            self.lDig4.setNum(self.sld4.value())
            self.lDig5.setNum(self.sld5.value())
        self.save()

    def save(self):
        self.c['Params'][0] = self.sld1.value()
        self.c['Params'][1] = self.sld2.value()
        self.c['Params'][2] = self.sld3.value()
        self.c['Params'][3] = self.sld4.value()
        self.c['Params'][4] = self.sld5.value()
        self.g.update(self.c)

    @QtCore.pyqtSignature("int")
    def on_sld1_valueChanged(self):
        self.sld2.setMinimum(self.sld1.value())

    @QtCore.pyqtSignature("int")
    def on_sld2_valueChanged(self):
        self.sld1.setMaximum(self.sld2.value())
        self.sld3.setMinimum(self.sld2.value())

    @QtCore.pyqtSignature("int")
    def on_sld3_valueChanged(self):
        self.sld2.setMaximum(self.sld3.value())
        self.sld4.setMinimum(self.sld3.value())

    @QtCore.pyqtSignature("int")
    def on_sld4_valueChanged(self):
        self.sld3.setMaximum(self.sld4.value())
        self.sld5.setMinimum(self.sld4.value())

    @QtCore.pyqtSignature("int")
    def on_sld5_valueChanged(self):
        self.sld4.setMaximum(self.sld5.value())
