# -*- coding: utf-8 -*-
import os
import sys

from PyQt4 import QtCore, QtGui

from Ui_MainWindow import Ui_MainWindow
from Ui_selectefitne import Ui_SelectEfitNe
from Ui_selectefitte import Ui_SelectEfitTe
from Ui_selectefitti import Ui_SelectEfitTi
from dataTransfer import *
from dialog6 import Dialog6
from dialog9 import Dialog9
from fileIO import open_file, save_file


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, profile, parent):

        """
        __init__
        :param profile: the string param from profile select widget used for choosing proper functions and other stuffs.
        :param parent:
        """
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.resize(1100, 600)

        # set title
        if profile == 'Te':
            self.setWindowTitle("Electron Temperature Profiles")
        elif profile == 'Ti':
            self.setWindowTitle("Ion Temperature Profiles")
        elif profile == 'ne':
            self.setWindowTitle("Electron Density Profiles")

        # # set style sheet with qss file
        # self.qss = QtCore.QFile('./qss/qss')
        # self.qss.open(QtCore.QIODevice.ReadOnly)
        # self.qssStyle = QtCore.QString().fromUtf8(self.qss.readAll())
        # self.qss.close()
        # if self.qssStyle:
        #     print self.qssStyle
        # self.setStyleSheet(self.qssStyle)

        # define dictionary param: par
        self.par = dict(EfitDir=os.environ.get('HOME'),
                        FileName=os.environ.get('HOME'),
                        RhoPsi='rho',
                        Time=3000,
                        Shot=100000,
                        Func='tanh_multi',
                        Profile=profile,
                        SourceSwitch=0,
                        Diag1=False,
                        Diag2=False,
                        Diag3=False,
                        Diag4=False,
                        Diag5=False,
                        Stretch=0,
                        Shift=0,
                        Tree=''
                        )

        # 'select efit' tab
        global tab1
        if profile == 'Te':
            tab1 = Ui_SelectEfitTe()
        elif profile == 'Ti':
            tab1 = Ui_SelectEfitTi()
        elif profile == 'ne':
            tab1 = Ui_SelectEfitNe()
        w1 = QtGui.QWidget()
        tab1.setupUi(w1)
        self.tabWidget.insertTab(0, w1, "select efit")
        self.tabWidget.setCurrentIndex(0)
        tab1.frame_2.show()
        tab1.frame_3.hide()
        tab1.frame_4.hide()
        tab1.spbShot.enterPressed.connect(self.on_bUpdate_clicked)
        tab1.rbFile.toggled.connect(self.on_rbFile_toggled)
        tab1.leGFileDir.textChanged.connect(self.on_leGFileDir_textChanged)
        tab1.leGFileDir.returnPressed.connect(self.on)
        tab1.leDataDir.textChanged.connect(self.on_leDataDir_textChanged)
        tab1.tbGFileDir.clicked.connect(self.on_tbGFileDir_clicked)
        tab1.leDataDir.returnPressed.connect(self.on)
        tab1.tbData.clicked.connect(self.on_tbData_clicked)
        tab1.bUpdate.clicked.connect(self.on_bUpdate_clicked)
        tab1.listTree.itemClicked.connect(self.showTimeList)
        tab1.listTime.itemClicked.connect(self.on_listTime_clicked)
        tab1.diagnostics1.toggled.connect(self.on_diagnostics1_toggled)
        tab1.diagnostics2.toggled.connect(self.on_diagnostics2_toggled)
        try:
            tab1.diagnostics3.toggled.connect(self.on_diagnostics3_toggled)
        except AttributeError:
            pass
        try:
            tab1.diagnostics4.toggled.connect(self.on_diagnostics4_toggled)
        except AttributeError:
            pass
        try:
            tab1.diagnostics5.toggled.connect(self.on_diagnostics5_toggled)
        except AttributeError:
            pass
        # for diag_checkbox in self.findChildren(QtGui.QCheckBox):
        #     diag_checkbox.toggled.connect(self.on_diagnostics_toggled)

        # set no focus
        # for x in self.findChildren(QtGui.QPushButton) \
        #         or self.findChildren(QtGui.QCheckBox) \
        #         or self.findChildren(QtGui.QComboBox) \
        #         or tab1.findChildren(QtGui.QComboBox):
        #     x.setFocusPolicy(QtCore.Qt.NoFocus)

        # Action
        self.actionSave.triggered.connect(self.on_bSave_clicked)
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.about)
        # self.actionHide = QtGui.QAction(self)
        # self.actionHide.setText("Hide MenuBar")
        # self.actionHide.setCheckable(True)
        # self.actionHide.toggled.connect(self.hide)

        # tab2 = Ui_Dialog6()
        # d1 = QtGui.QDialog()
        # tab2.setupUi(d1)
        # self.tabWidget.insertTab(3, d1, 'dialog6')

    @QtCore.pyqtSignature("QString")
    def on_cbFunctionSelect_activated(self):
        self.par['Func'] = str(self.cbFunctionSelect.currentText())
        self.plot()

    @QtCore.pyqtSignature("int")
    def on_sldStretch_valueChanged(self):
        self.par['Stretch'] = self.sldStretch.value()
        self.plot_data()

    @QtCore.pyqtSignature("int")
    def on_sldShift_valueChanged(self):
        self.par['Shift'] = self.sldShift.value()
        self.plot_data()

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
        self.par['EfitDir'] = tab1.leGFileDir.text()

    def on_leDataDir_textChanged(self):
        self.par['FileName'] = tab1.leDataDir.text()

    @QtCore.pyqtSignature("")
    def on_bRePlot_clicked(self):
        self.par['Shot'] = self.sShot.value()
        self.par['Time'] = self.sTime.value()
        self.lShowShot.setNum(self.sShot.value())
        self.lShowTime.setNum(self.sTime.value())
        self.mplCanvas.clean()
        self.sShot.setDisabled(False)
        self.sTime.setDisabled(False)
        self.initial_list('both')
        self.initial_importdata()
        self.initial_diagnostics()
        ImportData.value = {}

    def on_tbGFileDir_clicked(self):
        dlg = QtGui.QFileDialog(self)
        self.par['EfitDir'] = dlg.getExistingDirectory(self,
                                                       u"Choose the GFile Directory",
                                                       os.environ.get('HOME'))
        if not self.par['EfitDir'].isEmpty():
            tab1.leGFileDir.setText(self.par['EfitDir'])

    def on_tbData_clicked(self):
        ImportData.value['data'] = []
        ImportData.value['processed_data'] = None
        dlg = QtGui.QFileDialog(self)
        self.par['FileName'] = dlg.getOpenFileName(self,
                                                   u"Choose a File to Fit",
                                                   self.par['EfitDir'])
        if not self.par['FileName'].isEmpty():
            tab1.leDataDir.setText(self.par['FileName'])
            try:
                if tab1.rbRZMap.isChecked():
                    ImportData(self.par)
                elif tab1.rbRhoMap.isChecked():
                    ImportData.value['data'] = open_file(self.par['FileName'], 'rho')
                elif tab1.rbPsiMap.isChecked():
                    ImportData.value['data'] = open_file(self.par['FileName'], 'psi')
                self.plot_data()
            except IOError, e:
                print e
            self.sShot.setDisabled(True)
            self.sTime.setDisabled(True)

    def on(self):
        ImportData.value['data'] = []
        ImportData.value['processed_data'] = None
        self.on_leGFileDir_textChanged()
        self.on_leDataDir_textChanged()
        try:
            ImportData(self.par)
        except IOError, e:
            print e
        try:
            self.plot_data()
        except IOError, e:
            print e

    @QtCore.pyqtSignature("")
    def on_bSave_clicked(self):
        dlg = QtGui.QFileDialog(self)
        save_name = dlg.getSaveFileName(self,
                                        u"Save The Fitted Data",
                                        self.par['EfitDir'])
        if self.par['Func'] == 'tanh_multi':
            save_file(save_name, GlobalVar9.value, ImportData.value['processed_data'], self.mplCanvas.datafit, self.par)
        elif self.par['Func'] == 'tanh_0out':
            save_file(save_name, GlobalVar6.value, ImportData.value['processed_data'], self.mplCanvas.datafit, self.par)

    @QtCore.pyqtSignature("")
    def on_bManFit_clicked(self):
        if self.par['Func'] == 'tanh_multi':
            dlg = Dialog9(parent=self)
        elif self.par['Func'] == 'tanh_0out':
            dlg = Dialog6(parent=self)
        btn = self.findChildren(QtGui.QSlider) + self.findChildren(QtGui.QCheckBox)
        for i in btn:
            try:
                i.valueChanged.connect(dlg.save)
                if self.par['Func'] == 'tanh_multi':
                    i.valueChanged.connect(self.plot9)
                elif self.par['Func'] == 'tanh_0out':
                    i.valueChanged.connect(self.plot6)
            except AttributeError:
                i.stateChanged.connect(dlg.save)
                if self.par['Func'] == 'tanh_multi':
                    i.stateChanged.connect(self.plot9)
                elif self.par['Func'] == 'tanh_0out':
                    i.stateChanged.connect(self.plot6)
        dlg.exec_()

    def on_diagnostics1_toggled(self):
        self.par['Diag1'] = tab1.diagnostics1.isChecked()
        if tab1.diagnostics1.isChecked():
            ImportData(self.par, tab1.diagnostics1.text())
            self.plot_data()
        else:
            ImportData(self.par, tab1.diagnostics1.text(), False)
            self.plot_data()

    def on_diagnostics2_toggled(self):
        self.par['Diag2'] = tab1.diagnostics2.isChecked()
        if tab1.diagnostics2.isChecked():
            ImportData(self.par, tab1.diagnostics2.text())
            self.plot_data()
        else:
            ImportData(self.par, tab1.diagnostics2.text(), False)
            self.plot_data()
        # try:
        #     ImportData(self.par, tab1.diagnostics2.text())
        #     self.plot_data()
        # except (IOError, RuntimeError), e:
        #     print e
        #     tab1.diagnostics2.setCheckState(0)
        # self.par['Diag2'] = tab1.diagnostics2.isChecked()

    def on_diagnostics3_toggled(self):
        self.par['Diag3'] = tab1.diagnostics3.isChecked()
        if tab1.diagnostics3.isChecked():
            ImportData(self.par, tab1.diagnostics3.text())
            self.plot_data()
        else:
            ImportData(self.par, tab1.diagnostics3.text(), False)
            self.plot_data()
        # try:
        #     ImportData(self.par, tab1.diagnostics3.text())
        #     self.plot_data()
        # except (IOError, RuntimeError), e:
        #     print e
        #     tab1.diagnostics3.setCheckState(0)
        # self.par['Diag3'] = tab1.diagnostics3.isChecked()

    def on_diagnostics4_toggled(self):
        self.par['Diag4'] = tab1.diagnostics4.isChecked()
        if tab1.diagnostics4.isChecked():
            ImportData(self.par, tab1.diagnostics4.text())
            self.plot_data()
        else:
            ImportData(self.par, tab1.diagnostics4.text(), False)
            self.plot_data()
        # try:
        #     ImportData(self.par, tab1.diagnostics4.text())
        #     self.plot_data()
        # except (IOError, RuntimeError), e:
        #     print e
        #     tab1.diagnostics4.setCheckState(0)
        # self.par['Diag4'] = tab1.diagnostics4.isChecked()

    def on_diagnostics5_toggled(self):
        self.par['Diag5'] = tab1.diagnostics5.isChecked()
        if tab1.diagnostics5.isChecked():
            ImportData(self.par, tab1.diagnostics5.text())
            self.plot_data()
        else:
            ImportData(self.par, tab1.diagnostics5.text(), False)
            self.plot_data()
        # try:
        #     ImportData(self.par, tab1.diagnostics5.text())
        #     self.plot_data()
        # except (IOError, RuntimeError), e:
        #     print e
        #     tab1.diagnostics5.setCheckState(0)
        # self.par['Diag5'] = tab1.diagnostics5.isChecked()

    def on_rbFile_toggled(self):
        if tab1.rbFile.isChecked():
            self.par['SourceSwitch'] = 0
        else:
            self.par['SourceSwitch'] = 1

    def plot(self):
        if self.par['Func'] == 'tanh_multi':
            self.plot9()
        elif self.par['Func'] == 'tanh_0out':
            self.plot6()

    def plot9(self):
        self.mplCanvas.fit(ImportData.value, GlobalVar9.value, self.par)

    def plot6(self):
        self.mplCanvas.fit(ImportData.value, GlobalVar6.value, self.par)

    def plot_data(self):
        self.mplCanvas.plot_data(self.par)

    def about(self):
        msg = QtGui.QMessageBox(self)
        msg.about(self,
                  "About",
                  '<html>'
                  '<body>'
                  '<h3 style="text-align:center;"><b>A Profile Fitting Tool for EAST</b></h3>'
                  '<hr>'
                  '<p>If you have any questions or advices,</p>'
                  '<p>please contact with:</p>'
                  '<p align="center">'
                  'zhengzhen:'
                  '<a href="mailto:zhengzhen@ipp.ac.cn?Subject=About%20The%20Fitting%20Tool" target="_top">'
                  'zhengzhen@ipp.ac.cn</a>'
                  '</p>'
                  '</body>'
                  '</html>')

    def on_bUpdate_clicked(self):
        self.initial_list('both')
        self.initial_diagnostics()
        shot = tab1.spbShot.value()
        self.par['Shot'] = shot
        try:
            mdsconnect('202.127.204.12')
        except RuntimeError, e:
            print e
            sys.exit(0)
        for i in ['efit_east', 'efitrt_east', 'pefitrt_east']:
            try:
                mdsopen(i, shot)
            except RuntimeError:
                pass
            else:
                tab1.listTree.addItem(i)
        self.lShowShot.setNum(shot)
        self.sShot.setDisabled(True)
        self.sTime.setDisabled(True)

    # noinspection PyArgumentList
    def showTimeList(self):
        self.initial_list('time')
        self.initial_diagnostics()
        mdsopen(str(tab1.listTree.currentItem().text()), tab1.spbShot.value())
        time = mdsvalue("\ATIME")
        for i in time:
            tab1.listTime.addItem(str(i))

    # noinspection PyArgumentList
    def on_listTime_clicked(self):
        self.initial_diagnostics()
        self.initial_importdata()
        self.mplCanvas.clean()
        self.par['Tree'] = tab1.listTree.currentItem().text()
        time = int(float(tab1.listTime.currentItem().text())*1000)
        self.par['Time'] = time
        self.lShowTime.setNum(time)

        # check which diagnostics work

        if self.par['Profile'] == 'Te':
            # Thomson_core
            try:
                mdsopen('TS_EAST', self.par['Shot'])
                mdsvalue('dim_of(Te_coreTS)')
            except RuntimeError:
                print 'Te_coreTS data:\t .... .... .... N/A'
            else:
                tab1.diagnostics1.setDisabled(False)
                print 'Te_coreTS data:\t .... .... .... OK'

            # ECE
            try:
                mdsopen('HRS_EAST', self.par['Shot'])
                mdsvalue('dim_of(Te_HRS)')
            except RuntimeError:
                print 'Te_HRS data:\t .... .... .... N/A'
            else:
                tab1.diagnostics3.setDisabled(False)
                print 'Te_HRS data:\t .... .... .... OK'

            # Michelson
            try:
                mdsopen('MPI_Analy', self.par['Shot'])
                mdsvalue('dim_of(Te_MI)')
            except RuntimeError:
                print 'Te_MI data:\t\t .... .... .... N/A'
            else:
                tab1.diagnostics4.setDisabled(False)
                print 'Te_MI data:\t\t .... .... .... OK'

            # TXCS
            try:
                mdsopen('TXCS_EAST', self.par['Shot'])
                mdsvalue('dim_of(Te_TXCS)')
            except RuntimeError:
                print 'Te_TXCS data:\t .... .... .... N/A'
            else:
                tab1.diagnostics5.setDisabled(False)
                print 'Te_TXCS data:\t .... .... .... OK'

        elif self.par['Profile'] == 'Ti':
            # CXRS
            try:
                mdsopen('CXRS_EAST', self.par['Shot'])
                mdsvalue('dim_of(Ti_CXRS_T)')
            except RuntimeError:
                print 'Ti_CXRS_T data:\t .... .... .... N/A'
            else:
                tab1.diagnostics1.setDisabled(False)
                print 'Ti_CXRS_T data:\t .... .... .... OK'

            # TXCS
            try:
                mdsopen('TXCS_EAST', self.par['Shot'])
                print mdsvalue('dim_of(Te_TXCS)')
            except RuntimeError, e:
                print e
                print 'Ti_TXCS data:\t .... .... .... N/A'
            else:
                tab1.diagnostics3.setDisabled(False)
                print 'Ti_TXCS data:\t .... .... .... OK'

        elif self.par['Profile'] == 'ne':
            # Reflectometry
            try:
                mdsopen('ReflJ_EAST', self.par['Shot'])
                mdsvalue('dim_of(ne_ReflJ)')
            except RuntimeError:
                print 'ne_TeflJ data:\t .... .... .... N/A'
            else:
                tab1.diagnostics1.setDisabled(False)
                print 'ne_ReflJ data:\t .... .... .... OK'

            # Thomson_core
            try:
                mdsopen('TS_EAST', self.par['Shot'])
                mdsvalue('dim_of(ne_coreTS)')
            except RuntimeError:
                print 'ne_coreTS data:\t .... .... .... N/A'
            else:
                tab1.diagnostics2.setDisabled(False)
                print 'ne_coreTS data:\t .... .... .... OK'

            # POINT
            try:
                mdsopen('POINT_Analy', self.par['Shot'])
                mdsvalue('dim_of(\\ne_POINT,0)')
            except RuntimeError:
                print 'ne_POINT data:\t .... .... .... N/A'
            else:
                tab1.diagnostics4.setDisabled(False)
                print 'ne_POINT data:\t .... .... .... OK'

    def initial_diagnostics(self):
        if self.par['Profile'] == 'Te':
            for i in [tab1.diagnostics1, tab1.diagnostics2, tab1.diagnostics3, tab1.diagnostics4, tab1.diagnostics5]:
                i.setCheckState(0)
                i.setDisabled(True)
        elif self.par['Profile'] == 'Ti':
            for i in [tab1.diagnostics1, tab1.diagnostics2, tab1.diagnostics3]:
                i.setCheckState(0)
                i.setDisabled(True)
        elif self.par['Profile'] == 'ne':
            for i in [tab1.diagnostics1, tab1.diagnostics2, tab1.diagnostics3, tab1.diagnostics4]:
                i.setCheckState(0)
                i.setDisabled(True)

    @staticmethod
    def initial_list(obj):
        if obj == 'tree' or obj == 'both':
            if tab1.listTree.item(0):
                tab1.listTree.clear()
        if obj == 'time' or obj == 'both':
            if tab1.listTime.item(0):
                tab1.listTime.clear()

    @staticmethod
    def initial_importdata():
        from data import Data
        ImportData.value['data'] = np.array([])
        ImportData.value['diagnostic1'] = np.array([])
        ImportData.value['diagnostic2'] = np.array([])
        ImportData.value['diagnostic3'] = np.array([])
        ImportData.value['diagnostic4'] = np.array([])
        ImportData.value['diagnostic5'] = np.array([])
        ImportData.value['time1'] = float
        ImportData.value['time2'] = float
        ImportData.value['time3'] = float
        ImportData.value['time4'] = float
        ImportData.value['time5'] = float
        ImportData.value['processed_data'] = Data()
        ImportData.value['processed_d1'] = Data()
        ImportData.value['processed_d2'] = Data()
        ImportData.value['processed_d3'] = Data()
        ImportData.value['processed_d4'] = Data()
        ImportData.value['processed_d5'] = Data()

    # def hide(self):
    #     if self.actionHide.isChecked():
    #         self.menuBar.setVisible(False)
    #     else:
    #         self.menuBar.setVisible(True)

    # def contextMenuEvent(self, event):  # 重载弹出式菜单事件
    #     menu = QtGui.QMenu(self)
    #     menu.addAction(self.actionHide)
    #     menu.addAction(self.actionAbout)
    #     menu.addAction(self.actionSave)
    #     menu.addAction(self.actionExit)
    #     menu.exec_(QtGui.QCursor().pos())

#     def closeEvent(self, event):
#         msg = QtGui.QMessageBox(self)
#         result = msg.question(self,
#                               u"Confirm Exit...",
#                               u"Are you sure you want to exit ?",
#                               QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
#         event.ignore()
#
#         if result == QtGui.QMessageBox.Yes:
#             event.accept()
#
#
# if __name__ == "__main__":
#     import sys
#
#     app = QtGui.QApplication(sys.argv)
#     fit = MainWindow()
#     fit.show()
#     sys.exit(app.exec_())
