import numpy as np


def openFile(filename):
    fileName = open(filename)
    try:
        importData = np.loadtxt(fileName, dtype=float)
    except Exception, e:
        print e
    # judge the magnitude of the data so that determine what data it is, then process them automatically.
    # begin:
    ind = importData.shape[1]
    if ind >= 3:
        i = 2
    elif ind > 1:
        i = 1
    elif ind == 1:
        print "THERE'S ONLY ONE LINE IN THE DATA FILE!"
        return
    if (importData[:, i] > 1.e10).any():
        importData[:, i] = importData[:, i] / 1.e19
    elif (10. < importData[:, i]).any() and (importData[:, i] < 10000.).any():
        importData[:, i] = importData[:, i] / 1000.
    # end.
    print importData
    return {'rz': importData[:, 0:i], 'data': importData[:, i], 'all': importData}


def saveFile(save_name, value, data, datafit, library, database, par):
    if not save_name.isEmpty():
        output = open(save_name, 'w')

    # &namelist is a file format that can be read by OMFIT and etc.

    # write params
    output.write('# ' + str(par['Shot']) + '\t' + str(par['Time']) + ' ms\t' + par['Func'] + '\n')
    output.write('\n&params\n')
    if len(value):
        try:
            output.write('c =\n')
            if par['Func'] == 'tanh_multi':
                c = value[0][:]
            elif par['Func'] == 'tanh_0out':
                c = value[0][:]
            elif par['Func'] == 'spline':
                c = value
            for l in c:
                output.write('%s ' % l)
            if not par['Func'] == 'spline':
                output.write('\nifix =\n')
                if par['Func'] == 'tanh_multi':
                    iFix = [i / 2 for i in value[-1]]
                elif par['Func'] == 'tanh_0out':
                    iFix = [i / 2 for i in value[-1]]
                for l in iFix:
                    output.write('%s ' % l)
            output.write('\nstretch =\n')
            output.write(str(par['Stretch']))
            output.write('\nshift =\n')
            output.write(str(par['Shift']))
            output.write('\nequilibrium dir =\n')
            output.write(str(par['EfitDir']))
            output.write('\ndata dir =\n')
            output.write(str(par['FileName']))
        except IndexError:
            pass
    else:
        pass
    output.write('\n/\n')

    # write raw data
    output.write('\n&raw_data\n')
    try:
        rawX_rho = data['processed_data_rho'].x[0]
    except AttributeError:
        rawX_rho = None
    try:
        rawX_psi = data['processed_data_psi'].x[0]
    except AttributeError:
        rawX_psi = None
    if par['Profile'] == 'ne':
        rawY = data['processed_data_rho'].y * 1.e13
    else:
        # data['processed_data_rho'].y and data['processed_data_psi'].y are exactly the same
        rawY = data['processed_data_rho'].y
    output.write('rho =\n')
    try:
        for l in rawX_rho:
            output.write('%s\n' % l)
    except TypeError:
        pass
    output.write('psi =\n')
    try:
        for l in rawX_psi:
            output.write('%s\n' % l)
    except TypeError:
        pass
    output.write('\ndata =\n')
    for l in rawY:
        output.write('%s\n' % l)
    output.write('/\n')

    # write excluded data if any
    output.write('\n&excluded_data\n')
    if library is not None:
        excludedX_rho = library['data_rho'][:, 0]
        excludedX_psi = library['data_psi'][:, 0]
        # library['data_rho'][:, 1] and library['data_psi'][:, 1] are exactly the same
        excludedY = library['data_rho'][:, 1]
        output.write('rho =\n')
        for l in excludedX_rho:
            output.write('%s\n' % l)
        output.write('psi =\n')
        for l in excludedX_psi:
            output.write('%s\n' % l)
        output.write('\ndata =\n')
        for l in excludedY:
            output.write('%s\n' % l)
    output.write('/\n')

    # write fitted data
    output.write('\n&fitted_data\n')
    try:
        fitX = datafit.x[0]
        if par['Profile'] == 'ne':
            fitY = datafit.y[:] * 1.e13
        else:
            fitY = datafit.y[:]
        output.write('rho =\n')
        for l in fitX:
            output.write('%s\n' % l)
        # output.write('psi =\n')
        # try:
        #     for l in fitX_psi:
        #         output.write('%s\n' % l)
        # except TypeError:
        #     pass
        output.write('\ndata =\n')
        for l in fitY:
            output.write('%s\n' % l)
    except:
        pass
    output.write('/\n')

    # write database

    # close the file
    output.close()


def transFloat(l):
    for ind, i in enumerate(l):
        l[ind] = float('%0.8f' % i)
    return l


def SaveFile(save_name, value, data, datafit, library, par):
    import namelist as nl

    # PARAMS
    if len(value):
        if par['Func'] == 'tanh_multi':
            c = list(value[0][:])
        elif par['Func'] == 'tanh_0out':
            c = list(value[0][:])
        elif par['Func'] == 'spline':
            c = list(value)

        if not par['Func'] == 'spline':
            if par['Func'] == 'tanh_multi':
                iFix = list([i / 2 for i in value[-1]])
            elif par['Func'] == 'tanh_0out':
                iFix = list([i / 2 for i in value[-1]])
        else:
            iFix = []
    else:
        c = []
        iFix = []
    c = transFloat(c)
    iFix = transFloat(iFix)

    # RAW DATA
    if data.x:
        rawX = transFloat(data.x[0])
        if par['Profile'] == 'ne':
            rawY = list(data.y * 1.e13)
        else:
            rawY = list(data.y)
        rawY = transFloat(rawY)
    else:
        rawX = []
        rawY = []

    # EXCLUDED DATA

    output = {'PARAMS': {'_nl_header': '#' + str(par['Shot']) + '\t' + str(par['Time']) + 'ms',
                         '_nl_order': ['c params', 'ifix params', 'data stretch', 'data shift'],
                         '_nl_sequence': 0,
                         'c params': c,
                         'ifix params': iFix,
                         'data stretch': par['Stretch'],
                         'data shift': par['Shift']},
              'RAW_DATA': {'_nl_header': '',
                           '_nl_order': ['raw rho', 'raw data'],
                           '_nl_sequence': 1,
                           'raw rho': rawX,
                           'raw data': rawY},
              'FITTED_DATA': {'_nl_header': '',
                              '_nl_order': ['fitted rho', 'fitted data'],
                              '_nl_sequence': 2,
                              'fitted rho': '',
                              'fitted data': ''},
              '_delimiter': '&',
              'tailer': ''
              }
    nl.write(output, save_name, max_line_length=128)


def restoreFile(filename, value, data, datafit, library, par):
    import namelist as nl
    import re
    _input = nl.read(filename)
    header = _input['PARAMS']['_nl_header']
    junk1, shot, time, junk2, rhoPsi, function = re.split(r'[\s\t]+', header)
    par['Shot'] = int(shot)
    par['Time'] = int(time)
    par['Toggle'] = rhoPsi
    par['Func'] = function
    par['Stretch'] = _input['PARAMS']['stretch']
    par['Shift'] = _input['PARAMS']['shift']
    print _input['PARAMS']
    if par['Func'] == 'tanh_multi':
        value = [[], [], []]
        value[0] = _input['PARAMS']['c']
    if par['Func'] == 'tanh_0out':
        value = [[], [], []]
        value[0] = _input['PARAMS']['c']
    elif par['Func'] == 'spline':
        value = _input['PARAMS']['c']
    print value

    if not par['Func'] == 'spline':
        if par['Func'] == 'tanh_multi':
            value[-1] = _input['PARAMS']['ifix'] * 2
        elif par['Func'] == 'tanh_0out':
            value[-1] = _input['PARAMS']['ifix'] * 2

    data.x = [_input['RAW_DATA'][rhoPsi]]
    data.y = _input['RAW_DATA']['data']

    if _input['EXCLUDED_DATA']['_nl_order']:
        library = np.array([_input['EXCLUDED_DATA'][rhoPsi], _input['EXCLUDED_DATA']['data']]).T

    if _input['FITTED_DATA']['_nl_order']:
        datafit.x = [_input['FITTED_DATA']['data']]
        datafit.y = _input['FITTED_DATA'][rhoPsi]

    return {'value': value, 'data': data, 'datafit': datafit, 'library': library, 'par': par}
