# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 18:33:56 2015

@author: ykilic
"""


import os
import math
import glob

try:
    import pyfits
except ImportError:
    print "Did you install pyfits?"
    raise SystemExit

try:
    import matplotlib.pyplot as plt
except ImportError:
    print "Did you install matplotlib?"
    raise SystemExit

try:
    import numpy as np
except ImportError:
    print "Did you install pandas?"
    raise SystemExit

class Plot:
    """
    MOD's plotting class.
                
    """
    def fits2png(self, fitsfile, outdir, movingobjects = None, skymotion_limit = 0.07):
        """
        f2n is a tiny python module to transfrom FITS images into PNG files, built around pyfits and PIL. 
        I tend to include these PNG files into html pages for fast visualization, that's why the module is called "fits to net".
        More information: http://obswww.unige.ch/~tewes/f2n_dot_py

        @param fitsfile: FITS file.
        @type fitsfile: File object.
        @param outdir: PNG file out directory.
        @type outdir: Directory object.
        @param movingobjects: numpy array of moving objects in one file.
        @type movingobjects: array.
        @param skymotion_limit: sky velocity limit of object.
        @type skymotion_limit: float.
        @return boolean
        """
        try:
            import f2n
        except ImportError:
            print "Couldn't import f2n -- install it !"
            return
        imframe = f2n.fromfits(fitsfile, verbose=False)
        imframe.setzscale("auto", "auto")
        imframe.makepilimage("log", negative = False)
        
        try:
            if movingobjects.size:
                for i in xrange(len(movingobjects)):
                    if movingobjects[i][7] >= skymotion_limit:
                        #green
                        aperture_colour = (0, 255, 0)
                    else:
                        #red
                        aperture_colour = (255, 0, 0)
                    imframe.drawcircle(movingobjects[i][2], movingobjects[i][3], r = 10, colour = aperture_colour, 
                                       label="%s" %(int(movingobjects[i][6])))
        except AttributeError:
            pass

        imframe.writetitle(os.path.basename(fitsfile))
        if not os.path.isdir(outdir):
                os.makedirs(outdir)
        base_fitsfile = os.path.basename(fitsfile)
        h_fitsfile, e_fitsfile = base_fitsfile.split(".")
        try:
            hdulist = pyfits.open(fitsfile)
            obsdate = hdulist[0].header['date-obs']
            imframe.writeinfo([obsdate], colour=(255,100,0))
        except:
            pass
        imframe.tonet(os.path.join(outdir, h_fitsfile + ".png"))
        return True

    def plot2ds9(self, fitsfile, catfile):
        """
        Plots objects in catalogue file into DS9.
        @param fitsfile: FITS file.
        @type fitsfile: File object.
        @param catfile: Catalogue file.
        @type catfile: File object.
        @return boolean
        """
        import os
        try:
            import pyds9 as ds
        except:
            print("pyds9'? http://hea-www.harvard.edu/RD/pyds9/")
            raise SystemExit

        print '\033[1;32mNow, openning DS9!\033[0m'
        try:
            d = ds.DS9()
            d.set("file %s" %(fitsfile))
            #Zoom to fit
            d.set('zoom to fit')
            #Scale to zscales
            d.set('scale zscale')
            #Getting Params

            h_catfile, e_catfile = catfile.split(".")
            
            if e_catfile == "pysexcat":
                print '\033[1;34mDetecting stars on %s!\033[0m' %(catfile)
                coordinate = np.genfromtxt(catfile, delimiter=None, comments='#')[:,[1,2]]
            elif e_catfile == "txt":
                print '\033[1;34mDetecting stars on %s!\033[0m' %(catfile)
                coordinate = np.genfromtxt(catfile, delimiter=",", comments='#',skip_header=1)[:,[1,2]]
                 
            for id, coor in enumerate(coordinate):
                x_coor,  y_coor = coor[0], coor[1]
                d.set('regions', 'image; circle(%s,%s,5) # color=red text={%s}' %(x_coor,  y_coor, id))
            print '\033[1;34mDetecting stars job is completed!\033[0m'
        except:
            print '\033[1;31mSomething went wrong with DS9!\033[0m'
            return False
            raise SystemExit
        return True