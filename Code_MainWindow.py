# -*- coding: utf-8 -*-
import os

from PyQt4 import QtCore, QtGui, uic

from param import *
from Ui_MainWindow import Ui_MainWindow
from dialog6 import Dialog6
from dialog9 import Dialog9
from Ui_selectefitwidgette import Ui_SelectEfitTe
from Ui_selectefitwidgetne import Ui_SelectEfitNe


class Code_MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, profile, parent=None):

        """

        :type profile: the string param from profile select widget used for choosing proper functions and other stuffs.
        """
        QtGui.QMainWindow.__init__(self, parent)
        self.path = dict(EfitDir=os.environ.get('HOME'),
                         FileName=os.environ.get('HOME'))
        self.saveFileName = ""
        self.theFile = dict(FileName=os.getcwd())
        self.rhopsi = dict(RhoPsi='rho')
        self.time = dict(Time=3000)
        self.shot = dict(Shot=100000)
        self.setupUi(self)
        self.profile = profile
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
        self.leGFileDir = tab1.leGFileDir
        self.leDataDir = tab1.leDataDir
        tab1.leGFileDir.textChanged.connect(self.on_leGFileDir_textChanged)
        tab1.leDataDir.textChanged.connect(self.on_leDataDir_textChanged)
        tab1.tbOpen.clicked.connect(self.on_tbOpen_clicked)
        tab1.tbData.clicked.connect(self.on_tbData_clicked)

    @QtCore.pyqtSignature("QString")
    def on_cRhoPsi_activated(self):
        self.rhopsi['RhoPsi'] = self.cRhoPsi.currentText()
        if self.cbFunctionSelect.currentIndex() == 0:
            Globalvar9(self.rhopsi)
        elif self.cbFunctionSelect.currentIndex() == 1:
            Globalvar6(self.rhopsi)

    def on_leGFileDir_textChanged(self):
        self.path['EfitDir'] = self.leGFileDir.text()
        if self.cbFunctionSelect.currentIndex() == 0:
            Globalvar9(self.path)
        elif self.cbFunctionSelect.currentIndex() == 1:
            Globalvar6(self.path)

    def on_leDataDir_textChanged(self):
        self.path['EfitDir'] = self.leDataDir.text()
        if self.cbFunctionSelect.currentIndex() == 0:
            Globalvar9(self.path)
        elif self.cbFunctionSelect.currentIndex() == 1:
            Globalvar6(self.path)

    @QtCore.pyqtSignature("")
    def on_bPlot_clicked(self):
        self.shot['Shot'] = self.sShot.value()
        self.time['Time'] = self.sTime.value()
        self.lShowShot.setNum(self.sShot.value())
        self.lShowTime.setNum(self.sTime.value())
        if self.cbFunctionSelect.currentIndex() == 0:
            Globalvar9(self.shot)
            Globalvar9(self.time)
            self.plot9()
        elif self.cbFunctionSelect.currentIndex() == 1:
            Globalvar6(self.shot)
            Globalvar6(self.time)
            self.plot6()

    def on_tbOpen_clicked(self):
        dlg = QtGui.QFileDialog(self)
        temp = self.path['EfitDir']
        self.path['EfitDir'] = dlg.getExistingDirectory(self,
                                                        u"Choose the Gfile Directory",
                                                        os.environ.get('HOME'))
        if len(self.path['EfitDir']) == 0:
            self.path['EfitDir'] = temp
        self.leGFileDir.setText(self.path['EfitDir'])
        if self.cbFunctionSelect.currentIndex() == 0:
            Globalvar9(self.path)
        elif self.cbFunctionSelect.currentIndex() == 1:
            Globalvar6(self.path)

    def on_tbData_clicked(self):
        # if self.cbSourceSelect.currentIndex() == 1:
            dlg = QtGui.QFileDialog(self)
            temp = self.path['EfitDir']
            self.path['FileName'] = dlg.getOpenFileName(self,
                                                        u"Choose a File to Fit",
                                                        self.path['EfitDir'])
            if len(self.path['EfitDir']) == 0:
                self.path['EfitDir'] = temp
            self.leDataDir.setText(self.path['EfitDir'])
            if self.cbFunctionSelect.currentIndex() == 0:
                Globalvar9(self.path)
            elif self.cbFunctionSelect.currentIndex() == 1:
                Globalvar6(self.path)

    @QtCore.pyqtSignature("")
    def on_bSave_clicked(self):
        dlg = QtGui.QFileDialog(self)
        self.saveFileName = dlg.getSaveFileName(self,
                                                u"Save The Fitted Data",
                                                self.path['EfitDir'])
        output = open(self.saveFileName, 'w')
        print >> output, "# ", self.shot['Shot'], "\t", self.time['Time'], "\n"
        print >> output, "#params:\n\n"
        if self.cbFunctionSelect.currentIndex() == 0:
            print >> output, "  #c params:"
            c = str(Globalvar9.book['Params'][0][:-1])
            c = c.replace("[", "")
            c = c.replace("]", "") + "\n"
            print >> output, "  " + c
            output.write("  #data shift:\n")
            shift = str(Globalvar9.book['Params'][0][-1])
            print >> output, "  " + shift + "\n"
            output.write("  #ifix params:\n")
            ifix = str([i / 2 for i in Globalvar9.book['Params'][-1]])
            ifix = ifix.replace("[", "")
            ifix = ifix.replace("]", "") + "\n"
            print >> output, "  " + ifix + "\n"
            print >> output, "#raw data\n"
            print >> output, "  " + "#" + str(self.rhopsi['RhoPsi'])
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
            print >> output, "  " + "#" + str(self.rhopsi['RhoPsi'])
            print >> output, " " + fitx + "\n"
            print >> output, "  #data"
            print >> output, " " + fity
        elif self.cbFunctionSelect.currentIndex() == 1:
            print >> output, "  #c params:"
            c = str(Globalvar6.book['Params'][0][:-1])
            c = c.replace("[", "")
            c = c.replace("]", "") + "\n"
            print >> output, "  " + c
            output.write("  #data shift\n")
            shift = str(Globalvar6.book['Params'][0][-1])
            print >> output, "  " + shift + "\n"
            output.write("  #ifix params:\n")
            ifix = str([i / 2 for i in Globalvar6.book['Params'][-1]])
            ifix = ifix.replace("[", "")
            ifix = ifix.replace("]", "") + "\n"
            print >> output, "  " + ifix + "\n"
            print >> output, "#raw data\n"
            print >> output, "  " + "#" + str(self.rhopsi['RhoPsi'])
            rawx = str(self.mplCanvas.data.x)
            rawx = rawx.replace("array([", "")
            rawx = rawx.replace("[", "")
            rawx = rawx.replace("])", "") + "\n"
            rawx = rawx.replace("]", "") + "\n"
            rawy = str(self.mplCanvas.data.y)
            rawy = rawy.replace("[", "")
            rawy = rawy.replace("]", "") + "\n"
            print >> output, "  " + rawx + "\n"
            print >> output, "  #data\n"
            print >> output, " " + rawy + "\n"
            print >> output, "#fitted data\n"
            fitx = str(self.mplCanvas.rho)
            fitx = fitx.replace("[", "")
            fitx = fitx.replace("]", "") + "\n"
            fity = str(self.mplCanvas.datafit.y)
            fity = fity.replace("[", "")
            fity = fity.replace("]", "") + "\n"
            print >> output, "  " + "#" + str(self.rhopsi['RhoPsi'])
            print >> output, " " + fitx + "\n"
            print >> output, "  #data\n"
            print >> output, " " + fity

    @QtCore.pyqtSignature("bool")
    def on_rbFile_clicked(self):
        pass

    @QtCore.pyqtSignature("")
    def on_bManFit_clicked(self):
        if self.cbFunctionSelect.currentIndex() == 0:
            dlg = Dialog9(parent=self)
            for sld in [dlg.sld1, dlg.sld2, dlg.sld3, dlg.sld4, dlg.sld5, dlg.sld6, dlg.sld7, dlg.sld8, dlg.sld9,
                        dlg.sld10]:
                sld.valueChanged.connect(dlg.save)
                sld.valueChanged.connect(self.plot9)
            for chbtn in [dlg.chb1, dlg.chb2, dlg.chb3, dlg.chb4, dlg.chb5, dlg.chb6, dlg.chb7, dlg.chb8, dlg.chb9]:
                chbtn.stateChanged.connect(dlg.save)
                chbtn.stateChanged.connect(self.plot9)
            dlg.exec_()
            dlg.destroy()
        elif self.cbFunctionSelect.currentIndex() == 1:
            dlg = Dialog6(parent=self)
            for sld in [dlg.sld1, dlg.sld2, dlg.sld3, dlg.sld4, dlg.sld5, dlg.sld6, dlg.sld7]:
                sld.valueChanged.connect(dlg.save)
                sld.valueChanged.connect(self.plot6)
            for chbtn in [dlg.chb1, dlg.chb2, dlg.chb3, dlg.chb4, dlg.chb5, dlg.chb6]:
                chbtn.stateChanged.connect(dlg.save)
                chbtn.stateChanged.connect(self.plot6)
            dlg.exec_()
            dlg.destroy()

    def plot9(self):
        self.mplCanvas.calculation(Globalvar9.book, self.cbFunctionSelect.currentText(), self.profile)

    def plot6(self):
        self.mplCanvas.calculation(Globalvar6.book, self.cbFunctionSelect.currentText(), self.profile)

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
