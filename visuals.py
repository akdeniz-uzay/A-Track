# -*- coding: utf-8 -*-
# Authors: Yücel Kılıç
# This is an open-source software licensed under GPLv3.


import os

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


def fits2png(fitsfile, outdir, asteroids=None, SPEED_MIN=0.1):

    '''
    Transforms FITS images into PNG files.

    @param fitsfile: FITS file.
    @type fitsfile: string
    @param outdir: Output directory for the png files.
    @type outdir: string
    @param asteroids: numpy array for the moving objects.
    @type asteroids: numpy.ndarray
    @param SPEED_MIN: Minimum speed of a moving object.
    @type SPEED_MIN: float
    '''

    try:
        import f2n
    except ImportError:
        print('Python cannot import f2n. Make sure f2n is installed.')
        return

    image = f2n.fromfits(fitsfile, verbose=False)
    image.setzscale('auto', 'auto')
    image.makepilimage('log', negative=False)

    if asteroids.size:

        for i in range(len(asteroids)):

            if asteroids[i][7] >= SPEED_MIN:
                color = (0, 255, 0)

            else:
                color = (255, 0, 0)

            image.drawcircle(asteroids[i][2], asteroids[i][3], r=10,
                             colour=color,
                             label='{0}'.format(int(asteroids[i][6])))

    image.writetitle(os.path.basename(fitsfile))

    fits_head = os.path.basename(fitsfile).split('.')[0]

    hdu = pyfits.open(fitsfile)
    obs_date = hdu[0].header['date-obs']
    image.writeinfo([obs_date], colour=(255, 100, 0))

    image.tonet(os.path.join(outdir, fits_head + '.png'))


def plot2ds9(fitsfile, catalog):

    '''
    Plots the sources in the catalog in DS9.

    @param fitsfile: FITS file.
    @type fitsfile: string
    @param catalog: Catalog file.
    @type catalog: string
    '''

    try:
        import pyds9 as ds
    except:
        print('Python cannot import pyds9. Make sure pyds9 is installed.')
        raise SystemExit

    print('\033[1;32mStarting DS9...\033[0m')

    d = ds.DS9()
    d.set('file' + fitsfile)
    d.set('zoom to fit')
    d.set('scale zscale')

    print('\033[1;34mDetecting sources on {0}...\033[0m'.format(catalog))

    extension = catalog.split('.')[1]

    if extension == 'pysexcat':
        coordinates = np.genfromtxt(catalog, delimiter=None,
                                    comments='#')[:, [1, 2]]

    elif extension == 'cat':
        coordinates = np.genfromtxt(catalog, delimiter=',', comments='#',
                                    skip_header=1)[:, [1, 2]]

    for i, coordinate in enumerate(coordinates):

        x, y = coordinate[0], coordinate[1]
        cmd = 'image; circle({0},{1},5) # color=red text={{2}}'
        d.set('regions', cmd.format(x, y, i))

    print('\033[1;34mAll sources detected.\033[0m')
