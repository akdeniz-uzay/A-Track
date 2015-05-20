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
    
    def catalogue(self, star_cat, target_folder):
        """
        Reads given ordered (corrected) coordinate file plot stars.
        @param star_cat: Ordered (corrected) star catalogue.
        @type star_cat: Text file object..
                    
        """
        #catxy = pd.read_csv(star_cat, sep=",", names=["ref_x", "ref_y"], header=0)
        catxy = np.genfromtxt(star_cat, dtype='float32', delimiter=' ', skip_header=1)
        plt.figure(figsize=(10, 10))
        if catxy.size:
            plt.scatter(catxy[:,1], catxy[:,2], s=2.0, color="black")
            #plt.plot(kind="scatter", x = "ref_x", y = "ref_y", xlim=, ylim=, fontsize=12, figsize=(10, 10))

        starcatfile = os.path.basename(star_cat)
        h_starcatfile, e_starcatfile = starcatfile.split(".")
    
        if os.path.exists(target_folder):
            pass
        else:
            os.mkdir(target_folder)
        if catxy.size:
            plt.xlim(0, 2048)
            plt.ylim(0, 2048)
            plt.xlabel("ref x")
            plt.ylabel("ref y")
            plt.title("Detected %s stray objects on %s" % (len(catxy), h_starcatfile))
            ax = plt.gca()
            ax.set_aspect('equal', 'datalim')
            plt.savefig("%s/%s.png" %(target_folder, h_starcatfile))
            plt.close()
        else:
            print "No objects detected on %s." %(starcatfile)
        return


    def plotallcat(self, ordered_cats, target_folder):
        """
        Reads and plots all ordered (corrected) coordinate files under given directory.
        
        @param ordered_cats: Ordered coordinate folder.
        @type stray_cats: Directory object.
                    
        """      
        for catfile in sorted(glob.glob("%s/*affineremap.txt" %(ordered_cats))):
            self.catalogue(catfile, target_folder)
            print "Plotted all detected objects on: %s." %(os.path.basename(catfile))
        return

    def plotallobjects(self, catdir, target_folder):
        """
        Reads all catalogue files under given ordered catalogue folder to draw all objects in one figure.
        
        @param ordered_cats: Ordered coordinate folder.
        @type stray_cats: Directory object.
                    
        """      
        starcat = sorted(glob.glob("%s/*affineremap.cat" %(catdir)))
        #onecatlist = pd.DataFrame(columns=["ref_x", "ref_y"])
        onecatlist = []
        
        for objctlist in starcat:
            objtcat = np.genfromtxt(objctlist, dtype='float32', delimiter=' ', skip_header=1)
            onecatlist = onecatlist.append(objtcat)
        
        #onecatlist.plot(kind="scatter", x = "ref_x", y = "ref_y", xlim=(0, 2048), ylim=(0, 2048), fontsize=12, figsize=(10, 10))          
        plt.figure(figsize=(10, 10))
        plt.scatter(onecatlist[:,1], onecatlist[:,2], s=2.0, color="blue")
   
        if os.path.exists(target_folder):
            pass
        else:
            os.mkdir(target_folder)
        plt.xlabel("ref x")
        plt.ylabel("ref y")
        plt.title("Detected %s objects." % (len(onecatlist)))
        plt.xlim(0, 2048)
        plt.ylim(0, 2048)
        ax = plt.gca()
        ax.set_aspect('equal', 'datalim')   
        plt.savefig("%s/allobjects.png" %(target_folder))
        plt.close()
        return

    def plot(self, coorlist, output_figure = None):
        """
        Plots data (x, y) object
        @param coorlist: Array data (x, y).
        @type coorlist: Array
        @param output_figure: PNG file.
        @type output_figure: Directory or file object.
        """
        #coorlist.plot(kind="scatter", x = "ref_x", y = "ref_y", xlim=(0, 2048), ylim=(0, 2048), fontsize=12, figsize=(10, 10))
        plt.xlabel("ref x")
        plt.ylabel("ref y")
        plt.title("Detected %s objects." %(len(coorlist)))
        print coorlist[:,2]
        print coorlist[:,3]
        plt.scatter(coorlist[:,2], coorlist[:,3], s=coorlist[:,4]/1000, color="red")
        plt.xlim(0, 2048)
        plt.ylim(0, 2048)
        ax = plt.gca()
        ax.set_aspect('equal', 'datalim')

        if output_figure != "-nosave" and output_figure != "-noplot":
            plt.savefig("%s" %(output_figure))
            plt.close()
        elif output_figure == "-nosave":
            plt.show()
            plt.close()
        elif output_figure == "-noplot":
            pass
        return

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
                    myimage.drawrectangle(datalxy[i][2] - 10, datalxy[i][3] + 10, datalxy[i][2] - 10, datalxy[i][3] + 10, colour=(0,255,0), label="%s" %(int(datalxy[i][3])))
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
