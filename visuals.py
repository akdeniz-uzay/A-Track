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

import os
from configparser import ConfigParser

config = ConfigParser()

if os.path.exists('./atrack.config'):
    config.read('./atrack.config')
else:
    print('Python cannot open the configuration file. Make sure atrack.config',
          'is in the same folder as atrack.py.')
    raise SystemExit


def fits2png(fitsfile, outdir, asteroid=None,
             SPEED_MIN=float(config.get('visuals', 'SPEED_MIN'))):

    '''
    Transforms FITS images into PNG files.

    @param fitsfile: FITS file.
    @type fitsfile: string
    @param outdir: Output directory for the png files.
    @type outdir: string
    @param asteroid: numpy array for the moving objects.
    @type asteroid: numpy.ndarray
    @param SPEED_MIN: Minimum speed of a moving object.
    @type SPEED_MIN: float
    '''

    try:
        import f2n
    except ImportError:
        print('Python cannot import f2n. Make sure f2n is installed.')
        raise SystemExit

    image = f2n.fromfits(fitsfile, verbose=False)
    image.setzscale('auto', 'auto')
    image.makepilimage('log', negative=False)

    if asteroid.size:

        for i in range(len(asteroid)):

            x = asteroid.iloc[i]['x']
            y = asteroid.iloc[i]['y']
            speed = asteroid.iloc[i]['Speed(px/min)']
            label = '{0}'.format(int(asteroid.iloc[i]['ObjectID']))

            if speed >= SPEED_MIN:
                color = (0, 255, 0)

            else:
                color = (255, 0, 0)

            image.drawcircle(x, y, r=10, colour=color, label=label)

    image.writetitle(os.path.basename(fitsfile))

    fits_head = os.path.splitext(os.path.basename(fitsfile))[0]

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
    d.set('file {0}'.format(fitsfile))
    d.set('zoom to fit')
    d.set('scale zscale')

    print('\033[1;34mDetecting sources on {0}...\033[0m'.format(catalog))

    extension = os.path.splitext(os.path.basename(catalog))[1]

    if extension == '.pysexcat':
        coordinates = np.genfromtxt(catalog, delimiter=None,
                                    comments='#')[:, [1, 2]]

    elif extension == '.cnd':
        coordinates = np.genfromtxt(catalog, delimiter=',', comments='#',
                                    skip_header=1)[:, [1, 2]]

    for i, coordinate in enumerate(coordinates):

        x, y = coordinate[0], coordinate[1]
        cmd = 'image; circle({0},{1},5) # color=red text=\"' + str(i) + '\"'
        d.set('regions', cmd.format(x, y))

    print('\033[1;34mAll sources plotted.\033[0m')
