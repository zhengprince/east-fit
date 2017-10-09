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


def saveFile(save_name, value, data, datafit, library, par):
    if not save_name.isEmpty():
        output = open(save_name, 'w')

    # &namelist is a file format that can be read by OMFIT and etc.

    # write params
    print >> output, "# " + str(par['Shot']) + "\t" + str(par['Time']) + " ms\t" + str(par['RhoPsi'])\
                     + '\t' + par['Func'] + "\n"
    print >> output, "&params\n"
    if len(value):
        try:
            # print >> output, " function ="
            # print >> output, "  " + par['Func'] + "\n"
            print >> output, " c ="
            if par['Func'] == 'tanh_multi':
                c = str(value[0][:])
            elif par['Func'] == 'tanh_0out':
                c = str(value[0][:])
            elif par['Func'] == 'spline':
                c = str(value)
            c = c.replace("[", "")
            c = c.replace("]", "") + "\n"
            print >> output, "  " + c
            if not par['Func'] == 'spline':
                output.write(" ifix =\n")
                if par['Func'] == 'tanh_multi':
                    iFix = str([i / 2 for i in value[-1]])
                elif par['Func'] == 'tanh_0out':
                    iFix = str([i / 2 for i in value[-1]])
                iFix = iFix.replace("[", "")
                iFix = iFix.replace("]", "") + "\n"
                print >> output, "  " + iFix + "\n"
            output.write(" stretch =\n")
            stretch = str(par['Stretch'])
            print >> output, "  " + stretch + "\n"
            output.write(" shift =\n")
            shift = str(par['Shift'])
            print >> output, "  " + shift + "\n"
        except IndexError:
            pass
    else:
        pass
    print >> output, '/'

    # write raw data
    print >> output, "&raw_data"
    # print >> output, ";#raw data\n"
    # print >> output, ";  #" + str(par['RhoPsi'])
    rawx = str(data.x[0])
    rawx = rawx.replace("array([", "")
    rawx = rawx.replace("[", "")
    rawx = rawx.replace("])", "") + "\n"
    rawx = rawx.replace("]", "") + "\n"
    if par['Profile'] == 'ne':
        rawy = str(data.y * 1.e13)
    else:
        rawy = str(data.y)
    rawy = rawy.replace("[", "")
    rawy = rawy.replace("]", "") + "\n"
    print >> output, " " + str(par['RhoPsi']) + " ="
    print >> output, " " + rawx + "\n"
    # print >> output, ";  #data"
    print >> output, " data ="
    print >> output, " " + rawy + "\n"
    print >> output, "/"

    # write excluded data if any
    print >> output, "&excluded_data"
    if library != None:
        # print >> output, ";#excluded data\n"
        # print >> output, ";  #" + str(par['RhoPsi'])
        excludedX = str(library[:, 0])
        excludedX = excludedX.replace("array([", "")
        excludedX = excludedX.replace("[", "")
        excludedX = excludedX.replace("])", "") + "\n"
        excludedX = excludedX.replace("]", "") + "\n"
        excludedY = str(library[:, 1])
        excludedY = excludedY.replace("array([", "")
        excludedY = excludedY.replace("[", "")
        excludedY = excludedY.replace("])", "") + "\n"
        excludedY = excludedY.replace("]", "") + "\n"
        print >> output, " " + str(par['RhoPsi']) + " ="
        print >> output, "  " + excludedX
        # print >> output, ";  #data"
        print >> output, " data ="
        print >> output, "  " + excludedY
    print >> output, "/"

    # write fitted data
    print >> output, "&fitted_data"
    try:
        # print >> output, ";#fitted data\n"
        rho = np.linspace(0, 1, datafit.y.shape[0])
        fitX = str(rho)
        fitX = fitX.replace("[", "")
        fitX = fitX.replace("]", "") + "\n"
        if par['Profile'] == 'ne':
            fitY = str(datafit.y[:] * 1.e13)
        else:
            fitY = str(datafit.y[:])
        fitY = fitY.replace("[", "")
        fitY = fitY.replace("]", "") + "\n"
        # print >> output, ";  " + "#" + str(par['RhoPsi'])
        print >> output, " " + str(par['RhoPsi']) + " ="
        print >> output, " " + fitX + "\n"
        # print >> output, ";  #data"
        print >> output, " data ="
        print >> output, " " + fitY
    except:
        pass
    print >> output, "/"


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

    if par['Func'] == 'tanh_multi':
        value[0] = _input['PARAMS']['c']
    if par['Func'] == 'tanh_0out':
        value[0] = _input['PARAMS']['c']
    elif par['Func'] == 'spline':
        value = _input['PARAMS']['c']

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
