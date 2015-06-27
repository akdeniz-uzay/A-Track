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
    from plot import *
except ImportError:
    print "Can not load plot. Do you have plot.py?"
    raise SystemExit

try:
    from detect import *
except ImportError:
    print "Can not load detect. Do you have detect.py?"
    raise SystemExit

try:
    import cosmics
except ImportError:
	print("Can not load cosmics")
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
        catfiles = glob.glob("%s/*.cat" %(catdir))
        with open("%s/starcat.cat" %(catdir), "a") as outfile:
            for f in catfiles:
                objectcat = np.genfromtxt(f, delimiter=' ', skip_header=1)
                np.savetxt(outfile, objectcat, delimiter=' ')
    return True
                    


def cleancosmics(image, odir, gain=2.2, readnoise=10.0, sigclip = 5.0, sigfrac = 0.3, objlim = 5.0, maxiter = 4):
    """
    Detect and clean cosmic ray hits on images (numpy arrays or FITS), using scipy, and based on Pieter van Dokkum's L.A.Cosmic algorithm.
    @sigclip: increase this if you detect cosmics where there are none. Default is 5.0, a good value for earth-bound images. objlim : increase this if normal stars are detected as cosmics. Default is 5.0, a good value for earth-bound images.
    Constructor of the cosmic class, takes a 2D numpy array of your image as main argument. sigclip : laplacian-to-noise limit for cosmic ray detection objlim : minimum contrast between laplacian image and fine structure image. Use 5.0 if your image is undersampled, HST, ...
    @satlevel: if we find agglomerations of pixels above this level, we consider it to be a saturated star and do not try to correct and pixels around it. A negative satlevel skips this feature.
    pssl is the previously subtracted sky level!
    @real gain = 1.8 # gain (electrons/ADU) (0=unknown) real readn = 6.5 # read noise (electrons) (0=unknown) ##gain0 string statsec = "*,*" # section to use for automatic computation of gain real skyval = 0. # sky level that has been subtracted (ADU) real sigclip = 3.0 # detection limit for cosmic rays (sigma) real sigfrac = 0.5 # fractional detection limit for neighbouring pixels real objlim = 3.0 # contrast limit between CR and underlying object int niter = 1 # maximum number of iterations
    More information: http://obswww.unige.ch/~tewes/cosmics_dot_py/    
    """
    # Read the FITS :
    array, header = cosmics.fromfits(image)
    # array is a 2D numpy array
    
    # Build the object :
    c = cosmics.cosmicsimage(array, gain, readnoise, sigclip, sigfrac, objlim)
    # There are other options, check the manual...
    
    # Run the full artillery :
    c.run(maxiter)
    
    impath = os.path.basename(image)
    h_impath, e_impath = impath.split(".")    
    # Write the cleaned image into a new FITS file, conserving the original header :
    cosmics.tofits("%s/%s_clean.fits" %(odir, h_impath), c.cleanarray, header)

if __name__ == "__main__":
    start_time = time.time()
    # Reads FITS file and ident/align stars
    if sys.argv[1] == "-ri -se":
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
        
    elif sys.argv[1] == "-ra":
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
        for catfile in sorted(glob.glob("%s/*affineremap.cat" %(sys.argv[2]))):
            detect = Detect()
            detect.detectstrayobjects(catfile, "%s/starcat.cat" %(sys.argv[2]), sys.argv[3])
            print "Saved all detected stray objects to: %s/%s." %(sys.argv[2], os.path.basename(catfile))
        print "Candidate objects in catalogues has extracted."
        print "Elapsed time: %s" %(time.time() - start_time)
        #except:
        #    print "Usage error!"
        #    print "Usage: python asterotrek.py -mods <ordered_cats_folder> <target_folder>"
        #    raise SystemExit    
    # Plot objects in catalogue file    
    elif sys.argv[1] == "-plt":
        """
        Plot objects in given catalogue (ordered) file.
        Usage: python asterotrek.py -plt <catalogue_file> <target_folder>      		
        """
        try:
            plotCat = Plot()
            plotCat.catalogue(sys.argv[2], sys.argv[3])
            print "Given catalogue file (%s) ploted." %(sys.argv[2])
            print "Elapsed time: %s" %(time.time() - start_time)
        except:
            print "Usage error!"
            print "Usage: python asterotrek.py -plt <catalogue_file> <target_folder>"
            raise SystemExit 
            
    # Plot objects in catalogue folder 
    elif sys.argv[1] == "-plts":
        """
        Plot each catalogue files in given catalogue (ordered) folder.
        Usage: python asterotrek.py -plts <ordered_cat_folder> <target_folder>    		
        """
        try:
            print "Please wait until processing is complete."
            plotCat = Plot()
            plotCat.plotallcat(sys.argv[2], sys.argv[3])
            print "All catalogue files ploted into %s." %(sys.argv[3])
            print "Elapsed time: %s" %(time.time() - start_time)
        except:
            print "Usage error!"
            print "Usage: python asterotrek.py -plts <ordered_cat_folder> <target_folder>"
            raise SystemExit
    
    # Detect lines. 
    elif sys.argv[1] == "-dl":
        """
        Detect lines from the stray cats.
        Usage: python asterotrek.py -dl <ordered_cat_folder> <detectedlines.png>   		
        """
        #try:
        print "Please wait until processing is complete."
        detectlines = Detect()
        detectlines.detectlines(sys.argv[2], sys.argv[3], sys.argv[4])
        print "Line detection process is completed."
        print "Elapsed time: %s" %(time.time() - start_time)
        #except:
        #    print "Usage error!"
        #    print "Usage: python asterotrek.py -dl <ordered_cat_folder> <detectedlines.png>"
        #    raise SystemExit
            
    # Plot all objects to one matplotlib figure
    elif sys.argv[1] == "-pltone":
        """
        Plot all objects in given catalogue (ordered) folder to one figure.
        Usage: python asterotrek.py -pltone <ordered_cat_folder> <target_folder>    		
        """
        try:
            plotCat = Plot()
            plotCat.plotallobjects(sys.argv[2], sys.argv[3])
            print "All catalogue files ploted into %s/allobjects.png." %(sys.argv[3])
            print "Elapsed time: %s" %(time.time() - start_time)
        except:
            print "Usage error!"
            print "Usage: python asterotrek.py -pltone <ordered_cat_folder> <target_folder>"
            raise SystemExit
    elif sys.argv[1] == "-cc":
        """
        Detect and clean cosmic ray hits on images (numpy arrays or FITS), using scipy, and based on Pieter van Dokkum’s L.A.Cosmic algorithm.
        Usage: python asterotrek.py -cc <fitsimage(s)> <target_folder>    		
        """
        try:
            print "Please wait until processing is complete."
            if os.path.isdir(sys.argv[2]):
                for fitsimage in sorted(glob.glob("%s/*.fits" %(sys.argv[2]))):
                    cleancosmics(fitsimage, sys.argv[3])
            elif os.path.isfile(sys.argv[2]):
                cleancosmics(sys.argv[2], sys.argv[3])
            print "Cosmic cleaner is done."
            print "Elapsed time: %s" %(time.time() - start_time)
        except:
            print "Usage error!"
            print "Usage: python asterotrek.py -cc <fitsimage(s)> <target_folder>" 
            raise SystemExit
    
    elif sys.argv[1] == "-fits2png" and len(sys.argv) == 5:
        """
        Converts FITS images into PNG files with detected objects.
        Usage: python asterotrek.py -fits2png <stray_cats> <fitsimage(s)> <target_folder>    		
        """
        #try:
        print "Please wait until processing is complete."
        f2n = Plot()
        detectlines = Detect()
        datalxy = detectlines.detectlines(sys.argv[3], sys.argv[2], output_figure=None)
        
        if os.path.isdir(sys.argv[3]):
            for i, fitsimage in enumerate(sorted(glob.glob("%s/*.fits" %(sys.argv[3])))):
                print sys.argv[4]
                print fitsimage
                print i
                datacat = datalxy[datalxy[:, 0].astype(int) == i]
                f2n.fits2png(fitsimage, sys.argv[4], datacat)
                print "%s converted into %s" %(fitsimage, sys.argv[4])
        elif os.path.isfile(sys.argv[3]):
            f2n.fits2png(sys.argv[3], sys.argv[4], datacat)
            print "%s converted into %." %(sys.argv[3], sys.argv[4])
        print "Plotted all detected objects into PNG files."
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
        f2n = Plot()
        
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
        f2p = Plot()
        
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
        p2ds9 = Plot()
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
        try:
            print "Please wait until processing is complete."
            os.popen("convert -delay 20 -loop 0 %s/*.png %s/%s.gif" %(sys.argv[2], sys.argv[2], sys.argv[3]))
            print "Elapsed time: %s" %(time.time() - start_time)
        except:
            print "Usage error!"
            print "python asterotrek.py -makegif <PNG(s)> <target_folder>" 
            raise SystemExit 