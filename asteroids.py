# -*- coding: utf-8 -*-
# Authors: Yücel Kılıç, Murat Kaplan, Nurdan Karapınar, Tolga Atay.
# This is an open-source software licensed under GPLv3.


try:
    import pyfits
except ImportError:
    print('Python cannot import pyfits. Make sure pyfits is installed.')
    raise SystemExit

try:
    import numpy as np
except ImportError:
    print('Python cannot import numpy. Make sure numpy is installed.')
    raise SystemExit

try:
    import pandas as pd
except ImportError:
    print('Python cannot import pandas. Make sure pandas is installed.')
    raise SystemExit

import math
import glob
import os
import time
import itertools as it
import pickle as pk
from multiprocessing import Pool, cpu_count
from configparser import ConfigParser

config = ConfigParser()

if os.path.exists('./atrack.config'):
    config.read('./atrack.config')

else:
    print('Python cannot open the configuration file. Make sure atrack.config',
          'is in the same folder as atrack.py.')
    raise SystemExit


def distance(p1, p2):

    '''
    Returns the distance between two points.

    @param p1: x and y coordinates of the first point.
    @type p1: list, tuple
    @param p2: x and y coordinates of the second point.
    @type p2: list, tuple
    @return: float
    '''

    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def isClose(p1, p2, dmax):

    '''
    Checks if the distance between two points is less than a given value.

    @param p1: x and y coordinates of the first point.
    @type p1: list, tuple
    @param p2: x and y coordinates of the second point.
    @type p2: list, tuple
    @param dmax: Distance to compare.
    @type dmax: float, integer
    @return: boolean
    '''

    d12 = distance(p1, p2)

    return d12 <= dmax


def ordered(p1, p2, p3):

    '''
    Reorders the vertices p1,p2,p3 of a triangle such that first two points
    define the longest edge.

    @param p1: x and y coordinates of the first point.
    @type p1: list, tuple
    @param p2: x and y coordinates of the second point.
    @type p2: list, tuple
    @param p3: x and y coordinates of the third point.
    @type p3: list
    @return: tuple
    '''

    d12 = distance(p1, p2)
    d13 = distance(p1, p3)
    d23 = distance(p2, p3)

    long = max(d12, d23, d13)

    if long == d12:
        return (p1, p2, p3)
    elif long == d13:
        return (p1, p3, p2)
    elif long == d23:
        return (p2, p3, p1)


def height(p1, p2, p3):

    '''
    Returns the shortest distance between a line and a point.

    @param p1: x and y coordinates of the first point on the line.
    @type p1: list, tuple
    @param p2: x and y coordinates of the second point on the line.
    @type p2: list, tuple
    @param p3: x and y coordinates of the third point.
    @type p3: list
    @return: float
    '''

    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    x3 = p3[0]
    y3 = p3[1]

    try:
        h = math.fabs((x2 - x1)*y3 - (y2 - y1)*x3 + x1*y2 - x2*y1) \
            / math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
    except ZeroDivisionError:
        h = 0

    return h


def partitions(workload):

    '''
    Distributes the workload (3-combinations of all images) among available
    CPUs as evenly as possible.

    @param workload: List of 3-combinations of all images.
    @type workload: list
    @return: list
    '''

    nCPU = cpu_count()
    partition = []
    n = nCPU

    while len(partition) != nCPU and len(workload) != 0:

        size = math.ceil(len(workload) / n)
        partition.append(workload[:size])
        del workload[:size]
        n = n - 1

    return(partition)


def detect_candidates(CMO,
                      FWHM_MIN=float(config.get('asteroids', 'FWHM_MIN')),
                      FWHM_COEFFICIENT=float(config.get('asteroids',
                                                        'FWHM_COEFFICIENT')),
                      FLUX_MAX=float(config.get('asteroids', 'FLUX_MAX')),
                      FLAG_MAX=int(config.get('asteroids', 'FLAG_MAX')),
                      ELONGATION_MAX=float(config.get('asteroids',
                                                      'ELONGATION_MAX')),
                      SNR_MIN=float(config.get('asteroids', 'SNR_MIN')),
                      TRAVEL_MIN=float(config.get('asteroids', 'TRAVEL_MIN'))):

    '''
    Eliminates the sources, that do not satisfy the given criteria, from given
    SExtractor catalog files.

    @param CMO: Tuple (list of SExtractor catalog files, master catalog file,
    output directory for the new catalog file).
    @type CMO: tuple
    @param FWHM_MIN: Minimum FWHM for the candidate objects.
    @type FWHM_MIN: float
    @param FWHM_COEFFICIENT: FWHM coefficient.
    @type FWHM_COEFFICIENT: float
    @param FLUX_MAX: Maximum flux for the candidate objects.
    @type FLUX_MAX: float
    @param ELONGATION_MAX: Maximum ellipticity for the candidate objects.
    @param FLAG_MAX: Maximum number of sum of FLAG values.
    @type FLAG_MAX: int
    @type ELONGATION_MAX: float
    @param SNR_MIN: Minimum SNR_MIN for the candidate objects.
    @type SNR_MIN: float
    @param TRAVEL_MIN: Minimum travel distance between two images for a
    moving object.
    @type TRAVEL_MIN: float
    '''

    catalogs, master, outdir = CMO[0], CMO[1], CMO[2]

    masterF = np.genfromtxt(master, delimiter=None, comments='#')
    COLUMNS = ['flags', 'x', 'y', 'flux', 'background', 'fwhm', 'elongation',
               'fluxerr']
    FWHM_MAX = np.mean(masterF[:, 5]) * FWHM_COEFFICIENT
    masterF = pd.DataFrame.from_records(masterF, columns=COLUMNS)
    masterF = masterF[
        (masterF.flags <= FLAG_MAX) &
        (masterF.fwhm <= FWHM_MAX) &
        (masterF.fwhm >= FWHM_MIN) &
        (masterF.flux <= FLUX_MAX) &
        (masterF.flux > masterF.background) &
        (masterF.flux / masterF.fluxerr > SNR_MIN) &
        (masterF.elongation <= ELONGATION_MAX)]
    masterF = masterF[COLUMNS[:5]].reset_index(drop=True)

    for catalog in catalogs:

        catalogF = np.genfromtxt(catalog, delimiter=None, comments='#')
        catalogF = pd.DataFrame.from_records(catalogF, columns=COLUMNS)

        catalogF = catalogF[
            (catalogF.flags <= FLAG_MAX) &
            (catalogF.fwhm <= FWHM_MAX) &
            (catalogF.fwhm >= FWHM_MIN) &
            (catalogF.flux <= FLUX_MAX) &
            (catalogF.flux > catalogF.background) &
            (catalogF.flux / catalogF.fluxerr > SNR_MIN) &
            (catalogF.elongation <= ELONGATION_MAX)]

        catalogF = catalogF[COLUMNS[:5]].reset_index(drop=True)

        candidates = pd.DataFrame(columns=COLUMNS[:5])

        for i in range(len(catalogF.x)):

            if len(masterF[(masterF.x - catalogF.x[i])**2 +
                           (masterF.y - catalogF.y[i])**2 <=
                           TRAVEL_MIN ** 2]) < 2:

                candidates = candidates.append(catalogF.iloc[i],
                                               ignore_index=True)

        catalog_head = os.path.splitext(os.path.basename(catalog))[0]
        candidates.to_csv('{0}/{1}.cnd'.format(outdir, catalog_head),
                          index=False)


def all_candidates(catdir, outdir):

    '''
    Eliminates the sources, that do not satisfy the given criteria, from all
    SExtractor catalog files.

    @param catdir: Directory for the catalog files.
    @type catdir: string
    @param outdir: Output directory for the new catalog files.
    @type outdir: string
    '''

    nCPU = cpu_count()
    workload = sorted(glob.glob(catdir + '/*affineremap.pysexcat'))
    cmds = []

    for catalogs in partitions(workload):
        cmds.append(tuple([catalogs, catdir + '/master.pysexcat', outdir]))

    with Pool(nCPU) as pool:
        pool.map(detect_candidates, cmds)


def detect_segments(CFP,
                    TRAVEL_MIN=float(config.get('asteroids', 'TRAVEL_MIN')),
                    HEIGHT_MAX=float(config.get('asteroids', 'HEIGHT_MAX')),
                    SCALE=float(config.get('asteroids', 'SCALE')),
                    V_MAX=float(config.get('asteroids', 'V_MAX')),
                    TOLERANCE=float(config.get('asteroids', 'TOLERANCE'))):

    '''
    Detects line segments inside a given list of 3-combinations.

    @param catdir: Tuple (directory for the catalog files, directory for the
    aligned FITS images, processor number).
    @type CFP: tuple
    @param TRAVEL_MIN: Minimum travel distance between two images for a
    moving object.
    @type TRAVEL_MIN: float
    @param HEIGHT_MAX: Maximum height of the triangle for the 3 points to
    be considered as collinear.
    @type HEIGHT_MAX: float
    @param SCALE: Pixel scale subtended by the telescope/CCD system
    (arcsec).
    @type SCALE: float
    @param V_MAX: Theoretical maximum angular velocity of NEOs ("/sec).
    @type V_MAX: float
    @param TOLERANCE: Tolerance for the position of third point (pixel).
    @type TOLERANCE: float
    '''

    catdir, fitsdir, processor = CFP[0], CFP[1], CFP[2]
    images = sorted(glob.glob(fitsdir + '/*.fits'))
    files = sorted(glob.glob(catdir + '/*affineremap.cnd'))
    fileids = list(range(len(files)))
    workload = list(it.combinations(fileids, 3))

    catalogs = []

    for file in files:

        catalog = pd.read_csv(file, sep=',',
                              names=['flags', 'x', 'y', 'flux', 'background'],
                              header=0)
        catalogs.append(catalog.values)

    segments = []
    partition = partitions(workload)[int(processor)]

    for i, j, k in partition:

        hdu1 = pyfits.open(images[i])
        hdu2 = pyfits.open(images[j])
        hdu3 = pyfits.open(images[k])
        try:
            xbin = hdu1[0].header['xbinning']
        except:
            xbin = 1

        exp_time1 = hdu1[0].header['exptime']
        exp_time2 = hdu2[0].header['exptime']
        exp_time3 = hdu3[0].header['exptime']

        obs_date1 = hdu1[0].header['date-obs']
        obs_date2 = hdu2[0].header['date-obs']
        obs_date3 = hdu3[0].header['date-obs']

        if "T" not in obs_date1:
            time_obs1 = hdu1[0].header['time-obs']
            obs_date1 = "{0}T{1}".format(obs_date1.strip(),
                                         time_obs1.strip())

        if "T" not in obs_date2:
            time_obs2 = hdu2[0].header['time-obs']
            obs_date2 = "{0}T{1}".format(obs_date2.strip(),
                                         time_obs2.strip())

        if "T" not in obs_date3:
            time_obs3 = hdu3[0].header['time-obs']
            obs_date3 = "{0}T{1}".format(obs_date3.strip(),
                                         time_obs3.strip())

        try:
            obs_time1 = time.strptime(obs_date1, '%Y-%m-%dT%H:%M:%S.%f')
        except:
            obs_time1 = time.strptime(obs_date1, '%Y-%m-%dT%H:%M:%S')
        try:
            obs_time2 = time.strptime(obs_date2, '%Y-%m-%dT%H:%M:%S.%f')
        except:
            obs_time2 = time.strptime(obs_date2, '%Y-%m-%dT%H:%M:%S')
        try:
            obs_time3 = time.strptime(obs_date3, '%Y-%m-%dT%H:%M:%S.%f')
        except:
            obs_time3 = time.strptime(obs_date3, '%Y-%m-%dT%H:%M:%S')

        dmax = (time.mktime(obs_time2) - time.mktime(obs_time1) +
                (exp_time2 - exp_time1) / 2) * V_MAX / (SCALE * xbin)

        for p1, p2 in it.product(range(len(catalogs[i])),
                                 range(len(catalogs[j]))):

            if not isClose(catalogs[i][p1, [1, 2]], catalogs[j][p2, [1, 2]],
                           dmax):
                continue

            d12 = distance(catalogs[i][p1][1:3], catalogs[j][p2][1:3])
            t12 = (time.mktime(obs_time2) - time.mktime(obs_time1) +
                   (exp_time2 - exp_time1) / 2)

            for p3 in range(len(catalogs[k])):

                d23 = distance(catalogs[j][p2][1:3],
                               catalogs[k][p3][1:3])
                t23 = (time.mktime(obs_time3) - time.mktime(obs_time2) +
                       (exp_time3 - exp_time2) / 2)

                if not (t23 * d12 / t12 - TOLERANCE <= d23 <=
                        t23 * d12 / t12 + TOLERANCE):
                    continue

                points = ordered(catalogs[i][p1, [1, 2]],
                                 catalogs[j][p2, [1, 2]],
                                 catalogs[k][p3, [1, 2]])
                HEIGHT = height(points[0], points[1], points[2])
                LENGTH = distance(points[0], points[1])

                if LENGTH > TRAVEL_MIN * 2 and HEIGHT < HEIGHT_MAX:
                    segments.append([[i,
                                      catalogs[i][p1][0], catalogs[i][p1][1],
                                      catalogs[i][p1][2], catalogs[i][p1][3],
                                      catalogs[i][p1][4]],
                                     [j,
                                      catalogs[j][p2][0], catalogs[j][p2][1],
                                      catalogs[j][p2][2], catalogs[j][p2][3],
                                      catalogs[j][p2][4]],
                                     [k,
                                      catalogs[k][p3][0], catalogs[k][p3][1],
                                      catalogs[k][p3][2], catalogs[k][p3][3],
                                      catalogs[k][p3][4]]])

    with open(catdir + '/Processor{0}.sgm'.format(processor), 'wb') as result:
        pk.dump(segments, result)

    print('Processor {0} complete.'.format(processor))


def merge_segments(segments):

    '''
    Merges 3-point segments that belong to the same line.
    @param segments: List of 3-point segments.
    @type segments: list
    @return: list
    '''

    lines = []

    for segment in segments:

        p1 = segment[0][2:4]
        p2 = segment[1][2:4]
        p3 = segment[2][2:4]

        if lines:

            for line in lines:

                points = [point[2:4] for point in line]
                check1 = p1 in points
                check2 = p2 in points
                check3 = p3 in points
                checks = (check1, check2, check3)

                if True in checks and False in checks:

                    for i in range(3):
                        if checks[i] is False:
                            line.append(segment[i])
                    break

                elif False not in checks:
                    break

            if True not in checks:
                lines.append([segment[0], segment[1], segment[2]])

        else:
            lines.append([segment[0], segment[1], segment[2]])

    return lines


def detect_lines(catdir, fitsdir):

    '''
    Detects all line segments in a project.

    @param catdir: Directory for the catalog files.
    @type catdir: string
    @param fitsdir: Directory for the aligned FITS images.
    @type fitsdir: string
    @return: list
    '''

    nCPU = cpu_count()
    cmds = []

    for i in range(nCPU):
        cmds.append(tuple([catdir, fitsdir, str(i)]))

    try:
        with Pool(nCPU) as pool:
            pool.map(detect_segments, cmds, 1)

    except IndexError:
        detect_segments((catdir, fitsdir, 0))

    results = sorted(glob.glob(catdir + '/*.sgm'))
    segments = []

    for result in results:

        with open(result, 'rb') as res:
            segments += pk.load(res)

        os.remove(result)

    return merge_segments(segments)


def results(fitsdir, lines,
            SPEED_MIN=float(config.get('asteroids', 'SPEED_MIN'))):

    '''
    Reports detected moving objects and uncertain objects.

    @param fitsdir: Directory for the aligned FITS images.
    @type fitsdir: string
    @param lines: List of detected lines.
    @type lines: list
    @param SPEED_MIN: Minimum speed of a moving object.
    @type SPEED_MIN: float
    @return: numpy.ndarray
    '''

    moving_objects = []
    uncertain_objects = []

    images = sorted(glob.glob(fitsdir + '/*.fits'))

    for i in range(len(lines)):

        line = sorted(lines[i])
        nmin = int(line[0][0])
        nmax = int(line[-1][0])
        hdu1 = pyfits.open(images[nmin])
        hdu2 = pyfits.open(images[nmax])

        obs_date1 = hdu1[0].header['date-obs']
        if "T" not in obs_date1:
            time_obs1 = hdu1[0].header['time-obs']
            obs_date1 = "{0}T{1}".format(obs_date1.strip(),
                                         time_obs1.strip())
        exp_time1 = hdu1[0].header['exptime']

        # Second image
        obs_date2 = hdu2[0].header['date-obs']
        if "T" not in obs_date2:
            time_obs2 = hdu2[0].header['time-obs']
            obs_date2 = "{0}T{1}".format(obs_date2.strip(),
                                         time_obs2.strip())
        exp_time2 = hdu2[0].header['exptime']

        try:
            obs_time1 = time.strptime(obs_date1, '%Y-%m-%dT%H:%M:%S.%f')
        except:
            obs_time1 = time.strptime(obs_date1, '%Y-%m-%dT%H:%M:%S')
        try:
            obs_time2 = time.strptime(obs_date2, '%Y-%m-%dT%H:%M:%S.%f')
        except:
            obs_time2 = time.strptime(obs_date2, '%Y-%m-%dT%H:%M:%S')

        length = distance(line[0][2:4], line[-1][2:4])

        try:
            speed = 60 * length / (time.mktime(obs_time2) + exp_time2 / 2 -
                                   time.mktime(obs_time1) - exp_time1 / 2)
        except:
            speed = 0

        info = np.concatenate((np.asarray(line),
                               np.asarray([[int(i) + 1] * len(line)]).T,
                               np.asarray([[speed] * len(line)]).T),
                              axis=1)

        if speed >= SPEED_MIN:
            moving_objects.append(info)
        else:
            uncertain_objects.append(info)

    if len(moving_objects) == 1:
        moving_objects = moving_objects[0]
    elif len(moving_objects) > 1:
        moving_objects = np.concatenate(tuple(moving_objects), axis=0)
    elif len(moving_objects) == 0:
        moving_objects = np.array([])

    if len(uncertain_objects) == 1:
        uncertain_objects = uncertain_objects[0]
    elif len(uncertain_objects) > 1:
        uncertain_objects = np.concatenate(tuple(uncertain_objects), axis=0)
    elif len(uncertain_objects) == 0:
        uncertain_objects = np.array([])

    return moving_objects, uncertain_objects
