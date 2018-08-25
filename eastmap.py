from efit_eqdsk import get_gdat, read_gfiles, eqdsk_to_1t
from profiles_mapping import get_mapping


def east_mapping(shot, time, efit_tree, Rz):
    # Programed by Guoqiang Li, July 20, 2015
    # This function is to read the gfile data from MDS+ (if efit_tree=efitrt_east or efit_east)
    #  or from local drive, then map the(R,z) coordinates to flux surface coordinates psi or rho
    # This function is based on PyD3D modules, which are developed by Tom Orsborne at GA.
    # But this function is specially for EAST, due to the specific data structure on
    #  EAST's MDS+ server
    from efit_eqdsk import get_gdat, read_gfiles, eqdsk_to_1t
    from profiles_mapping import get_mapping
    # MDS_SERVER = '202.127.204.12'
    # GFILE: FROM FILE, TIME IS MS; FROM MDS+, TIME IS S.
    if efit_tree == 'efitrt_east' or efit_tree == 'efit_east':
        # mdsconnect(MDS_SERVER)
        time /= 1000.
        # Only the keys for profile mapping
        gdat_keys = ['gtime', 'rmaxis', 'zmaxis', 'cpasma', 'ssibry', 'ssimag', 'psirz',
                     'fpol', 'rhovn', 'qpsi', 'nbdry', 'bdry', 'lim']
        gdat = get_gdat(shot, tmin=time, tmax=time, efit=efit_tree, gnames=gdat_keys, open_tree=True)
    else:
        gdat = read_gfiles(shot, tmin=time, tmax=time, efdir=efit_tree)
    gdat = eqdsk_to_1t(gdat, time)

    # Do mapping
    mapping = get_mapping(1, 1, efittree='EFITxx', efdat=gdat)

    if Rz.any():
        rhob = mapping['rhob']
        psirz = gdat['psirz']
        ssibry = gdat['ssibry']
        ssimag = gdat['ssimag']
        psirzn = (psirz - ssimag) / (ssibry - ssimag)
        psirzn = psirzn.spline(quiet=1)

        psi_map = psirzn(Rz)
        rho_map = rhob(psi_map)

        return {'psi': psi_map, 'rho': rho_map}
    else:
        return {'mapping': mapping}


def psi2rho(shot, time, efit_tree, psi):
    # MDS_SERVER = '202.127.204.12'
    if efit_tree == 'efitrt_east' or efit_tree == 'efit_east':
        # mdsconnect(MDS_SERVER)
        time /= 1000.
        gdat_keys = ['gtime', 'rmaxis', 'zmaxis', 'cpasma', 'ssibry', 'ssimag', 'psirz',
                     'fpol', 'rhovn', 'qpsi', 'nbdry', 'bdry', 'lim']
        gdat = get_gdat(shot, tmin=time, tmax=time, efit=efit_tree, gnames=gdat_keys, open_tree=True)
    else:
        gdat = read_gfiles(shot, tmin=time, tmax=time, efdir=efit_tree)
    gdat = eqdsk_to_1t(gdat, time)

    # Do mapping
    mapping = get_mapping(1, 1, efittree='EFITxx', efdat=gdat)
    rhob = mapping['rhob']
    rho_map = rhob(psi)

    return {'rho': rho_map}


def rho2psi(shot, time, efit_tree, rho):
    # MDS_SERVER = '202.127.204.12'
    if efit_tree == 'efitrt_east' or efit_tree == 'efit_east':
        # mdsconnect(MDS_SERVER)
        time /= 1000.
        gdat_keys = ['gtime', 'rmaxis', 'zmaxis', 'cpasma', 'ssibry', 'ssimag', 'psirz',
                     'fpol', 'rhovn', 'qpsi', 'nbdry', 'bdry', 'lim']
        gdat = get_gdat(shot, tmin=time, tmax=time, efit=efit_tree, gnames=gdat_keys, open_tree=True)
    else:
        gdat = read_gfiles(shot, tmin=time, tmax=time, efdir=efit_tree)
    gdat = eqdsk_to_1t(gdat, time)

    mapping = get_mapping(1, 1, efittree=efit_tree, efdat=gdat)
    invrhob = mapping['invrhob']
    psi_map = invrhob(rho)

    return {'psi': psi_map}


def xRZmap(shot, time0, efitDir, rzdata):
    # gg is the gfile instance, reading by the pyD3D.efit.read_gfiles
    #   it must be reduced to one time silce.
    # dataFile the file name of the data file, it must have three column:
    #   (r, z, data), (r,z) are in meter
    import numpy
    import rhopsi
    import efit
    # import pylab

    gg = efit.read_gfiles(shot, tmin=time0, tmax=time0, efdir=efitDir, reduce_if_1t=1)
    psirz = gg['psirz']
    psibry = gg['ssibry']
    psimax = gg['ssimag']
    rmaxis = gg['rmaxis']
    zmaxis = gg['zmaxis']
    qpsi = gg['qpsi']
    polflux = psibry - psimax
    psinor = (psirz - psimax) / (psibry - psimax)
    psinor = psinor.spline(quiet=1)

    dtype = [('psi', float), ('data', float)]
    psiY = []
    psiYY = []
    rhoYY = []
    for i in range(len(rzdata)):
        rr = rzdata[i][0]
        zz = rzdata[i][1]
        psiY.append((psinor(rr, zz), rzdata[i][2]))
    psiY = numpy.array(psiY, dtype=dtype)
    psiY = numpy.sort(psiY, order='psi')
    for i in range(len(psiY)):
        psiYY.append(list(psiY[i]))
    psiYY = numpy.array(psiYY)
    for i in range(len(psiYY) - 1):  # Make the psi monotonic
        if psiYY[i + 1][0] - psiYY[i][0] <= 0.:
            psiYY[i + 1] = psiYY[i] + 0.001

    rhopsi = rhopsi.rhopsi(qpsi, polflux)
    rhob = rhopsi['rhob']
    rhoYY = numpy.copy(psiYY)
    rhoYY[:, 0] = rhob.spline(quiet=1)(psiYY[:, 0])
    for i in range(len(rhoYY)):  # For those rho>1, rho=sqrt(psi)
        if rhoYY[i][0] > 1.:
            rhoYY[i][0] = numpy.sqrt(psiYY[i][0])
    return {"psiY": psiYY, "rhoY": rhoYY}


# !/bin/env /project/imd/python/Python-2.7.8/bin/python
#
# programmed by Guoqiang Li
# first created on July 15, 2012
# fixed bug on Oct. 15, 2012: for those rho>1, rho=sqrt(psi)
# fixed bug on Oct. 16, 2012: made the psi monotonic
# updated on Mar. 16, 2015, make it easier to call from command line

def RZmap(shot, time0, efitDir, dataFile):
    # gg is the gfile instance, reading by the pyD3D.efit.read_gfiles
    #   it must be reduced to one time silce.
    # dataFile the file name of the data file, it must have three column:
    #   (r, z, data), (r,z) are in meter
    import numpy
    import rhopsi
    import efit
    # import pylab

    gg = efit.read_gfiles(shot, tmin=time0, tmax=time0, efdir=efitDir, reduce_if_1t=1)
    psirz = gg['psirz']
    psibry = gg['ssibry']
    psimax = gg['ssimag']
    rmaxis = gg['rmaxis']
    zmaxis = gg['zmaxis']
    qpsi = gg['qpsi']
    polflux = psibry - psimax
    psinor = (psirz - psimax) / (psibry - psimax)
    psinor = psinor.spline(quiet=1)

    rzdata = numpy.loadtxt(dataFile)

    dtype = [('psi', float), ('data', float)]
    psiY = []
    psiYY = []
    rhoYY = []
    for i in range(len(rzdata)):
        rr = rzdata[i][0]
        zz = rzdata[i][1]
        psiY.append((psinor(rr, zz), rzdata[i][2]))
    psiY = numpy.array(psiY, dtype=dtype)
    psiY = numpy.sort(psiY, order='psi')
    for i in range(len(psiY)):
        psiYY.append(list(psiY[i]))
    psiYY = numpy.array(psiYY)
    for i in range(len(psiYY) - 1):  # Make the psi monotonic
        if psiYY[i + 1][0] - psiYY[i][0] <= 0.:
            psiYY[i + 1][0] = psiYY[i][0] + 0.0001

    rhopsi = rhopsi.rhopsi(qpsi, polflux)
    rhob = rhopsi['rhob']
    rhoYY = numpy.copy(psiYY)
    rhoYY[:, 0] = rhob.spline(quiet=1)(psiYY[:, 0])
    for i in range(len(rhoYY)):  # For those rho>1, rho=sqrt(psi)
        if rhoYY[i][0] > 1.:
            rhoYY[i][0] = numpy.sqrt(psiYY[i][0])
    return {"psi": psiYY, "rho": rhoYY}
