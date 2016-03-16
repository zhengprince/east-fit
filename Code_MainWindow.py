# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from Ui_MainWindow import Ui_MainWindow
from Ui_selectefitwidgetne import Ui_SelectEfitNe
from Ui_selectefitwidgette import Ui_SelectEfitTe
from dialog6 import Dialog6
from dialog9 import Dialog9
from param import *


class Code_MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, profile, parent):

        """

        :type profile: the string param from profile select widget used for choosing proper functions and other stuffs.
        """
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.resize(1100, 600)

        self.par = dict(EfitDir=os.environ.get('HOME'),
                        FileName=os.environ.get('HOME'),
                        RhoPsi='rho',
                        Time=3000,
                        Shot=100000,
                        Func='tanh_multi',
                        profile=profile,
                        Diagnostics1=False,
                        Diagnostics2=False,
                        sourceSwitch=0,
                        )
        if profile == 'Te':
            self.setWindowTitle("Electron Temperature Profiles")
        elif profile == 'Ti':
            self.setWindowTitle("Ion Temperature Profiles")
        elif profile == 'ne':
            self.setWindowTitle("Electron Density Profiles")
        self.profile = profile

        # select efit tab
        global tab1
        if profile == 'Te':
            tab1 = Ui_SelectEfitTe()
        elif profile == 'ne':
            tab1 = Ui_SelectEfitNe()
        w1 = QtGui.QWidget()
        tab1.setupUi(w1)
        self.tabWidget.insertTab(0, w1, "select efit")
        self.tabWidget.setCurrentIndex(0)
        tab1.frame_2.show()
        tab1.frame_3.hide()
        tab1.frame_4.hide()
        self.rbFile = tab1.rbFile
        self.rbMdsPlus = tab1.rbMdsPlus
        self.leGFileDir = tab1.leGFileDir
        self.leDataDir = tab1.leDataDir
        self.diagnostics1 = tab1.diagnostics1
        self.diagnostics2 = tab1.diagnostics2
        try:
            self.diagnostics3 = tab1.diagnostics3
        except AttributeError:
            pass
        tab1.rbFile.toggled.connect(self.on_rbFile_toggled)
        tab1.leGFileDir.textChanged.connect(self.on_leGFileDir_textChanged)
        tab1.leDataDir.textChanged.connect(self.on_leDataDir_textChanged)
        tab1.tbGFileDir.clicked.connect(self.on_tbGFileDir_clicked)
        tab1.tbData.clicked.connect(self.on_tbData_clicked)
        tab1.diagnostics1.toggled.connect(self.on_diagnostics1_toggled)
        tab1.diagnostics2.toggled.connect(self.on_diagnostics2_toggled)

        # Action
        self.actionSave.triggered.connect(self.on_bSave_clicked)
        self.actionExit.triggered.connect(self.close)
        self.action_About.triggered.connect(self.onAbout)

    @QtCore.pyqtSignature("int")
    def on_sShot_valueChanged(self):
        self.par['Shot'] = self.sShot.value()

    @QtCore.pyqtSignature("int")
    def on_sTime_valueChanged(self):
        self.par['Time'] = self.sTime.value()

    @QtCore.pyqtSignature("QString")
    def on_cRhoPsi_activated(self):
        self.par['RhoPsi'] = self.cRhoPsi.currentText()

    def on_leGFileDir_textChanged(self):
        self.par['EfitDir'] = self.leGFileDir.text()

    def on_leDataDir_textChanged(self):
        self.par['FileName'] = self.leDataDir.text()

    @QtCore.pyqtSignature("")
    def on_bPlot_clicked(self):
        self.par['Shot'] = self.sShot.value()
        self.par['Time'] = self.sTime.value()
        self.lShowShot.setNum(self.sShot.value())
        self.lShowTime.setNum(self.sTime.value())
        if self.cbFunctionSelect.currentIndex() == 0:
            self.plot9()
        elif self.cbFunctionSelect.currentIndex() == 1:
            self.plot6()

    def on_tbGFileDir_clicked(self):
        dlg = QtGui.QFileDialog(self)
        temp = self.par['EfitDir']
        self.par['EfitDir'] = dlg.getExistingDirectory(self,
                                                       u"Choose the Gfile Directory",
                                                       os.environ.get('HOME'))
        if len(self.par['EfitDir']) == 0:
            self.par['EfitDir'] = temp
        self.leGFileDir.setText(self.par['EfitDir'])

    def on_tbData_clicked(self):
        dlg = QtGui.QFileDialog(self)
        temp = self.par['FileName']
        self.par['FileName'] = dlg.getOpenFileName(self,
                                                   u"Choose a File to Fit",
                                                   self.par['EfitDir'])
        if len(self.par['FileName']) == 0:
            self.par['FileName'] = temp
        self.leDataDir.setText(self.par['FileName'])

    @QtCore.pyqtSignature("")
    def on_bSave_clicked(self):
        dlg = QtGui.QFileDialog(self)
        save_name = dlg.getSaveFileName(self,
                                        u"Save The Fitted Data",
                                        self.par['EfitDir'])
        output = open(save_name, 'w')
        print >> output, "# ", self.par['Shot'], "\t", self.par['Time'], "\n"
        print >> output, "#params:\n\n"
        print >> output, "  #c params:"
        if self.profile == 'Te':
            c = str(GlobalVar9.value['Params'][0][:-1])
        elif self.profile == 'ne':
            c = str(GlobalVar6.value['Params'][0][:-1])
        c = c.replace("[", "")
        c = c.replace("]", "") + "\n"
        print >> output, "  " + c
        output.write("  #data shift:\n")
        global shift
        if self.profile == 'Te':
            shift = str(GlobalVar9.value['Params'][0][-1])
        elif self.profile == 'ne':
            shift = str(GlobalVar6.value['Params'][0][-1])
        print >> output, "  " + shift + "\n"
        output.write("  #ifix params:\n")
        global ifix
        if self.profile == 'Te':
            ifix = str([i / 2 for i in GlobalVar9.value['Params'][-1]])
        elif self.profile == 'ne':
            ifix = str([i / 2 for i in GlobalVar6.value['Params'][-1]])
        ifix = ifix.replace("[", "")
        ifix = ifix.replace("]", "") + "\n"
        print >> output, "  " + ifix + "\n"
        print >> output, "#raw data\n"
        print >> output, "  " + "#" + str(self.par['RhoPsi'])
        rawx = str(self.mplCanvas.data.x)
        rawx = rawx.replace("array([", "")
        rawx = rawx.replace("[", "")
        rawx = rawx.replace("])", "") + "\n"
        rawx = rawx.replace("]", "") + "\n"
        rawy = str(self.mplCanvas.data.y)
        rawy = rawy.replace("[", "")
        rawy = rawy.replace("]", "") + "\n"
        print >> output, "  " + rawx + "\n"
        print >> output, "  #data"
        print >> output, " " + rawy + "\n"
        print >> output, "#fitted data\n"
        fitx = str(self.mplCanvas.rho)
        fitx = fitx.replace("[", "")
        fitx = fitx.replace("]", "") + "\n"
        fity = str(self.mplCanvas.datafit.y)
        fity = fity.replace("[", "")
        fity = fity.replace("]", "") + "\n"
        print >> output, "  " + "#" + str(self.par['RhoPsi'])
        print >> output, " " + fitx + "\n"
        print >> output, "  #data"
        print >> output, " " + fity

    @QtCore.pyqtSignature("")
    def on_bManFit_clicked(self):
        slider = []
        checkbox = []
        if self.profile == 'Te':
            dlg = Dialog9(parent=self)
            S = self.findChildren(QtGui.QSlider)
            for sld in slider:
                sld.valueChanged.connect(dlg.save)
                sld.valueChanged.connect(self.plot9)
            for chbtn in checkbox:
                chbtn.stateChanged.connect(dlg.save)
                chbtn.stateChanged.connect(self.plot9)
            dlg.exec_()
            dlg.destroy()
        elif self.profile == 'ne':
            dlg = Dialog6(parent=self)
            for sld in slider:
                sld.valueChanged.connect(dlg.save)
                sld.valueChanged.connect(self.plot6)
            for chbtn in checkbox:
                chbtn.stateChanged.connect(dlg.save)
                chbtn.stateChanged.connect(self.plot6)
            dlg.exec_()
            dlg.destroy()

    def on_diagnostics1_toggled(self):
        if self.diagnostics1.isChecked():
            self.par['Diagnostics1'] = True
        else:
            self.par['Diagnostics1'] = False
        if self.profile == 'Te':
            self.plot9()
        elif self.profile == 'ne':
            self.plot6()

    def on_diagnostics2_toggled(self):
        if self.diagnostics2.isChecked():
            self.par['Diagnostics2'] = True
        else:
            self.par['Diagnostics2'] = False
        if self.profile == 'Te':
            self.plot9()
        elif self.profile == 'ne':
            self.plot6()

    def on_rbFile_toggled(self):
        if self.rbFile.isChecked():
            self.par['sourceSwitch'] = 0
        else:
            self.par['sourceSwitch'] = 1

    def plot9(self):
        self.mplCanvas.calculation(GlobalVar9.value, self.par)

    def plot6(self):
        self.mplCanvas.calculation(GlobalVar6.value, self.par)

    def onAbout(self):
        QtGui.QMessageBox.about(self,
                                "About",
                                "<b>A Fitting Tool for East</b>"
                                "<br>"
                                "zhengzhen@ipp.ac.cn")
        # def closeEvent(self, event):
        #     result = QtGui.QMessageBox.question(self,
        #                                         u"Confirm Exit...",
        #                                         u"Are you sure you want to exit ?",
        #                                         QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        #     event.ignore()
        #
        #     if result == QtGui.QMessageBox.Yes:
        #         event.accept()


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    fit = Code_MainWindow()
    fit.show()
    sys.exit(app.exec_())
