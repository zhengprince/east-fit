def east_mapping(shot, time, efit_tree, Rz):
    # Programed by Guoqiang Li, July 20, 2015
    # This function is to read the gfile data from MDS+ (if efit_tree=efitrt_east or efit_east)
    #  or from local drive, then map the(R,z) coordinates to flux surface coordinates psi or rho
    # This function is based on PyD3D modules, which are developed by Tom Orsborne at GA.
    # But this function is specially for EAST, due to the specific data structure on
    #  EAST's MDS+ server
    from pmds import mdsconnect
    from efit_eqdsk import get_gdat, read_gfiles, eqdsk_to_1t
    from profiles_mapping import get_mapping

    if efit_tree == 'efitrt_east' or efit_tree == 'efit_east':
        mdsconnect(MDS_SERVER)
        # Only the keys for profile mapping
        gdat_keys = ['gtime', 'rmaxis', 'zmaxis', 'cpasma', 'ssibry', 'ssimag', 'psirz', \
                     'fpol', 'rhovn', 'qpsi', 'nbdry', 'bdry', 'lim']
        gdat = get_gdat(shot, tmin=time, tmax=time, efit=efit_tree, gnames=gdat_keys, open_tree=True)
    else:
        gdat = read_gfiles(shot, tmin=time, tmax=time, efdir=efit_tree)
    gdat = eqdsk_to_1t(gdat, time)

    # Do mapping
    mapping = get_mapping(1, 1, efittree=efit_tree, efdat=gdat)
    rhob = mapping['rhob']

    psirz = gdat['psirz']
    ssibry = gdat['ssibry']
    ssimag = gdat['ssimag']
    psirzn = (psirz - ssimag) / (ssibry - ssimag)
    psirzn = psirzn.spline(quiet=1)

    psi_map = psirzn(Rz)
    rho_map = rhob(psi_map)

    return {'psi': psi_map, 'rho': rho_map}


if __name__ == '__main__':
    from pmds import *
    import numpy as np

    global MDS_SERVER
    MDS_SERVER = '202.127.204.12'
    shot = 55935
    time = 6.1
    efit_tree = 'efit_east'

    mdsconnect(MDS_SERVER)

    ## Read the Microwave reflectometry from MDS+
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
    psi = mapping['psi']
    rho = mapping['rho']

    from pylab import *

    figure(1)
    plot(psi, ne_MR, 'ro')
    xlabel('psi')
    figure(2)
    plot(rho, ne_MR, 'bo')
    xlabel('rho')
    show()

    print('Normal termination')
