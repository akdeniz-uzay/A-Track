# -*- coding: utf-8 -*-
# Authors: Yücel Kılıç, Murat Kaplan, Nurdan Karapınar, Tolga Atay.
# This is an open-source software licensed under GPLv3.


try:
    import numpy as np
except ImportError:
    print('Python cannot import numpy. Make sure numpy is installed.')
    raise SystemExit

try:
    import alipy
    from alipy import pysex
except ImportError:
    print('Python cannot import alipy. Make sure alipy is installed.')
    raise SystemExit

import glob
import os
from configparser import ConfigParser

config = ConfigParser()

if os.path.exists('./atrack.config'):
    config.read('./atrack.config')
else:
    print('Python cannot open the configuration file. Make sure atrack.config',
          'is in the same folder as atrack.py.')
    raise SystemExit


def align(fitsdir, reference, outdir):

    '''
    Aligns the given FITS images using alipy.

    @param fitsdir: Directory for the FITS images to be aligned.
    @type fitsdir: string
    @param reference: Reference FITS image.
    @type reference: string
    @param outdir: Output directory for the aligned images.
    @type outdir: string
    '''

    images = sorted(glob.glob(fitsdir + '/*.fits'))

    if not reference:
        reference = images[0]

    identifications = alipy.ident.run(reference, images, visu=False,
                                      sexkeepcat=False, verbose=False)

    outshape = alipy.align.shape(reference, verbose=False)

    for idn in identifications:

        if idn.ok:
            alipy.align.affineremap(idn.ukn.filepath, idn.trans,
                                    shape=outshape, outdir=outdir,
                                    makepng=False, verbose=False)


def make_catalog(fitsdir, outdir,
                 DETECT_THRESH=float(config.get('sources', 'DETECT_THRESH')),
                 ANALYSIS_THRESH=float(config.get('sources',
                                                  'ANALYSIS_THRESH')),
                 DETECT_MINAREA=float(config.get('sources', 'DETECT_MINAREA')),
                 PIXEL_SCALE=float(config.get('sources', 'PIXEL_SCALE')),
                 SEEING_FWHM=float(config.get('sources', 'SEEING_FWHM')),
                 PHOT_AUTOPARAMS=config.get('sources', 'PHOT_AUTOPARAMS'),
                 BACK_SIZE=int(config.get('sources', 'BACK_SIZE')),
                 BACK_FILTERSIZE=int(config.get('sources', 'BACK_FILTERSIZE')),
                 DEBLEND_NTHRESH=int(config.get('sources', 'DEBLEND_NTHRESH')),
                 SATUR_LEVEL=float(config.get('sources', 'SATUR_LEVEL')),
                 DEBLEND_MINCONT=float(config.get('sources',
                                                  'DEBLEND_MINCONT')),
                 GAIN=float(config.get('sources', 'GAIN')),
                 rerun=config.get('sources', 'rerun'),
                 keepcat=config.get('sources', 'keepcat'),
                 verbose=config.get('sources', 'verbose')):

    '''
    Creates SExtractor catalogs from FITS files.

    @param fitsdir: Directory for the FITS files to be used.
    @type fitsdir: string
    @param outdir: Output directory for SExtractor's catalog files.
    @type outdir: string
    @param DETECT_THRESH: Number of σ’s above the local background that an
    object must have in order to be detected.
    @type DETECT_THRESH: float, integer
    @param ANALYSIS_THRESH: Surface brightness threshold at which CLASS STAR
    and FWHM operate. 1 argument: Relative to background RMS. 2 arguments: mu
    (mag.arcsec^−2 ), Zero-point (mag).
    @type ANALYSIS_THRESH: float, integer
    @param DETECT_MINAREA: Minimum number of pixels a group should have inorder
    to trigger detection. This parameter can be used just like DETECT_THRESH to
    detect only the bright and 'big' sources, or to increase detection
    reliability. However, it is tricky to manipulate at low detection
    thresholds because of the complex interplay of the object topology, noise
    correlations (including those induced by filtering), and sampling.
    Therefore, it is recommended to keep DETECT_MINAREA small, typically 1 to 5
    pixels and let DETECT_THRESH define SExtractor’s sensitivity.
    @type DETECT_MINAREA: float, integer
    @param PIXEL_SCALE: Pixel scale subtended by the telescope/CCD system
    (arcsec).
    @type PIXEL_SCALE: float, integer
    @param SEEING_FWHM: FWHM of stellar images in arcsec for star/galaxy
    separation.
    @type SEEING_FWHM: float, integer
    @param PHOT_AUTOPARAMS: MAG_AUTO parameters: <Kron_fact>, <min_radius>.
    @type PHOT_AUTOPARAMS: float, integer
    @param BACK_SIZE: Background mesh: <size> or <width>,<height>.
    @type BACK_SIZE: float, integer
    @param BACK_FILTERSIZE: Background filter: <size> or <width>,<height>.
    @type BACK_FILTERSIZE: float, integer
    @param DEBLEND_NTHRESH: Number of deblending sub-thresholds.
    @type DEBLEND_NTHRESH: float, integer
    @param SATUR_LEVEL: Saturation level (ADU).
    @type SATUR_LEVEL: float, integer
    @param DEBLEND_MINCONT: Minimum contrast parameter for deblending.
    @type DEBLEND_MINCONT: float, integer
    @param GAIN: Detector gain (e-/ADU).
    @type GAIN: float, integer
    @param rerun: Runs SExtractor even if the catalog directory already exists.
    @type rerun: boolean
    @param keepcat: Keeps extracted catalog files.
    @type keepcat: boolean
    @param verbose: Notifies the user via terminal.
    @type verbose: boolean
    '''

    fitsfiles = sorted(glob.glob(fitsdir + '/*.fits'))

    for fitsfile in fitsfiles:

        pysex.run(fitsfile,
                  conf_args={'DETECT_THRESH': DETECT_THRESH,
                             'ANALYSIS_THRESH': ANALYSIS_THRESH,
                             'DETECT_MINAREA': DETECT_MINAREA,
                             'SATUR_LEVEL': SATUR_LEVEL,
                             'GAIN': GAIN,
                             'DEBLEND_NTHRESH': DEBLEND_NTHRESH,
                             'DEBLEND_MINCONT': DEBLEND_MINCONT,
                             'PIXEL_SCALE': PIXEL_SCALE,
                             'SEEING_FWHM': SEEING_FWHM,
                             'PHOT_AUTOPARAMS': PHOT_AUTOPARAMS,
                             'BACK_SIZE': BACK_SIZE,
                             'BACK_FILTERSIZE': BACK_FILTERSIZE,
                             'FILTER': 'Y',
                             'VERBOSE_TYPE': 'QUIET'},
                  params=['FLAGS', 'X_IMAGE', 'Y_IMAGE', 'FLUX_AUTO',
                          'BACKGROUND', 'FWHM_IMAGE', 'ELONGATION',
                          'FLUXERR_AUTO'],
                  rerun=rerun, keepcat=keepcat, catdir=outdir)


def make_master(catdir):

    '''
    Combines all catalog files in a given directory into one master file named
    'master.pysexcat'.

    @param catdir: Directory which contains the catalog files.
    @type catdir: string
    '''

    catfiles = sorted(glob.glob(catdir + '/*affineremap.pysexcat'))

    with open(catdir + '/master.pysexcat', 'wb') as outfile:
        for catfile in catfiles:
            catalog = np.genfromtxt(catfile, delimiter=None, comments='#')
            np.savetxt(outfile, catalog, delimiter=' ')
