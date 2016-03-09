import efit
import sys, os
from data import *
from Namelist import Namelist
from RZmap import *
import numpy as np
from PyQt4 import QtGui
from RZmap import *
from data import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# from pylab import *

MP = 1.67e-27  # the mass of proton, in kg
ee = 1.602e-19
zz = 6  # Carbon
zeff = 2.5  #
nedge = 10  # edge points to fix current


class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ax.set_xlabel(r'$\rho$')
        self.l1 = None
        self.l2 = None

    def plot(self, data, datafit, profile):
        self.ax.set_ylabel(profile)
        if self.l1:
            self.ax.lines.remove(self.l1)
        if self.l2:
            self.ax.lines.remove(self.l2)
        self.l1, = self.ax.plot(data.x[0], data.y, 'yo', label='original', picker=self.line_picker)
        self.l2, = self.ax.plot(datafit.x[0], datafit.y, 'r', label='Fitted')
        self.ax.legend()
        # cax = gca()
        # for label in cax.get_xticklabels() + cax.get_yticklabels():
        #     label.set_fontsize(20)
        self.fig.canvas.mpl_connect('pick_event', self.onpick)
        self.draw()

    def line_picker(self, line, event):
        # picking with a custom hit test function
        # you can define custom pickers by setting picker to a callable
        # function.  The function has the signature
        #
        #  hit, props = func(artist, mouseevent)
        #
        # to determine the hit test.  if the mouse event is over the artist,
        # return hit=True and props is a dictionary of
        # properties you want added to the PickEvent attributes
        """
        find the points within a certain distance from the mouseclick in
        data coords and attach some extra attributes, pickx and picky
        which are the data points that were picked
        :param line: artist
        :param event: mouse event
        """
        if event.xdata is None:
            return False, dict()
        xdata = line.get_xdata()
        ydata = line.get_ydata()
        maxd = 0.05
        d = np.sqrt((xdata - event.xdata) ** 2. + (ydata - event.ydata) ** 2.)

        ind = np.nonzero(np.less_equal(d, maxd))
        if len(ind):
            pickx = np.take(xdata, ind)
            picky = np.take(ydata, ind)
            self.props = dict(ind=ind, pickx=pickx, picky=picky)
            return True, self.props
        else:
            return False, dict()

    def onpick(self, event):
        print('point:', event.pickx, event.picky)


class MplCanvasWrapper(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vb1 = QtGui.QVBoxLayout()
        self.ntb = NavigationToolbar(self.canvas, parent)
        self.vb1.addWidget(self.ntb)
        self.vb1.addWidget(self.canvas)
        self.setLayout(self.vb1)
        psi = np.linspace(0, 1, 51)
        self.rho = psi
        self.data = Data()
        self.datafit = Data()

    def calculation(self, book, func, profile):
        print 'in'
        if profile == 'Te':
            func = 'tanh_multi'
        elif profile == 'ne':
            func = 'tanh_0out'
        if len(book['Params']) == 0:
            if func == 'tanh_multi':
                book['Params'] = [[970, 50, 100, 20, 100, 0, 0, 0, 0, 0],
                                  [[0, 1000], [0, 1000], [0, 1000], [0, 1000], [0, 1000], [0, 1000], [0, 1000],
                                   [0, 1000], [0, 1000], [-100, 100]], [0, 0, 0, 0, 0, 2, 2, 2, 2]]
            elif func == 'tanh_0out':
                book['Params'] = [[950, 100, 2300, -100, 0, 0, 0],
                                  [[0, 1000], [0, 1000], [0, 3000], [0, 1000], [0, 1000], [0, 1000], [-100, 100]],
                                  [0, 0, 0, 2, 2, 2]]
        shot = book['Shot']
        time = book['Time']
        filename = str(book['FileName'])  # '/home/users/zhengzhen/Desktop/kefit_tutor/56963/Te_TS'  # book['FileName']
        efitdir = str(book['EfitDir'])  # '/home/users/zhengzhen/Desktop/kefit_tutor/56963/copy2'  # book['EfitDir']
        gfile_name = 'g' + str(shot).zfill(6) + '.' + str(time).zfill(5)
        print book['Params'][0], shot, time, filename, efitdir, gfile_name, '\n', func
        yyy = RZmap(shot, time, efitdir, filename)
        rhodata = yyy['rhoY']
        shiftte = book['Params'][0][-1] / 1000.
        c = [i / 1000. for i in book['Params'][0][:-1]]
        ifix = [i / 2 for i in book['Params'][-1]]
        tens = 5
        self.data = Data()
        self.data.x = [rhodata[:, 0] + shiftte]

        if profile == 'Te':
            self.data.y = rhodata[:, 1] / 1000.
        elif profile == 'ne':
            self.data.y = rhodata[:, 1] / 1.e19

        self.data = self.data.spline(quiet=1)

        if profile == 'Te':
            pass
        elif profile == 'ne':
            # self.data /= 1.e13
            pass

        self.datafit = self.data.fit(func, c, epsfcn=1.e-8, use_odr=1, ifixb=ifix, param=0.)

        if profile == 'Te':
            self.datafit = self.datafit.newx(self.rho)
        elif profile == 'ne':
            self.data.y *= 1.e13
            self.datafit = self.datafit.newx(self.rho) * 1.e13
            # self.datafit.x[0] = self.rho**0.9
            self.datafit = self.datafit.spline()
            self.datafit = self.datafit.newx(self.rho)

        self.datafit *= 1.0
        self.canvas.plot(self.data, self.datafit, profile)
