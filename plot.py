# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 18:33:56 2015

@author: ykilic
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import pyfits

class Plot:
    """
    MOD's plotting class.
                
    """
    def fits2png(self, alifilepath, outdir, datalxy = None):
        """
        f2n is a tiny python module to transfrom FITS images into PNG files, built around pyfits and PIL. I tend to include these PNG files into html pages for fast visualization, that's why the module is called "fits to net".
        More information: http://obswww.unige.ch/~tewes/f2n_dot_py

        @param alifilepath: FITS file.
        @type alifilepath: File object.
        @param outdir: PNG file out directory.
        @type outdir: Directory object.
        """
        try:
            import f2n
        except ImportError:
            print "Couldn't import f2n -- install it !"
            return
        myimage = f2n.fromfits(alifilepath, verbose=False)
        myimage.setzscale("auto", "auto")
        myimage.makepilimage("log", negative = False)

        try:
            if datalxy.size:
                for i in xrange(len(datalxy)):
                    myimage.drawrectangle(datalxy[i][2] - 10, datalxy[i][2] + 10, datalxy[i][3] - 10, datalxy[i][3] + 10, colour=(0,255,0), label="%s" %(int(datalxy[i][0])))
        except AttributeError:
            pass
        myimage.writetitle(os.path.basename(alifilepath))
        if not os.path.isdir(outdir):
                os.makedirs(outdir)
        base_alifilepath = os.path.basename(alifilepath)
        h_alifilepath, e_alifilepath = base_alifilepath.split(".")
        try:
            hdulist = pyfits.open(alifilepath)
            obsdate = hdulist[0].header['date-obs']
            myimage.writeinfo([obsdate], colour=(255,100,0))
        except:
            pass
        myimage.tonet(os.path.join(outdir, h_alifilepath + ".png"))
        return

    def fits2pnm(self, fits_path, outdir):
        """
        f2n is a tiny python module to transfrom FITS images into PNG files, built around pyfits and PIL. I tend to include these PNG files into html pages for fast visualization, that's why the module is called "fits to net".
        More information: http://obswww.unige.ch/~tewes/f2n_dot_py

        @param alifilepath: FITS file.
        @type alifilepath: File object.
        @param outdir: PNG file out directory.
        @type outdir: Directory object.
        """
        astrometry = "/usr/local/astrometry/bin/"
        fitsfiles = sorted(glob.glob("%s/*.fit?" %(fits_path)))
    
        for filepath in fitsfiles:
            base_filepath = os.path.basename(filepath)
            h_filepath, e_filepath = base_filepath.split(".")
            if not os.path.isdir(outdir):
                    os.makedirs(outdir)                 
            os.popen("%san-fitstopnm -i %s -o %s/%s.pnm" %(astrometry, filepath, outdir, h_filepath))
        return True

    def plot2ds9(self, fits_path, cat_path):
        """
        Descriptions will be provided.
        """
        import os
        try:
            import ds9 as ds
        except:
        	print("pyds9'? http://hea-www.harvard.edu/RD/pyds9/")
        	raise SystemExit  

        print '\033[1;32mNow, openning DS9!\033[0m'
        try: 
            os.popen("kill -9  $(pidof ds9)")
            d = ds.ds9()
            d.set("file %s" %(fits_path))
            #Zoom to fit
            d.set('zoom to fit')
            #Scale to zscales
            d.set('scale zscale')
            #Getting Params 
        except:
            print '\033[1;31mSomething went wrong with DS9!\033[0m'
        
        catfile = os.path.basename(cat_path)
        h_catfile, e_catfile = catfile.split(".")
        
        if e_catfile == "pysexcat":
            print '\033[1;34mDetecting stars on %s!\033[0m' %(cat_path)
            coordinate = os.popen("cat %s|grep -v '#'|awk '{print $2,$3}'" %(cat_path))
        elif e_catfile == "txt":
            print '\033[1;34mDetecting stars on %s!\033[0m' %(cat_path)
            coordinate = os.popen("cat %s|tail -n +2|awk -F' *, *' '{print $2,$3}'" %(cat_path))
        elif e_catfile == "cat":
            print '\033[1;34mDetecting stars on %s!\033[0m' %(cat_path)
            coordinate = os.popen("cat %s|tail -n +2|awk '{print $2,$3}'" %(cat_path)) 
        
        counter = 0
        for line in coordinate.readlines():
            counter += 1
            line = line.replace("\n", "")
            x_coor,  y_coor = line.split(" ")
            d.set('regions', 'image; circle(%s,%s,5) # color=red text={%s}' %(x_coor,  y_coor, counter))
        print '\033[1;34mDetecting stars job is completed!\033[0m'
        return True