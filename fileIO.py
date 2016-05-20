import numpy as np
import re
from dataTransfer import GlobalVar6, GlobalVar9, ExcludedData, ImportData


def open_file(filename, key):
    filename = open(filename)
    s = filename.readlines()
    iii = np.array(s)
    iii = iii[iii != '\n']
    l = len(iii)
    ij = np.zeros((l, 2))
    for x in range(l):
        ij[x, 0], ij[x, 1], junk = re.split(r'[\s\t\n,;]+', iii[x])
        if key == 'psi':
            ij[x, 0] = np.sqrt(ij[x, 0])
        else:
            pass
    import_data = ij[np.argsort(ij, axis=0)][:, 0]
    return import_data


def save_file(save_name, value, data, datafit, par):
    if not save_name.isEmpty():
        output = open(save_name, 'w')

    # write params
    print >> output, "# ", par['Shot'], "\t", par['Time'], "ms\n"
    if len(value['Params']):
        try:
            print >> output, "#params:\n\n"
            print >> output, "  #c params:"
            if par['Func'] == 'tanh_multi':
                c = str(value['Params'][0][:-1])
            elif par['Func'] == 'tanh_0out':
                c = str(value['Params'][0][:-1])
            c = c.replace("[", "")
            c = c.replace("]", "") + "\n"
            print >> output, "  " + c
            output.write("  #data Stretch:\n")
            stretch = str(par['Stretch'])
            print >> output, "  " + stretch + "\n"
            output.write("  #data shift:\n")
            shift = str(par['Shift'])
            print >> output, "  " + shift + "\n"
            output.write("  #ifix params:\n")
            if par['Func'] == 'tanh_multi':
                ifix = str([i / 2 for i in value['Params'][-1]])
            elif par['Func'] == 'tanh_0out':
                ifix = str([i / 2 for i in value['Params'][-1]])
            ifix = ifix.replace("[", "")
            ifix = ifix.replace("]", "") + "\n"
            print >> output, "  " + ifix + "\n"
        except IndexError:
            pass
    else:
        pass

    # write raw data
    print >> output, "&namelist"
    print >> output, ";#raw data\n"
    print >> output, ";  #" + str(par['RhoPsi'])
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
    print >> output, "raw" + str(par['RhoPsi']) + " ="
    print >> output, " " + rawx + "\n"
    print >> output, ";  #data"
    print >> output, "raw_data ="
    print >> output, " " + rawy + "\n"

    # write excluded data if any
    if ExcludedData.library['data'].any():
        print >> output, ";#excluded data\n"
        print >> output, ";  #" + str(par['RhoPsi'])
        excludedx = str(ExcludedData.library['data'][:, 0])
        excludedx = excludedx.replace("array([", "")
        excludedx = excludedx.replace("[", "")
        excludedx = excludedx.replace("])", "") + "\n"
        excludedx = excludedx.replace("]", "") + "\n"
        excludedy = str(ExcludedData.library['data'][:, 1])
        excludedy = excludedy.replace("array([", "")
        excludedy = excludedy.replace("[", "")
        excludedy = excludedy.replace("])", "") + "\n"
        excludedy = excludedy.replace("]", "") + "\n"
        print >> output, "excluded_rho ="
        print >> output, "  " + excludedx + "\n"
        print >> output, ";  #data"
        print >> output, "excluded_data ="
        print >> output, "  " + excludedy + "\n"

    # write fitted data
    try:
        print >> output, ";#fitted data\n"
        rho = np.linspace(0, 1, 51)
        fitx = str(rho)
        fitx = fitx.replace("[", "")
        fitx = fitx.replace("]", "") + "\n"
        if par['Profile'] == 'ne':
            fity = str(datafit.y[:51] * 1.e13)
        else:
            fity = str(datafit.y[:51])
        fity = fity.replace("[", "")
        fity = fity.replace("]", "") + "\n"
        print >> output, ";  " + "#" + str(par['RhoPsi'])
        print >> output, "fit" + str(par['RhoPsi']) + " ="
        print >> output, " " + fitx + "\n"
        print >> output, ";  #data"
        print >> output, "fit_data ="
        print >> output, " " + fity
    except:
        pass

    print >> output, "/"
