from dataTransfer import *
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # set the range of x axis
        self.ax.set_xlim(0, 1.2)
        self.pickx = []
        self.picky = []
        self.par = {}
        self.value = {}
        self.l1 = None
        self.l2 = None
        self.l3 = None
        self.d1 = None
        self.d2 = None
        self.d3 = None
        self.d4 = None
        self.d5 = None
        self.lines = []
        self.ls = np.array([], dtype=object)
        self.lined = dict()
        self.artist_label = ''
        self.ax.grid(alpha=0.4)
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('button_release_event', self.on_press)

    def plot(self, datafit):
        if self.l1:
            self.ax.lines.remove(self.l1)
        self.l1, = self.ax.plot(datafit.x[0], datafit.y, 'b-', linewidth=3, label='fitted')
        self.show_legend()
        if self.par['vis']:
            pass
        else:
            self.draw()

    def plot_data(self, globalvar, d, par):
        """
        plot_data
        :param d:
        :param globalvar:          GlobalVar
        :param par:                parameter dictionary from main window
        """
        self.g = globalvar
        self.d = d
        self.par = par

        # draw the x,y labels
        self.ax.set_xlabel(r'$\rho$')
        if par['Profile'] == 'Te':
            self.ax.set_ylabel(r'$T_e (keV)$')
        elif par['Profile'] == 'Ti':
            self.ax.set_ylabel(r'$T_i (keV)$')
        elif par['Profile'] == 'ne':
            self.ax.set_ylabel(r'$n_e (10^{19}m^{-3})$')
        elif par['Profile'] == 'Vt':
            self.ax.set_ylabel(r'$V_t (10^{4}m/s)$')

        # draw the title
        # print 'title'
        title = get_title(self.g, par)
        self.ax.set_title(title, fontsize=11, family='Arial')

        # draw each diagnostic separately
        label = get_label(par)

        if self.par['Toggle'] == 'rho':
            s = 'rho'
        elif self.par['Toggle'] == 'psi':
            s = 'psi'

        # draw diagnostic 1
        if par['Diag1']:
            # print "in plot_data\nglobalvar.value['diagnostic1']:\n", globalvar.value['diagnostic1']
            # print "globalvar.value['processed_d1_'+s]\n", globalvar.value['processed_d1_'+s], "\n\n\n\n"
            if self.d1:
                self.ax.lines.remove(self.d1)
            if 0:  # globalvar.value['diagnostic1_err'].any():
                self.d1 = self.ax.errorbar(globalvar.value['processed_d1_' + s].x[0],
                                           globalvar.value['processed_d1_' + s].y,
                                           yerr=globalvar.value['diagnostic1_err'], fmt='yd', label=label[0],
                                           capsize=3, picker=1, alpha=0.8)
            else:
                self.d1, = self.ax.plot(globalvar.value['processed_d1_' + s].x[0],
                                        globalvar.value['processed_d1_' + s].y, 'yd', label=label[0],
                                        picker=1, alpha=0.8)
        else:
            if self.d1:
                self.ax.lines.remove(self.d1)
            self.d1 = None

        # draw diagnostic 2
        if par['Diag2']:
            if self.d2:
                self.ax.lines.remove(self.d2)
            self.d2, = self.ax.plot(globalvar.value['processed_d2_' + s].x[0], globalvar.value['processed_d2_' + s].y,
                                    'ms', label=label[1], picker=1, alpha=0.8)
        else:
            if self.d2:
                self.ax.lines.remove(self.d2)
            self.d2 = None

        # draw diagnostic 3
        if par['Diag3']:
            if self.d3:
                self.ax.lines.remove(self.d3)
            self.d3, = self.ax.plot(globalvar.value['processed_d3_' + s].x[0], globalvar.value['processed_d3_' + s].y,
                                    'c^', label=label[2], picker=1, alpha=0.8)
        else:
            if self.d3:
                self.ax.lines.remove(self.d3)
            self.d3 = None

        # draw diagnostic 4
        if par['Diag4']:
            if self.d4:
                self.ax.lines.remove(self.d4)
            self.d4, = self.ax.plot(globalvar.value['processed_d4_' + s].x[0], globalvar.value['processed_d4_' + s].y,
                                    'gv', label=label[3], picker=1, alpha=0.8)
        else:
            if self.d4:
                self.ax.lines.remove(self.d4)
            self.d4 = None

        # draw diagnostic 5
        if par['Diag5']:
            if self.d5:
                self.ax.lines.remove(self.d5)
            if 0:  # globalvar.value['diagnostic5_err'].any():
                self.d5 = self.ax.errorbar(globalvar.value['processed_d5_' + s].x[0],
                                           globalvar.value['processed_d5_' + s].y,
                                           yerr=globalvar.value['diagnostic5_err'], fmt='r>', label=label[4],
                                           picker=1, alpha=0.8)
            else:
                self.d5, = self.ax.plot(globalvar.value['processed_d5_' + s].x[0],
                                        globalvar.value['processed_d5_' + s].y,
                                        'r>', label=label[4], picker=1, alpha=0.8)
        else:
            if self.d5:
                self.ax.lines.remove(self.d5)
            self.d5 = None

        # draw the total
        if not (par['Diag1'] or par['Diag2'] or par['Diag3'] or par['Diag4'] or par['Diag5']):
            if not par['SourceSwitch']:
                if self.l3:
                    self.ax.lines.remove(self.l3)
                self.l3, = \
                    self.ax.plot(globalvar.value['processed_filein_' + s].x[0],
                                 globalvar.value['processed_filein_' + s].y,
                                 'yo', label='raw data', picker=1, alpha=0.8)
        else:
            if self.l3:
                self.ax.lines.remove(self.l3)
            self.l3 = None

        # draw the excluded data
        if isinstance(globalvar.library['processed_' + s], Data):
            if len(globalvar.library['processed_' + s].x) is not 0:
                if self.l2:
                    self.ax.lines.remove(self.l2)
                self.l2, = self.ax.plot(globalvar.library['processed_' + s].x[0], globalvar.library['processed_' + s].y,
                                        'kx', markersize=10, label='excluded data', picker=1)
            else:
                if self.l2:
                    self.ax.lines.remove(self.l2)
                self.l2 = None
        else:
            if self.l2:
                self.ax.lines.remove(self.l2)
            self.l2 = None

        # set the range of y axis
        # print "globalvar.value['data_'+s]=", globalvar.value['data_'+s]
        if globalvar.value['data_' + s].any():
            self.lim = self.ax.set_ylim(0, np.max(globalvar.value['data_' + s][:, 1]) * 1.2)

        for i in [self.l1, self.l2, self.l3, self.d1, self.d2, self.d3, self.d4, self.d5]:
            if i:
                self.lines.append(i)
        if globalvar.value['data_' + s].any():
            self.show_legend()
        self.draw()

    def plot_knots(self, pos, vis=False):
        if vis:
            if self.ls.any():
                for i in range(self.ls.size):
                    self.ax.lines.remove(self.ls[i])
                self.ls = np.array([], dtype=object)
            for i in range(len(pos)):
                l, = self.ax.plot(pos[i], 0, 'Dr', ms=4, fillstyle='none', alpha=0.4)
                self.ls = np.insert(self.ls, i, l)
        else:
            if self.ls.size:
                for i in range(self.ls.size):
                    if self.ls[i]:
                        self.ax.lines.remove(self.ls[i])
                    self.ls[i] = None
        self.draw()

    def clean_lines(self):
        if self.l1:
            self.ax.lines.remove(self.l1)
            self.l1 = None
        if self.l2:
            self.ax.lines.remove(self.l2)
            self.l2 = None
        if self.l3:
            self.ax.lines.remove(self.l3)
            self.l3 = None
        if self.d1:
            self.ax.lines.remove(self.d1)
            self.d1 = None
        if self.d2:
            self.ax.lines.remove(self.d2)
            self.d2 = None
        if self.d3:
            self.ax.lines.remove(self.d3)
            self.d3 = None
        if self.d4:
            self.ax.lines.remove(self.d4)
            self.d4 = None
        if self.d5:
            self.ax.lines.remove(self.d5)
            self.d5 = None
        if self.ls.size:
            for i in range(self.ls.size):
                if self.ls[i]:
                    self.ax.lines.remove(self.ls[i])
                self.ls[i] = None
        if self.ax.legend_:
            self.ax.legend_.remove()
        self.draw()

    def show_legend(self):
        legend = self.ax.legend(loc='best', fancybox=False, shadow=False)
        legend.get_frame().set_edgecolor('None')
        legend.get_frame().set_alpha(0.4)

    def on_pick(self, event):
        N = len(event.ind)
        if not N:
            return True

        # print '\n'.join(['%s:%s' % item for item in self.d1[1].__dict__.items()])
        print '\n'.join(['%s:%s' % item for item in event.artist.__dict__.items()])
        self.artist_label = event.artist.__getattribute__('_label')
        for junk, ind in enumerate(event.ind):
            line = event.artist
            xdata = line.get_xdata()
            ydata = line.get_ydata()
            self.pickx = xdata[ind]
            self.picky = ydata[ind]
        return True

    def on_press(self, event):
        if event.button == 3:
            if not self.pickx:
                pass
            else:
                pick = {}
                a = ''
                b = ''
                c = psi2rho
                if self.par['Toggle'] == 'rho':
                    a = 'rho'
                    b = 'psi'
                    c = rho2psi
                elif self.par['Toggle'] == 'psi':
                    a = 'psi'
                    b = 'rho'
                    c = psi2rho
                # print 'len(self.pickx[0]): ', len(self.pickx[0])
                pick[a] = np.array([[self.pickx, self.picky]])
                if self.par['RbFile2']:
                    efitDir = str(self.par['EfitDir'])
                    efitDir = os.path.dirname(efitDir)
                    tmp = c(self.par['Shot'], self.par['Time'], efitDir, pick[a][:, 0])
                    pick[b] = np.array([tmp[b], pick[a][:, 1]]).T
                else:
                    # tree = str(self.par['Tree'])
                    tmp = c(self.par['Shot'], self.par['Time'], str(self.par['Tree']), pick[a][:, 0])
                    pick[b] = np.array([tmp[b], pick[a][:, 1]]).T
                self.g = process_excluded_data(self.artist_label, self.par['Profile'], self.par, self.g, pick)
                self.plot_data(self.g, self.d, self.par)

            if self.l1:
                if self.par['Toggle'] == 'rho':
                    processed_data = self.g.value['processed_data_rho']
                elif self.par['Toggle'] == 'psi':
                    processed_data = self.g.value['processed_data_psi']
                params = self.d.value['Params']
                datafit, junk = fit(processed_data, self.par, params)
                self.plot(datafit)
        else:
            pass


class MplCanvasWrapper(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MplCanvas(parent)
        self.vb = QtGui.QVBoxLayout(self)
        self.vb.setMargin(0)
        self.ntb = NavigationToolbar(self.canvas, parent)
        self.vb.addWidget(self.ntb)
        self.vb.addWidget(self.canvas)
        self.setLayout(self.vb)
        self.data = Data()
        self.datafit = Data()

    def fit(self, data, value, par):
        if par['Toggle'] == 'rho':
            self.datafit, value['Params'] = fit(data['processed_data_rho'], par, value['Params'])
        elif par['Toggle'] == 'psi':
            self.datafit, value['Params'] = fit(data['processed_data_psi'], par, value['Params'])
        # self.datafit *= 1.0
        self.canvas.plot(self.datafit)
        if par['Func'] == 'spline':
            return self.datafit.spline_chisq, value, self.datafit
        else:
            return self.datafit.fit_chisq, value, self.datafit

    def plot_data(self, globalvar, d, par):
        globalvar = process_data(globalvar, par)
        self.canvas.plot_data(globalvar, d, par)

    def clean(self):
        self.canvas.clean_lines()


def fit(processed_data, par, params):
    """
    fit data with fit function
    :param processed_data:
    :param par:
    :param params:
    :return: datafit, params
    """
    # Choose grid sizes
    if par['FittingRange'] == 1.0:
        grid = par['GridSize']
    elif par['FittingRange'] == 1.1:
        grid = par['GridSize'] + 5
    elif par['FittingRange'] == 1.2:
        grid = par['GridSize'] + 10
    rho = np.linspace(0, par['FittingRange'], grid)
    # print rho
    func = par['Func']
    if par['Func'] == 'tanh_multi' and (len(params) == 0 or len(params) != 3):
        params = [[970, 50, 100, 20, 100, 0, 0, 0, 0],
                  [[0, 1000], [0, 1000], [0, 1000], [0, 1000], [0, 1000], [0, 1000], [0, 1000],
                   [0, 1000], [0, 1000]], [0, 0, 0, 0, 2, 2, 2, 2, 2]]
    elif par['Func'] == 'tanh_0out' and (len(params) == 0 or len(params) != 3):
        params = [[950, 100, 2300, -100, 0, 0], [[0, 1000], [0, 1000], [0, 3000], [0, 1000], [0, 1000], [0, 1000]],
                  [0, 0, 0, 2, 2, 2]]
    elif par['Func'] == 'spline' and (len(params) == 0 or len(params) != 5):
        params = [0, 500, 900, 950, 1000]
    if par['Func'] == 'spline':
        print params
        knots = [i / 1000. for i in params]
    else:
        c = [i / 1000. for i in params[0]]
        iFix = [i / 2 for i in params[-1]]
    if par['Func'] == 'spline':
        datafit = processed_data.spline(s=20, knots=knots)
    else:
        datafit = processed_data.fit(func, c, epsfcn=1.e-8, use_odr=1, ifixb=iFix, param=0.)
    # print '1111', rho, datafit
    datafit = datafit.newx(rho)
    # print '2222', datafit
    return datafit, params


def process_data(globalvar, par):
    for s in 'rho', 'psi':
        if len(globalvar.value['data_' + s]) is not 0:
            globalvar.value['processed_data_' + s] = scale_shift(globalvar.value['data_' + s], par)
        if type(globalvar.library['data_' + s]).__module__ == np.__name__:
            if len(globalvar.library['data_' + s]) is not 0:
                globalvar.library['processed_' + s] = scale_shift(globalvar.library['data_' + s], par)
        else:
            pass
        if par['SourceSwitch']:
            if globalvar.value['diagnostic1_' + s].any():
                globalvar.value['processed_d1_' + s] = scale_shift(globalvar.value['diagnostic1_' + s], par)
            if globalvar.value['diagnostic2_' + s].any():
                globalvar.value['processed_d2_' + s] = scale_shift(globalvar.value['diagnostic2_' + s], par)
            if globalvar.value['diagnostic3_' + s].any():
                globalvar.value['processed_d3_' + s] = scale_shift(globalvar.value['diagnostic3_' + s], par)
            if globalvar.value['diagnostic4_' + s].any():
                globalvar.value['processed_d4_' + s] = scale_shift(globalvar.value['diagnostic4_' + s], par)
            if globalvar.value['diagnostic5_' + s].any():
                globalvar.value['processed_d5_' + s] = scale_shift(globalvar.value['diagnostic5_' + s], par)
        else:
            if globalvar.value['filein_' + s].any():
                globalvar.value['processed_filein_' + s] = scale_shift(globalvar.value['filein_' + s], par)
    return globalvar


def scale_shift(raw, par):
    data = Data()
    temp = raw.copy()
    h = temp.shape[0]
    zoom = 1 + par['Stretch'] / 1000.
    if zoom != 1:
        for i in range(h):
            temp[i, 0] *= zoom
    shift = par['Shift'] / 1000.
    data.x = [temp[:, 0] + shift]
    data.y = temp[:, 1]
    # if par['Profile'] == 'Te':
    #     if temp[:, 1].max(axis=0) > 10:
    #         data.y = temp[:, 1] / 1000.
    #     else:
    #         data.y = temp[:, 1]
    # elif par['Profile'] == 'Ti':
    #     data.y = temp[:, 1] / 1000.
    # elif par['Profile'] == 'ne':
    #     data.y = temp[:, 1] / 1.e19

    # data = data.spline(quiet=1)
    return data


def get_label(par):
    label = ['', '', '', '', '']
    # diagnostic 1
    if par['Diag1']:
        if par['Profile'] == 'Te':
            label[0] = 'Thomson (Core)'
        elif par['Profile'] == 'Ti':
            label[0] = 'CXRS (Core)'
        elif par['Profile'] == 'ne':
            label[0] = 'Reflectometry'
        elif par['Profile'] == 'Vt':
            label[0] = 'CXRS (Core)'

    # diagnostic 2
    if par['Diag2']:
        if par['Profile'] == 'Te':
            label[1] = 'Thomson (Edge)'
        elif par['Profile'] == 'Ti':
            label[1] = 'CXRS (Edge)'
        elif par['Profile'] == 'ne':
            label[1] = 'Thomson (Core)'
        elif par['Profile'] == 'Vt':
            label[0] = 'TXCS'

    # diagnostic 3
    if par['Diag3']:
        if par['Profile'] == 'Te':
            label[2] = 'ECE'
        elif par['Profile'] == 'Ti':
            label[2] = 'TXCS'
        elif par['Profile'] == 'ne':
            label[2] = 'Thomson (Edge)'

    # diagnostic 4
    if par['Diag4']:
        if par['Profile'] == 'Te':
            label[3] = 'Michelson'
        elif par['Profile'] == 'Ti':
            label[3] = None
        elif par['Profile'] == 'ne':
            label[3] = 'POINT'

    # diagnostic 5
    if par['Diag5']:
        if par['Profile'] == 'Te':
            label[4] = 'TXCS'
        elif par['Profile'] == 'Ti':
            label[4] = None
        elif par['Profile'] == 'ne':
            label[4] = None

    return label


def get_title(g, par):
    title = ''
    # diagnostic 1
    if par['Diag1']:
        if par['Profile'] == 'Te':
            title += 'Thomson'
        elif par['Profile'] == 'Ti':
            title += 'CXRS'
        elif par['Profile'] == 'ne':
            title += 'Reflectometry'
        elif par['Profile'] == 'Vt':
            title += 'CXRS'
        title += ' ' + str(round(g.value['time1'] * 1000, 3)) + 'ms' + ' + '

    # diagnostic 2
    if par['Diag2']:
        if par['Profile'] == 'Te':
            title += None
        elif par['Profile'] == 'Ti':
            title += None
        elif par['Profile'] == 'ne':
            title += 'Thomson'
        elif par['Profile'] == 'Vt':
            title += 'TXCS'
        title += ' ' + str(round(g.value['time2'] * 1000, 3)) + 'ms' + ' + '

    # diagnostic 3
    if par['Diag3']:
        if par['Profile'] == 'Te':
            title += 'ECE'
        elif par['Profile'] == 'Ti':
            title += 'TXCS'
        elif par['Profile'] == 'ne':
            title += None
        title += ' ' + str(round(g.value['time3'] * 1000, 3)) + 'ms' + ' + '

    # diagnostic 4
    if par['Diag4']:
        if par['Profile'] == 'Te':
            title += 'Michelson'
        elif par['Profile'] == 'Ti':
            title += None
        elif par['Profile'] == 'ne':
            title += 'POINT'
        title += ' ' + str(round(g.value['time4'] * 1000, 3)) + 'ms' + ' + '

    # diagnostic 5
    if par['Diag5']:
        if par['Profile'] == 'Te':
            title += 'TXCS'
        elif par['Profile'] == 'Ti':
            title += None
        elif par['Profile'] == 'ne':
            title += None
        title += ' ' + str(round(g.value['time5'] * 1000, 3)) + 'ms'

    if title[:3] == ' + ':
        title = title[3:]
    if title[-3:] == ' + ':
        title = title[:-3]
    return title


def process_excluded_data(label, text, par, globalvar, pick):
    """
    process_excluded_data
    :param label: label got from event.artist._label, used to decide to choose which data to process
    :param text: Te or Ti or ne
    :param par: par
    :param globalvar: GlobalVar
    :param pick: event.pickx and event.picky
    """
    value = globalvar.value.copy()
    library = globalvar.library.copy()
    database = globalvar.database.copy()
    for s in 'rho', 'psi':
        globalvar.value['data_' + s], globalvar.value['processed_data_' + s], globalvar.library \
            = process_pick(value['processed_data_' + s], value['data_' + s], pick[s], library, par, s)
        if label == 'raw data':
            globalvar.value['filein_' + s], globalvar.value['processed_filein_' + s], globalvar.library \
                = process_pick(value['processed_filein_' + s], value['filein_' + s], pick[s], library, par, s)
        elif label == 'Thomson (Core)':
            if text == 'Te':
                globalvar.value['diagnostic1_' + s], globalvar.value['processed_d1_' + s], globalvar.library \
                    = process_pick(value['processed_d1_' + s], value['diagnostic1_' + s], pick[s], library, par, s)
            elif text == 'ne':
                globalvar.value['diagnostic2_' + s], globalvar.value['processed_d2_' + s], globalvar.library \
                    = process_pick(value['processed_d2_' + s], value['diagnostic2_' + s], pick[s], library, par, s)
        elif label == 'CXRS (Core)':
            globalvar.value['diagnostic1_' + s], globalvar.value['processed_d1_' + s], globalvar.library \
                = process_pick(value['processed_d1_' + s], value['diagnostic1_' + s], pick[s], library, par, s)
        elif label == 'ECE':
            globalvar.value['diagnostic3_' + s], globalvar.value['processed_d3_' + s], globalvar.library \
                = process_pick(value['processed_d3_' + s], value['diagnostic3_' + s], pick[s], library, par, s)
        elif label == 'Michelson':
            globalvar.value['diagnostic4_' + s], globalvar.value['processed_d4_' + s], globalvar.library \
                = process_pick(value['processed_d4_' + s], value['diagnostic4_' + s], pick[s], library, par, s)
        elif label == 'TXCS':
            if text == 'Te':
                globalvar.value['diagnostic5_' + s], globalvar.value['processed_d5_' + s], globalvar.library \
                    = process_pick(value['processed_d5_' + s], value['diagnostic5_' + s], pick[s], library, par, s)
            elif text == 'Ti':
                globalvar.value['diagnostic3_' + s], globalvar.value['processed_d3_' + s], globalvar.library \
                    = process_pick(value['processed_d3_' + s], value['diagnostic3_' + s], pick[s], library, par, s)
        elif label == 'Reflectometry':
            globalvar.value['diagnostic1_' + s], globalvar.value['processed_d1_' + s], globalvar.library \
                = process_pick(value['processed_d1_' + s], value['diagnostic1_' + s], pick[s], library, par, s)
        elif label == 'POINT':
            globalvar.value['diagnostic3_' + s], globalvar.value['processed_d3_' + s], globalvar.library \
                = process_pick(value['processed_d3_' + s], value['diagnostic3_' + s], pick[s], library, par, s)
        elif label == 'excluded data':
            # print "in line 603:\ndatabase=", database, "//\n"
            pick_tmp = Data()
            pick_tmp.x = [pick[s][:, 0]]
            pick_tmp.y = pick[s][:, 1]
            pick_tmp = undo_scale_shift(pick_tmp, par)
            for k, i in database.iteritems():
                # print 'a'
                if k[-3:] == s:
                    for j in pick_tmp:
                        if j in i:
                            # print 'b'
                            for key, var in database.iteritems():
                                # print 'c'
                                if key[-3:] == s:
                                    foo = var == i
                                    # print foo
                                    if type(foo).__module__ == np.__name__:
                                        judge = foo.all()
                                    else:
                                        judge = foo
                                    if judge:
                                        # print 'd'
                                        globalvar = process_pick2(pick[s], globalvar, key, par, s)
    return globalvar


def process_pick(processed, data, pick, library, par, s):
    """
    if pick is in processed, delete the diagnostic point, return new processed and data
    if not, return original processed and data
    :param s: string, 'rho' or 'psi'
    :param library: globalvar.library
    :param processed: original processed
    :param data: original data
    :param pick: pick
    :param par: parameter
    :return: processed, data
    """
    for i in pick[:, 1]:
        if i in processed.y:  # if pick is in processed, delete the diagnostic point, return new processed and data
            # delete the point from processed
            temp1 = processed.copy()
            ind = temp1.y != i
            temp1.y = temp1.y[ind]
            temp1.x[0] = temp1.x[0][ind]
            # get data corresponding to processed
            temp2 = undo_scale_shift(temp1, par)

            # get point in pick corresponding to i
            index = pick[:, 1] == i
            j = pick[:, 0][index][0]
            point = np.array([[j, i]])
            # add the point to GlobalVar.library['processed_rho']
            library = ExcludedData(library, point, s)
            # get data corresponding to processed of excluded, and add it to GlobalVar.library['data_rho']
            library['data_' + s] = undo_scale_shift(library['processed_' + s], par)
            # return new processed and data
            return temp2, temp1, library
        else:  # if not, return original processed and data
            return data, processed, library


def process_pick2(pick, globalvar, key, par, s):
    """
    add pick to processed_data_rho/d1/d2/d3/d4/d5, delete it from excluded data
    :param s: string, 'rho', or 'psi'
    :param globalvar:
    :param pick: pick
    :param key: d1, d2, d3, d4, d5
    :param par: par
    """
    # print "in process_pick2, before:\nglobalvar.library=\n", globalvar.library
    temp1 = globalvar.value['processed_data_' + s].copy()
    if par['SourceSwitch']:
        if key == 'd1_' + s:
            temp2 = globalvar.value['processed_d1_' + s].copy()
        elif key == 'd2_' + s:
            temp2 = globalvar.value['processed_d2_' + s].copy()
        elif key == 'd3_' + s:
            temp2 = globalvar.value['processed_d3_' + s].copy()
        elif key == 'd4_' + s:
            temp2 = globalvar.value['processed_d4_' + s].copy()
        elif key == 'd5_' + s:
            temp2 = globalvar.value['processed_d5_' + s].copy()
    else:
        temp2 = globalvar.value['processed_filein_' + s].copy()
    for i in pick[:, 0]:
        if i in globalvar.library['processed_' + s].x[0]:
            # if par['SourceSwitch']:
            index = pick[:, 0] == i
            j = pick[:, 1][index][0]

            temp1.x[0] = np.hstack((temp1.x[0], i))
            temp1.y = np.hstack((temp1.y, j))
            # sort by ascending
            sort = np.argsort(temp1.x[0], axis=0)
            temp1.x[0] = temp1.x[0][sort]
            temp1.y = temp1.y[sort]
            temp3 = undo_scale_shift(temp1, par)

            temp2.x[0] = np.hstack((temp2.x[0], i))
            temp2.y = np.hstack((temp2.y, j))
            # sort by ascending
            sort = np.argsort(temp2.x[0], axis=0)
            temp2.x[0] = temp2.x[0][sort]
            temp2.y = temp2.y[sort]
            temp4 = undo_scale_shift(temp2, par)

            point = np.array([[i, j]])
            globalvar.library = ExcludedData(globalvar.library, point, s, False)
            globalvar.library['data_' + s] = undo_scale_shift(globalvar.library['processed_' + s], par)
            # print "in process_pick2:\nGlobalVar.library['data_rho']=\n", GlobalVar.library['data_rho']

            if par['SourceSwitch']:
                if key == 'd1_' + s:
                    globalvar.value['processed_data_' + s], globalvar.value['processed_d1_' + s] = temp1, temp2
                    globalvar.value['data_' + s], globalvar.value['diagnostic1_' + s] = temp3, temp4
                elif key == 'd2_' + s:
                    globalvar.value['processed_data_' + s], globalvar.value['processed_d2_' + s] = temp1, temp2
                    globalvar.value['data_' + s], globalvar.value['diagnostic2_' + s] = temp3, temp4
                elif key == 'd3_' + s:
                    globalvar.value['processed_data_' + s], globalvar.value['processed_d3_' + s] = temp1, temp2
                    globalvar.value['data_' + s], globalvar.value['diagnostic3_' + s] = temp3, temp4
                elif key == 'd4_' + s:
                    globalvar.value['processed_data_' + s], globalvar.value['processed_d4_' + s] = temp1, temp2
                    globalvar.value['data_' + s], globalvar.value['diagnostic4_' + s] = temp3, temp4
                elif key == 'd5_' + s:
                    globalvar.value['processed_data_' + s], globalvar.value['processed_d5_' + s] = temp1, temp2
                    globalvar.value['data_' + s], globalvar.value['diagnostic5_' + s] = temp3, temp4
            else:
                globalvar.value['processed_data_' + s], globalvar.value['processed_filein_' + s] = temp1, temp2
                globalvar.value['data_' + s], globalvar.value['filein_' + s] = temp3, temp4
        else:
            pass
            # print "in process_pick2, after:\nglobalvar.library=\n", globalvar.library
    return globalvar


def undo_scale_shift(data, par):
    temp = data.deepcopy()
    # print "in undo_scale_shift:\ntemp=\n", temp
    h = temp.x[0].shape[0]
    zoom = 1 + par['Stretch'] / 1000.
    for i in range(h):
        temp.x[0][i] /= zoom
    shift = par['Shift'] / 1000.
    temp.x[0][:] = temp.x[0][:] - shift
    result = np.array([temp.x[0], temp.y]).T
    return result
