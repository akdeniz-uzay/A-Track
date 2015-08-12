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
    def fits2png(self, fitsfile, outdir, movingobjectsinfile = None, movingobjects = None, basepar = 1):
        """
        f2n is a tiny python module to transfrom FITS images into PNG files, built around pyfits and PIL. 
        I tend to include these PNG files into html pages for fast visualization, that's why the module is called "fits to net".
        More information: http://obswww.unige.ch/~tewes/f2n_dot_py

        @param fitsfile: FITS file.
        @type fitsfile: File object.
        @param outdir: PNG file out directory.
        @type outdir: Directory object.
        @param movingobjectsinfile: numpy array of moving objects in one file.
        @type movingobjectsinfile: array.
        @param movingobjects: numpy array of all detected moving objects.
        @type movingobjects: array.
        @param basepar: lenght of line.
        @type basepar: float.
        @return boolean
        """
        try:
            import f2n
        except ImportError:
            print "Couldn't import f2n -- install it !"
            return
        myimage = f2n.fromfits(fitsfile, verbose=False)
        myimage.setzscale("auto", "auto")
        myimage.makepilimage("log", negative = False)

        try:
            if movingobjectsinfile.size:
                for i in xrange(len(movingobjectsinfile)):
                    linepoints = movingobjects[movingobjects[:, 6].astype(int) == int(movingobjectsinfile[i][6])]
                    linelenght = math.sqrt((linepoints[len(linepoints)-1][3] - linepoints[0][3])**2 + \
                                           (linepoints[len(linepoints)-1][2] - linepoints[0][2])**2)
                    if linelenght < basepar * 2:
                        rectcolour = (255, 0, 0)
                        print linelenght
                    else:
                        rectcolour = (0,255,0)
                    
                    myimage.drawrectangle(movingobjectsinfile[i][2] - 10, movingobjectsinfile[i][2] + 10, movingobjectsinfile[i][3] - 10,\
                                          movingobjectsinfile[i][3] + 10, colour = rectcolour, label="%s" %(int(movingobjectsinfile[i][6])))
        except AttributeError:
            pass
        myimage.writetitle(os.path.basename(fitsfile))
        if not os.path.isdir(outdir):
                os.makedirs(outdir)
        base_fitsfile = os.path.basename(fitsfile)
        h_fitsfile, e_fitsfile = base_fitsfile.split(".")
        try:
            hdulist = pyfits.open(fitsfile)
            obsdate = hdulist[0].header['date-obs']
            myimage.writeinfo([obsdate], colour=(255,100,0))
        except:
            pass
        myimage.tonet(os.path.join(outdir, h_fitsfile + ".png"))
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

            catfile = os.path.basename(catfile)
            h_catfile, e_catfile = catfile.split(".")
            
            if e_catfile == "pysexcat":
                print '\033[1;34mDetecting stars on %s!\033[0m' %(catfile)
                coordinate = os.popen("cat %s|grep -v '#'|awk '{print $2,$3}'" %(catfile))
            elif e_catfile == "txt":
                print '\033[1;34mDetecting stars on %s!\033[0m' %(catfile)
                coordinate = os.popen("cat %s|tail -n +2|awk -F' *, *' '{print $2,$3}'" %(catfile))
            elif e_catfile == "cat":
                print '\033[1;34mDetecting stars on %s!\033[0m' %(catfile)
                coordinate = os.popen("cat %s|tail -n +2|awk '{print $2,$3}'" %(catfile)) 
            counter = 0
            for line in coordinate.readlines():
                counter += 1
                line = line.replace("\n", "")
                x_coor,  y_coor = line.split(" ")
                d.set('regions', 'image; circle(%s,%s,5) # color=red text={%s}' %(x_coor,  y_coor, counter))
            print '\033[1;34mDetecting stars job is completed!\033[0m'
        except:
            print '\033[1;31mSomething went wrong with DS9!\033[0m'
            return False
            raise SystemExit
        return True