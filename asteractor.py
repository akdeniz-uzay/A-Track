# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 23:16:29 2015

@author: ykilic
"""

# -*- coding: utf-8 -*-
#
# Copyleft, Yücel Kılıç (yucelkilic@myrafproject.org).
# This is open-source software licensed under a GPLv3 license.
import glob
import os

try:
    import alipy
    from alipy import pysex
except ImportError:
    print "Do you have alipy?"
    raise SystemExit

try:
    import numpy as np
except ImportError:
    print "Did you install numpy?"
    raise SystemExit
 

def makecat(fitsfiles, catdir, detect_thresh=3, analysis_thresh=3, detect_minarea=1, pixel_scale=0.31, seeing_fwhm=1.5, 
            phot_autoparams='\"2.5, 3.5\"', back_size=64, back_filtersize=3, deblend_nthresh=16, 
            satur_level=60000, deblend_mincont=0.00001, gain=0.55, rerun=True, keepcat=True, verbose=True):
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
    @param phot_autoparams: MAG_AUTO parameters: <Kron_fact>,<min_radius>.
    @type phot_autoparams: float, integer
    @param back_size: Background mesh: <size> or <width>,<height>.
    @type back_size: float, integer
    @param back_filtersize: Background filter: <size> or <width>,<height>.
    @type back_filtersize: float, integer
    @param deblend_nthresh: Number of deblending sub-thresholds.
    @type deblend_nthresh: float, integer
    @param satur_level: level (in ADUs) at which arises saturation.
    @type satur_level: float, integer
    @param deblend_mincont: Minimum contrast parameter for deblending.
    @type deblend_mincont: float, integer
    @param gain: detector gain in e-/ADU.
    @type gain: float, integer
    @param rerun: Rerun sextractor if catalogue directory exist.
    @type rerun: boolean
    @param keepcat: Keep extracted catalogue files.
    @type keepcat: boolean
    @param verbose: Notify me via terminal.
    @type verbose: boolean.
    @return: boolean
    """
    for filepath in sorted(glob.glob(fitsfiles)):
        pysex.run(filepath, conf_args={'DETECT_THRESH':detect_thresh, 'ANALYSIS_THRESH':analysis_thresh, 'DETECT_MINAREA':detect_minarea, 'SATUR_LEVEL':satur_level, 
        'GAIN':gain ,'DEBLEND_NTHRESH':deblend_nthresh, 'DEBLEND_MINCONT':deblend_mincont, 'PIXEL_SCALE':pixel_scale, 'SEEING_FWHM':seeing_fwhm, 
        "PHOT_AUTOPARAMS":phot_autoparams, "BACK_SIZE":back_size, "BACK_FILTERSIZE":back_filtersize, "FILTER":"Y", 'VERBOSE_TYPE':'NORMAL' if verbose else 'QUIET'},
        params=['FLAGS', 'X_IMAGE', 'Y_IMAGE', 'FLUX_AUTO', 'BACKGROUND', 'FWHM_IMAGE', 'ELONGATION', 'FLUXERR_AUTO'],
        rerun=rerun, keepcat=keepcat, catdir=catdir)
    return True

def makemastercat(catdir):
    """
    Reads all catalogue file under catalogue directory and extracts all elements to "one catalogue file" named as "mastercat.txt".
    
    @param catdir: The target directory which contains all catalogue files.
    @type catdir: Directory object.
                
    """
    
    if os.path.exists(catdir):
        if os.path.isfile("%s/mastercat.cat" %(catdir)):
            print "%s/mastercat.cat" %(catdir)
            os.remove("%s/mastercat.cat" %(catdir))
        catfiles = glob.glob("%s/*cat" %(catdir))
        with open("%s/mastercat.cat" %(catdir), "a") as outfile:
            for f in catfiles:
                e_catfile = os.path.splitext(f)[1]
                if e_catfile == ".pysexcat":
                    objectcat = np.genfromtxt(f, delimiter=None, comments='#')                                      
                np.savetxt(outfile, objectcat, delimiter=' ')
    return True

def align(fitsfiles, refimage, outdir):
    """
    FITS file align for alipy.

    @param fitsfiles: FITS images which will be aligned.
    @type fitsfiles: string.
    @param refimage: Reference FITS image.
    @type refimage: file.  
    @param outdir: Out directory for aligned FITS images.
    @type outdir: Directory.
    @return: boolean              
    """   
    # Minimal example of how to align images :
    images_to_align = sorted(glob.glob(fitsfiles))

    identifications = alipy.ident.run(refimage, images_to_align, visu=False, sexkeepcat=True)
    # That's it !
    # Put visu=True to get visualizations in form of png files (nice but much slower)
    # On multi-extension data, you will want to specify the hdu (see API doc).
    
    # The output is a list of Identification objects, which contain the transforms :       
    outputshape = alipy.align.shape(refimage)
    # This is simply a tuple (width, height)... you could specify any other shape.
    
    for id in identifications:
            if id.ok == True:
                    # Variant 1, using only scipy and the simple affine transorm :
                    alipy.align.affineremap(id.ukn.filepath, id.trans, shape=outputshape, outdir=outdir, makepng=False)
                    # By default, the aligned images are written into a directory "alipy_out".
    return True

        
        