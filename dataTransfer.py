from pmds import mdsconnect, mdsopen, mdsvalue, mdsdisconnect

import numpy as np
from RZmap import RZmap
from data import Data

from eastmap import east_mapping

data = Data()


class GlobalVar5(object):
    value = dict(Params=[])

    def __init__(self, value):
        for key in value:
            self.value[key] = value[key]

    def __call__(self, c):
        for key in c:
            self.value[key] = c[key]
        return self.value


class GlobalVar6(object):
    value = dict(Params=[])

    def __init__(self, value):
        for key in value:
            self.value[key] = value[key]
        print 'in GlobalVar6', '\n', self.value

    def __call__(self, c):
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
    value = dict(Params=[])

    def __init__(self, value):
        for key in value:
            self.value[key] = value[key]
        print 'in GlobalVar9', '\n', self.value

    def __call__(self, c):
        for key in c:
            self.value[key] = c[key]
        return self.value


class GlobalVar(object):
    value6 = dict(Params=[])
    value7 = dict(Params=[])
    value8 = dict(Params=[])
    value9 = dict(Params=[])

    def __init__(self, value, index):
        for key in value:
            if index == 6:
                self.value6[key] = value[key]
            elif index == 7:
                self.value7[key] = value[key]
            elif index == 8:
                self.value8[key] = value[key]
            elif index == 9:
                self.value9[key] = value[key]
        print 'in GlobalVar\n'

    def __call__(self, index):
        if index == 6:
            value = self.value6
        elif index == 7:
            value = self.value7
        elif index == 8:
            value = self.value8
        elif index == 9:
            value = self.value9
        return value


# def upDict():
#     GlobalVar5.value = {'key': 'var'}
#     GlobalVar6.value = {'key': 'var'}
#     GlobalVar7.value = {'key': 'var'}
#     GlobalVar8.value = {'key': 'var'}
#     GlobalVar9.value = {'key': 'var'}
# GlobalVar.c = {'key': 'var'}


# def GlobalVar(c):
#     c = [c]
#     return c
class ExcludedData(object):
    library = dict(data=np.array([]),
                   processed=data)

    def __init__(self, input_, default=True):
        """
        ExcludedData
        :param input_:  excluded data passed in.
        :param default: True: add, which is default, False: delete.
        """
        print "input_=", input_
        print "type(input_)=", type(input_)
        # print "self.library=", self.library
        print "type(self.library['data'])=", type(self.library['data'])
        if default:
            if isinstance(self.library['processed'], Data):
                if len(self.library['processed'].x) is not 0:
                    for i in input_[:, 1]:
                        if i in self.library['processed'].y:
                            pass
                        else:
                            self.library['processed'].x = [np.hstack((self.library['processed'].x[0], input_[:, 0][0]))]
                            self.library['processed'].y = np.hstack((self.library['processed'].y, input_[:, 1][0]))
                else:
                    self.library['processed'].x = [input_[:, 0]]
                    self.library['processed'].y = input_[:, 1]
            else:
                self.library['processed'].x = [input_[:, 0]]
                self.library['processed'].y = input_[:, 1]
        else:
            if len(self.library['processed'].x) is not 0:
                for i in input_[:, 0]:
                    foo = self.library['processed'].x[0] != i
                    self.library['processed'].x[0] = self.library['processed'].x[0][foo]
                    self.library['processed'].y = self.library['processed'].y[foo]
            else:
                pass

        print "self.library['processed']=", self.library['processed']


class DataBase(object):
    library = dict()

    def __init__(self, **kwargs):
        """
        ExcludedData
        :param input_:  dict passed in
        """
        self.library = self.library.update(kwargs)


class ImportData(object):
    value = dict(data=np.array([]),  # contain all of diagnostics
                 processed_data=data,
                 diagnostic1=np.array([]),
                 time1=float,
                 processed_d1=data,
                 diagnostic2=np.array([]),
                 time2=float,
                 processed_d2=data,
                 diagnostic3=np.array([]),
                 time3=float,
                 processed_d3=data,
                 diagnostic4=np.array([]),
                 time4=float,
                 processed_d4=data,
                 diagnostic5=np.array([]),
                 time5=float,
                 processed_d5=data,
                 filein=np.array([]),
                 processed_filein=data)

    def __init__(self,
                 par,  # parameter from main window
                 text='',  # diagnostic name
                 default=True):  # True: data stack, False: data delete
        """
        __init__
        :param par:                # parameter from main window
        :param text:               # diagnostic name
        :param default:            # True: data stack, False: data delete
        """
        rhopsi = par['RhoPsi']
        shot = par['Shot']
        time = par['Time']
        # print shot, type(shot), time, type(time)
        if not par['SourceSwitch']:
            filename = str(par['FileName'])
            efit_dir = str(par['EfitDir'])
            # shot = 62946
            # time = 3800
            # efit_dir = '/nfs_share/users/zhengzhen/Desktop/kefit_tutor/62946/mag'
            # filename = '/nfs_share/users/zhengzhen/Desktop/kefit_tutor/62946/profiles/Teprof_2000.txt'
            yyy = RZmap(shot, time, efit_dir, filename)
            print yyy
            if rhopsi == 'rho':
                self.value['data'] = yyy['rhoY']
            elif rhopsi == 'psi':
                self.value['data'] = yyy['psiY']
        else:

            # delete the selected data from the whole data
            if not default:
                if self.value['data'].any():
                    if text == 'Reflectometry':
                        target = self.value['diagnostic1']
                    elif text == 'Thomson (Core)':
                        if par['Profile'] == 'Te':
                            target = self.value['diagnostic1']
                        elif par['Profile'] == 'ne':
                            target = self.value['diagnostic2']
                    elif text == 'ECE':
                        target = self.value['diagnostic3']
                    elif text == 'Michelson':
                        target = self.value['diagnostic4']
                    elif text == 'TXCS':
                        if par['Profile'] == 'Te':
                            target = self.value['diagnostic5']
                        elif par['Profile'] == 'Ti':
                            target = self.value['diagnostic3']
                    elif text == 'CXRS (Core)':
                        target = self.value['diagnostic1']
                    elif text == 'POINT':
                        target = self.value['diagnostic4']
                    for i in target:
                        foo = self.value['data'] != i
                        for j in range(len(foo)):
                            foo[j] = foo[j].any()
                        foo = foo[:, 0]
                        self.value['data'] = self.value['data'][foo]
                else:
                    pass

            # default: not delete the data, obtain it
            else:
                if text == 'Reflectometry':
                    target = self.value['diagnostic1']
                elif text == 'Thomson (Core)':
                    if par['Profile'] == 'Te':
                        target = self.value['diagnostic1']
                    elif par['Profile'] == 'ne':
                        target = self.value['diagnostic2']
                elif text == 'ECE':
                    target = self.value['diagnostic3']
                elif text == 'Michelson':
                    target = self.value['diagnostic4']
                elif text == 'TXCS':
                    if par['Profile'] == 'Te':
                        target = self.value['diagnostic5']
                    elif par['Profile'] == 'Ti':
                        target = self.value['diagnostic3']
                elif text == 'CXRS (Core)':
                    target = self.value['diagnostic1']
                elif text == 'POINT':
                    target = self.value['diagnostic4']

                # if the data exist, use it
                if target.any():
                    self.value['data'] = target

                # if not, obtain it
                else:
                    # shot = 63688  # 56963
                    # time = 4019  # 3418
                    subtree = ''
                    node_r = ''
                    node_z = ''
                    node_p = ''
                    if text == 'Reflectometry':
                        subtree = 'ReflJ_EAST'
                        node_r = 'R_ReflJ'
                        node_z = 'Z_ReflJ'
                        node_p = 'ne_ReflJ'
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
                        node_r = 'R_HRS'
                        node_z = 'Z_HRS'
                        node_p = 'Te_HRS'
                    elif text == 'Michelson':
                        subtree = 'MPI_Analy'
                        node_r = 'R_MI'
                        node_z = 'Z_MI'
                        node_p = 'Te_MI'
                    elif text == 'TXCS':
                        subtree = 'TXCS_EAST'
                        node_r = 'R_TXCS'
                        node_z = 'Z_TXCS'
                        if par['Profile'] == 'Te':
                            node_p = 'Te_TXCS'
                        elif par['Profile'] == 'Ti':
                            node_p = 'Ti_TXCS'
                    elif text == 'CXRS (Core)':
                        subtree = 'CXRS_EAST'
                        node_r = 'R_CXRS_T'
                        node_z = 'Z_CXRS_T'
                        node_p = 'Ti_CXRS_T'
                    elif text == 'POINT':
                        subtree = 'POINT_Analy'
                        node_r = ''
                        node_z = ''
                        node_p = ''
                    node_times = 'dim_of(' + node_p + ')'
                    data_r = 'data(' + node_r + ')'
                    data_z = 'data(' + node_z + ')'
                    data_p = 'data(' + node_p + ')'
                    mds_server = '202.127.204.12'
                    time /= 1000.
                    efit_tree = str(par['Tree'])
                    mdsconnect(mds_server)
                    mdsopen(subtree, shot)

                    result = []
                    if text == 'Reflectometry':
                        result = self.reflectometry(shot, time, node_times, data_r, data_p, efit_tree, rhopsi)
                    elif text == 'Thomson (Core)':
                        result = self.thomson_core(shot, time, node_times, data_r, data_z, data_p, efit_tree, rhopsi,
                                                   par)
                    elif text == 'POINT':
                        result = self.point(time)
                    elif text == 'TXCS':
                        result = self.txcs(shot, time, node_times, data_z, data_p, efit_tree, rhopsi, par)
                    elif text == 'CXRS (core)':
                        result = self.cxrs(shot, time, node_times, data_r, data_p, efit_tree, rhopsi)
                    elif text == 'ECE':
                        result = self.ece(shot, time, node_times, data_r, data_p, efit_tree, rhopsi)
                    elif text == 'Michelson':
                        result = self.michelson(shot, time, node_times, data_r, data_p, efit_tree, rhopsi)
                    mdsdisconnect()

                    if self.value['data'].any():
                        self.value['data'] = np.vstack((self.value['data'], result))
                    else:
                        self.value['data'] = result

    # noinspection PyArgumentList
    def reflectometry(self, shot, time, node_times, data_r, data_p, efit_tree, rhopsi):
        times = mdsvalue(node_times)
        ind = np.argmin(abs(times - time))
        time = times[ind]
        index = '[*,' + str(ind) + ']'
        ne = mdsvalue(data_p + index)
        r = mdsvalue(data_r + index)
        not_nan_idx = np.isfinite(ne)
        ne = ne[not_nan_idx]
        r = r[not_nan_idx]
        z = np.ones(len(r)) * 0.03
        rz = np.transpose([r, z])
        mapping = east_mapping(shot, time, efit_tree, rz)
        result = np.array([mapping[rhopsi], ne]).T
        result = result[np.argsort(result, axis=0)][:, 0]
        self.value['diagnostic1'] = result
        self.value['time1'] = time
        DataBase(d1=result)
        return result

    # noinspection PyArgumentList
    def thomson_core(self, shot, time, node_times, data_r, data_z, data_p, efit_tree, rhopsi, par):
        times = mdsvalue(node_times)
        # time_window = 0.01  # time window for the MR diagnostic
        ind = np.argmin(abs(times - time))
        time = times[ind]
        index = '[*,' + str(ind) + ']'
        data = mdsvalue(data_p + index)
        r = mdsvalue(data_r)
        not_nan_idx = np.isfinite(data)
        data = data[not_nan_idx]
        z = mdsvalue(data_z)
        rz = np.transpose([r, z])
        mapping = east_mapping(shot, time, efit_tree, rz)
        result = np.array([mapping[rhopsi], data]).T
        result = result[np.argsort(result, axis=0)][:, 0]
        if par['Profile'] == 'Te':
            result[:, 1] /= 1000.
            self.value['diagnostic1'] = result
            self.value['time1'] = time
            DataBase(d1=result)
        elif par['Profile'] == 'ne':
            result[:, 1] /= 1.e19
            self.value['diagnostic2'] = result
            self.value['time2'] = time
            DataBase(d2=result)
        return result

    # noinspection PyArgumentList
    def point(self, time):
        times = mdsvalue('dim_of(\\ne_POINT,0)')
        ind = np.argmin(abs(times - time))
        rho = np.linspace(0, 1, 21)
        ne = mdsvalue('\\ne_POINT')[ind]
        result = np.array([rho, ne]).T
        result = result[np.argsort(result, axis=0)][:, 0]
        self.value['diagnostic4'] = result
        self.value['time4'] = times[ind]
        DataBase(d4=result)
        return result

    # noinspection PyArgumentList
    def txcs(self, shot, time, node_times, data_z, data_p, efit_tree, rhopsi, par):
        times = mdsvalue(node_times)
        ind = np.argmin(abs(times - time))
        print ind
        t_index = np.searchsorted(times, time)
        print t_index
        time = times[ind]
        print time
        print times[t_index]
        data = mdsvalue(data_p)
        print data
        print data.shape
        r = 1.9  # mdsvalue('data(R_TXCS)' )
        z = mdsvalue(data_z) / 100.
        data = data[:, ind]
        print data
        not_nan_idx = np.isfinite(data)
        data = data[not_nan_idx]
        print data
        z = z[not_nan_idx]
        r = np.ones(len(z)) * r
        rz = np.transpose([r, z])
        mapping = east_mapping(shot, time, efit_tree, rz)
        result = np.array([mapping[rhopsi], data]).T
        result = result[np.argsort(result, axis=0)][:, 0]
        result[:, 1] /= 1000.
        if par['Profile'] == 'Te':
            self.value['diagnostic5'] = result
            self.value['time5'] = time
            DataBase(d5=result)
        elif par['Profile'] == 'Ti':
            self.value['diagnostic3'] = result
            self.value['time3'] = time
            DataBase(d3=result)
        return result

    # noinspection PyArgumentList
    def cxrs(self, shot, time, node_times, data_r, data_p, efit_tree, rhopsi):
        times = mdsvalue(node_times)
        # time_window = 0.01  # time window for the MR diagnostic
        ind = np.argmin(abs(times - time))
        time = times[ind]
        index = '[*,' + str(ind) + ']'
        data = mdsvalue(data_p + index)
        r = mdsvalue(data_r)
        not_nan_idx = np.isfinite(data)
        data = data[not_nan_idx]
        z = np.ones(len(r)) * 0.02
        rz = np.transpose([r, z])
        mapping = east_mapping(shot, time, efit_tree, rz)
        result = np.array([mapping[rhopsi], data]).T
        result = result[np.argsort(result, axis=0)][:, 0]
        result[:, 1] /= 1000.
        self.value['diagnostic1'] = result
        self.value['time1'] = time
        DataBase(d1=result)
        return result

    # noinspection PyArgumentList
    def ece(self, shot, time, node_times, data_r, data_p, efit_tree, rhopsi):
        times = mdsvalue(node_times)
        # time_window = 0.01  # time window for the MR diagnostic
        ind = np.argmin(abs(times - time))
        time = times[ind]
        index = '[*,' + str(ind) + ']'
        data = mdsvalue(data_p + index)
        r = mdsvalue(data_r)
        not_nan_idx = np.isfinite(data)
        data = data[not_nan_idx]
        z = np.ones(len(r)) * 0.02
        rz = np.transpose([r, z])
        mapping = east_mapping(shot, time, efit_tree, rz)
        result = np.array([mapping[rhopsi], data]).T
        result = result[np.argsort(result, axis=0)][:, 0]
        result[:, 1] /= 1000.
        self.value['diagnostic3'] = result
        self.value['time3'] = time
        DataBase(d3=result)
        return result

    # noinspection PyArgumentList
    def michelson(self, shot, time, node_time, data_r, data_p, efit_tree, rhopsi):
        times = mdsvalue(node_time)
        ind = np.argmin(abs(times - time))
        time = times[ind]
        index = '[*,' + str(ind) + ']'
        data = mdsvalue(data_p + index)
        r = mdsvalue(data_r)
        not_nan_idx = np.isfinite(data)
        data = data[not_nan_idx]
        z = np.ones(len(r)) * 0.02
        rz = np.transpose([r, z])
        mapping = east_mapping(shot, time, efit_tree, rz)
        result = np.array([mapping[rhopsi], data]).T
        result = result[np.argsort(result, axis=0)][:, 0]
        result[:, 1] /= 1000.
        self.value['diagnostic4'] = result
        self.value['time4'] = time
        DataBase(d4=result)
        return result

    def __call__(self):
        return self.value
