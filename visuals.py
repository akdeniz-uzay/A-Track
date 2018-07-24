# -*- coding: utf-8 -*-
# Authors: Yücel Kılıç, Murat Kaplan, Nurdan Karapınar, Tolga Atay.
# This is an open-source software licensed under GPLv3.


try:
    from astropy.io import fits
except ImportError:
    print('Python cannot import astropy. Make sure astropy is installed.')
    raise SystemExit

try:
    import numpy as np
except ImportError:
    print('Python cannot import numpy. Make sure numpy is installed.')
    raise SystemExit

try:
    import f2n
except ImportError:
    print('Python cannot import f2n. Make sure f2n is installed.')
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
             SPEED_MIN=float(config.get('asteroids', 'SPEED_MIN'))):

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

    hdu = fits.open(fitsfile)
    obs_date = hdu[0].header['date-obs']
    image.writeinfo([obs_date], colour=(255, 100, 0))

    image.tonet(os.path.join(outdir, fits_head + '.png'))


def object_plot(fitsfile, catalog):

    image = f2n.fromfits(fitsfile, verbose=False)
    image.setzscale('auto', 'auto')
    image.makepilimage('log', negative=False)

    print('\033[1;34mPlotting sources on {0}...\033[0m'.format(catalog))

    extension = os.path.splitext(os.path.basename(catalog))[1]

    if extension == '.pysexcat':
        coordinates = np.genfromtxt(catalog, delimiter=None,
                                    comments='#')[:, [1, 2]]

    elif extension == '.cnd':
        coordinates = np.genfromtxt(catalog, delimiter=',', comments='#',
                                    skip_header=1)[:, [1, 2]]

    for i, coordinate in enumerate(coordinates):
        x, y = coordinate[0], coordinate[1]
        label = '{0}'.format(i + 1)
        image.drawcircle(x,
                         y,
                         r=10,
                         colour=(0, 255, 0),
                         label=label)

    image.writetitle(os.path.basename(fitsfile))
    fitshead, fitsextension = os.path.splitext(fitsfile)
    image.tonet('{0}.png'.format(fitshead))

    print('\033[1;34mAll sources plotted on: {0}.png\033[0m'.format(fitshead))

    return True
