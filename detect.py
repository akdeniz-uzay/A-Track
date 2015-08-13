# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 19:43:14 2015

@author: ykilic
"""
import math
import glob
import os, time
import itertools as it
import pickle as pk
from _ast import Return

try:
    import pyfits
except ImportError:
    print "Did you install pyfits?"
    raise SystemExit

try:
    import pandas as pd
except ImportError:
    print "Did you install pandas?"
    raise SystemExit

try:
    import matplotlib.pyplot as plt
except ImportError:
    print "Did you install matplotlib?"
    raise SystemExit

try:
    import subprocess
    from multiprocessing.pool import ThreadPool
    from multiprocessing import cpu_count, Queue
except ImportError:
    print "Can not load multiprocessing tools!"
    raise SystemExit

try:
    import numpy as np
except ImportError:
    print "Did you install pandas?"
    raise SystemExit

try:
    import plot as pt
except ImportError:
    print "Can not load plot. Do you have plot.py?"
    raise SystemExit


class Detect:
    """
    MOD's detection class.
                
    """

    def distance(self, xcoor0, ycoor0, xcoor1, ycoor1):
        """
        distance(xcoor0, ycoor0, xcoor1, ycoor1) -> float
        Returns distence between two points.
        
        @param xcoor0: x coordinate for first point
        @type xcoor0: float, integer
        @param ycoor0: y coordinate for first point
        @type ycoor0: float, integer
        @param xcoor1: x coordinate for second point
        @type xcoor1: float, integer
        @param ycoor1: y coordinate for second point
        @type ycoor1: float, integer
        @return: float
        """
        dist = math.sqrt((ycoor1 - ycoor0)**2 + (xcoor1 - xcoor0)**2)
        return dist

    def finalcheck(self, coor0, coor1, coor2):
        """
        finalcheck(self, coor0, coor1, coor2) -> boolean
        Returns of tree points moving back or forward moving status
        True: One of points moving back
        False: One of points moving forward

        @param coor0: first point's x and y coordinates
        @type coor0: list        
        @param coor1: first point's x and y coordinates
        @type coor1: list
        @param coor2: second point's x and y coordinates
        @type coor2: list
        @return: boolean
        """
        longest = self.longest(coor0, coor1, coor2)
        if longest == (coor0, coor2, coor1):
          return True
        else:
          return False

    def isClose(self, coor1, coor2, rad):
        """
        isClose(coor1, coor2, r) -> boolean
        Returns true and false if the second point is in the selected r radius.
        
        @param coor1: first point's x and y coordinates
        @type coor1: list
        @param coor2: second point's x and y coordinates
        @type coor2: list
        @param r: radius for search point
        @type r: float, integer
        @return: boolean
        """
        dist = self.distance(coor1[0], coor1[1], coor2[0], coor2[1])
        if float(dist) <= float(rad):
            return True
        else:
            return False
    
    
    def longest(self, coor1, coor2, coor3):
        """
        longest(coor1, coor2, coor3) -> list
        Returns longest side of triangle
        
        @param coor1: first point's x and y coordinates
        @type coor1: list
        @param coor2: second point's x and y coordinates
        @type coor2: list
        @param coor3: third point's x and y coordinates
        @type coor3: list
        @return: list
        """

        d12 = self.distance(coor1[0], coor1[1], coor2[0], coor2[1])
        d13 = self.distance(coor1[0], coor1[1], coor3[0], coor3[1])
        d23 = self.distance(coor3[0], coor3[1], coor2[0], coor2[1])
        distlist = [d12, d23, d13]
        ref = distlist[0]
        index = 0
                
        for n, i in enumerate(distlist):
            if ref < i:
                ref = i
                index = n
        
        if index == 0:
            return coor1, coor2, coor3
        elif index == 1:
            return coor2, coor3, coor1
        elif index == 2:
            return coor1, coor3, coor2
    
    def height(self, line, xy):
        """
        height(line, xy) -> float
        Returns shortest distance a point to a line.
        
        @param line: line's coordinates as [[x1, y1], [x2, y2]]
        @type line: list
        @param xy: coordinates of a point (x, y)
        @type xy: list
        @return: float
        """
        x0 = line[0][0]
        y0 = line[0][1]
        x1 = line[1][0]
        y1 = line[1][1]
        x2 = xy[0]
        y2 = xy[1]
        try:
            h = math.fabs((x1 - x0)*y2 + (y0 - y1)*x2 + x0*y1 - x1*y0) / math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 -y0, 2))
        except ZeroDivisionError:
            h = 0
        return h 

    def detectcandidateobjects(self, referencecat, mastercat, outdir, min_fwhm=1, max_fwhm=10, max_flux=500000, elongation=1.8, snrsigma=5, basepar=0.35):
        """
        Reads given sextractor's catalogue file and detect candidate objects in "mastercat.txt".
        
        @param referencecat: Catalogue file of extracted objects from FITS image.
        @type referencecat: Text file object.
        @param mastercat: Master catalogue file of all extracted objects from all images.
        @type mastercat: Text file object.
        @param outdir: Out directory of candidate objects file which will be saved in.
        @type outdir: Directory
        @param min_fwhm: Minimum FWHM value of searching objects.
        @type min_fwhm: float
        @param max_fwhm: Maximum FWHM value of searching objects.
        @type max_fwhm: float
        @param elongation: Ellipticity of searching value.
        @type elongation: float
        @param snrsigma: SNR value of searching value.
        @type snrsigma: float
        @param basepar: Distance between two points.
        @type basepar: float
        @return: array           
        """
        catfile = os.path.basename(referencecat)
        h_catfile, e_catfile = catfile.split(".")
        
        if e_catfile == "pysexcat":
            ref_np = np.genfromtxt(referencecat, delimiter=None, comments='#')
            master_np = np.genfromtxt(mastercat, delimiter=None, comments='#')
            
            referencecatalogue = pd.DataFrame.from_records(ref_np, columns=["flags", "x", "y", "flux", "background", "fwhm", "elongation", "fluxerr"])
            mastercatalogue = pd.DataFrame.from_records(master_np, columns=["flags", "x", "y", "flux", "background", "fwhm", "elongation", "fluxerr"])
            
            refcatfiltered = referencecatalogue[((referencecatalogue.flags <= 16)) & (referencecatalogue.flux <= max_flux) & (referencecatalogue.fwhm <= max_fwhm) & \
            ((referencecatalogue.flux / referencecatalogue.fluxerr) > snrsigma) & (referencecatalogue.fwhm >= min_fwhm) & (referencecatalogue.elongation <= elongation)]
            mascat_all = mastercatalogue[((mastercatalogue.flags <= 16)) & (mastercatalogue.flux <= max_flux) & (mastercatalogue.fwhm <= max_fwhm) & \
            ((mastercatalogue.flux / mastercatalogue.fluxerr) > snrsigma) & (mastercatalogue.fwhm >= min_fwhm) & (mastercatalogue.elongation <= elongation)]
            
            refcat = refcatfiltered[["flags", "x", "y", "flux", "background"]]
            refcat = refcat.reset_index(drop=True)
            mascat = mascat_all[["flags", "x", "y", "flux", "background"]]
            mascat = mascat.reset_index(drop=True)
            
            # flags or id, first column is not important, i added first column for just check.
        
        candidateobjects = pd.DataFrame(columns=["flags", "x", "y", "flux", "background"])
        for i in range(len(refcat.x)):
            if len(mascat[((mascat.x - refcat.x[i])**2 + (mascat.y - refcat.y[i])**2)**0.5 <= basepar]) < 2:
                candidateobjects = candidateobjects.append(refcat.iloc[i], ignore_index=True)

        if os.path.exists(outdir):
            pass
        else:
            os.mkdir(outdir)        
        
        candidateobjects.to_csv("%s/candidates_%s.txt" %(outdir, h_catfile), index = False)
        return candidateobjects

    def detectlines(self, catdir, fitsdir, combinationindex = None, basepar=0.35, heightpar=0.1, pixel_scale=0.31, vmax=0.03, radiussigma = 1):
        """
        
        Reads given candidate files and detect lines with randomized algorithm.

        @param catdir: Directory of candidate objects.
        @type catdir: Directory.
        @param fitsdir: Directory of aligned FITS images.
        @type fitsdir: Directory.
        @param combinationindex: Index of candidates array divided by parallelized processing.
        @type combinationindex: integer
        @param basepar: Distance between two points.
        @type basepar: float                  
        @param heightpar: The length of the triangle's height.
        @type heightpar: float
        @param pixel_scale: Pixel scale of CCD.
        @type pixel_scale: float
        @param vmax: Theoretical maximum angular velocity of NEOs (px/").
        @type vmax: float
        @param radiussigma: Maximum error value (pixel) of moving objects calculated position.
        @type radiussigma: float
        @return: array
        """

        candidatefiles = sorted(glob.glob("%s/*affineremap.txt" %(catdir)))
        fitsfiles = sorted(glob.glob("%s/*.fit*" %(fitsdir)))
        
        containerlist = []
        fileidlist = []
        candidates = []
        
        #all files copying to list
        for fileid, candidatefile in enumerate(candidatefiles):
            candidatelist = pd.read_csv(candidatefile, sep=",", names = ["flags", "x", "y", "flux", "background"], header=0)
            if not candidatelist.empty:
                containerlist.append(candidatelist.values)
                fileidlist.append(fileid)

        if combinationindex:
            combinationlist = self.combinecatfiles(catdir)[int(combinationindex)]
        else:
            combinationlist = it.combinations(fileidlist, 3)

        for cyc, selectedfileids in enumerate(combinationlist):
        #for i in xrange(len(containerlist)-2):
            fileid_i, fileid_j, fileid_k = selectedfileids
            #print "Searching lines in %s., %s., %s. (%s) files" %(fileid_i, fileid_j, fileid_k, cyc)
            hdulist1 = pyfits.open(fitsfiles[fileid_i])
            hdulist2 = pyfits.open(fitsfiles[fileid_j])
            hdulist3 = pyfits.open(fitsfiles[fileid_k])
            xbin = hdulist1[0].header['xbinning']
            ybin = hdulist1[0].header['ybinning']
            naxis1 = hdulist1[0].header['NAXIS1']
            naxis2 = hdulist1[0].header['NAXIS2']
            obsdate1 = hdulist1[0].header['date-obs']
            exptime1 = hdulist1[0].header['exptime']
            obsdate2 = hdulist2[0].header['date-obs']
            exptime2 = hdulist2[0].header['exptime']
            obsdate3 = hdulist3[0].header['date-obs']
            exptime3 = hdulist3[0].header['exptime']
            otime1 =  time.strptime(obsdate1, "%Y-%m-%dT%H:%M:%S.%f")
            otime2 =  time.strptime(obsdate2, "%Y-%m-%dT%H:%M:%S.%f")
            otime3 =  time.strptime(obsdate3, "%Y-%m-%dT%H:%M:%S.%f")
            radius =  (time.mktime(otime2) - time.mktime(otime1) + (exptime2 - exptime1) / 2) * vmax / (pixel_scale * xbin)
            radius2 =  (time.mktime(otime3) - time.mktime(otime2) + (exptime3 - exptime2) / 2) * vmax / (pixel_scale * xbin)
            for u in xrange(len(containerlist[fileid_i])):
                for z in xrange(len(containerlist[fileid_j])):
                    #ilk çift nokta seçiliyor
                    absradius1 = self.distance(containerlist[fileid_i][u][1], containerlist[fileid_i][u][2], \
                                               containerlist[fileid_j][z][1], containerlist[fileid_j][z][2])
                    deltaobs1 = (time.mktime(otime2) - time.mktime(otime1)) + (exptime2 - exptime1) / 2
                    if self.isClose(containerlist[fileid_i][u, [1,2]], containerlist[fileid_j][z, [1,2]], radius):
                        for x in xrange(len(containerlist[fileid_k])):
                            absradius2 = self.distance(containerlist[fileid_j][z][1], containerlist[fileid_j][z][2], \
                                                       containerlist[fileid_k][x][1], containerlist[fileid_k][x][2])
                            deltaobs2 =  (time.mktime(otime3) - time.mktime(otime2)) + (exptime3 - exptime2) / 2
                            if self.isClose(containerlist[fileid_j][z, [1,2]], containerlist[fileid_k][x, [1,2]], radius2):
                                if ((deltaobs2 * absradius1 / deltaobs1) - radiussigma) <= absradius2 and \
                                ((deltaobs2 * absradius1 / deltaobs1) + radiussigma) >= absradius2:                                             
                                    base = self.longest(containerlist[fileid_i][u, [1,2]], containerlist[fileid_j][z, [1,2]], containerlist[fileid_k][x, [1,2]])
                                    hei = self.height(base[:-1], base[-1])
                                    lengh = self.distance(base[0][0], base[0][1], base[1][0], base[1][1])
                                    if lengh > basepar * 1.5 and hei < heightpar:
                                        
                                        p1 = [containerlist[fileid_i][u][1], containerlist[fileid_i][u][2]]
                                        p2 = [containerlist[fileid_j][z][1], containerlist[fileid_j][z][2]]
                                        p3 = [containerlist[fileid_k][x][1], containerlist[fileid_k][x][2]]
                                     
                                        if self.finalcheck(p1, p2, p3):
                                            candidates.append([[fileid_i,containerlist[fileid_i][u][0], containerlist[fileid_i][u][1], containerlist[fileid_i][u][2], \
                                                        containerlist[fileid_i][u][3], containerlist[fileid_i][u][4]],\
                                                        [fileid_j, containerlist[fileid_j][z][0], containerlist[fileid_j][z][1], containerlist[fileid_j][z][2], \
                                                        containerlist[fileid_j][z][3], containerlist[fileid_j][z][4]],\
                                                        [fileid_k, containerlist[fileid_k][x][0], containerlist[fileid_k][x][1], containerlist[fileid_k][x][2], \
                                                        containerlist[fileid_k][x][3], containerlist[fileid_k][x][4]]])                                                                                                           
                                        else:
                                            print "final check failed"

        if combinationindex:
            with open("./%s_result.txt" %(combinationindex), 'wb') as fl:
                pk.dump(candidates, fl)
            print "All detected lines added to ./%s_result.txt in %s. process." %(combinationindex, combinationindex)
            return True
        else:
            if candidates:
                return self.uniqueanditemlist(res)
            else:
                print "No lines detected!"
                return False

    def collectpointsonline(self, pointarray):
        """
        Reads three points on same line respectively and collects them in same list if conditions are valid.

        @param pointarray: List of three points which are on same line.
        @type pointarray: list
        @return: list
        """

        pointlist = []

        for points in pointarray:

            p1 = points[0][2:4]
            p2 = points[1][2:4]
            p3 = points[2][2:4]

            if pointlist:
                for linelist in pointlist:
                    p1status = (p1 in [xy[2:4] for xy in linelist])
                    p2status = (p2 in [xy[2:4] for xy in linelist])
                    p3status = (p3 in [xy[2:4] for xy in linelist])

                    if (p1status, p2status, p3status) == (True, False,False):
                        linelist.append(points[1])                                                                                                               
                        linelist.append(points[2])
                    elif (p1status, p2status, p3status) == (False, True,False):
                        linelist.append(points[0])                                                                                                               
                        linelist.append(points[2])                                                      
                    elif (p1status, p2status, p3status) == (False, False,True):
                        linelist.append(points[0])                                                                                                               
                        linelist.append(points[1])                                                       
                    elif (p1status, p2status, p3status) == (True, True,False):                                                                                                             
                        linelist.append(points[2])                                                                           
                    elif (p1status, p2status, p3status) == (False, True,True):                                                            
                        linelist.append(points[0])                                                                                                                                                                       
                    elif (p1status, p2status, p3status) == (True, False,True):                                                            
                        linelist.append(points[1])                                                                                                               
                if (p1status, p2status, p3status) == (False, False, False):
                    pointlist.append([points[0], points[1], points[2]])
            else:
                pointlist.append([points[0], points[1], points[2]])
        return pointlist

    def uniqueanditemlist(self, resultarray):
        """
        Reads points in same list respectively runs after collectpointsonline funtion and tags same id in same list if conditions are valid.

        @param pointarray: List of points which are on same line.
        @type pointarray: list
        @return: array
        """

        pointid = 0
        candidates = []

        #tekrarlı noktaların kontrol işlemi başlıyor
        for line in resultarray:
            pointid +=1
            pc = 0
            for point in line:
                #belirlenen doğrular için id'leme işlemi başlıyor
                #seçilen nokta daha önce id'lendi ise bulunduğu dizi içindeki (line(i)) tespit sırasını alıyor.
                if (point[0:6] in [xy[0:6] for xy in candidates]) == False:
                    #candidates'e son atamalar yapılmış mı kontrol ediliyor.
                    if candidates:
                        #eger candidates (nihai dizi)'in son elemanı point id'den küçükse,
                        #line içinde gruplanan noktaların tamamı başka noktalarda var demektir.
                        #bu yüzden line grup sırası id'leme için kullanılamaz.
                        if candidates[len(candidates) -1][-1] < pointid:
                            #yeni bir line id sayacı tanımlanıyor.
                            pc +=1
                            #eğer pc 1 ise candidates'te son verilen id numarasından bir fazlası yeni yeni nokta için id olarak verilir.
                            #eger 1'den fazla ise o point grubu için candidates'te en son verilen id yeni point'e verilir.
                            if pc == 1:
                                point.append(candidates[len(candidates) -1][-1] + 1)
                                candidates.append(point)
                            else:
                                point.append(candidates[len(candidates) -1][-1])
                                candidates.append(point)
                        else:
                            point.append(pointid)
                            candidates.append(point)
                    else:
                        point.append(pointid)
                        candidates.append(point)
        
        #candidates numpy dizine dönüştürülüyor. duplication'lar eleniyor.                          
        movingobjects = pd.DataFrame.from_records(np.asarray(candidates), columns=["file_id", "flags", "x", "y", "flux", "background", "lineid"])
        movingobjects = movingobjects.drop_duplicates(["file_id", "flags", "x", "y", "flux", "background", "lineid"])
        return movingobjects.values

    def chunker(self, seq, size):
        """
        It divides the worklist of combinated files to CPU count (multiple work).

        @param seq: List of combinated files.
        @type seq: list
        @param size: Multiple work of detectlines sequence.
        @type size: list
        @return: list
        """
        return list(seq[pos:pos + size] for pos in xrange(0, len(seq), size))
    
    def combinecatfiles(self, catdir):
        """
        It divides the worklist of combinated files to CPU count (multiple work).

        @param catdir: Directory of candidate objects file which will be combine.
        @type catdir: Directory
        @return: list
        """

        candidatefiles = sorted(glob.glob("%s/*affineremap.txt" %(catdir)))
        fileidlist = []
        
        for fileid, candidatefile in enumerate(candidatefiles):
            candidatelist = pd.read_csv(candidatefile, sep=",", names = ["flags", "x", "y", "flux", "background"], header=0)
            if not candidatelist.empty:
                fileidlist.append(fileid)
        
        combinatedfiles = it.combinations(fileidlist, 3)
        combinatedfiles = list(combinatedfiles)

        numberofcpus = cpu_count()
        quotient = int(len(combinatedfiles) / numberofcpus)

        if (len(combinatedfiles) % numberofcpus) != 0:
            if len(combinatedfiles) < numberofcpus:
                sizeofworklist = len(combinatedfiles)
            else:
                sizeofworklist = quotient +1
        else:
            sizeofworklist = quotient

        return self.chunker(combinatedfiles, sizeofworklist)

    def multilinedetector(self, catdir, fitsdir):
        """
        Runs multi-processing tasks of the worklist.

        @param catdir: Directory of candidate objects file which will be combine.
        @type catdir: Directory
        @param fitsdir: Directory of aligned FITS image.
        @type fitsdir: Directory
        @return: array
        """
        
        cmds = list()
        
        sizeofworklist = len(self.combinecatfiles(catdir))
        for i in range(sizeofworklist):
            cmds.append(["python", "asterotrek.py", "-dl", catdir, fitsdir, str(i)])
        
        tp = ThreadPool(sizeofworklist)
        
        for cmd in cmds:
            tp.apply_async(self.rundl, (cmd,))
        
        tp.close()
        tp.join()

        rawcandidatesfiles = sorted(glob.glob("*_result.txt"))
        rawcandidates = []

        for rawcandidatesfile in rawcandidatesfiles:
            #To read it back:
            with open(rawcandidatesfile, 'rb') as fl:
                rawcandidates += pk.load(fl)

        lines = self.collectpointsonline(rawcandidates)
        return self.uniqueanditemlist(lines)
    
    def rundl(self, cmd):
        """
        Runs multi-processing tasks as subprocesses.

        @param cmd: Commands for main file.
        @type cmd: list
        @return: boolean
        """
        p = subprocess.Popen(cmd)
        p.wait()
        return True
    
    def resultreporter(self, fitsdir, movingobjects, basepar = 1.0):
        """
        Categorize and report MOs as slow and fast objects.

        @param fitsdir: Directory of aligned FITS image.
        @type fitsdir: Directory
        @param movingobjects: Numpy array of detected lines.
        @type movingobjects: array
        @param basepar: lenght of line.
        @type basepar: float.
        @return: boolean
        """
        tmp = []
        fastmos = []
        slowmos = []
        fitsfiles = sorted(glob.glob("%s/*.fit*" %(fitsdir)))
        numberoflines = movingobjects[:,6].max()
        
        for lineid in xrange(1, int(numberoflines)+1):
            linepoints = movingobjects[movingobjects[:, 6].astype(int) == int(lineid)]
            fileid_min, fileid_max = int(linepoints[:,0].min()), int(linepoints[:,0].max())
            hdulist1 = pyfits.open(fitsfiles[fileid_min])
            hdulist2 = pyfits.open(fitsfiles[fileid_max])
            obsdate1 = hdulist1[0].header['date-obs']
            exptime1 = hdulist1[0].header['exptime']
            obsdate2 = hdulist2[0].header['date-obs']
            exptime2 = hdulist2[0].header['exptime']
            otime1 =  time.strptime(obsdate1, "%Y-%m-%dT%H:%M:%S.%f")
            otime2 =  time.strptime(obsdate2, "%Y-%m-%dT%H:%M:%S.%f")
            
            linelenght = math.sqrt((linepoints[len(linepoints)-1][3] - linepoints[0][3])**2 + \
                                   (linepoints[len(linepoints)-1][2] - linepoints[0][2])**2)
            
            skymotion = (linelenght / ((time.mktime(otime2) + exptime2) - (time.mktime(otime1) + exptime1))) * 60

            mowithmu = np.concatenate((linepoints, np.asarray([[skymotion] * len(linepoints)]).T), axis=1)
            
            if  linelenght > basepar * 2:
                fastmos.append(mowithmu)
            else:
                slowmos.append(mowithmu)
                
        if len(fastmos) == 1:
            retfast = fastmos[0]
        elif len(fastmos) > 1:
            retfast = np.concatenate(tuple(fastmos), axis = 0)
        elif len(fastmos) == 0:
            retfast = np.array(tmp)

        if len(slowmos) == 1:
            retslow = slowmos[0]
        elif len(fastmos) > 1:
            retslow = np.concatenate(tuple(slowmos), axis = 0)
        elif len(slowmos) == 0:
            retslow = np.array(tmp)

        return retfast, retslow




