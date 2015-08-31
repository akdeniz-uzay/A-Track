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
    import pandas as pd
except ImportError:
    print "Did you install pandas?"
    raise SystemExit

try:
    import numpy as np
except ImportError:
    print "Did you install numpy?"
    raise SystemExit

import sys, os, time


if __name__ == "__main__":
    start_time = time.time()
    # Reads FITS file and ident/align stars
    if sys.argv[1] == "-align":
        """
        Align all FITS images according to reference image.
        Usage: python asterotrek.py -align "path/*.fits" path/reference.fits path/aligned
                    
        """   
        try:
            print "Please wait until processing is complete."
            asteractor.align(sys.argv[2], sys.argv[3], sys.argv[4])
            print "Identification and align processes are completed."
            print "Elapsed time: %s min. %s sec." %(int((time.time() - start_time) / 60), "%.2f" % ((time.time() - start_time) % 60))
        except:
            print "Usage error!"
            print "Usage: python asterotrek.py -align <fitsfiles> <reference.fits> <outdir>"
            raise SystemExit

    elif sys.argv[1] == "-sextractor":
        """
        Ident stars on all FITS images according to reference catalogue image.
        Use this option for you have already aligned images.
        Usage: python asterotrek.py -sextractor "path/*.fits" path/catdir
            		
        """
        try:
            asteractor.makecat(sys.argv[2], sys.argv[3])
            print "Please wait until processing is complete."
            print "Identification process is completed."
            print "Elapsed time: %s min. %s sec." %(int((time.time() - start_time) / 60), "%.2f" % ((time.time() - start_time) % 60))
        except:
            print "Usage error!"
            print "Usage: python asterotrek.py -sextractor <fitsfiles> <catdir>" 
            raise SystemExit
  
    elif sys.argv[1] == "-makemaster":
        """
        Makes master catalogue file.
        Usage: python asterotrek.py -makemaster path/catdir	
        """
        try:
            asteractor.makemastercat(sys.argv[2])
            print "Making all in one star catalogue process is completed."
            print "Elapsed time: %s min. %s sec." %(int((time.time() - start_time) / 60), "%.2f" % ((time.time() - start_time) % 60))
        except:
            print "Usage error!"
            print "Usage: python asterotrek.py -makemaster <path/catdir>"
            raise SystemExit
        
    elif sys.argv[1] == "-xcan":
        """
        Detects candidate objects in given catalogue file.
        Usage: python asterotrek.py -xcan catalogue_file master_catalogue_file path/candidatedir
            		
        """
        #try:
        detectlines = dt.Detect()
        detectlines.detectcandidateobjects(sys.argv[2], sys.argv[3], sys.argv[4])
        print "%s: Extracting all detected candidate objects to: %s." %(sys.argv[2], sys.argv[4])
        #except:
        #    print "Usage error!"
        #    print "Usage:python asterotrek.py -xcan <catalogue_file> <master_catalogue_file> <path/candidatedir>"
        #    raise SystemExit
        
    elif sys.argv[1] == "-mxcan":
        """
        Detects all candidate objects in given catalogue folder with multi-processsing.
        Usage: python asterotrek.py -mxcan path/cats path/candidatedir
     
        """
        try:
            print "Please wait until processing is complete."
            detectlines = dt.Detect()
            detectlines.multidcos(sys.argv[2], sys.argv[3])
            print "Saved all detected candidate objects to: %s." %(sys.argv[3])
            print "Candidate objects in catalogues has extracted."
            print "Elapsed time: %s min. %s sec." %(int((time.time() - start_time) / 60), "%.2f" % ((time.time() - start_time) % 60))
        except:
            print "Usage error!"
            print "Usage: python asterotrek.py -xcan <path/catdir> <path/candidatedir>"
            raise SystemExit     

    # Detect lines. 
    elif sys.argv[1] == "-dl":
        """
        Detect lines from the candidate cats.
        Usage: python asterotrek.py -dl path/candidatedir path/   		
        """
        try:
            detectlines = dt.Detect()
            if len(sys.argv) == 5:
                detectlines.detectlines(sys.argv[2], sys.argv[3], sys.argv[4])
            else:
                detectlines.detectlines(sys.argv[2], sys.argv[3])
            print "Elapsed time: %s min. %s sec." %(int((time.time() - start_time) / 60), "%.2f" % ((time.time() - start_time) % 60))
        except:
            print "Usage error!"
            print "Usage: python asterotrek.py -dl <path/candidatedir> <path/>"
            raise SystemExit

    elif sys.argv[1] == "-mdl":
        """
        Multi-Detect lines from the candidate cats.
        Usage: python asterotrek.py -mdl path/candidatedir path/           
        """
        try:
            print "Please wait until processing is complete (multiprocessing)."
            detectlines = dt.Detect()
            movingobjects = detectlines.multilinedetector(sys.argv[2], sys.argv[3])
            if len(movingobjects) != 0:
                fastmos, slowmos = detectlines.resultreporter(sys.argv[3], movingobjects)
                pd.set_option('expand_frame_repr', False)
                if fastmos.size:
                    fastmos = pd.DataFrame.from_records(fastmos, columns=["file_id", "flags", "x", "y", "flux", "background", "lineid", "skymotion(px/min)"])
                    print "\033[1;32mList of Fast Moving Objects\033[0m"
                    print "\033[1;32m===========================\033[0m"
                    print fastmos
                if slowmos.size:
                    slowmos = pd.DataFrame.from_records(slowmos, columns=["file_id", "flags", "x", "y", "flux", "background", "lineid", "skymotion(px/min)"])
                    print "\033[1;31mList of Slow Moving Objects (Please check these objects! Are these really MOs?)\033[0m"
                    print "\033[1;31m===========================\033[0m"
                    print slowmos
            print "Multi line detection process is completed."
            print "Elapsed time: %s min. %s sec." %(int((time.time() - start_time) / 60), "%.2f" % ((time.time() - start_time) % 60))
        except:
            print "Usage error!"
            print "Usage: python asterotrek.py -mdl <path/candidatedir> <path/>"
            raise SystemExit

    elif sys.argv[1] == "-mdlwpng" and len(sys.argv) == 5:
        """
        Converts FITS images into PNG files with detected objects (with-multi-processing).
        Usage: python asterotrek.py -mdlwpng path/candidatedir path/ path/png/    		
        """
        try:
            print "Please wait until processing is complete (multiprocessing)."
            f2n = plt.Plot()
            detectlines = dt.Detect()
            lines = detectlines.multilinedetector(sys.argv[2], sys.argv[3])
            fastmos, slowmos = detectlines.resultreporter(sys.argv[3], lines)
    
            movingobjects = np.concatenate((fastmos, slowmos), axis=0)
    
            if len(movingobjects) != 0:
                if os.path.isdir(sys.argv[3]):
                    for i, fitsimage in enumerate(sorted(glob.glob("%s/*.fits" %(sys.argv[3])))):
                        f2n.fits2png(fitsimage, sys.argv[4], movingobjects[movingobjects[:, 0].astype(int) == i])
                        print "%s converted into %s" %(fitsimage, sys.argv[4])
                print "Plotted all detected objects into PNG files."
                
                #List of Fast (greater than basepar value between first and last image) Moving Objects
                pd.set_option('expand_frame_repr', False)
                if fastmos.size:
                    fastmos = pd.DataFrame.from_records(fastmos, columns=["file_id", "flags", "x", "y", "flux", "background", "lineid", "skymotion(px/min)"])
                    print "\033[1;32mList of Fast Moving Objects\033[0m"
                    print "\033[1;32m===========================\033[0m"
                    print fastmos
                if slowmos.size:
                    slowmos = pd.DataFrame.from_records(slowmos, columns=["file_id", "flags", "x", "y", "flux", "background", "lineid", "skymotion(px/min)"])
                    print "\033[1;31mList of Slow Moving Objects (Please check these objects! Are these really MOs?)\033[0m"
                    print "\033[1;31m===========================\033[0m"
                    print slowmos
            else:
                print "No line detected!!!!"
            print "Elapsed time: %s min. %s sec." %(int((time.time() - start_time) / 60), "%.2f" % ((time.time() - start_time) % 60))
        except:
            print "Usage error!"
            print "Usage: python asterotrek.py -mdlwpng <path/candidatedir> <fitsdir> <outdir/png/>" 
            raise SystemExit
            
    elif sys.argv[1] == "-fits2png" and len(sys.argv) == 4:
        """
        Converts FITS images into PNG files.
        Usage: python asterotrek.py -fits2png <fitsimage(s)> <outdir>    		
        """
        try:
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
            print "Elapsed time: %s min. %s sec." %(int((time.time() - start_time) / 60), "%.2f" % ((time.time() - start_time) % 60))
        except:
            print "Usage error!"
            print "Usage: python asterotrek.py -fits2png <fitsimage(s)> <outdir>" 
            raise SystemExit

    elif sys.argv[1] == "-plot2ds9" and len(sys.argv) == 4:
        """
        Plots catalogue files into ds9.
        Usage: python asterotrek.py -plot2ds9 <fitsimage> <catfile>    		
        """
        try:
            print "Please wait until processing is complete."
            p2ds9 = plt.Plot()
            p2ds9.plot2ds9(sys.argv[2], sys.argv[3])
            print "Elapsed time: %s min. %s sec." %(int((time.time() - start_time) / 60), "%.2f" % ((time.time() - start_time) % 60))
        except:
            print "Usage error!"
            print "Usage: python asterotrek.py -fits2png <fitsimage(s)> <outdir>" 
            raise SystemExit
    elif sys.argv[1] == "-makegif":
        """
        Converts PNG images to animated GIF file.
        Usage: python asterotrek.py -makegif <PNG(s)> <outdir>    		
        """
        try:
            print "Please wait until processing is complete."
            os.popen("convert -delay 20 -loop 0 %s/*.png %s/%s.gif" %(sys.argv[2], sys.argv[2], sys.argv[3]))
            "%.2f" % 3.14159
            print "Elapsed time: %s min. %s sec." %(int((time.time() - start_time) / 60), "%.2f" % ((time.time() - start_time) % 60))
        except:
            print "Usage error!"
            print "python asterotrek.py -makegif <PNG(s)> <outdir>" 
            raise SystemExit 