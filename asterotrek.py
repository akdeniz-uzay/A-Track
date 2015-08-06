# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 13:26:22 2015

@author: ykilic
"""

try:
    import asteractor
except ImportError:
    print "Can not load asteractor. Do you have asteractor.py?"
    raise SystemExit

try:
    import glob
except ImportError:
    print "Did you install glob?"
    raise SystemExit

try:
    import plot as plt
except ImportError:
    print "Can not load plot. Do you have plot.py?"
    raise SystemExit

try:
    import detect as dt
except ImportError:
    print "Can not load detect. Do you have detect.py?"
    raise SystemExit

try:
    import numpy as np
except ImportError:
    print "Did you install numpy?"
    raise SystemExit

import sys, os, time


def makestarcat(catdir):
    """
    Reads all coordinate file under catalogue directory and extracts all elements to "one catalogue file" named as "starcat.txt".
    
    @param catdir: The target directory which contains all corrected(readeble) coordinate files.
    @type catdir: Directory object.
        		
    """
    
    if os.path.exists(catdir):
        if os.path.isfile("%s/starcat.cat" %(catdir)):
            print "%s/starcat.cat" %(catdir)
            os.remove("%s/starcat.cat" %(catdir))
        catfiles = glob.glob("%s/*cat" %(catdir))
        with open("%s/starcat.cat" %(catdir), "a") as outfile:
            for f in catfiles:
                h_catfile, e_catfile = f.split(".")
                if e_catfile == "cat":
                    objectcat = np.genfromtxt(f, delimiter=None, comments='#', skip_header=1)
                elif e_catfile == "pysexcat":
                    objectcat = np.genfromtxt(f, delimiter=None, comments='#')                                      
                np.savetxt(outfile, objectcat, delimiter=' ')
    return True

if __name__ == "__main__":
    start_time = time.time()
    # Reads FITS file and ident/align stars
    if sys.argv[1] == "-sextractor":
        """
        Ident stars on all FITS images according to reference image.
        Use this option for you have already aligned images.
        Usage: python asterotrek.py -ri <fitsfiles> <catdir>
            		
        """
        #try:
        asteractor.makecat(sys.argv[2], sys.argv[3])
        print "Please wait until processing is complete."
        print "Identification process is completed."
        print "Elapsed time: %s" %(time.time() - start_time)
        #except:
        #    print "Usage error!"
        #    print "Usage: python asterotrek.py -ri <fitsfiles> <catdir>" 
        #    raise SystemExit
    elif sys.argv[1] == "-image2xy":
        """
        Ident stars on all FITS images according to reference image.
        Use this option for you have already aligned images.
        Usage: python asterotrek.py -ri <fitsfiles> <catdir>
            		
        """
        #try:
        asteractor.image2xy(sys.argv[2], sys.argv[3])
        print "Please wait until processing is complete."
        print "Identification process is completed."
        print "Elapsed time: %s" %(time.time() - start_time)
        #except:
        #    print "Usage error!"
        #    print "Usage: python asterotrek.py -ri <fitsfiles> <catdir>" 
        #    raise SystemExit
        
    elif sys.argv[1] == "-align":
        """
        Align stars on all FITS images according to reference image.
        Usage: python asterotrek.py -ra <images_to_align> <reference_img.fits> <alipy_out>
            		
        """   
        #try:
        print "Please wait until processing is complete."
        asteractor.align(sys.argv[2], sys.argv[3], sys.argv[4])
        print "Identification and align processes are completed."
        print "Elapsed time: %s" %(time.time() - start_time)
        #except:
        #    print "Usage error!"
        #    print "Usage: python asterotrek.py -ra <images_to_align> <reference_img.fits> <alipy_out>"
        #    raise SystemExit
    # Create readable catalogue file for comparison and check stars    
    elif sys.argv[1] == "-msc":
        """
        Makes stars cats as one file.
        Usage: python asterotrek.py -moc <ordered_cats_folder>
            		
        """
        #try:
        makestarcat(sys.argv[2])
        print "Making all in one star catalogue process is completed."
        print "Elapsed time: %s" %(time.time() - start_time)
        #except:
        #    print "Usage error!"
        #    print "Usage: python asterotrek.py -moc <ordered_cats_folder>"
        #    raise SystemExit
    # Detect stray objects in given catalogue folder
    elif sys.argv[1] == "-dso":
        """
        Detects all stray stars in given catalogue folder.
        Usage: python asterotrek.py -mods <ordered_cats_folder> <target_folder>
            		
        """
        #try:
        print "Please wait until processing is complete."
        for catfile in sorted(glob.glob("%s/*affineremap.*cat" %(sys.argv[2]))):
            detect = dt.Detect()
            detect.detectstrayobjects(catfile, "%s/starcat.cat" %(sys.argv[2]), sys.argv[3])
            print "Saved all detected stray objects to: %s/%s." %(sys.argv[2], os.path.basename(catfile))
        print "Candidate objects in catalogues has extracted."
        print "Elapsed time: %s" %(time.time() - start_time)
        #except:
        #    print "Usage error!"
        #    print "Usage: python asterotrek.py -mods <ordered_cats_folder> <target_folder>"
        #    raise SystemExit    

    # Detect lines. 
    elif sys.argv[1] == "-dl":
        """
        Detect lines from the stray cats.
        Usage: python asterotrek.py -dl <ordered_cat_folder> <detectedlines.png>   		
        """
        #try:
        print "Please wait until processing is complete."

        detectlines = dt.Detect()
        if len(sys.argv) == 5:
            detectlines.detectlines(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            detectlines.detectlines(sys.argv[2], sys.argv[3])
        print "Line detection process is completed."
        print "Elapsed time: %s" %(time.time() - start_time)
        #except:
        #    print "Usage error!"
        #    print "Usage: python asterotrek.py -dl <ordered_cat_folder> <detectedlines.png>"
        #    raise SystemExit

    elif sys.argv[1] == "-mdl":

        print "Please wait until processing is complete (multiprocessing)."
        detectlines = dt.Detect()
        detectlines.multilinedetector(sys.argv[2], sys.argv[3])

        print "Line detection process is completed."
        print "Elapsed time: %s" %(time.time() - start_time)

    elif sys.argv[1] == "-fits2png" and len(sys.argv) == 5:
        """
        Converts FITS images into PNG files with detected objects.
        Usage: python asterotrek.py -fits2png <stray_cats> <fitsimage(s)> <target_folder>    		
        """
        #try:
        print "Please wait until processing is complete."
        f2n = plt.Plot()
        detectlines = dt.Detect()
        datalxy = detectlines.multilinedetector(sys.argv[2], sys.argv[3])

        if len(datalxy) != 0:
            if os.path.isdir(sys.argv[3]):
                for i, fitsimage in enumerate(sorted(glob.glob("%s/*.fits" %(sys.argv[3])))):
                    print sys.argv[4]
                    print str(i) + " " + fitsimage
                    datacat = datalxy[datalxy[:, 0].astype(int) == i]
                    f2n.fits2png(fitsimage, sys.argv[4], datacat)
                    print "%s converted into %s" %(fitsimage, sys.argv[4])
            elif os.path.isfile(sys.argv[3]):
                f2n.fits2png(sys.argv[3], sys.argv[4], datacat)
                print "%s converted into %." %(sys.argv[3], sys.argv[4])
            print "Plotted all detected objects into PNG files."
        else:
            print "No line detected!!!!"
        print "Elapsed time: %s" %(time.time() - start_time)
        #except:
        #    print "Usage error!"
        #    print "Usage: python asterotrek.py -fits2png <stray_cats> <fitsimage(s)> <target_folder>" 
        #    raise SystemExit
            
    elif sys.argv[1] == "-fits2png" and len(sys.argv) == 4:
        """
        Converts FITS images into PNG files.
        Usage: python asterotrek.py -fits2png <fitsimage(s)> <target_folder>    		
        """
        #try:
        print "Please wait until processing is complete."
        f2n = plt.Plot()
        
        if os.path.isdir(sys.argv[2]):
            for fitsimage in sorted(glob.glob("%s/*.fits" %(sys.argv[2]))):
                f2n.fits2png(fitsimage, sys.argv[3])
                print "%s converted into %s." %(fitsimage, sys.argv[3])
        elif os.path.isfile(sys.argv[2]):
            f2n.fits2png(sys.argv[2], sys.argv[3])
            print "%s converted into %." %(sys.argv[2], sys.argv[3])
        print "Converted all FITS files to PNG files."
        print "Elapsed time: %s" %(time.time() - start_time)
        #except:
        #    print "Usage error!"
        #    print "Usage: python asterotrek.py -fits2png <fitsimage(s)> <target_folder>" 
        #    raise SystemExit
    elif sys.argv[1] == "-fits2pnm" and len(sys.argv) == 4:
        """
        Converts FITS images into PNM files.
        Usage: python asterotrek.py -fits2png <fitsimage(s)> <target_folder>    		
        """
        #try:
        print "Please wait until processing is complete."
        f2p = plt.Plot()
        
        if os.path.isdir(sys.argv[2]):
            for fitsimage in sorted(glob.glob(sys.argv[2])):
                f2p.fits2pnm(fitsimage, sys.argv[3])
                print "%s converted into %s." %(fitsimage, sys.argv[3])
        elif os.path.isfile(sys.argv[2]):
            f2p.fits2pnm(sys.argv[2], sys.argv[3])
            print "%s converted into %." %(sys.argv[2], sys.argv[3])
        print "Converted all FITS files to PNG files."
        print "Elapsed time: %s" %(time.time() - start_time)
        #except:
        #    print "Usage error!"
        #    print "Usage: python asterotrek.py -fits2png <fitsimage(s)> <target_folder>" 
        #    raise SystemExit
    elif sys.argv[1] == "-plot2ds9" and len(sys.argv) == 4:
        """
        Plots catalogue files into ds9.
        Usage: python asterotrek.py -plot2ds9 <fitsimage> <catfile>    		
        """
        #try:
        print "Please wait until processing is complete."
        p2ds9 = plt.Plot()
        p2ds9.plot2ds9(sys.argv[2], sys.argv[3])
        print "Elapsed time: %s" %(time.time() - start_time)
        #except:
        #    print "Usage error!"
        #    print "Usage: python asterotrek.py -fits2png <fitsimage(s)> <target_folder>" 
        #    raise SystemExit
    elif sys.argv[1] == "-makegif":
        """
        Converts PNG images to animated GIF file.
        Usage: python asterotrek.py -makegif <PNG(s)> <target_folder>    		
        """
        #try:
        print "Please wait until processing is complete."
        os.popen("convert -delay 20 -loop 0 %s/*.png %s/%s.gif" %(sys.argv[2], sys.argv[2], sys.argv[3]))
        print "Elapsed time: %s" %(time.time() - start_time)
        #except:
        #    print "Usage error!"
        #    print "python asterotrek.py -makegif <PNG(s)> <target_folder>" 
        #    raise SystemExit 