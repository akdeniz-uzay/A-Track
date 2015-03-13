# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 23:16:29 2015

@author: ykilic
"""

# -*- coding: utf-8 -*-
#
# Copyleft, Yücel Kılıç (yucelkilic@myrafproject.org).
# This is open-source software licensed under a GPLv3 license.

import alipy
import glob
from alipy import pysex
 

def makecat(fitsfiles, catdir, detect_thresh=3.0, analysis_thresh=3.0, detect_minarea=1, pixel_scale=1.0, seeing_fwhm=2.0, rerun=True, keepcat=True, verbose=True):
    """
    Makes SExtractor catalogues for files.
    
    @param catdir: SExtractor's catalogue files outdir.
    @type catdir: string
    @param detect_thresh: DETECT THRESH sets the threshold value. If one single value is given, it is interpreted as a threshold in units of the background’s standard deviation.
    @type detect_thresh: float, integer
    @param analysis_thresh: Threshold (in surface brightness) at which CLASS STAR and FWHM operate. 1 argument: relative to Background RMS. 2 arguments: mu (mag.arcsec^−2 ), Zero-point (mag).
    @type analysis_thresh: float, integer
    @param detect_minarea: DETECT MINAREA sets the minimum number of pixels a group should have to trigger a detection.
    Obviously this parameter can be used just like DETECT THRESH to detect only bright and “big”
    sources, or to increase detection reliability. It is however more tricky to manipulate at low
    detection thresholds because of the complex interplay of object topology, noise correlations
    (including those induced by filtering), and sampling. In most cases it is therefore recommended
    to keep DETECT MINAREA at a small value, typically 1 to 5 pixels, and let DETECT THRESH and
    the filter define SExtractor’s sensitivity.
    @type detect_minarea: float, integer
    @param pixel_scale: Pixel size in arcsec (for surface brightness parameters, FWHM and star/galaxy separation only).
    @type pixel_scale: float, integer
    @param seeing_fwhm: FWHM of stellar images in arcsec (only for star/galaxy separation).
    @type seeing_fwhm: float, integer
    """
    for filepath in sorted(glob.glob(fitsfiles)):
        pysex.run(filepath, conf_args={'DETECT_THRESH':3.0, 'ANALYSIS_THRESH':3.0, 'DETECT_MINAREA':1,
        'PIXEL_SCALE':1.0, 'SEEING_FWHM':2.0, "FILTER":"Y", 'VERBOSE_TYPE':'NORMAL' if verbose else 'QUIET'},
        params=['X_IMAGE', 'Y_IMAGE', 'FLUX_AUTO', 'FWHM_IMAGE', 'FLAGS', 'ELONGATION', 'NUMBER', "EXT_NUMBER"],
        rerun=rerun, keepcat=keepcat, catdir=catdir)
    return

def align(fitsfiles, ref_image, outdir):
    """
    FITS file align for alipy.

    @param outdir: Out directory for aligned FITS images.
    @type outdir: string                    
    """   
    # Minimal example of how to align images :
    images_to_align = sorted(glob.glob(fitsfiles))

    identifications = alipy.ident.run(ref_image, images_to_align, visu=False, skipsaturated=True, sexkeepcat=True)
    # That's it !
    # Put visu=True to get visualizations in form of png files (nice but much slower)
    # On multi-extension data, you will want to specify the hdu (see API doc).
    
    # The output is a list of Identification objects, which contain the transforms :       
    outputshape = alipy.align.shape(ref_image)
    # This is simply a tuple (width, height)... you could specify any other shape.
    
    for id in identifications:
            if id.ok == True:
                    # Variant 1, using only scipy and the simple affine transorm :
                    alipy.align.affineremap(id.ukn.filepath, id.trans, shape=outputshape, outdir=outdir, makepng=False)
                    # By default, the aligned images are written into a directory "alipy_out".
    return

        
        