from PyQt4 import QtGui
from data import Data
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolbar)
# from matplotlib.widgets import Cursor
import numpy as np
import matplotlib.pyplot as plt
from dataTransfer import GlobalVar6, GlobalVar9, ExcludedData, DataBase, ImportData

MP = 1.67e-27  # the mass of proton, in kg
ee = 1.602e-19
zz = 6  # Carbon
zeff = 2.5  #
nedge = 10  # edge points to fix current
rho = np.linspace(0, 1.0, 51)


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
    # for property, value in vars(event).iteritems():
    #     print property, ": ", value
    if event.xdata is None:
        return False, dict()
    xdata = line.get_xdata()
    ydata = line.get_ydata()
    maxd = 0.025
    d = np.sqrt((xdata - event.xdata) ** 2. + (ydata - event.ydata) ** 2.)
    ind = np.nonzero(np.less_equal(d, maxd))
    if len(ind):
        pickx = np.take(xdata, ind)
        picky = np.take(ydata, ind)
        props = dict(ind=ind, pickx=pickx, picky=picky)
        if not pickx.any():
            return False, dict()
        return True, props
    else:
        return False, dict()


# def on_pick(event):
#     print('point:', event.pickx, event.picky)
#
#
# def on_press(event):
#     print('you pressed', event.button)


class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ax.set_xlabel(r'$\rho$', fontsize=16)
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
        self.lined = dict()
        self.artist_label = ''
        # cursor = Cursor(self.ax, useblit=True, color='red', linewidth=2)
        self.ax.grid(True)
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)

    def plot(self, datafit):
        if self.l1:
            self.ax.lines.remove(self.l1)
        self.l1, = self.ax.plot(datafit.x[0], datafit.y, 'b-', linewidth=3, label='fitted')
        self.show_legend()
        self.draw()

    def plot_data(self, par, excluded_data=ExcludedData.library['processed']):
        """
        plot_data
        :param excluded_data:      excluded data
        :param par:                parameter dictionary from main window
        """
        self.par = par

        # draw the x,y labels
        if par['Profile'] == 'Te':
            self.ax.set_ylabel(r'$T_e (keV)$', fontsize=16)
        elif par['Profile'] == 'Ti':
            self.ax.set_ylabel(r'$T_i (keV)$', fontsize=16)
        elif par['Profile'] == 'ne':
            self.ax.set_ylabel(r'$n_e (10^{19}m^{-3})$', fontsize=16)

        # draw the title
        print 'title'
        title = get_title(par)
        self.ax.set_title(title)

        # draw each diagnostic separately
        label = get_label(par)
        # draw diagnostic 1
        if par['Diag1']:
            # print "in plot_data\nvalue['diagnostic1']:\n", value['diagnostic1']
            # print "value['processed_d1']\n", value['processed_d1'], "\n\n\n\n"
            if self.d1:
                self.ax.lines.remove(self.d1)
            self.d1, = self.ax.plot(ImportData.value['processed_d1'].x[0], ImportData.value['processed_d1'].y,
                                    'yd', label=label[0], picker=line_picker, alpha=0.8)
        else:
            if self.d1:
                self.ax.lines.remove(self.d1)
            self.d1 = None

        # draw diagnostic 2
        if par['Diag2']:
            if self.d2:
                self.ax.lines.remove(self.d2)
            self.d2, = self.ax.plot(ImportData.value['processed_d2'].x[0], ImportData.value['processed_d2'].y,
                                    'ms', label=label[1], picker=line_picker, alpha=0.8)
        else:
            if self.d2:
                self.ax.lines.remove(self.d2)
            self.d2 = None

        # draw diagnostic 3
        if par['Diag3']:
            if self.d3:
                self.ax.lines.remove(self.d3)
            self.d3, = self.ax.plot(ImportData.value['processed_d3'].x[0], ImportData.value['processed_d3'].y,
                                    'c^', label=label[2], picker=line_picker, alpha=0.8)
        else:
            if self.d3:
                self.ax.lines.remove(self.d3)
            self.d3 = None

        # draw diagnostic 4
        if par['Diag4']:
            if self.d4:
                self.ax.lines.remove(self.d4)
            self.d4, = self.ax.plot(ImportData.value['processed_d4'].x[0], ImportData.value['processed_d4'].y,
                                    'gv', label=label[3], picker=line_picker, alpha=0.8)
        else:
            if self.d4:
                self.ax.lines.remove(self.d4)
            self.d4 = None

        # draw diagnostic 5
        if par['Diag5']:
            if self.d5:
                self.ax.lines.remove(self.d5)
            self.d5, = self.ax.plot(ImportData.value['processed_d5'].x[0], ImportData.value['processed_d5'].y,
                                    'r>', label=label[4], picker=line_picker, alpha=0.8)
        else:
            if self.d5:
                self.ax.lines.remove(self.d5)
            self.d5 = None

        # draw the total
        if not (par['Diag1'] or par['Diag2'] or par['Diag3'] or par['Diag4'] or par['Diag5']):
            if not par['SourceSwitch']:
                if self.l3:
                    self.ax.lines.remove(self.l3)
                self.l3, = self.ax.plot(ImportData.value['processed_data'].x[0], ImportData.value['processed_data'].y,
                                        'yo', label='raw data', picker=line_picker, alpha=0.8)
        else:
            if self.l3:
                self.ax.lines.remove(self.l3)
            self.l3 = None

        # draw the excluded data
        # if self.l2:
        #     self.ax.lines.remove(self.l2)
        # if type(excluded_data).__module__ != np.__name__:
        # # if not excluded_data:
        #     self.l2 = None
        # else:
        #     self.l2, = self.ax.plot(excluded_data[0], excluded_data[1], 'kx', markersize=10,
        #                             label='excluded data', picker=line_picker)
        if isinstance(ExcludedData.library['processed'], Data):
            if len(ExcludedData.library['processed'].x) is not 0:
                if self.l2:
                    self.ax.lines.remove(self.l2)
                self.l2, = self.ax.plot(excluded_data.x[0], excluded_data.y, 'kx', markersize=10,
                                        label='excluded data', picker=line_picker)
            else:
                if self.l2:
                    self.ax.lines.remove(self.l2)
                self.l2 = None
        else:
            if self.l2:
                self.ax.lines.remove(self.l2)
            self.l2 = None

        # set the range of y axis
        print "ImportData.value['data']=", ImportData.value['data']
        self.ax.set_ylim(0, np.max(ImportData.value['data'][:, 1]) * 1.2)

        for i in [self.l1, self.l2, self.l3, self.d1, self.d2, self.d3, self.d4, self.d5]:
            if i:
                self.lines.append(i)
        self.show_legend()
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
        self.draw()

    def show_legend(self):
        legend = self.ax.legend(loc='upper right', fancybox=True, shadow=True)
        legend.get_frame().set_alpha(0.4)

        # # we will set up a dict mapping legend line to orig line, and enable
        # # picking on the legend line
        # for legline, origline in zip(legend.get_lines(), self.lines):
        #     legline.set_picker(5)
        #     self.lined[legline] = origline

    def on_pick(self, event):
        ###############################################################
        for property, value in vars(event).iteritems():
            print property, ": ", value
        # for property, value in vars(event.artist).iteritems():
        #     print property, ": ", value
        # print '\n\n\n\n\n\n\n'
        print event.artist.__getattribute__('_label')
        # print type(event.artist.__getattribute__('_label'))
        # print str(event.artist.__getattribute__('_label'))
        ###############################################################
        self.artist_label = event.artist.__getattribute__('_label')
        print('point:', event.pickx, event.picky, self.artist_label)
        self.pickx = event.pickx
        self.picky = event.picky

        # # on the pick event, find the orig line corresponding to the
        # # legend proxy line, and toggle the visibility
        # legline = event.artist
        # origline = self.lined[legline]
        # vis = not origline.get_visible()
        # origline.set_visible(vis)
        # # Change the alpha on the line in the legend so we can see what liens
        # # have been toggled
        # if vis:
        #     legline.set_alpha(1.0)
        # else:
        #     legline.set_alpha(0.2)
        # self.fig.canvas.draw()

    def on_press(self, event):
        if event.button == 3:
            # print "before process excluded data\n"
            # print "value['processed_data]:\n", ImportData.value['processed_data']
            # print "value['processed_d1]:\n", ImportData.value['processed_d1']
            if len(self.pickx[0]) != 1:
                pick = np.array(zip(self.pickx[0], self.picky[0]))
            else:
                pick = np.array([[self.pickx[0][0], self.picky[0][0]]])
            print "pick=", pick
            process_excluded_data(self.artist_label, self.par['Profile'], self.par, pick)
            # if type(excluded_data).__module__ == np.__name__:  # if it's not numpy type,it's NoneType
            # # if excluded_data.any():
            #     ExcludedData(excluded_data)
            # else:
            #     ExcludedData(excluded_data, False)
            # print "after process excluded data\n"
            # print "value['processed_data']:\n", ImportData.value['processed_data']
            # print "value['processed_d1]:\n", ImportData.value['processed_d1'], "\n\n\n\n\n"
            self.plot_data(self.par)

            if self.l1:
                processed_data = ImportData.value['processed_data']
                func = self.par['Func']
                c = []
                i_fix = []
                if self.par['Func'] == 'tanh_multi':
                    func = self.par['Func']
                    if len(GlobalVar9.value['Params']) == 0:
                        GlobalVar9.value['Params'] = [[970, 50, 100, 20, 100, 0, 0, 0, 0],
                                                      [[0, 1000], [0, 1000], [0, 1000], [0, 1000], [0, 1000], [0, 1000],
                                                       [0, 1000],
                                                       [0, 1000], [0, 1000]], [0, 0, 0, 0, 2, 2, 2, 2, 2]]
                    c = [i / 1000. for i in GlobalVar9.value['Params'][0]]
                    i_fix = [i / 2 for i in GlobalVar9.value['Params'][-1]]
                elif self.par['Func'] == 'tanh_0out':
                    func = self.par['Func']
                    if len(GlobalVar6.value['Params']) == 0:
                        GlobalVar6.value['Params'] = [[950, 100, 2300, -100, 0, 0],
                                                      [[0, 1000], [0, 1000], [0, 3000], [0, 1000], [0, 1000],
                                                       [0, 1000]],
                                                      [0, 0, 0, 2, 2, 2]]
                    c = [i / 1000. for i in GlobalVar6.value['Params'][0]]
                    i_fix = [i / 2 for i in GlobalVar6.value['Params'][-1]]
                datafit = processed_data.fit(func, c, epsfcn=1.e-8, use_odr=1, ifixb=i_fix, param=0.)
                datafit = datafit.newx(rho)
                self.plot(datafit)
        else:
            pass


class MplCanvasWrapper(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vb = QtGui.QVBoxLayout(self)
        self.vb.setMargin(0)
        self.ntb = NavigationToolbar(self.canvas, parent)
        self.vb.addWidget(self.ntb)
        self.vb.addWidget(self.canvas)
        self.setLayout(self.vb)
        self.data = Data()
        self.datafit = Data()

    def fit(self, data, value, par):
        func = par['Func']
        if len(value['Params']) == 0:
            if func == 'tanh_multi':
                value['Params'] = [[970, 50, 100, 20, 100, 0, 0, 0, 0],
                                   [[0, 1000], [0, 1000], [0, 1000], [0, 1000], [0, 1000], [0, 1000], [0, 1000],
                                    [0, 1000], [0, 1000]], [0, 0, 0, 0, 2, 2, 2, 2, 2]]
            elif func == 'tanh_0out':
                value['Params'] = [[950, 100, 2300, -100, 0, 0],
                                   [[0, 1000], [0, 1000], [0, 3000], [0, 1000], [0, 1000], [0, 1000]],
                                   [0, 0, 0, 2, 2, 2]]
        c = [i / 1000. for i in value['Params'][0]]
        i_fix = [i / 2 for i in value['Params'][-1]]
        self.datafit = data['processed_data'].fit(func, c, epsfcn=1.e-8, use_odr=1, ifixb=i_fix, param=0.)
        self.datafit = self.datafit.newx(rho)

        # self.datafit *= 1.0
        self.canvas.plot(self.datafit)

    def plot_data(self, par):
        process_data(par)
        self.canvas.plot_data(par)

    def clean(self):
        self.canvas.clean_lines()


def process_data(par):
    if len(ImportData.value['data']) is not 0:
        ImportData.value['processed_data'] = scale_shift(ImportData.value['data'], par)
    if type(ExcludedData.library['data']).__module__ == np.__name__:
        if len(ExcludedData.library['data']) is not 0:
            ExcludedData.library['processed'] = scale_shift(ExcludedData.library['data'], par)
    else:
        # ExcludedData.library['processed'] = None
        pass
    if par['SourceSwitch']:
        if ImportData.value['diagnostic1'].any():
            ImportData.value['processed_d1'] = scale_shift(ImportData.value['diagnostic1'], par)
            x = ImportData.value['processed_d1'].x[0]
            y = np.array(ImportData.value['processed_d1'].y)
            temp = np.array([x, y]).T
            DataBase(d1=temp)
        if ImportData.value['diagnostic2'].any():
            ImportData.value['processed_d2'] = scale_shift(ImportData.value['diagnostic2'], par)
            x = ImportData.value['processed_d2'].x[0]
            y = np.array(ImportData.value['processed_d2'].y)
            temp = np.array([x, y]).T
            DataBase(d2=temp)
        if ImportData.value['diagnostic3'].any():
            ImportData.value['processed_d3'] = scale_shift(ImportData.value['diagnostic3'], par)
            x = ImportData.value['processed_d3'].x[0]
            y = np.array(ImportData.value['processed_d3'].y)
            temp = np.array([x, y]).T
            DataBase(d3=temp)
        if ImportData.value['diagnostic4'].any():
            ImportData.value['processed_d4'] = scale_shift(ImportData.value['diagnostic4'], par)
            x = ImportData.value['processed_d4'].x[0]
            y = np.array(ImportData.value['processed_d4'].y)
            temp = np.array([x, y]).T
            DataBase(d4=temp)
        if ImportData.value['diagnostic5'].any():
            ImportData.value['processed_d5'] = scale_shift(ImportData.value['diagnostic5'], par)
            x = ImportData.value['processed_d5'].x[0]
            y = np.array(ImportData.value['processed_d5'].y)
            temp = np.array([x, y]).T
            DataBase(d5=temp)


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


# def scale_shift_for_excluded_data(raw, par):
#     data = Data()
#     temp = raw.copy()
#     zoom = 1 + par['Stretch'] / 1000.
#     temp[:, 0] *= zoom
#     shift = par['Shift'] / 1000.
#     data.x = [temp[:, 0] + shift]
#     data.y = temp[:, 1]
#     return data


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

    # diagnostic 2
    if par['Diag2']:
        if par['Profile'] == 'Te':
            label[1] = 'Thomson (Edge)'
        elif par['Profile'] == 'Ti':
            label[1] = 'CXRS (Edge)'
        elif par['Profile'] == 'ne':
            label[1] = 'Thomson (Core)'

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


def get_title(par):
    title = ''
    # diagnostic 1
    if par['Diag1']:
        if par['Profile'] == 'Te':
            title += 'Thomson'
        elif par['Profile'] == 'Ti':
            title += 'CXRS'
        elif par['Profile'] == 'ne':
            title += 'Reflectometry'
        title += ' ' + str(round(ImportData.value['time1'], 3)) + 's' + ' + '

    # diagnostic 2
    if par['Diag2']:
        if par['Profile'] == 'Te':
            title += None
        elif par['Profile'] == 'Ti':
            title += None
        elif par['Profile'] == 'ne':
            title += 'Thomson'
        title += ' ' + str(round(ImportData.value['time2'], 3)) + 's' + ' + '

    # diagnostic 3
    if par['Diag3']:
        if par['Profile'] == 'Te':
            title += 'ECE'
        elif par['Profile'] == 'Ti':
            title += 'TXCS'
        elif par['Profile'] == 'ne':
            title += None
        title += ' ' + str(round(ImportData.value['time3'], 3)) + 's' + ' + '

    # diagnostic 4
    if par['Diag4']:
        if par['Profile'] == 'Te':
            title += 'Michelson'
        elif par['Profile'] == 'Ti':
            title += None
        elif par['Profile'] == 'ne':
            title += 'POINT'
        title += ' ' + str(round(ImportData.value['time4'], 3)) + 's' + ' + '

    # diagnostic 5
    if par['Diag5']:
        if par['Profile'] == 'Te':
            title += 'TXCS'
        elif par['Profile'] == 'Ti':
            title += None
        elif par['Profile'] == 'ne':
            title += None
        title += ' ' + str(round(ImportData.value['time5'], 3)) + 's'

    if title[:3] == ' + ':
        title = title[3:]
    if title[-3:] == ' + ':
        title = title[:-3]
    return title


def process_excluded_data(label,  # label got from event.artist._label, used to decide to choose which data to process
                          text,  # Te or Ti or ne
                          par,  # par
                          pick):  # event.pickx and event.picky
    """
    process_excluded_data
    :param label: label got from event.artist._label, used to decide to choose which data to process
    :param text: Te or Ti or ne
    :param par: par
    :param pick: event.pickx and event.picky
    """
    # ImportData.value['processed_data'] = process_pick(pick, ImportData.value['processed_data'], par)
    ImportData.value['data'], ImportData.value['processed_data'] \
        = pppp(ImportData.value['processed_data'], pick, par)
    # if type(ExcludedData.library['processed']).__module__ != np.__name__:
    #     # if len(ExcludedData.library['processed']) is not 0:
    #     #     ExcludedData.library['processed'] = process_pick(pick, ExcludedData.library['processed'], label)
    #     pass
    # else:
    #     if len(ExcludedData.library['processed']) is not 0:
    #         ExcludedData.library['processed'] = process_pick(pick, ExcludedData.library['processed'], label)
    if label == 'Thomson (Core)':
        if text == 'Te':
            # x = ImportData.value['processed_d1'].copy().x[0]
            # y = ImportData.value['processed_d1'].copy().y
            # x, y = process_pick(pick, x, y, par)
            # foo = Data()
            # foo.x[0] = x
            # foo.y = y
            # xx = undo_scale_shift(foo, par)
            # d1, d2 = process_pick(pick, xx[:, 0], xx[:, 1], par)
            # ImportData.value['diagnostic1'] = np.array([d1, d2]).T
            ImportData.value['diagnostic1'], ImportData.value['processed_d1']\
                = pppp(ImportData.value['processed_d1'], pick, par)
        elif text == 'ne':
            # ImportData.value['processed_d2'] \
                # = process_pick(pick, ImportData.value['processed_d2'], par)
            ImportData.value['diagnostic2'], ImportData.value['processed_d2']\
                = pppp(ImportData.value['processed_d2'], pick, par)
    elif label == 'CXRS (Core)':
        # ImportData.value['processed_d1'] \
        #     = process_pick(pick, ImportData.value['processed_d1'], par)
        ImportData.value['diagnostic1'], ImportData.value['processed_d1']\
            = pppp(ImportData.value['processed_d1'], pick, par)
    elif label == 'ECE':
        # ImportData.value['processed_d3'] \
        #     = process_pick(pick, ImportData.value['processed_d3'], par)
        ImportData.value['diagnostic3'], ImportData.value['processed_d3']\
            = pppp(ImportData.value['processed_d3'], pick, par)
    elif label == 'Michelson':
        # ImportData.value['processed_d4'] \
        #     = process_pick(pick, ImportData.value['processed_d4'], par)
        ImportData.value['diagnostic4'], ImportData.value['processed_d4']\
            = pppp(ImportData.value['processed_d4'], pick, par)
    elif label == 'TXCS':
        if text == 'Te':
            # ImportData.value['processed_d5'] \
            #     = process_pick(pick, ImportData.value['processed_d5'], par)
            ImportData.value['diagnostic5'], ImportData.value['processed_d5']\
                = pppp(ImportData.value['processed_d5'], pick, par)
        elif text == 'Ti':
            # ImportData.value['processed_d3'] \
            #     = process_pick(pick, ImportData.value['processed_d3'], par)
            ImportData.value['diagnostic3'], ImportData.value['processed_d3']\
                = pppp(ImportData.value['processed_d3'], pick, par)
    elif label == 'Reflectometry':
        # ImportData.value['processed_d1'] \
        #     = process_pick(pick, ImportData.value['processed_d1'], par)
        ImportData.value['diagnostic1'], ImportData.value['processed_d1']\
            = pppp(ImportData.value['processed_d1'], pick, par)
    elif label == 'POINT':
        # ImportData.value['processed_d3'] \
        #     = process_pick(pick, ImportData.value['processed_d3'], par)
        ImportData.value['diagnostic3'], ImportData.value['processed_d3']\
            = pppp(ImportData.value['processed_d3'], pick, par)
    elif label == 'excluded data':
        for i in DataBase.library.values():
            print 'a'
            for j in pick:
                if j in i:
                    print 'b'
                    for key, var in DataBase.library.iteritems():
                        print 'c'
                        foo = var == i
                        print foo
                        if type(foo).__module__ == np.__name__:
                            judge = foo.all()
                        else:
                            judge = foo
                        if judge:
                            print 'd'
                            # if key == 'd1':
                            #     print 'd1'
                            #     process_pick2(pick, ExcludedData.library['processed'],
                            #                   ImportData.value['processed_data'],
                            #                   ImportData.value['processed_d1'])
                            # if key == 'd2':
                            #     print 'd2'
                            #     process_pick2(pick, ExcludedData.library['processed'],
                            #                   ImportData.value['processed_data'],
                            #                   ImportData.value['processed_d2'])
                            # if key == 'd3':
                            #     print 'd3'
                            #     process_pick2(pick, ExcludedData.library['processed'],
                            #                   ImportData.value['processed_data'],
                            #                   ImportData.value['processed_d3'])
                            # if key == 'd4':
                            #     print 'd4'
                            #     process_pick2(pick, ExcludedData.library['processed'],
                            #                   ImportData.value['processed_data'],
                            #                   ImportData.value['processed_d4'])
                            # if key == 'd5':
                            #     print 'd5'
                            #     process_pick2(pick, ExcludedData.library['processed'],
                            #                   ImportData.value['processed_data'],
                            #                   ImportData.value['processed_d5'])
                            process_pick2(pick, ExcludedData.library['processed'], key, par)


def pppp(p, pick, par):
    """
    delete the diagnostic point which is excluded
    :param p: processed diagnostic
    :param pick: pick
    :param par: par
    :return: diagnostic without the excluded point, and processed diagnostic
    """
    x = p.copy().x[0]
    y = p.copy().y
    x, y = process_pick(pick, x, y, par)
    foo = Data()
    foo.x = [x]
    foo.y = y
    xx = undo_scale_shift(foo, par)
    d1, d2 = process_pick(pick, xx[:, 0], xx[:, 1], par)
    d = np.array([d1, d2]).T
    return d, foo


# def process_pick(pick, data, par):
#     temp = data.copy()
#     # excluded = np.array([[pick[0][0][0], pick[1][0][0]]])
#     for i in pick[:, 0]:
#         if i in temp.x[0]:
#             # if label not in 'excluded data':
#             ind = temp.x[0] != i
#             temp.x[0] = temp.x[0][ind]
#             temp.y = temp.y[ind]
#
#             ExcludedData(pick)
#
#             ExcludedData.library['data'] = undo_scale_shift(ExcludedData.library['processed'], par)
#             # else:
#             #     temp.x[0] = np.hstack((temp.x[0], i))
#             #     index = pick[:, 0] == i
#             #     j = pick[:, 1][index][0]
#             #     temp.y = np.hstack((temp.y, j))
#             #     ExcludedData(pick, False)
#             # else:
#             #     pass
#     return temp


def process_pick(pick, x, y, par):
    # excluded = np.array([[pick[0][0][0], pick[1][0][0]]])
    for i in pick[:, 0]:
        if i in x:
            # if label not in 'excluded data':
            ind = x != i
            x = x[ind]
            y = y[ind]

            ExcludedData(pick)

            ExcludedData.library['data'] = undo_scale_shift(ExcludedData.library['processed'], par)
            # else:
            #     temp.x[0] = np.hstack((temp.x[0], i))
            #     index = pick[:, 0] == i
            #     j = pick[:, 1][index][0]
            #     temp.y = np.hstack((temp.y, j))
            #     ExcludedData(pick, False)
            # else:
            #     pass
    return x, y


def process_pick2(pick, exclude, key, par):
    """
    add pick to processed_data/d1/d2/d3/d4/d5, delete it from excluded data
    :param pick: pick
    :param exclude: excluded data
    :param key: d1, d2, d3, d4, d5
    :param par: par
    """
    temp1 = ImportData.value['processed_data'].copy()
    if par['SourceSwitch']:
        if key == 'd1':
            temp2 = ImportData.value['processed_d1'].copy()
        if key == 'd2':
            temp2 = ImportData.value['processed_d2'].copy()
        if key == 'd3':
            temp2 = ImportData.value['processed_d3'].copy()
        if key == 'd4':
            temp2 = ImportData.value['processed_d4'].copy()
        if key == 'd5':
            temp2 = ImportData.value['processed_d5'].copy()
    else:
        pass
    for i in pick[:, 0]:
        if i in exclude.x[0]:
            temp1.x[0] = np.hstack((temp1.x[0], i))
            index = pick[:, 0] == i
            j = pick[:, 1][index][0]
            temp1.y = np.hstack((temp1.y, j))

            if par['SourceSwitch']:
                temp2.x[0] = np.hstack((temp2.x[0], i))
                index = pick[:, 0] == i
                j = pick[:, 1][index][0]
                temp2.y = np.hstack((temp2.y, j))

            ExcludedData(pick, False)

            ExcludedData.library['data'] = undo_scale_shift(ExcludedData.library['processed'], par)

    if par['SourceSwitch']:
        if key == 'd1':
            ImportData.value['processed_data'], ImportData.value['processed_d1'] = temp1, temp2
        if key == 'd2':
            ImportData.value['processed_data'], ImportData.value['processed_d2'] = temp1, temp2
        if key == 'd3':
            ImportData.value['processed_data'], ImportData.value['processed_d3'] = temp1, temp2
        if key == 'd4':
            ImportData.value['processed_data'], ImportData.value['processed_d4'] = temp1, temp2
        if key == 'd5':
            ImportData.value['processed_data'], ImportData.value['processed_d5'] = temp1, temp2
    else:
        ImportData.value['processed_data'] = temp1


def undo_scale_shift(data, par):
    temp = data.copy()
    print temp
    h = temp.x[0].shape[0]
    zoom = 1 + par['Stretch'] / 1000.
    for i in range(h):
        temp.x[0][i] /= zoom
    shift = par['Shift'] / 1000.
    temp.x[0][:] = temp.x[0][:] - shift
    result = np.array([temp.x[0], temp.y]).T
    return result
