# -*- coding:utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

from MainWindow import MainWindow
from Ui_profileselect import Ui_ProfileSelect


class Panel(QtGui.QWidget, Ui_ProfileSelect):
    def __init__(self, parent=None):

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
        qbtn_minus.setGeometry(115, 0, 30, 30)
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

    @QtCore.pyqtSignature("")
    def on_bIonTemperature_clicked(self):
        win = MainWindow(parent=self, profile='Ti')
        win.show()

    @QtCore.pyqtSignature("")
    def on_bElectronDensity_clicked(self):
        win = MainWindow(parent=self, profile='ne')
        win.show()


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    mw = Panel()
    mw.show()
    sys.exit(app.exec_())
