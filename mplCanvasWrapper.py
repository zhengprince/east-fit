from PyQt4 import QtGui
from RZmap import *
from data import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from pylab import *
from eastmap import east_mapping
from pmds import *

MP = 1.67e-27  # the mass of proton, in kg
ee = 1.602e-19
zz = 6  # Carbon
zeff = 2.5  #
nedge = 10  # edge points to fix current


def line_picker(line, event):
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
        props = dict(ind=ind, pickx=pickx, picky=picky)
        return True, props
    else:
        return False, dict()


def onpick(event):
    print('point:', event.pickx, event.picky)


class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ax.set_xlabel(r'$\rho$', fontsize=16)
        self.l1 = None
        self.l2 = None

    def plot(self, data, datafit, profile):
        if profile == 'Te':
            self.ax.set_ylabel(r'$T_e (keV)$', fontsize=16)
        elif profile == 'ne':
            self.ax.set_ylabel(r'$n_e (10^{19}m^{-3})$', fontsize=16)
        if self.l1:
            self.ax.lines.remove(self.l1)
        if self.l2:
            self.ax.lines.remove(self.l2)
        self.l1, = self.ax.plot(data.x[0], data.y, 'yo', label='original', picker=line_picker)
        self.l2, = self.ax.plot(datafit.x[0], datafit.y, 'r', label='Fitted')
        self.ax.legend()
        cax = gca()
        for label in cax.get_xticklabels() + cax.get_yticklabels():
            label.set_fontsize(20)
        self.fig.canvas.mpl_connect('pick_event', onpick)
        self.draw()


def import_data(par):
    global rhoData
    shot = par['Shot']
    time = par['Time']
    filename = str(par['FileName'])
    efitdir = str(par['EfitDir'])
    gfile_name = 'g' + str(shot).zfill(6) + '.' + str(time).zfill(5)
    print value['Params'][0], shot, time, filename, efitdir, gfile_name, '\n', func
    if par['sourceSwitch'] == 0:
        yyy = RZmap(shot, time, efitdir, filename)
        rhoData = yyy['rhoY']
    elif par['sourceSwitch'] == 1:
        MDS_SERVER = '202.127.204.12'
        time /= 1000
        efit_tree = 'efitrt_east'
        if par['profile'] == 'Te':
            pass
        elif par['profile'] == 'ne':
            mdsconnect(MDS_SERVER)
            mdsopen('ReflJ_EAST', shot)
            times = mdsvalue('dim_of(ne_ReflJ)')
            # time_window = 0.01  # time window for the MR diagnostic
            t_index = np.searchsorted(times, time)
            index = '[*,' + str(t_index) + ']'
            ne_MR = mdsvalue('data(ne_ReflJ)' + index)
            R_MR = mdsvalue('data(R_ReflJ)' + index)

            not_nan_idx = np.isfinite(ne_MR)
            ne_MR = ne_MR[not_nan_idx]
            R_MR = R_MR[not_nan_idx]
            #
            z_MR = np.ones(len(R_MR)) * 0.03
            Rz = np.transpose([R_MR, z_MR])
            mapping = east_mapping(shot, time, efit_tree, Rz)
            ne_MR *= 1.e19
            rhoData = column_stack((mapping['rho'].reshape(len(mapping['rho']), 1),
                                    ne_MR.reshape(len(ne_MR), 1)))
    return rhoData


class MplCanvasWrapper(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vb = QtGui.QVBoxLayout()
        self.vb.setMargin(0)
        self.ntb = NavigationToolbar(self.canvas, parent)
        self.vb.addWidget(self.ntb)
        self.vb.addWidget(self.canvas)
        self.setLayout(self.vb)
        psi = np.linspace(0, 1, 51)
        self.rho = psi
        self.data = Data()
        self.datafit = Data()

    def calculation(self, value, par):
        global func
        if par['profile'] == 'Te':
            func = 'tanh_multi'
        elif par['profile'] == 'ne':
            func = 'tanh_0out'
        if len(value['Params']) == 0:
            if func == 'tanh_multi':
                value['Params'] = [[970, 50, 100, 20, 100, 0, 0, 0, 0, 0],
                                   [[0, 1000], [0, 1000], [0, 1000], [0, 1000], [0, 1000], [0, 1000], [0, 1000],
                                   [0, 1000], [0, 1000], [-100, 100]], [0, 0, 0, 0, 2, 2, 2, 2, 2]]
            elif func == 'tanh_0out':
                value['Params'] = [[950, 100, 2300, -100, 0, 0, 0],
                                   [[0, 1000], [0, 1000], [0, 3000], [0, 1000], [0, 1000], [0, 1000], [-100, 100]],
                                   [0, 0, 0, 2, 2, 2]]

        rho_data = import_data(par)

        shift_te = value['Params'][0][-1] / 1000.
        c = [i / 1000. for i in value['Params'][0][:-1]]
        i_fix = [i / 2 for i in value['Params'][-1]]
        tens = 5
        self.data.x = [rho_data[:, 0] + shift_te]
        if par['profile'] == 'Te':
            self.data.y = rho_data[:, 1] / 1000.
        elif par['profile'] == 'ne':
            self.data.y = rho_data[:, 1] / 1.e6

        self.data = self.data.spline(quiet=1)
        self.datafit = self.data.fit(func, c, epsfcn=1.e-8, use_odr=1, ifixb=i_fix, param=0.)

        if par['profile'] == 'Te':
            self.datafit = self.datafit.newx(self.rho)
        elif par['profile'] == 'ne':
            # self.data.y *= 1.e13
            # self.datafit = self.datafit.newx(self.rho) * 1.e13
            # self.datafit.x[0] = self.rho**0.9
            self.datafit = self.datafit.spline()
            self.datafit = self.datafit.newx(self.rho)

        self.datafit *= 1.0
        self.canvas.plot(self.data, self.datafit, par['profile'])
