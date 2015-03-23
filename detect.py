# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 19:43:14 2015

@author: ykilic
"""

import math
import glob
import os

try:
    import pandas as pd
except ImportError:
    print "Did you install pandas?"
    raise SystemExit

try:
    from plot import *
except ImportError:
    print "Can not load plot. Do you have plot.py?"
    raise SystemExit


class Detect:
    """
    MOD's detection class.
        		
    """

    def slope(self, xcoor0, ycoor0, xcoor1, ycoor1):
        '''
        Get the slope of a line segment.
        @param xcoor0: x coordinate for first point
        @type xcoor0: float, integer
        @param ycoor0: y coordinate for first point
        @type ycoor0: float, integer
        @param xcoor1: x coordinate for second point
        @type xcoor1: float, integer
        @param ycoor1: y coordinate for second point
        @type ycoor1: float, integer
        @return: float, None
        '''
        try:
            return (float(ycoor1)-float(ycoor0))/(float(xcoor1)-float(xcoor0))
        except ZeroDivisionError:
            # line is vertical
            return None

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
    
    def isClose(self, coor1, coor2, r):
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
        d = self.distance(coor1[0], coor1[1], coor2[0], coor2[1])
        if float(d) <= float(r):
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
        d12 = self.distance(coor1[0], coor1[1], coor2[0], coor1[1])
        d13 = self.distance(coor1[0], coor1[1], coor3[0], coor3[1])
        d32 = self.distance(coor3[0], coor3[1], coor2[0], coor1[1])
        lis = [d12, d13, d32]
        ref = lis[0]
        index = 0
        for n, i in enumerate(lis):
            if ref > i:
                ref = i
                index = n
        
        if index == 0:
            return coor1, coor2, coor3
        elif index == 1:
            return coor1, coor3, coor2
        elif index == 2:
            return coor3, coor2, coor1
    
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
        h = math.fabs((x1 - x0)*y2 + (y0 - y1)*x2 + x0*y1 - x1*y0) / math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 -y0, 2))
        return h

    def detectstrayobjects(self, reference_cat, star_cat, target_folder):
        """
        Reads given ordered (corrected) coordinate file and detect stray objects in "starcat.txt".
        
        @param reference_cat: Ordered (corrected) star catalogue file for one image.
        @type reference_cat: Text file object.
        @param star_cat: Ordered (corrected) star catalogue file for all image.
        @type star_cat: Text file object...
            		
        """ 
        refcat = pd.read_csv(reference_cat, sep=" ", names=["ref_x", "ref_y"], header=None)
        starcat = pd.read_csv(star_cat, sep=" ", names=["ref_x", "ref_y"], header=None)
        
        strayobjectlist = pd.DataFrame(columns=["ref_x", "ref_y"])
        for i in range(len(refcat.ref_x)):
            if len(starcat[(abs(starcat.ref_x - refcat.ref_x[i]) < 1) & (abs(starcat.ref_y - refcat.ref_y[i]) < 1)]) < 2:
                strayobjectlist = strayobjectlist.append(starcat[(abs(starcat.ref_x - refcat.ref_x[i]) < 1) & (abs(starcat.ref_y - refcat.ref_y[i]) < 1)])
        
        starcatfile = os.path.basename(reference_cat)
        h_starcatfile, e_starcatfile = starcatfile.split(".")
        
        if os.path.exists(target_folder):
            pass
        else:
            os.mkdir(target_folder)        
        
        strayobjectlist.to_csv("%s/stray_%s.txt" %(target_folder, h_starcatfile))
        return strayobjectlist

    def detectlines(self, ordered_cats, output_figure, basepar=1.5, heightpar=1.0, areapar=1.0, interval = 20):
        """
        Reads given ordered (corrected) coordinate file and detect lines with randomized algorithm.
        
        @param ordered_cats: Ordered (corrected) star catalogues folder.
        @type ordered_cats: Directory object.
        @param output_figure: Plot figure path to save.
        @type output_figure: PNG object.
        @param basepar: The length of the base.
        @type basepar: Float            		
        @param heightpar: The length of the triangle's height.
        @type heightpar: Float
        @param areapar: The area of triangle.
        @type areapar: Float
        """ 
        starcat = sorted(glob.glob("%s/*affineremap.txt" %(ordered_cats)))
        onecatlist = pd.DataFrame(columns=["ref_x", "ref_y"])
        
        lst = []
        can = []
        
        #all files copying to list
        for objctlist in starcat:
            objtcat = pd.read_csv(objctlist, sep=",", names = ["ref_x", "ref_y"], header=0)
            if not objtcat.empty:
                onecatlist = onecatlist.append(objtcat)
                lst.append(objtcat.values)
        #calculation of a triangle's area and checking points on a same line.
        sayac = 0
        slope1 = 0.0
        slope2 = 0.0
        lastcoorx = 0
        lastcoory = 0
        for i in xrange(len(lst)-2):
            print "Searching lines on %s. file" %(i)
            for u in xrange(len(lst[i])):
                for z in xrange(len(lst[i+1])):
                    if self.isClose(lst[i][u], lst[i+1][z], interval):
                        for x in xrange(len(lst[i+2])):
                            if self.isClose(lst[i+1][z], lst[i+2][x], interval):
                                base = self.longest(lst[i][u], lst[i+1][z], lst[i+2][x])
                                hei = self.height(base[:-1], base[-1])
                                x1 = lst[i][u][0]
                                y1 = lst[i][u][1]
                                x2 = lst[i+1][z][0]
                                y2 = lst[i+1][z][1]
                                x3 = lst[i+2][x][0]
                                y3 = lst[i+2][x][1]
                                lengh = self.distance(base[0][0], base[0][1], base[1][0], base[1][1])
                                area = math.fabs(0.5*((x2-x1)*(y3-y1) - (x3-x1)*(y2-y1)))
                                
                                if lengh > basepar and hei < heightpar and area < areapar:
                                    slope1 = self.slope(lst[i][u][0], lst[i][u][1], lst[i+1][z][0], lst[i+1][z][1])
                                    gapx = lst[i+2][x][0] - lastcoorx
                                    gapy = lst[i+2][x][1] - lastcoory
                                    lastcoorx = lst[i+2][x][0]
                                    lastcoory = lst[i+2][x][1]
                                    if gapx <= interval and gapy <= interval:
                                        sayac = sayac + 1
                                    can.append([i,lst[i][u][0], lst[i][u][1], slope1, sayac])
                                    can.append([i+1, lst[i+1][z][0], lst[i+1][z][1], slope1, sayac])
                                    can.append([i+2, lst[i+2][x][0], lst[i+2][x][1], slope1, sayac])
        
        #removing duplicates.
        if can:
            res = pd.DataFrame(can, columns=["ref_file", "ref_x", "ref_y", "slope", "line_id"])
            res = res.drop_duplicates(["ref_file", "ref_x", "ref_y", "slope", "line_id"])
            if output_figure != None:
                plotxy = Plot()
                plotxy.plot(res, output_figure)
            print res
            res.to_csv("lines.csv")
            return res
        else:
            print "No lines detected!"
            return