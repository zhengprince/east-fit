# -*- coding:utf-8 -*-

import sys, time
from pmds import mdsconnect, mdsopen, mdsvalue, mdsdisconnect

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

from MainWindow import MainWindow
from Ui_profileselect import Ui_ProfileSelect


class Panel(QtGui.QWidget, Ui_ProfileSelect):
    def __init__(self, connected=False, parent=None):

        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        # 初始化position
        self.m_DragPosition = self.pos()

        self.resize(170, 500)
        self.move(100, 250)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setMouseTracking(True)

        # 添加最小化按钮
        qbtn_minus = QtGui.QPushButton(self)
        qbtn_minus.setGeometry(114, 0, 30, 30)
        qbtn_minus.setObjectName(u'qbtn_minus')

        # 添加关闭按钮
        qbtn_close = QtGui.QPushButton(self)
        qbtn_close.setGeometry(145, 0, 30, 30)
        qbtn_close.setObjectName(u'qbtn_close')

        for btn in self.findChildren(QtGui.QPushButton):
            btn.setFocusPolicy(QtCore.Qt.NoFocus)

        qbtn_close.setStyleSheet("QPushButton#qbtn_close"
                                 "{background-color:none;"
                                 "image:url(:/image/appbar.close1.png);"
                                 "border:none;}"
                                 "QPushButton#qbtn_close:hover"
                                 "{background-color:#FF0000;"
                                 "image:url(:/image/appbar.close2.png);"
                                 "border:none;}"
                                 "QPushButton#qbtn_close:pressed"
                                 "{background-color:#F1707A;"
                                 "image:url(:/image/appbar.close2.png);"
                                 "border:none;}")
        qbtn_minus.setStyleSheet("QPushButton#qbtn_minus"
                                 "{background-color:none;"
                                 "image:url(:/image/appbar.minus1.png);"
                                 "border:none;}"
                                 "QPushButton#qbtn_minus:hover"
                                 "{background-color:rgba(0%,0%,0%,15%);"  # #1972B8;"
                                 "image:url(:/image/appbar.minus2.png);"
                                 "border:none}"
                                 "QPushButton#qbtn_minus:pressed"
                                 "{background-color:rgba(0%,0%,0%,10%);"  # #3382C0;"
                                 "image:url(:/image/appbar.minus2.png);"
                                 "border:none;}")
        self.lSelectProfile.setStyleSheet("QLabel#lSelectProfile"
                                          "{font: bold 11pt;}")
        # self.setStyleSheet("QFrame#frame_2"
        #                    "{border-top: 23px solid #0064B1;}")

        # 注册事件
        qbtn_minus.clicked.connect(self.showMinimized)
        qbtn_close.clicked.connect(sys.exit)

        self.connected = connected

    # 支持窗口拖动,重写两个方法
    def mousePressEvent(self, event):
        if event.button() and Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.frameGeometry().topLeft()  # - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton:
            self.move(event.globalPos() - self.m_DragPosition)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_drag = False

    @QtCore.pyqtSignature("")
    def on_bElectronTemperature_clicked(self):
        win = MainWindow(parent=self, profile='Te')
        win.show()
        # self.statusBarP(win)

    @QtCore.pyqtSignature("")
    def on_bIonTemperature_clicked(self):
        win = MainWindow(parent=self, profile='Ti')
        win.show()
        # self.statusBarP(win)

    @QtCore.pyqtSignature("")
    def on_bElectronDensity_clicked(self):
        win = MainWindow(parent=self, profile='ne')
        win.show()
        # self.statusBarP(win)

    def receiveSig(self, connected):
        if connected:
            self.connected = True
        else:
            self.connected = False

    def statusBarP(self, win):
        if self.connected:
            win.statusBar.showMessage('MDS+ SERVER CONNECTED!')
        else:
            win.statusBar.showMessage('CANNOT CONNECT THE MDS+ SERVER!')
            win.tab1.rbMdsPlus.setDisabled(True)
            win.tab1.rbMdsPlus_2.setDisabled(True)


class ConnectMDS(QtCore.QThread):
    trigger = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super(ConnectMDS, self).__init__(parent)

    def run(self):
        try:
            mdsconnect('mds.ipp.ac.cn')
            connected = True
        except Exception, e:
            print Exception, ":", e
            connected = False
        self.trigger.emit(connected)
#
#
# class SlaveWindow(QtGui.QWidget):
#     def __init__(self, parent=None):
#         super(SlaveWindow, self).__init__(parent)
#         top = QtGui.QWidget(self)
#         layout = QtGui.QVBoxLayout(top)  # 垂直布局类QVBoxLayout；
#         self.lcdNumber = QtGui.QLCDNumber()  # 加个显示屏
#         layout.addWidget(self.lcdNumber)
#         # button = QtGui.QPushButton(u"测试")
#         # layout.addWidget(button)
#     @QtCore.pyqtSlot(int)
#     def up(self, v):
#         self.lcdNumber.display(v)

# if __name__ == "__main__":
def run():
    app = QtGui.QApplication(sys.argv)
    mw = Panel()
    mw.show()
    # cm = ConnectMDS()
    # cm.trigger.connect(mw.receiveSig)
    # cm.start()
    sys.exit(app.exec_())
