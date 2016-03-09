# -*- coding:utf-8 -*-
import sys

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

from Code_MainWindow import Code_MainWindow
from Ui_profileselectwidget import Ui_ProfileSelectWidget


class MainWindow(QtGui.QWidget, Ui_ProfileSelectWidget):
    def __init__(self, parent=None):

        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        # 初始化position
        self.m_DragPosition = self.pos()

        self.resize(170, 380)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setMouseTracking(True)

        qbtn_close = QtGui.QPushButton(self)
        qbtn_close.setGeometry(140, 0, 30, 30)
        qbtn_close.setStyleSheet("QPushButton"
                                 "{background-color:#D35400;image:url(:/image/appbar.close2.png);border:none;}"
                                 "QPushButton:hover"
                                 "{background-color:#FF0000;image:url(:/image/appbar.close2.png);border:none;}"
                                 "QPushButton:pressed"
                                 "{background-color:#A00000;image:url(:/image/appbar.close2.png);border:none;}")

        # 注册事件
        qbtn_close.clicked.connect(quit)

    # 支持窗口拖动,重写两个方法
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if QMouseEvent.buttons() and Qt.LeftButton:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False

    @QtCore.pyqtSignature("")
    def on_bElectronTemperature_clicked(self):
        win = Code_MainWindow(parent=self, profile='Te')
        win.show()

    @QtCore.pyqtSignature("")
    def on_bElectronDensity_clicked(self):
        win = Code_MainWindow(parent=self, profile='ne')
        win.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
