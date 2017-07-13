# -*- coding: utf-8 -*-

from astropy import coordinates
from astropy import units as u
from astropy.wcs import WCS
from astropy.io import fits
from astropy.time import Time

from datetime import datetime
from datetime import timedelta

import math
import os
import numpy as np

from . import env


class fits_op():

    def __init__(self, verb=True):
        self.verb = verb
        self.eetc = env.etc(verb=self.verb)

    def return_out_file_header(self, obs="YK", tel="TUG 100", cod="A84",
        contact="yucelkilic@myrafproject.org", catalog="GAIA"):
        head = """COD %s
OBS %s
MEA %s
TEL %s + CCD
ACK MPCReport file updated %s
AC2 %s
NET %s""" % (cod, obs, obs, tel, self.eetc.time_stamp(), contact, catalog)

        return(head)

    def get_header(self, file_name, key):
        try:
            hdu = fits.open(file_name, "readonly")
            dat = hdu[0].header[key]
            return(dat)
        except Exception as e:
            print(e)

    def radec2wcs(self, ra, dec):
        try:
            c = coordinates.SkyCoord('{0} {1}'.format(ra, dec),
                                     unit=(u.hourangle, u.deg), frame='fk5')

            return(c)
        except Exception as e:
            # print(e)
            pass

    def xy2sky(self, file_name, x, y):
        try:
            header = fits.getheader(file_name)
            w = WCS(header)
            # astcoords_deg = w.all_pix2world([[x, y]], 0)
            astcoords_deg = w.wcs_pix2world([[x, y]], 0)
            astcoords = coordinates.SkyCoord(astcoords_deg * u.deg,
                                             frame='fk5')
            alpha = ' '.join(astcoords.to_string(
                style='hmsdms', sep=" ", precision=2)[0].split(" ")[:3])
            delta = ' '.join(astcoords.to_string(
                style='hmsdms', sep=" ", precision=1)[0].split(" ")[3:])
            return("{0} {1}".format(alpha, delta))
        except Exception as e:
            # print(e)
            pass

    def xy2sky2(self, file_name, x, y):
        try:
            header = fits.getheader(file_name)
            w = WCS(header)
            astcoords_deg = w.wcs_pix2world([[x, y]], 0)
            astcoords = coordinates.SkyCoord(
                astcoords_deg * u.deg, frame='fk5')
            return(astcoords[0])
        except Exception as e:
            # print(e)
            pass

    def xy2skywcs(self, file_name, x, y):
        try:
            file_path, file_and_ext = os.path.split(file_name)
            os.system("xy2sky {0} {1} {2} > {3}/coors".format(
                file_name,
                x,
                y,
                file_path))
            coors = np.genfromtxt('{0}/coors'.format(file_path),
                                  comments='#',
                                  invalid_raise=False,
                                  delimiter=None,
                                  usecols=(0, 1),
                                  dtype="U")

            os.system("rm -rf {0}/coors".format(file_path))

            c = coordinates.SkyCoord('{0} {1}'.format(coors[0], coors[1]),
                                     unit=(u.hourangle, u.deg), frame='fk5')

            alpha = c.to_string(style='hmsdms', sep=" ", precision=2)[:11]
            delta = c.to_string(style='hmsdms', sep=" ", precision=1)[11:]
            
            return('{0} {1}'.format(alpha, delta))
        
        except Exception as e:
            # print(e)
            pass

    def xy2sky2wcs(self, file_name, x, y):
        try:
            file_path, file_and_ext = os.path.split(file_name)
            os.system("xy2sky {0} {1} {2} > {3}/coors".format(
                file_name,
                x,
                y,
                file_path))
            coors = np.genfromtxt('{0}/coors'.format(file_path),
                                  comments='#',
                                  invalid_raise=False,
                                  delimiter=None,
                                  usecols=(0, 1),
                                  dtype="U")

            os.system("rm -rf {0}/coors".format(file_path))

            c = coordinates.SkyCoord('{0} {1}'.format(coors[0], coors[1]),
                                     unit=(u.hourangle, u.deg), frame='fk5')

            return(c)
        except Exception as e:
            # self.eetc.print_if(e)
            pass

    def center_finder(self, file_name):
        try:
            naxis1 = self.get_header(file_name, "naxis1")
            naxis2 = self.get_header(file_name, "naxis2")
            x, y = [float(naxis1) / 2, float(naxis2) / 2]
            coor = self.xy2sky(file_name, x, y)
            ra = ' '.join(coor.split(" ")[:3])
            dec = ' '.join(coor.split(" ")[3:])

            return([ra, dec])
        except Exception as e:
            self.eetc.print_if(e)

    def solve_field(self,
                    image_path,
                    tweak_order=2,
                    downsample=4,
                    radius=0.5,
                    ra=None,
                    dec=None):
    
        try:
            os.system(("solve-field --no-fits2fits --no-plots "
                       "--no-verify --tweak-order {0} "
                       "--downsample {1} --overwrite --radius {2} --no-tweak "
                       "--ra {3} --dec {4} {5}").format(tweak_order,
                                                        downsample,
                                                        radius,
                                                        ra.replace(" ", ":"),
                                                        dec.replace(" ", ":"),
                                                        image_path))
            # Cleaning
            root, extension = os.path.splitext(image_path)
            os.system(("rm -rf {0}-indx.png {0}-indx.xyls "
                      "{0}-ngc.png {0}-objs.png "
                       "{0}.axy {0}.corr "
                       "{0}.match {0}.rdls "
                       "{0}.solved {0}.wcs").format(root))

            if not os.path.exists(root + '.new'):
                print(image_path + ' cannot be solved!')
                return(False)
            else:
                print('Image has been solved!')
                return(True)
        
        except Exception as e:
            self.eetc.print_if(e)


class dt_op():

    def __init__(self, verb=True):
        self.verb = verb
        self.eetc = env.etc(verb=self.verb)
        self.ffit = fits_op(verb=self.verb)

    def get_timestamp(self, dt, frmt="%Y-%m-%dT%H:%M:%S.%f"):
        try:
            if len(dt) == 19:
                frmt = "%Y-%m-%dT%H:%M:%S"
            
            t = datetime.strptime(dt, frmt)
            return(t)
        except Exception as e:
            self.eetc.print_if(e)

    def get_timestamp_exp(self, file_name, dt="date-obs", exp="exptime"):
        try:
            expt = self.ffit.get_header(file_name, exp)
            dat = self.ffit.get_header(file_name, dt)
            tmstamp = self.get_timestamp(dat)
            ret = tmstamp + timedelta(seconds=float(expt) / 2)
        except Exception as e:
            self.eetc.print_if(e)

        return(ret)

    def date2jd(self, dat):
        try:
            # 2015-03-08 23:10:01.890000
            date_t = str(dat).replace(" ", "T")
            t = Time(date_t, format='isot', scale='utc')
        except Exception as e:
            self.eetc.print_if(e)

        return(t.jd)

    def convert_time_format(self, timestamp):
        try:
            y = timestamp.year
            m = timestamp.month
            d = timestamp.day

            h = timestamp.hour
            M = timestamp.minute
            s = timestamp.second

            if d >= 10:
                ret = "C%s %02.f %.5f" % (y, m,
                    d + float(h) / 24 + float(M) / 1440 + float(s) / 86400)
            else:
                ret = "C%s %02.f 0%.5f" % (y, m,
                    d + float(h) / 24 + float(M) / 1440 + float(s) / 86400)
            return(ret)
        except Exception as e:
            self.eetc.print_if(e)


class linear_op():

    def __init__(self, verb=True):
        self.verb = verb
        self.eetc = env.etc(verb=self.verb)

    def is_object(self, coor1, coor2, max_dist=10, min_dist=0):
        ret = coor1.separation(coor2)
        # print(coor1, coor2, " => ", ret.arcsecond)
        return(min_dist <= ret.arcsecond <= max_dist)


class mag_op():

    def __init__(self, verb=True):
        self.verb = verb
        self.eetc = env.etc(verb=self.verb)

    def flux2mag(self, flux):
        try:
            mag = 25 - 2.5 * math.log10(flux)
            return("%.1f" % mag)
        except Exception as e:
            self.eetc.print_if(e)


class online_op():

    def __init__(self, verb=True):
        self.verb = verb
        self.verb = verb
        self.eetc = env.etc(verb=self.verb)
        self.efile_op = env.file_op(verb=self.verb)
        self.ddtop = dt_op(verb=self.verb)

    def find_skybot_objects(self, dat, ra, dec, radius=16,
                            limmag=20.5, observat="A84"):
        try:
            epoch = self.ddtop.date2jd(dat)
            bashcmd = ("wget -q \"http://vo.imcce.fr/webservices/skybot/"
                       "skybotconesearch_query.php"
                       "?-ep={0}&-ra={1}&-dec={2}&-rm={3}&-output=object&"
                       "-loc={4}&-filter=120&-objFilter=120&-from="
                       "SkybotDoc&-mime=text\" -O skybot.cat").format(epoch,
                                                                      ra,
                                                                      dec,
                                                                      radius,
                                                                      observat)

            os.system(bashcmd)
            skyresult = self.efile_op.read_file_as_array("skybot.cat")
            os.system('rm -rf skybot.cat')
            return(skyresult)
            
        except Exception as e:
            self.eetc.print_if(e)
