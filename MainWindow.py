# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui, QtWebKit

from GUI.Ui_MainWindow import Ui_MainWindow
from GUI.Ui_selectefitne import Ui_SelectEfitNe
from GUI.Ui_selectefitte import Ui_SelectEfitTe
from GUI.Ui_selectefitti import Ui_SelectEfitTi
from GUI.Ui_selectefitvt import Ui_SelectEfitVt
from GUI.setting import Setting
from GUI.dialog6 import Dialog6
from GUI.dialog9 import Dialog9
from GUI.dialog5 import Dialog5
from dataTransfer import *
import re


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, profile, parent):

        """
        __init__
        :param profile: the string param from profile select widget used for choosing proper functions and other stuffs.
        :param parent:
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.resize(1100, 624)
        self.listWindowTime.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

        # set title
        if profile == 'Te':
            self.setWindowTitle("Electron Temperature Profiles")
        elif profile == 'Ti':
            self.setWindowTitle("Ion Temperature Profiles")
        elif profile == 'ne':
            self.setWindowTitle("Electron Density Profiles")
        elif profile == 'Vt':
            self.setWindowTitle("Rotation Velocity Profiles")

        # set style sheet with qss file
        # self.qss = QtCore.QFile('./GUI/qss/qss')
        # self.qss.open(QtCore.QIODevice.ReadOnly)
        # self.qssStyle = QtCore.QString().fromUtf8(self.qss.readAll())
        # self.qss.close()
        # if self.qssStyle:
        #     print 'OK'
        # self.setStyleSheet(self.qssStyle)

        # define dictionary param: par
        self.par = dict(EfitDir='',
                        FileName='',
                        Toggle='rho',
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
                        Tree='',
                        RbFile1=True,
                        RbMds1=False,
                        RbFile2=True,
                        RbMds2=False,
                        vis=False,
                        GridSize=51,
                        FittingRange=1.0,
                        WindowTime=0
                        )
        self.importData = ImportData()
        self.g = GlobalVar()
        self.g5 = GlobalVar5()
        self.g6 = GlobalVar6()
        self.g9 = GlobalVar9()

        # 'select efit' tab widget
        if profile == 'Te':
            self.tab1 = Ui_SelectEfitTe()
        elif profile == 'Ti':
            self.tab1 = Ui_SelectEfitTi()
        elif profile == 'ne':
            self.tab1 = Ui_SelectEfitNe()
        elif profile == 'Vt':
            self.tab1 = Ui_SelectEfitVt()

        w1 = QtGui.QWidget()
        self.tab1.setupUi(w1)
        self.tabWidget.insertTab(0, w1, "select efit")
        self.tabWidget.setCurrentIndex(0)
        self.tab1.frame.show()
        self.tab1.frame_2.show()
        self.tab1.frame_3.hide()
        self.tab1.frame_4.hide()
        self.tab1.frame_5.show()
        self.tab1.frame_6.show()

        # connect signals with the functions
        # spb:spinbox, rb:radio button, le:line edit, tb:tool box, pb:push button, l:label, list:list widget
        self.tab1.spbShot.enterPressed.connect(self.on_pbUpdate_clicked)
        self.tab1.rbFile.toggled.connect(self.on_rbFile_toggled)
        self.tab1.rbRhoMap.toggled.connect(self.on_rbRhoMap_toggled)
        self.tab1.rbPsiMap.toggled.connect(self.on_rbPsiMap_toggled)
        self.tab1.leGFileDir.textChanged.connect(self.on_leGFileDir_textChanged)
        self.tab1.leGFileDir.returnPressed.connect(self.on)
        self.tab1.leDataDir.textChanged.connect(self.on_leDataDir_textChanged)
        self.tab1.tbGFileDir.clicked.connect(self.on_tbGFileDir_clicked)
        self.tab1.leDataDir.returnPressed.connect(self.on)
        self.tab1.tbData.clicked.connect(self.on_tbData_clicked)
        self.tab1.pbUpdate.clicked.connect(self.on_pbUpdate_clicked)
        self.tab1.listTree.itemClicked.connect(self.showTimeList)
        self.tab1.listTime.itemClicked.connect(self.on_listTime_clicked)
        self.tab1.diagnostics1.toggled.connect(self.on_diagnostics1_toggled)
        self.tab1.diagnostics2.toggled.connect(self.on_diagnostics2_toggled)

        # connect signals with the slots in self.tab1
        self.tab1.rbFile.clicked.connect(self.on_rbFile_clicked)
        self.tab1.rbMdsPlus.clicked.connect(self.on_rbMdsPlus_clicked)
        self.tab1.rbRZMap.clicked.connect(self.on_rbRZMap_clicked)
        self.tab1.rbRhoMap.clicked.connect(self.on_rbRhoMap_clicked)
        self.tab1.rbPsiMap.clicked.connect(self.on_rbPsiMap_clicked)
        self.tab1.rbFile_2.clicked.connect(self.on_rbFile_2_clicked)
        self.tab1.rbMdsPlus_2.clicked.connect(self.on_rbMdsPlus_2_clicked)
        self.tab1.pbTemplates.clicked.connect(self.on_pbTemplates_clicked)

        # FOR NE, TE AND TI, THEIRS DIAGNOSTICS ARE NOT THE SAME (NE 4, TE 5, TI 3),
        # SO THE FOLLOWING WILL DEAL WITH THIS.
        try:
            self.tab1.diagnostics3.toggled.connect(self.on_diagnostics3_toggled)
        except AttributeError:
            pass
        try:
            self.tab1.diagnostics4.toggled.connect(self.on_diagnostics4_toggled)
        except AttributeError:
            pass
        try:
            self.tab1.diagnostics5.toggled.connect(self.on_diagnostics5_toggled)
        except AttributeError:
            pass

        # Action
        # self.actionSave.triggered.connect(self.on_bSave_clicked)
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.about)
        self.actionSetting.triggered.connect(self.on_actionSetting_clicked)
        self.actionRestore.triggered.connect(self.on_actionRestore_clicked)
        # self.actionHide = QtGui.QAction(self)
        # self.actionHide.setText("Hide MenuBar")
        # self.actionHide.setCheckable(True)
        # self.actionHide.toggled.connect(self.hide)

        # tab2 = Ui_Dialog6()
        # d1 = QtGui.QDialog()
        # tab2.setupUi(d1)
        # self.tabWidget.insertTab(3, d1, 'dialog6')
        self.mds()

    # ### CONTROL THE BEHAVIOR OF self.tab1, CONNECT THE SIGNALS AND SLOTS. ###
    def on_rbFile_clicked(self):
        self.par['RbFile1'] = True
        self.par['RbMds1'] = False
        self.tab1.frame_6.setEnabled(True)
        self.tab1.frame_6.show()
        if self.tab1.rbFile_2.isChecked():
            self.tab1.frame_5.show()
            self.tab1.frame_4.hide()
        elif self.tab1.rbMdsPlus_2.isChecked():
            self.tab1.frame_5.hide()
            self.tab1.frame_4.show()
        self.tab1.frame_3.hide()
        self.tab1.frame_2.show()
        self.tab1.rbRZMap.setChecked(True)
        self.on_bRePlot_clicked()

    def on_rbMdsPlus_clicked(self):
        self.par['RbMds1'] = True
        self.par['RbFile1'] = False
        self.tab1.frame_6.setEnabled(True)
        self.tab1.frame_6.show()
        if self.tab1.rbFile_2.isChecked():
            self.tab1.frame_5.show()
            self.tab1.frame_4.hide()
        elif self.tab1.rbMdsPlus_2.isChecked():
            self.tab1.frame_5.hide()
            self.tab1.frame_4.show()
        self.tab1.frame_3.show()
        self.tab1.frame_2.hide()
        # self.on_bRePlot_clicked()
        try:
            self.chk_wh_dia_wk()
        except IOError, e:
            print e

    def on_rbRZMap_clicked(self):
        self.tab1.frame_6.setEnabled(True)
        self.tab1.frame_6.show()
        if self.tab1.rbFile_2.isChecked():
            self.tab1.frame_5.show()
            self.tab1.frame_4.hide()
        elif self.tab1.rbMdsPlus_2.isChecked():
            self.tab1.frame_5.hide()
            self.tab1.frame_4.show()
        self.tab1.frame_3.hide()

    def on_rbRhoMap_clicked(self):
        self.tab1.frame_6.setDisabled(True)
        self.tab1.frame_6.show()
        self.tab1.frame_5.hide()
        self.tab1.frame_4.hide()
        self.tab1.frame_3.hide()

    def on_rbPsiMap_clicked(self):
        self.tab1.frame_6.setDisabled(True)
        self.tab1.frame_6.show()
        self.tab1.frame_5.hide()
        self.tab1.frame_4.hide()
        self.tab1.frame_3.hide()

    def on_rbFile_2_clicked(self):
        self.par['RbFile2'] = True
        self.par['RbMds2'] = False
        self.tab1.frame_5.show()
        self.tab1.frame_4.hide()

    def on_rbMdsPlus_2_clicked(self):
        self.par['RbMds2'] = True
        self.par['RbFile2'] = False
        self.tab1.frame_5.hide()
        self.tab1.frame_4.show()

    # ### CONTROL THE BEHAVIOR OF self.tab1, CONNECT THE SIGNALS AND SLOTS. ###

    @QtCore.pyqtSignature("QString")
    def on_cbFunctionSelect_activated(self):
        self.par['Func'] = str(self.cbFunctionSelect.currentText())
        if self.par['Func'] == 'spline':
            self.par['vis'] = True
        else:
            self.par['vis'] = False
        try:
            self.plot()
        except (IndexError, AttributeError), e:
            print "Warning:", e
            self.statusBar.showMessage('Warning:' + e)
        self.mplCanvas.canvas.plot_knots([0, 0.5, 0.9, 0.95, 1], self.par['vis'])

    @QtCore.pyqtSignature("int")
    def on_sldStretch_valueChanged(self):
        self.par['Stretch'] = self.sldStretch.value()
        self.plot_data(self.par)

    @QtCore.pyqtSignature("")
    def on_pbAuto_clicked(self):
        if self.par['Toggle'] == 'rho':
            self.par['Stretch'] = (1 / self.g.value['data_rho'][-1, 0] - 1) * 1000
        elif self.par['Toggle'] == 'psi':
            self.par['Stretch'] = (1 / self.g.value['data_psi'][-1, 0] - 1) * 1000
        self.sldStretch.setValue(self.par['Stretch'])
        self.plot_data(self.par)
        pass

    @QtCore.pyqtSignature("int")
    def on_sldShift_valueChanged(self):
        self.par['Shift'] = self.sldShift.value()
        self.plot_data(self.par)

    @QtCore.pyqtSignature("QString")
    def on_cPlotToggle_activated(self):
        self.par['Toggle'] = self.cPlotToggle.currentText()
        # print 'def on_cPlotToggle_activated(self):'
        try:
            self.plot_data(self.par)
            if self.mplCanvas.canvas.l1:
                self.plot()
        except (IOError, IndexError, RuntimeError, AttributeError), e:
            print e

    def on_leGFileDir_textChanged(self):
        self.par['EfitDir'] = self.tab1.leGFileDir.text()

    def on_leDataDir_textChanged(self):
        self.par['FileName'] = self.tab1.leDataDir.text()

    @QtCore.pyqtSignature("")
    def on_bRePlot_clicked(self):
        self.mplCanvas.clean()
        self.initial_list('both')
        self.initial_importData()
        self.initial_diagnostics()
        self.leWindowTime.setDisabled(False)
        self.listWindowTime.setDisabled(False)
        self.leWindowTime.clear()
        self.listWindowTime.clear()

    def on_leWindowTime_returnPressed(self):
        self.listWindowTime.clear()
        self.par['WindowTime'] = int(self.leWindowTime.text())
        # filter the windowing time
        ntimes = (self.timelist >= self.par['Time'] - self.par['WindowTime']) & \
                 (self.timelist <= self.par['Time'] + self.par['WindowTime'])
        # output the windowing time list
        wtList = np.extract(ntimes, self.timelist)  # self.timelist[ntimes]
        # delete the element of self.par['Time']
        wtList = wtList[wtList != float(self.par['Time'])]
        # display the number of the windowing time on the left of the list widget
        self.lNTimes.setText(str(wtList.size))
        # show the windowing time list in the list widget
        for i in wtList:
            # [2:-2] will delete the "[[" "]]", eg. [[1]] => 1
            s = str(np.argwhere(wtList == i) + 1)[2:-2] + "  " + str('%0.3f' % i)
            self.listWindowTime.addItem(s)

    @QtCore.pyqtSignature("")
    def on_pbConfirm_clicked(self):
        self.leWindowTime.setDisabled(True)
        self.listWindowTime.setDisabled(True)
        print self.g.value['data_rho']
        print "========================="
        print self.g.value['data_rho'][:, 0] == self.g.value['processed_data_rho'].x[0]
        print "========================="

    def addData(self, v1, v2, n):
        for s in 'rho', 'psi':
            v1['diagnostic' + n + '_' + s] = np.concatenate((v1['diagnostic' + n + '_' + s],
                                                             v2['diagnostic' + n + '_' + s]), axis=0)
            v1['diagnostic' + n + '_' + s] = v1['diagnostic' + n + '_' + s][
                                                 np.argsort(v1['diagnostic' + n + '_' + s], axis=0)][:, 0]
            v1['data_' + s] = v1['diagnostic' + n + '_' + s]
        return v1

    def delData(self, v1, v2, n):
        for s in 'rho', 'psi':
            for i in v2['diagnostic' + n + '_' + s]:
                v1['diagnostic' + n + '_' + s] = \
                    v1['diagnostic' + n + '_' + s][v1['diagnostic' + n + '_' + s] != i].reshape(-1, 2)
            v1['data_' + s] = v1['diagnostic' + n + '_' + s]
        return v1

    def on_listWindowTime_itemClicked(self):
        """
        click (selected) -> return the plot of the clicked time (not other selected times)
        click (unselected) -> clear the plot of this time, other selected times remains.
        :return:
        """
        _g = GlobalVar()
        par_tmp = self.par
        par_tmp['Time'] = float(np.fromstring(str(self.listWindowTime.currentItem().text()), sep=" ")[1])
        for _obj in [self.tab1.diagnostics1, self.tab1.diagnostics2, self.tab1.diagnostics3] or \
                [self.tab1.diagnostics1, self.tab1.diagnostics2, self.tab1.diagnostics3, self.tab1.diagnostics4] or \
                [self.tab1.diagnostics1, self.tab1.diagnostics2, self.tab1.diagnostics3, self.tab1.diagnostics4,
                 self.tab1.diagnostics5]:
            if _obj == self.tab1.diagnostics1: dia = 'Diag1'; n = '1'
            elif _obj == self.tab1.diagnostics2: dia = 'Diag2'; n = '2'
            elif _obj == self.tab1.diagnostics3: dia = 'Diag3'; n = '3'
            elif _obj == self.tab1.diagnostics4: dia = 'Diag4'; n = '4'
            elif _obj == self.tab1.diagnostics5: dia = 'Diag5'; n = '5'
            if self.par[dia]:
                if self.tab1.rbMdsPlus_2.isChecked():
                    g_tmp = self.importData.mds_mds_n_file_mds(_g, par_tmp, _obj.text())
                elif self.tab1.rbFile_2.isChecked():
                    g_tmp = self.importData.mds_mds_n_file_mds(_g, par_tmp, _obj.text(), file_mds=True)
                if self.listWindowTime.currentItem().isSelected():
                    self.g.value = self.addData(self.g.value, g_tmp.value, n)
                else:
                    self.g.value = self.delData(self.g.value, g_tmp.value, n)
        self.plot_data(par_tmp)

    def on_tbGFileDir_clicked(self):
        dlg = QtGui.QFileDialog(self)
        if self.par['EfitDir']:
            _path = os.path.dirname(str(self.par['EfitDir']))
        else:
            _path = os.path.abspath('.')
        self.par['EfitDir'] = dlg.getOpenFileName(self,
                                                  u"Choose the GFile",
                                                  _path)
        if not self.par['EfitDir']:
            return
        if not self.par['EfitDir'].isEmpty():
            gFileName = os.path.basename(str(self.par['EfitDir']))
            self.par['Shot'] = int(gFileName[1:7])
            self.par['Time'] = int(gFileName[8:])
            self.lShowShot.setNum(self.par['Shot'])
            self.lShowTime.setNum(self.par['Time'])
            self.tab1.leGFileDir.setText(self.par['EfitDir'])
            self.lShowEfitTree.setText('FILE')

        # check which diagnostics work
        if self.tab1.rbMdsPlus.isChecked():
            self.chk_wh_dia_wk()

    def on_tbData_clicked(self):
        self.g.value['data_rho'] = []
        self.g.value['processed_data_rho'] = None
        self.g.value['data_psi'] = []
        self.g.value['processed_data_psi'] = None
        dlg = QtGui.QFileDialog(self)
        if self.par['EfitDir']:
            _path = os.path.dirname(str(self.par['EfitDir']))
        else:
            _path = os.path.abspath('.')
        print '_path=', _path
        self.par['FileName'] = dlg.getOpenFileName(self,
                                                   u"Choose a Data File to Fit",
                                                   _path,
                                                   "All Files (*);;Text Files (*.txt)")
        if not self.par['FileName']:
            return
        if not self.par['FileName'].isEmpty():
            self.tab1.leDataDir.setText(str(self.par['FileName']))
            self.lShowData.setText('FILE')
            try:
                self.judge_n_obtain_data()
                self.plot_data(self.par)
                self.statusBar.showMessage('DATA IMPORTED SUCCESSFULLY !')
            except IOError, e:
                print e

    def on(self):
        self.g.value['data_rho'] = []
        self.g.value['processed_data_rho'] = None
        self.on_leGFileDir_textChanged()
        self.on_leDataDir_textChanged()
        try:
            self.judge_n_obtain_data()
        except IOError, e:
            print e
        try:
            self.plot_data(self.par)
        except IOError, e:
            print e

    def judge_n_obtain_data(self):
        if self.tab1.rbFile_2.isChecked():
            if self.tab1.rbRZMap.isChecked():
                self.g = self.importData.file_file(self.g, self.par)
            elif self.tab1.rbRhoMap.isChecked():
                tmp = openFile(self.par['FileName'])['all']
                self.g.value['data_rho'] = tmp[np.argsort(tmp, axis=0)][:, 0]
                self.g.value['filein_rho'] = self.g.value['data_rho']
                self.g.d(filein_rho=self.g.value['data_rho'])
                self.lShowEfitTree.setText('None')
            elif self.tab1.rbPsiMap.isChecked():
                tmp = openFile(self.par['FileName'])['all']
                self.g.value['data_psi'] = tmp[np.argsort(tmp, axis=0)][:, 0]
                self.g.value['filein_psi'] = self.g.value['data_psi']
                self.g.d(filein_psi=self.g.value['data_psi'])
                self.lShowEfitTree.setText('None')
        elif self.tab1.rbMdsPlus_2.isChecked():
            if self.tab1.rbRZMap.isChecked():
                self.g.value['data_rho'] = openFile(self.par['FileName'])
                self.g.value['data_psi'] = openFile(self.par['FileName'])
                self.g = self.importData.mds_file(self.g, self.par)
                self.lShowData.setText('FILE')
            elif self.tab1.rbRhoMap.isChecked():
                tmp = openFile(self.par['FileName'])['all']
                self.g.value['data_rho'] = tmp[np.argsort(tmp, axis=0)][:, 0]
                self.g.value['filein_rho'] = self.g.value['data_rho']
                self.g.d(filein_rho=self.g.value['data_rho'])
                self.lShowEfitTree.setText('None')
                self.lShowData.setText('FILE')
            elif self.tab1.rbPsiMap.isChecked():
                tmp = openFile(self.par['FileName'])['all']
                self.g.value['data_psi'] = tmp[np.argsort(tmp, axis=0)][:, 0]
                self.g.value['filein_psi'] = self.g.value['data_psi']
                self.g.d(filein_psi=self.g.value['data_psi'])
                self.lShowEfitTree.setText('None')
                self.lShowData.setText('FILE')

    @QtCore.pyqtSignature("")
    def on_bSave_clicked(self):
        dlg = QtGui.QFileDialog(self)
        _name = './' + self.par['Profile'] + str(self.par['Shot']).zfill(5) + '.' + str(self.par['Time']).zfill(
            6) + '.fit'
        saveName = dlg.getSaveFileName(self,
                                       u"Save The Fitted Data",
                                       os.path.abspath(_name),
                                       "Fit Files (*.fit);;All Files (*)")
        if not saveName:
            return
        if self.par['Func'] == 'tanh_multi':
            value = self.g9.value['Params']
        elif self.par['Func'] == 'tanh_0out':
            value = self.g6.value['Params']
        elif self.par['Func'] == 'spline':
            value = self.g5.value['Params']
        fit = self.g.value['fit']
        par = self.par
        processed_data = self.g.value
        database = self.g.database
        if self.g.library['data_rho'].any() and self.g.library['data_psi'].any():
            libraryData = self.g.library
        else:
            print 'none'
            libraryData = None
        # if not self.g.library['data_rho'].any() and not self.g.library['data_psi'].any():
        #     self.statusBar.showMessage('NO DATA ! NO FILE SAVED !')
        try:
            saveFile(saveName, value, processed_data, fit, libraryData, database, par)
            self.statusBar.showMessage('FILE SAVED SUCCESSFULLY!')
        except:
            self.statusBar.showMessage('FILE SAVED UNSUCCESSFULLY!')

    @QtCore.pyqtSignature("")
    def on_bManFit_clicked(self):
        if self.par['Func'] == 'tanh_multi':
            dlg = Dialog9(self.g9, parent=self)
        elif self.par['Func'] == 'tanh_0out':
            dlg = Dialog6(self.g6, parent=self)
        elif self.par['Func'] == 'spline':
            dlg = Dialog5(self.g5, self.par['FittingRange'] * 1000, parent=self)
        btn = dlg.findChildren(QtGui.QSlider) + dlg.findChildren(QtGui.QCheckBox)
        for i in btn:
            try:
                i.valueChanged.connect(dlg.save)
                i.valueChanged.connect(self.plot)
                i.valueChanged.connect(self.plot_spline)
            except AttributeError:
                i.stateChanged.connect(dlg.save)
                i.stateChanged.connect(self.plot)
        dlg.exec_()

    def on_diagnostics1_toggled(self):
        self.par['Diag1'] = self.tab1.diagnostics1.isChecked()
        if self.par['Diag1']:
            self.lShowData.setText('MDSPLUS')
            if self.tab1.rbMdsPlus_2.isChecked():
                self.g = self.importData.mds_mds_n_file_mds(self.g, self.par, self.tab1.diagnostics1.text())
            elif self.tab1.rbFile_2.isChecked():
                self.g = self.importData.mds_mds_n_file_mds(self.g, self.par, self.tab1.diagnostics1.text(),
                                                            file_mds=True)
                self.lShowEfitTree.setText('FILE')
            self.plot_data(self.par)
        else:
            if self.mplCanvas.canvas.d1:
                self.g = self.importData.mds_mds_n_file_mds(self.g, self.par, self.tab1.diagnostics1.text(),
                                                            default=False)
                self.plot_data(self.par)
            else:
                pass

    def on_diagnostics2_toggled(self):
        self.par['Diag2'] = self.tab1.diagnostics2.isChecked()
        if self.par['Diag2']:
            self.lShowData.setText('MDSPLUS')
            if self.tab1.rbMdsPlus_2.isChecked():
                self.g = self.importData.mds_mds_n_file_mds(self.g, self.par, self.tab1.diagnostics2.text())
            elif self.tab1.rbFile_2.isChecked():
                self.g = self.importData.mds_mds_n_file_mds(self.g, self.par, self.tab1.diagnostics2.text(),
                                                            file_mds=True)
                self.lShowEfitTree.setText('FILE')
            self.plot_data(self.par)
        else:
            if self.mplCanvas.canvas.d2:
                self.g = self.importData.mds_mds_n_file_mds(self.g, self.par, self.tab1.diagnostics2.text(),
                                                            default=False)
                self.plot_data(self.par)
            else:
                pass

    def on_diagnostics3_toggled(self):
        self.par['Diag3'] = self.tab1.diagnostics3.isChecked()
        if self.par['Diag3']:
            self.lShowData.setText('MDSPLUS')
            if self.tab1.rbMdsPlus_2.isChecked():
                self.g = self.importData.mds_mds_n_file_mds(self.g, self.par, self.tab1.diagnostics3.text())
            elif self.tab1.rbFile_2.isChecked():
                self.g = self.importData.mds_mds_n_file_mds(self.g, self.par, self.tab1.diagnostics3.text(),
                                                            file_mds=True)
                self.lShowEfitTree.setText('FILE')
            self.plot_data(self.par)
        else:
            if self.mplCanvas.canvas.d3:
                self.g = self.importData.mds_mds_n_file_mds(self.g, self.par, self.tab1.diagnostics3.text(),
                                                            default=False)
                self.plot_data(self.par)
            else:
                pass

    def on_diagnostics4_toggled(self):
        self.par['Diag4'] = self.tab1.diagnostics4.isChecked()
        if self.par['Diag4']:
            self.lShowData.setText('MDSPLUS')
            if self.tab1.rbMdsPlus_2.isChecked():
                self.g = self.importData.mds_mds_n_file_mds(self.g, self.par, self.tab1.diagnostics4.text())
            elif self.tab1.rbFile_2.isChecked():
                self.g = self.importData.mds_mds_n_file_mds(self.g, self.par, self.tab1.diagnostics4.text(),
                                                            file_mds=True)
                self.lShowEfitTree.setText('FILE')
            self.plot_data(self.par)
        else:
            if self.mplCanvas.canvas.d4:
                self.g = self.importData.mds_mds_n_file_mds(self.g, self.par, self.tab1.diagnostics4.text(),
                                                            default=False)
                self.plot_data(self.par)
            else:
                pass

    def on_diagnostics5_toggled(self):
        self.par['Diag5'] = self.tab1.diagnostics5.isChecked()
        if self.par['Diag5']:
            self.lShowData.setText('MDSPLUS')
            if self.tab1.rbMdsPlus_2.isChecked():
                self.g = self.importData.mds_mds_n_file_mds(self.g, self.par, self.tab1.diagnostics5.text())
            elif self.tab1.rbFile_2.isChecked():
                self.g = self.importData.mds_mds_n_file_mds(self.g, self.par, self.tab1.diagnostics5.text(),
                                                            file_mds=True)
                self.lShowEfitTree.setText('FILE')
            self.plot_data(self.par)
        else:
            if self.mplCanvas.canvas.d5:
                self.g = self.importData.mds_mds_n_file_mds(self.g, self.par, self.tab1.diagnostics5.text(),
                                                            default=False)
                self.plot_data(self.par)
            else:
                pass

    def on_rbFile_toggled(self):
        if self.tab1.rbFile.isChecked():
            self.par['SourceSwitch'] = 0
        else:
            self.par['SourceSwitch'] = 1

    def on_rbRhoMap_toggled(self):
        if self.tab1.rbRhoMap.isChecked():
            pass
        else:
            pass

    def on_rbPsiMap_toggled(self):
        if self.tab1.rbPsiMap.isChecked():
            pass
        else:
            pass

    def plot(self):
        chiSq = int
        if self.par['Func'] == 'tanh_multi':
            chiSq, self.g9.value, self.g.value['fit'] = self.mplCanvas.fit(self.g.value, self.g9.value, self.par)
        elif self.par['Func'] == 'tanh_0out':
            chiSq, self.g6.value, self.g.value['fit'] = self.mplCanvas.fit(self.g.value, self.g6.value, self.par)
        elif self.par['Func'] == 'spline':
            chiSq, self.g5.value, self.g.value['fit'] = self.mplCanvas.fit(self.g.value, self.g5.value, self.par)
        self.lShowChisq.setText(str(chiSq))

    def plot_data(self, par):
        if self.par['Func'] == 'tanh_multi':
            self.mplCanvas.plot_data(self.g, self.g9, par)
        elif self.par['Func'] == 'tanh_0out':
            self.mplCanvas.plot_data(self.g, self.g6, par)
        elif self.par['Func'] == 'spline':
            self.mplCanvas.plot_data(self.g, self.g5, par)

    def plot_spline(self):
        k = [i / 1000. for i in self.g5.value['Params']]
        self.mplCanvas.canvas.plot_knots(k, True)

    def about(self):
        """
        Some help information in "About"
        :return: none
        """
        msg = QtGui.QMessageBox(self)
        msg.about(self,
                  "About",
                  '<html>'
                  '<body>'
                  '<p><font size="18" face="Lucida Grande"><b>EAST fit</b></font></p>'
                  '<p><font size="5" face="Lucida Grande"><b>A Profile Fitting Tool for EAST</b></font></p>'
                  '<p><font face="Lucida Grande">v0.4a</font></p>'
                  '<hr>'
                  '<p><font face="Lucida Grande">If you have any questions or advices,</font></p>'
                  '<p><font face="Lucida Grande">please contact with:</font></p>'
                  '<p align="center"><font face="Lucida Grande">'
                  'zhengzhen:'
                  '<a href="mailto:zhengzhen@ipp.ac.cn?Subject=About%20The%20Fitting%20Tool" target="_top">'
                  'zhengzhen@ipp.ac.cn</a>'
                  '</font></p>'
                  '</body>'
                  '</html>')

    def on_pbUpdate_clicked(self):
        # when pbUpdate button clicked, initialize list box and diagnostics, then try mdsopen, if success, it will
        # be shown in the list box, and the shot number will be shown in lShowShot.
        self.initial_list('both')
        self.initial_diagnostics()
        shot = self.tab1.spbShot.value()
        self.par['Shot'] = shot
        for i in ['efit_east', 'efitrt_east', 'pefitrt_east']:
            try:
                mdsopen(i, shot)
            except RuntimeError:
                pass
            else:
                self.tab1.listTree.addItem(i)
        self.lShowShot.setNum(shot)

    # noinspection PyArgumentList
    def showTimeList(self):
        self.initial_list('time')
        self.initial_diagnostics()
        mdsopen(str(self.tab1.listTree.currentItem().text()), self.tab1.spbShot.value())
        self.lShowEfitTree.setText(self.tab1.listTree.currentItem().text())
        self.timelist = 1000 * mdsvalue("\ATIME")
        for i in self.timelist:
            self.tab1.listTime.addItem(str('%0.3f' % i))

    # noinspection PyArgumentList
    def on_listTime_clicked(self):
        self.initial_diagnostics()
        self.initial_importData()
        self.mplCanvas.clean()
        self.par['Tree'] = self.tab1.listTree.currentItem().text()
        time = int(float(self.tab1.listTime.currentItem().text()))
        self.par['Time'] = time
        self.lShowTime.setNum(time)
        if self.tab1.rbMdsPlus.isChecked():
            self.chk_wh_dia_wk()

    # noinspection PyArgumentList
    def chk_wh_dia_wk(self):
        """
        check which diagnostics work
        :return: none
        """
        if self.par['Profile'] == 'Te':
            # Thomson_core
            try:
                mdsopen('TS_EAST', self.par['Shot'])
                mdsvalue('dim_of(Te_coreTS)')
            except RuntimeError:
                print 'Te_coreTS data:\t .... .... .... N/A'
            else:
                self.tab1.diagnostics1.setDisabled(False)
                print 'Te_coreTS data:\t .... .... .... OK'

            # ECE
            try:
                mdsopen('HRS_EAST', self.par['Shot'])
                mdsvalue('dim_of(Te_HRS)')
            except RuntimeError:
                print 'Te_HRS data:\t .... .... .... N/A'
            else:
                self.tab1.diagnostics3.setDisabled(False)
                print 'Te_HRS data:\t .... .... .... OK'

            # Michelson
            try:
                mdsopen('MPI_Analy', self.par['Shot'])
                mdsvalue('dim_of(Te_MI)')
            except RuntimeError:
                print 'Te_MI data:\t\t .... .... .... N/A'
            else:
                self.tab1.diagnostics4.setDisabled(False)
                print 'Te_MI data:\t\t .... .... .... OK'

            # TXCS
            try:
                mdsopen('TXCS_EAST', self.par['Shot'])
                mdsvalue('dim_of(Te_TXCS)')
            except RuntimeError:
                print 'Te_TXCS data:\t .... .... .... N/A'
            else:
                self.tab1.diagnostics5.setDisabled(False)
                print 'Te_TXCS data:\t .... .... .... OK'

        elif self.par['Profile'] == 'Ti':
            # CXRS
            try:
                mdsopen('CXRS_EAST', self.par['Shot'])
                mdsvalue('dim_of(Ti_CXRS_T)')
            except RuntimeError:
                print 'Ti_CXRS_T data:\t .... .... .... N/A'
            else:
                self.tab1.diagnostics1.setDisabled(False)
                print 'Ti_CXRS_T data:\t .... .... .... OK'

            # TXCS
            try:
                mdsopen('TXCS_EAST', self.par['Shot'])
                print mdsvalue('dim_of(Ti_TXCS)')
            except RuntimeError, e:
                print e
                print 'Ti_TXCS data:\t .... .... .... N/A'
            else:
                self.tab1.diagnostics3.setDisabled(False)
                print 'Ti_TXCS data:\t .... .... .... OK'

        elif self.par['Profile'] == 'ne':
            # Reflectometry
            try:
                mdsopen('ReflJ_EAST', self.par['Shot'])
                mdsvalue('dim_of(ne_ReflJ)')
            except RuntimeError:
                print 'ne_TeflJ data:\t .... .... .... N/A'
            else:
                self.tab1.diagnostics1.setDisabled(False)
                print 'ne_ReflJ data:\t .... .... .... OK'

            # Thomson_core
            try:
                mdsopen('TS_EAST', self.par['Shot'])
                mdsvalue('dim_of(ne_coreTS)')
            except RuntimeError:
                print 'ne_coreTS data:\t .... .... .... N/A'
            else:
                self.tab1.diagnostics2.setDisabled(False)
                print 'ne_coreTS data:\t .... .... .... OK'

            # POINT
            try:
                mdsopen('POINT_Analy', self.par['Shot'])
                mdsvalue('dim_of(\\ne_POINT,0)')
            except RuntimeError:
                print 'ne_POINT data:\t .... .... .... N/A'
            else:
                self.tab1.diagnostics4.setDisabled(False)
                print 'ne_POINT data:\t .... .... .... OK'

        elif self.par['Profile'] == 'Vt':
            # CXRS
            try:
                mdsopen('CXRS_EAST', self.par['Shot'])
                mdsvalue('dim_of(Vt_CXRS_T)')
            except RuntimeError:
                print 'Vt_CXRS_T data:\t .... .... .... N/A'
            else:
                self.tab1.diagnostics1.setDisabled(False)
                print 'Tt_CXRS_T data:\t .... .... .... OK'

            # TXCS
            try:
                mdsopen('TXCS_EAST', self.par['Shot'])
                print mdsvalue('dim_of(Vt_TXCS)')
            except RuntimeError, e:
                print e
                print 'Vt_TXCS data:\t .... .... .... N/A'
            else:
                self.tab1.diagnostics2.setDisabled(False)
                print 'Vt_TXCS data:\t .... .... .... OK'

    def initial_diagnostics(self):
        if self.par['Profile'] == 'Te':
            for i in [self.tab1.diagnostics1, self.tab1.diagnostics2, self.tab1.diagnostics3, self.tab1.diagnostics4,
                      self.tab1.diagnostics5]:
                i.setCheckState(0)
                i.setDisabled(True)
        elif self.par['Profile'] == 'Ti':
            for i in [self.tab1.diagnostics1, self.tab1.diagnostics2, self.tab1.diagnostics3]:
                i.setCheckState(0)
                i.setDisabled(True)
        elif self.par['Profile'] == 'ne':
            for i in [self.tab1.diagnostics1, self.tab1.diagnostics2, self.tab1.diagnostics3, self.tab1.diagnostics4]:
                i.setCheckState(0)
                i.setDisabled(True)
        elif self.par['Profile'] == 'Vt':
            for i in [self.tab1.diagnostics1, self.tab1.diagnostics2]:
                i.setCheckState(0)
                i.setDisabled(True)

    def initial_list(self, obj):
        if obj == 'tree' or obj == 'both':
            if self.tab1.listTree.item(0):
                self.tab1.listTree.clear()
        if obj == 'time' or obj == 'both':
            if self.tab1.listTime.item(0):
                self.tab1.listTime.clear()

    def initial_importData(self):
        from data import Data
        for s in ['data_rho', 'data_psi', 'filein_rho', 'filein_psi',
                  'diagnostic1_rho', 'diagnostic2_rho', 'diagnostic3_rho', 'diagnostic4_rho', 'diagnostic5_rho',
                  'diagnostic1_psi', 'diagnostic2_psi', 'diagnostic3_psi', 'diagnostic4_psi', 'diagnostic5_psi',
                  'diagnostic1_err', 'diagnostic2_err', 'diagnostic3_err', 'diagnostic4_err', 'diagnostic5_err']:
            self.g.value[s] = np.array([])
        for s in ['time1', 'time2', 'time3', 'time4', 'time5']:
            self.g.value[s] = float
        for s in ['processed_data_rho', 'processed_data_psi', 'processed_filein_rho', 'processed_filein_psi',
                  'processed_d1_rho', 'processed_d2_rho', 'processed_d3_rho', 'processed_d4_rho',
                  'processed_d5_rho', 'processed_d1_psi', 'processed_d2_psi', 'processed_d3_psi',
                  'processed_d4_psi', 'processed_d5_psi']:
            self.g.value[s] = Data()
        self.g.library['data_rho'] = np.array([])
        self.g.library['data_psi'] = np.array([])
        self.g.library['processed_rho'] = Data()
        self.g.library['processed_psi'] = Data()

    def mds(self):
        self.statusBar.showMessage('CONNECTING THE MDS+ SERVER...')
        try:
            mdsconnect('202.127.204.12')
            self.statusBar.showMessage('MDS+ SERVER CONNECTED!')
        except Exception, e:
            print Exception, ":", e
            self.statusBar.showMessage('CANNOT CONNECT THE MDS+ SERVER!')
            self.tab1.rbMdsPlus.setDisabled(True)
            self.tab1.rbMdsPlus_2.setDisabled(True)

    def on_actionSetting_clicked(self):
        dlg = Setting(self.par, parent=self)
        dlg.exec_()
        self.par['FittingRange'] = float(dlg.cbFittingRange.currentText())
        self.par['GridSize'] = int(dlg.cbGridSize.currentText())
        # print self.par['GridSize'], 'ii'

    def on_pbTemplates_clicked(self):
        dlg = QtGui.QDialog(self)
        dlg.setWindowTitle("Templates")
        layout = QtGui.QVBoxLayout()
        layout.setMargin(0)
        grid = QtGui.QGridLayout()
        textBrowser = QtGui.QTextBrowser()
        grid.addWidget(textBrowser)
        layout.addLayout(grid)
        dlg.setLayout(layout)
        dlg.resize(500, 500)
        if self.tab1.rbRZMap.isChecked():
            path = "/home/users/zhengzhen/east-fit/template_rz.html"
        elif self.tab1.rbRhoMap.isChecked():
            path = "/home/users/zhengzhen/east-fit/template_rho.html"
        elif self.tab1.rbPsiMap.isChecked():
            path = "/home/users/zhengzhen/east-fit/template_psi.html"
        textBrowser.setSource(QtCore.QUrl(path))
        dlg.show()

    def on_actionRestore_clicked(self):
        """restore the fit file to plot"""
        dlg = QtGui.QFileDialog(self)
        fileName = dlg.getOpenFileName(self,
                                       u"Choose a File to Restore",
                                       os.path.abspath('.'),
                                       "Fit Files (*.fit);;All Files (*)")
        if not fileName:
            return
        if self.par['Func'] == 'tanh_multi':
            value = self.g9.value['Params']
        elif self.par['Func'] == 'tanh_0out':
            value = self.g6.value['Params']
        elif self.par['Func'] == 'spline':
            value = self.g5.value['Params']
        if self.par['RhoPsi'] == 'rho':
            processed_data = self.g.value['processed_data_rho']
            libraryData = self.g.library['data_rho']
        elif self.par['RhoPsi'] == 'psi':
            processed_data = self.g.value['processed_data_psi']
            libraryData = self.g.library['data_psi']
        _input = restoreFile(str(fileName), value, processed_data, self.g.value['fit'], libraryData, self.par)

        self.par = _input['par']
        self.g.value['fit'] = _input['datafit']
        if self.par['Func'] == 'tanh_multi':
            self.g9.value['Params'] = _input['value']
        elif self.par['Func'] == 'tanh_0out':
            self.g6.value['Params'] = _input['value']
        elif self.par['Func'] == 'spline':
            self.g5.value['Params'] = _input['value']
        if self.par['Toggle'] == 'rho':
            self.g.value['processed_data_rho'] = _input['data']
            self.g.library['data_rho'] = _input['library']
        elif self.par['Toggle'] == 'psi':
            self.g.value['processed_data_psi'] = _input['data']
            self.g.library['data_psi'] = _input['library']

        if self.par['Toggle'] == 'rho':
            self.cPlotToggle.setCurrentIndex(0)
        elif self.par['Toggle'] == 'psi':
            self.cPlotToggle.setCurrentIndex(1)
        self.sldStretch.setValue(_input['par']['Stretch'])
        self.sldShift.setValue((_input['par']['Shift']))
        self.lShowShot.setNum(self.par['Shot'])
        self.lShowTime.setNum(self.par['Time'])
        if self.par['Func'] == 'tanh_multi':
            self.cbFunctionSelect.setCurrentIndex(0)
        elif self.par['Func'] == 'tanh_0out':
            self.cbFunctionSelect.setCurrentIndex(1)
        elif self.par['Func'] == 'spline':
            self.cbFunctionSelect.setCurrentIndex(2)
        print self.g.value
        print self.g.library
        self.plot_data(self.par)
        self.plot()
        if self.par['Func'] == 'spline':
            self.plot_spline()
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

# def closeEvent(self, event):
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
