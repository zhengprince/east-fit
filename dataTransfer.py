import os
from pmds import mdsconnect, mdsopen, mdsvalue, mdsdisconnect

from data import Data

from eastmap import east_mapping, rho2psi, psi2rho
from fileIO import *


class GlobalVar5(object):
    def __init__(self):
        self.value = dict(Params=[])

    def update(self, c):
        for key in c:
            self.value[key] = c[key]
        return self.value


class GlobalVar6(object):
    def __init__(self):
        self.value = dict(Params=[])

    def update(self, c):
        for key in c:
            self.value[key] = c[key]
        return self.value


class GlobalVar7(object):
    value = dict(Params=[])

    def __init__(self, value):
        for key in value:
            self.value[key] = value[key]

    def __call__(self, c):
        for key in c:
            self.value[key] = c[key]
        return self.value


class GlobalVar8(object):
    value = dict(Params=[])

    def __init__(self, value):
        for key in value:
            self.value[key] = value[key]

    def __call__(self, c):
        for key in c:
            self.value[key] = c[key]
        return self.value


class GlobalVar9(object):
    def __init__(self):
        self.value = dict(Params=[])

    def update(self, c):
        for key in c:
            self.value[key] = c[key]
        return self.value


class GlobalVar(object):
    def __init__(self):
        # containing all of diagnostics
        self.value = dict(data_rho=np.array([]),
                          data_psi=np.array([]),
                          processed_data_rho=Data(),
                          processed_data_psi=Data(),
                          diagnostic1_rho=np.array([]),
                          diagnostic1_psi=np.array([]),
                          diagnostic1_err=np.array([]),
                          time1=float,
                          processed_d1_rho=Data(),
                          processed_d1_psi=Data(),
                          diagnostic2_rho=np.array([]),
                          diagnostic2_psi=np.array([]),
                          diagnostic2_err=np.array([]),
                          time2=float,
                          processed_d2_rho=Data(),
                          processed_d2_psi=Data(),
                          diagnostic3_rho=np.array([]),
                          diagnostic3_psi=np.array([]),
                          diagnostic3_err=np.array([]),
                          time3=float,
                          processed_d3_rho=Data(),
                          processed_d3_psi=Data(),
                          diagnostic4_rho=np.array([]),
                          diagnostic4_psi=np.array([]),
                          diagnostic4_err=np.array([]),
                          time4=float,
                          processed_d4_rho=Data(),
                          processed_d4_psi=Data(),
                          diagnostic5_rho=np.array([]),
                          diagnostic5_psi=np.array([]),
                          diagnostic5_err=np.array([]),
                          time5=float,
                          processed_d5_rho=Data(),
                          processed_d5_psi=Data(),
                          filein_rho=np.array([]),
                          filein_psi=np.array([]),
                          processed_filein_rho=Data(),
                          processed_filein_psi=Data(),
                          fit=Data())

        # excluded data
        self.library = dict(data_rho=np.array([]),
                            data_psi=np.array([]),
                            processed_rho=Data(),
                            processed_psi=Data())
        self.database = dict()

    def d(self, **kwargs):
        self.database.update(kwargs)


def ExcludedData(library, input_, s, default=True):
    """
    ExcludedData
    :param s:
    :param library: GlobalVar.library
    :param input_:  excluded data passed in.
    :param default: True: add, which is default; False: delete.
    """
    # print "input_=", input_
    # print "type(input_)=", type(input_)
    # print "library=", library
    # print "type(library['data_rho'])=", type(library['data_rho'])
    # for s in 'rho', 'psi':
    if default:
        if isinstance(library['processed_' + s], Data):
            if len(library['processed_' + s].x) is not 0:
                for i in input_[:, 1]:
                    if i in library['processed_' + s].y:
                        pass
                    else:
                        library['processed_' + s].x = [np.hstack((library['processed_' + s].x[0], input_[:, 0][0]))]
                        library['processed_' + s].y = np.hstack((library['processed_' + s].y, input_[:, 1][0]))
            else:
                library['processed_' + s].x = [input_[:, 0]]
                library['processed_' + s].y = input_[:, 1]
        else:
            library['processed_' + s].x = [input_[:, 0]]
            library['processed_' + s].y = input_[:, 1]
    else:
        if len(library['processed_' + s].x) is not 0:
            for i in input_[:, 0]:
                foo = library['processed_' + s].x[0] != i
                library['processed_' + s].x[0] = library['processed_' + s].x[0][foo]
                library['processed_' + s].y = library['processed_' + s].y[foo]
        else:
            pass
    # print "library['processed_rho']=", library['processed_rho']
    return library


class ImportData(object):
    def __init__(self):
        self.rhopsi = ''
        self.shot = int
        self.time = int
        self.efitDir = ''
        self.fm = False

    def file_file(self,
                  globalvar,  # GlobalVar
                  par):  # parameter from main window
        """
        file_file
        :param globalvar:          GlobalVar
        :param par:                parameter from main window
        """
        self.shot = par['Shot']
        self.time = par['Time']
        # print shot, type(shot), time, type(time)
        fileName = str(par['FileName'])
        efitDir = str(par['EfitDir'])
        gFilePath = os.path.dirname(efitDir)
        # dataFile = np.loadtxt(fileName)
        # if (dataFile[:, -1] > 1.e10).any():
        #     print 'aaa'
        #     dataFile[:, -1] = dataFile[:, -1]/1.e19
        # elif (10. < dataFile[:, -1]).any() and (dataFile[:, -1] < 10000.).any():
        #     dataFile[:, -1] = dataFile[:, -1]/1000.
        # rz = dataFile[:, 0:2]
        dataFile = openFile(fileName)
        mapping = east_mapping(self.shot, self.time, gFilePath, dataFile['rz'])
        resultRho = np.array([mapping['rho'], dataFile['data']]).T
        resultPsi = np.array([mapping['psi'], dataFile['data']]).T
        resultRho = resultRho[np.argsort(resultRho, axis=0)][:, 0]
        resultPsi = resultPsi[np.argsort(resultPsi, axis=0)][:, 0]
        globalvar.value['data_rho'] = resultRho
        globalvar.value['data_psi'] = resultPsi
        # mapping = RZmap(self.shot, self.time, gFileDir, fileName)
        # globalvar.value['data_rho'] = mapping['rho']
        # globalvar.value['data_psi'] = mapping['psi']
        globalvar.value['filein_rho'] = globalvar.value['data_rho']
        globalvar.value['filein_psi'] = globalvar.value['data_psi']
        globalvar.d(filein_rho=globalvar.value['data_rho'])
        globalvar.d(filein_psi=globalvar.value['data_psi'])
        return globalvar

    def mds_file(self, globalvar, par):
        self.shot = par['Shot']
        self.time = par['Time']
        # mdsconnect('202.127.204.12')
        mdsopen(str(par['Tree']), self.shot)
        rz = globalvar.value['data_rho']['rz']
        mapping = east_mapping(self.shot, self.time, str(par['Tree']), rz)
        resultRho = np.array([mapping['rho'], globalvar.value['data_rho']['data']]).T
        resultPsi = np.array([mapping['psi'], globalvar.value['data_psi']['data']]).T
        resultRho = resultRho[np.argsort(resultRho, axis=0)][:, 0]
        resultPsi = resultPsi[np.argsort(resultPsi, axis=0)][:, 0]
        globalvar.value['data_rho'] = resultRho
        globalvar.value['data_psi'] = resultPsi
        globalvar.value['filein_rho'] = globalvar.value['data_rho']
        globalvar.value['filein_psi'] = globalvar.value['data_psi']
        globalvar.d(filein_rho=globalvar.value['data_rho'])
        globalvar.d(filein_psi=globalvar.value['data_psi'])
        return globalvar

    def mds_mds_n_file_mds(self,
                           globalvar,  # GlobalVar
                           par,  # parameter from main window
                           text='',  # diagnostic name
                           default=True,  # True: data stack, False: delete data
                           file_mds=False):  # True=get gfile from file, data from mds
        """
        get gfile from mds or file, data from mds
        :param globalvar:          GlobalVar
        :param par:                parameter from main window
        :param text:               diagnostic name
        :param default:            True: stack data, False: delete data
        :param file_mds:           True=get gfile from file, data from mds
        """
        # self.rhopsi = par['RhoPsi']
        self.shot = par['Shot']
        self.time = par['Time']
        self.efitDir = par['EfitDir']
        self.fm = file_mds

        # delete the selected diagnostic data from the whole data
        if not default:
            if globalvar.value['data_rho'].any() or globalvar.value['data_psi'].any():
                target1 = np.array([])
                target2 = target1
                if text == 'Reflectometry':
                    target1 = globalvar.value['diagnostic1_rho']
                    target2 = globalvar.value['diagnostic1_psi']
                elif text == 'Thomson (Core)':
                    if par['Profile'] == 'Te':
                        target1 = globalvar.value['diagnostic1_rho']
                        target2 = globalvar.value['diagnostic1_psi']
                    elif par['Profile'] == 'ne':
                        target1 = globalvar.value['diagnostic2_rho']
                        target2 = globalvar.value['diagnostic2_psi']
                elif text == 'ECE':
                    target1 = globalvar.value['diagnostic3_rho']
                    target2 = globalvar.value['diagnostic3_psi']
                elif text == 'Michelson':
                    target1 = globalvar.value['diagnostic4_rho']
                    target2 = globalvar.value['diagnostic4_psi']
                elif text == 'TXCS':
                    if par['Profile'] == 'Te':
                        target1 = globalvar.value['diagnostic5_rho']
                        target2 = globalvar.value['diagnostic5_psi']
                    elif par['Profile'] == 'Ti':
                        target1 = globalvar.value['diagnostic3_rho']
                        target2 = globalvar.value['diagnostic3_psi']
                elif text == 'CXRS (Core)':
                    target1 = globalvar.value['diagnostic1_rho']
                    target2 = globalvar.value['diagnostic1_psi']
                elif text == 'POINT':
                    target1 = globalvar.value['diagnostic4_rho']
                    target2 = globalvar.value['diagnostic4_psi']
                for i in target1:
                    foo = globalvar.value['data_rho'] != i
                    for j in range(len(foo)):
                        foo[j] = foo[j].any()
                    foo = foo[:, 0]
                    globalvar.value['data_rho'] = globalvar.value['data_rho'][foo]
                for i in target2:
                    foo = globalvar.value['data_psi'] != i
                    for j in range(len(foo)):
                        foo[j] = foo[j].any()
                    foo = foo[:, 0]
                    globalvar.value['data_psi'] = globalvar.value['data_psi'][foo]
            else:
                pass

        # default: not delete the data, obtain it and add them into the whole
        else:
            if text == 'Reflectometry':
                target1 = globalvar.value['diagnostic1_rho']
                target2 = globalvar.value['diagnostic1_psi']
            elif text == 'Thomson (Core)':
                if par['Profile'] == 'Te':
                    target1 = globalvar.value['diagnostic1_rho']
                    target2 = globalvar.value['diagnostic1_psi']
                elif par['Profile'] == 'ne':
                    target1 = globalvar.value['diagnostic2_rho']
                    target2 = globalvar.value['diagnostic2_psi']
            elif text == 'ECE':
                target1 = globalvar.value['diagnostic3_rho']
                target2 = globalvar.value['diagnostic3_psi']
            elif text == 'Michelson':
                target1 = globalvar.value['diagnostic4_rho']
                target2 = globalvar.value['diagnostic4_psi']
            elif text == 'TXCS':
                if par['Profile'] == 'Te':
                    target1 = globalvar.value['diagnostic5_rho']
                    target2 = globalvar.value['diagnostic5_psi']
                elif par['Profile'] == 'Ti':
                    target1 = globalvar.value['diagnostic3_rho']
                    target2 = globalvar.value['diagnostic3_psi']
            elif text == 'CXRS (Core)':
                target1 = globalvar.value['diagnostic1_rho']
                target2 = globalvar.value['diagnostic1_psi']
            elif text == 'POINT':
                target1 = globalvar.value['diagnostic4_rho']
                target2 = globalvar.value['diagnostic4_psi']

            # if the data exist, use it
            if target1.any():
                globalvar.value['data_rho'] = target1
            elif target2.any():
                globalvar.value['data_psi'] = target2

            # if not, obtain it
            else:
                subtree = ''
                node_r = ''
                node_z = ''
                node_p = ''
                node_err = ''
                if text == 'Reflectometry':
                    subtree = 'ReflJ_EAST'
                elif text == 'Thomson (Core)':
                    subtree = 'TS_EAST'
                    node_r = 'R_coreTS'
                    node_z = 'Z_coreTS'
                    if par['Profile'] == 'Te':
                        node_p = 'Te_coreTS'
                        node_err = 'Te_coreTSerr'
                    elif par['Profile'] == 'ne':
                        node_p = 'ne_coreTS'
                        node_err = 'ne_coreTSerr'
                elif text == 'ECE':
                    subtree = 'HRS_EAST'
                elif text == 'Michelson':
                    subtree = 'MPI_Analy'
                elif text == 'TXCS':
                    subtree = 'TXCS_EAST'
                    node_r = 'R_TXCS'
                    node_z = 'Z_TXCS'
                    if par['Profile'] == 'Te':
                        node_p = 'Te_TXCS'
                        node_err = 'Te_TXCSerr'
                    elif par['Profile'] == 'Ti':
                        node_p = 'Ti_TXCS'
                        node_err = 'Ti_TXCSerr'
                elif text == 'CXRS (Core)':
                    subtree = 'CXRS_EAST'
                elif text == 'POINT':
                    subtree = 'POINT_Analy'
                node_times = 'dim_of(' + node_p + ')'
                data_r = 'data(' + node_r + ')'
                data_z = 'data(' + node_z + ')'
                data_p = 'data(' + node_p + ')'
                data_err = 'data(' + node_err + ')'
                data_ = {'r': data_r, 'z': data_z, 'p': data_p, 'err': data_err}
                # self.time /= 1000.
                efit_tree = str(par['Tree'])
                mdsopen(subtree, self.shot)

                result = {}
                if text == 'Reflectometry':
                    result, globalvar = self.reflectometry(efit_tree, globalvar)
                elif text == 'Thomson (Core)':
                    result, globalvar = self.thomson_core(node_times, data_, efit_tree, par, globalvar)
                elif text == 'POINT':
                    result, globalvar = self.point(efit_tree, globalvar)
                elif text == 'TXCS':
                    result, globalvar = self.txcs(node_times, data_, efit_tree, par, globalvar)
                elif text == 'CXRS (Core)':
                    result, globalvar = self.cxrs(efit_tree, globalvar)
                elif text == 'ECE':
                    result, globalvar = self.ece(efit_tree, globalvar)
                elif text == 'Michelson':
                    result, globalvar = self.michelson(efit_tree, globalvar)
                # mdsdisconnect()

                for s in 'rho', 'psi':
                    if s == 'rho':
                        _data = 'data_rho'
                    elif s == 'psi':
                        _data = 'data_psi'
                    if globalvar.value[_data].any():
                        globalvar.value[_data] = np.vstack((globalvar.value[_data], result[_data]))
                    else:
                        globalvar.value[_data] = result[_data]
        return globalvar

    # noinspection PyArgumentList
    def reflectometry(self, efit_tree, globalvar):
        times = mdsvalue('dim_of(ne_ReflJ)')
        ind = np.argmin(abs(times - self.time / 1000.))
        time = times[ind]
        index = '[*,' + str(ind) + ']'
        ne = mdsvalue('data(ne_ReflJ)' + index)
        r = mdsvalue('data(R_ReflJ)' + index)
        not_nan_idx = np.isfinite(ne)
        ne = ne[not_nan_idx]
        r = r[not_nan_idx]
        z = np.ones(len(r)) * 0.03
        rz = np.transpose([r, z])
        if self.fm:
            efitDir = str(self.efitDir)
            efitDir = os.path.dirname(efitDir)
            mapping = east_mapping(self.shot, self.time, efitDir, rz)
        else:
            mapping = east_mapping(self.shot, time * 1000, efit_tree, rz)
        resultRho = np.array([mapping['rho'], ne]).T
        resultRho = resultRho[np.argsort(resultRho, axis=0)][:, 0]
        resultPsi = np.array([mapping['psi'], ne]).T
        resultPsi = resultPsi[np.argsort(resultPsi, axis=0)][:, 0]
        globalvar.value['diagnostic1_rho'] = resultRho
        globalvar.value['diagnostic1_psi'] = resultPsi
        globalvar.value['time1'] = time
        globalvar.d(d1_rho=resultRho)
        globalvar.d(d1_psi=resultPsi)
        return {'data_rho': resultRho, 'data_psi': resultPsi}, globalvar

    # noinspection PyArgumentList
    def thomson_core(self, node_times, data_, efit_tree, par, globalvar):
        try:
            times = mdsvalue('dim_of(Te_maxTS)')
        except RuntimeError:
            print 'There is NO "Te_maxTS" data!'
            times = mdsvalue(node_times)
        # time_window = 0.01  # time window for the MR diagnostic
        ind = np.argmin(abs(times - self.time / 1000.))
        time = times[ind]
        index = '[*,' + str(ind) + ']'
        data = mdsvalue(data_['p'] + index)
        err = mdsvalue(data_['err'] + index)
        not_nan_idx = np.isfinite(data)
        data = data[not_nan_idx]
        err = err[not_nan_idx]
        r = mdsvalue(data_['r'])
        z = mdsvalue(data_['z'])
        rz = np.transpose([r, z])
        if self.fm:
            efitDir = str(self.efitDir)
            efitDir = os.path.dirname(efitDir)
            mapping = east_mapping(self.shot, self.time, efitDir, rz)
        else:
            mapping = east_mapping(self.shot, time * 1000, efit_tree, rz)
        resultRho = np.array([mapping['rho'], data]).T
        resultRho = resultRho[np.argsort(resultRho, axis=0)][:, 0]
        resultPsi = np.array([mapping['psi'], data]).T
        resultPsi = resultPsi[np.argsort(resultPsi, axis=0)][:, 0]
        err = err[np.argsort(resultRho, axis=0)][:, 0]
        if par['Profile'] == 'Te':
            resultRho[:, 1] /= 1000.
            resultPsi[:, 1] /= 1000.
            err /= 1000.
            globalvar.value['diagnostic1_rho'] = resultRho
            globalvar.value['diagnostic1_psi'] = resultPsi
            globalvar.value['diagnostic1_err'] = err
            globalvar.value['time1'] = time
            globalvar.d(d1_rho=resultRho)
            globalvar.d(d1_psi=resultPsi)
        elif par['Profile'] == 'ne':
            resultRho[:, 1] /= 1.e19
            resultPsi[:, 1] /= 1.e19
            err /= 1.e19
            globalvar.value['diagnostic2_rho'] = resultRho
            globalvar.value['diagnostic2_psi'] = resultPsi
            globalvar.value['diagnostic2_err'] = err
            globalvar.value['time2'] = time
            globalvar.d(d2_rho=resultRho)
            globalvar.d(d2_psi=resultPsi)
        return {'data_rho': resultRho, 'data_psi': resultPsi}, globalvar

    # noinspection PyArgumentList
    def point(self, efit_tree, globalvar):
        times = mdsvalue('dim_of(\\ne_POINT,0)')
        ind = np.argmin(abs(times - self.time / 1000.))
        rho = np.linspace(0, 1, 21)
        ne = mdsvalue('\\ne_POINT')[ind]
        if self.fm:
            efitDir = str(self.efitDir)
            efitDir = os.path.dirname(efitDir)
            mapping = rho2psi(self.shot, self.time, efitDir, rho)
            resultPsi = np.array([mapping['psi'], ne]).T
        else:
            mapping = rho2psi(self.shot, self.time, efit_tree, rho)
            resultPsi = np.array([mapping['psi'], ne]).T
        resultRho = np.array([rho, ne]).T
        resultRho = resultRho[np.argsort(resultRho, axis=0)][:, 0]
        resultPsi = resultPsi[np.argsort(resultPsi, axis=0)][:, 0]
        globalvar.value['diagnostic4_rho'] = resultRho
        globalvar.value['diagnostic4_psi'] = resultPsi
        globalvar.value['time4'] = times[ind]
        globalvar.d(d4_rho=resultRho)
        globalvar.d(d4_psi=resultPsi)
        return {'data_rho': resultRho, 'data_psi': resultPsi}, globalvar

    # noinspection PyArgumentList
    def txcs(self, node_times, data_, efit_tree, par, globalvar):
        times = mdsvalue(node_times)
        ind = np.argmin(abs(times - self.time / 1000.))
        time = times[ind]
        data = mdsvalue(data_['p'])
        data = data[:, ind]
        err = mdsvalue(data_['err'])
        err = err[:, ind]
        not_nan_idx = np.isfinite(data)
        data = data[not_nan_idx] / 1000.
        err = err[not_nan_idx] / 1000.
        r = 1.9
        z = mdsvalue(data_['z']) / 100.
        z = z[not_nan_idx]
        r = np.ones(len(z)) * r
        rz = np.transpose([r, z])
        if self.fm:
            efitDir = str(self.efitDir)
            gFilePath = os.path.dirname(efitDir)
            mapping = east_mapping(self.shot, self.time, gFilePath, rz)
        else:
            mapping = east_mapping(self.shot, self.time, efit_tree, rz)
        print 'mapping:', mapping
        resultRho = np.array([mapping['rho'], data]).T
        resultRho = resultRho[np.argsort(resultRho, axis=0)][:, 0]
        resultPsi = np.array([mapping['psi'], data]).T
        resultPsi = resultPsi[np.argsort(resultPsi, axis=0)][:, 0]
        err = err[np.argsort(resultRho, axis=0)][:, 0]
        if par['Profile'] == 'Te':
            globalvar.value['diagnostic5_rho'] = resultRho
            globalvar.value['diagnostic5_psi'] = resultPsi
            globalvar.value['diagnostic5_err'] = err
            globalvar.value['time5'] = time
            globalvar.d(d5_rho=resultRho)
            globalvar.d(d5_psi=resultPsi)
        elif par['Profile'] == 'Ti':
            globalvar.value['diagnostic3_rho'] = resultRho
            globalvar.value['diagnostic3_psi'] = resultPsi
            globalvar.value['diagnostic3_err'] = err
            globalvar.value['time3'] = time
            globalvar.d(d3_rho=resultRho)
            globalvar.d(d3_psi=resultPsi)
        return {'data_rho': resultRho, 'data_psi': resultPsi}, globalvar

    # noinspection PyArgumentList
    def cxrs(self, efit_tree, globalvar):
        times = mdsvalue('dim_of(Ti_CXRS_T)')
        # time_window = 0.01  # time window for the MR diagnostic
        ind = np.argmin(abs(times - self.time / 1000.))
        time = times[ind]
        index = '[*,' + str(ind) + ']'
        data = mdsvalue('data(Ti_CXRS_T)' + index) / 1000.
        err = mdsvalue('data(Ti_CXRS_Terr)' + index) / 1000.
        r = mdsvalue('data(R_CXRS_T)')
        not_nan_idx = np.isfinite(data)
        data = data[not_nan_idx]
        err = err[not_nan_idx]
        z = np.ones(len(r)) * 0.02
        rz = np.transpose([r, z])
        if self.fm:
            efitDir = str(self.efitDir)
            efitDir = os.path.dirname(efitDir)
            mapping = east_mapping(self.shot, self.time, efitDir, rz)
        else:
            mapping = east_mapping(self.shot, time * 1000, efit_tree, rz)
        resultRho = np.array([mapping['rho'], data]).T
        resultRho = resultRho[np.argsort(resultRho, axis=0)][:, 0]
        resultPsi = np.array([mapping['psi'], data]).T
        resultPsi = resultPsi[np.argsort(resultPsi, axis=0)][:, 0]
        err = err[np.argsort(resultRho, axis=0)][:, 0]
        globalvar.value['diagnostic1_rho'] = resultRho
        globalvar.value['diagnostic1_psi'] = resultPsi
        globalvar.value['diagnostic1_err'] = err
        globalvar.value['time1'] = time
        globalvar.d(d1_rho=resultRho)
        globalvar.d(d1_psi=resultPsi)
        return {'data_rho': resultRho, 'data_psi': resultPsi}, globalvar

    # noinspection PyArgumentList
    def ece(self, efit_tree, globalvar):
        times = mdsvalue('dim_of(Te_HRS)')
        # time_window = 0.01  # time window for the MR diagnostic
        ind = np.argmin(abs(times - self.time / 1000.))
        time = times[ind]
        index = '[*,' + str(ind) + ']'
        data = mdsvalue('data(Te_HRS)' + index) / 1000.
        err = mdsvalue('data(Te_HRSerr)' + index) / 1000.
        r = mdsvalue('data(R_HRS)')
        not_nan_idx = np.isfinite(data)
        data = data[not_nan_idx]
        err = err[not_nan_idx]
        z = np.ones(len(r)) * 0.02
        rz = np.transpose([r, z])
        if self.fm:
            efitDir = str(self.efitDir)
            efitDir = os.path.dirname(efitDir)
            mapping = east_mapping(self.shot, self.time, efitDir, rz)
        else:
            mapping = east_mapping(self.shot, time * 1000, efit_tree, rz)
        resultRho = np.array([mapping['rho'], data]).T
        resultRho = resultRho[np.argsort(resultRho, axis=0)][:, 0]
        resultPsi = np.array([mapping['psi'], data]).T
        resultPsi = resultPsi[np.argsort(resultPsi, axis=0)][:, 0]
        err = err[np.argsort(resultRho, axis=0)][:, 0]
        globalvar.value['diagnostic3_rho'] = resultRho
        globalvar.value['diagnostic3_psi'] = resultPsi
        globalvar.value['diagnostic3_err'] = err
        globalvar.value['time3'] = time
        globalvar.d(d3_rho=resultRho)
        globalvar.d(d3_psi=resultPsi)
        return {'data_rho': resultRho, 'data_psi': resultPsi}, globalvar

    # noinspection PyArgumentList
    def michelson(self, efit_tree, globalvar):
        times = mdsvalue('dim_of(Te_MI)')
        ind = np.argmin(abs(times - self.time / 1000.))
        time = times[ind]
        index = '[*,' + str(ind) + ']'
        data = mdsvalue('data(Te_HRS)' + index)
        err = mdsvalue('data(Te_MISerr)' + index)
        not_nan_idx = np.isfinite(data)
        data = data[not_nan_idx] / 1000.
        err = err[not_nan_idx] / 1000.
        r = mdsvalue('data(R_HRS)')
        z = np.ones(len(r)) * 0.02
        rz = np.transpose([r, z])
        if self.fm:
            efitDir = str(self.efitDir)
            efitDir = os.path.dirname(efitDir)
            mapping = east_mapping(self.shot, self.time, efitDir, rz)
        else:
            mapping = east_mapping(self.shot, time * 1000, efit_tree, rz)
        resultRho = np.array([mapping['rho'], data]).T
        resultRho = resultRho[np.argsort(resultRho, axis=0)][:, 0]
        resultPsi = np.array([mapping['psi'], data]).T
        resultPsi = resultPsi[np.argsort(resultPsi, axis=0)][:, 0]
        err = err[np.argsort(resultRho, axis=0)][:, 0]
        globalvar.value['diagnostic4_rho'] = resultRho
        globalvar.value['diagnostic4_psi'] = resultPsi
        globalvar.value['diagnostic4_err'] = err
        globalvar.value['time4'] = time
        globalvar.d(d4_rho=resultRho)
        globalvar.d(d4_psi=resultPsi)
        return {'data_rho': resultRho, 'data_psi': resultPsi}, globalvar

    def __call__(self, globalvar):
        return globalvar.value
