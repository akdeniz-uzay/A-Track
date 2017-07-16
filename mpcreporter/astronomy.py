# -*- coding: utf-8 -*-

from astropy import coordinates
from astropy import units as u
from astropy.wcs import WCS
from astropy.io import fits
from astropy.time import Time

from datetime import datetime
from datetime import timedelta

from math import log10
from os import path, system
from numpy import genfromtxt

from .io import FileOps


class FitsOps:

    def __init__(self):
        self.timeops = TimeOps()

    def return_out_file_header(self, observer="YK", tel="TUG 100", code="A84",
                               contact="yucelkilic@myrafproject.org",
                               catalog="GAIA"):

        """
        Creates MPC report file's head.
        @param observer: Observer.
        @type observer: str
        @param tel: Telescope information.
        @type tel: str
        @param code: Observatory code.
        @type code: str
        @param contact: E-mail of the contact person.
        @type contact: str
        @param catalog: Used catalogue.
        @type catalog: str
        @return: str
        """

        head = """COD {0}
OBS {1}
MEA {2}
TEL {3} + CCD
ACK MPCReport file updated {4}
AC2 {5}
NET {6}""".format(code, observer, observer, tel,
                  self.timeops.time_stamp(),
                  contact, catalog)

        return(head)

    def get_header(self, file_name, key):

        """
        Extracts requested keyword from FITS header.
        @param file_name: FITS image name.
        @type file_name: str
        @param key: Requested keyword.
        @type key: str
        @return: str
        """

        try:
            hdu = fits.open(file_name, "readonly")
            header_key = hdu[0].header[key]
            return(header_key)
        except Exception as e:
            print(e)


class AstCalc:

    def __init__(self):
        self.fileops = FileOps()
        self.fitsops = FitsOps()
        self.timeops = TimeOps()

    def is_object(self, coor1, coor2, max_dist=10, min_dist=0):

        """
        It checks whether the object being queried is the same in the
        database within the specified limit.
        
        @param coor1: Detected object's coordinate.
        @type coor1: coordinate
        @param coor2: Calculated object's coordinate.
        @type coor2: coordinate
        @param max_dist: Max distance limit in arcsec.
        @type max_dist: integer
        @param min_dist: Max distance limit in arcsec.
        @type min_dist: integer
        @return: boolean
        """

        ret = coor1.separation(coor2)
        return(min_dist <= ret.arcsecond <= max_dist)

    def flux2mag(self, flux):

        """
        Converts flux to magnitude.
        @param flux: Flux.
        @type flux: float
        @return: float
        """

        try:
            mag = 25 - 2.5 * log10(flux)
            return("{:.1f}".format(mag))
        except Exception as e:
            print(e)

    def find_skybot_objects(self, odate, ra, dec, radius=16,
                            observatory="A84"):

        """
        Seek and identify all the known solar system objects
        in a field of view of a given size.
        
        @param odate: Observation date.
        @type odate: date
        @param ra: RA of field center for search, format: degrees or hh:mm:ss
        @type ra: str
        @param dec: DEC of field center for search, format: degrees or hh:mm:ss
        @type dec: str
        @param radius: Radius.
        @type radius: float
        @param observatory: Observation code.
        @type observatory: str
        @return: str
        """

        try:
            epoch = self.timeops.date2jd(odate)
            bashcmd = ("wget -q \"http://vo.imcce.fr/webservices/skybot/"
                       "skybotconesearch_query.php"
                       "?-ep={0}&-ra={1}&-dec={2}&-rm={3}&-output=object&"
                       "-loc={4}&-filter=120&-objFilter=120&-from="
                       "SkybotDoc&-mime=text\" -O skybot.cat").format(
                           epoch,
                           ra,
                           dec,
                           radius,
                           observatory)

            system(bashcmd)
            skyresult = self.fileops.read_file_as_array("skybot.cat")
            system('rm -rf skybot.cat')
            return (skyresult)

        except Exception as e:
            print(e)

    def radec2wcs(self, ra, dec):

        """
        Converts string RA, DEC coordinates to astropy format.
        @param ra: RA of field center for search, format: degrees or hh:mm:ss
        @type ra: str
        @param dec: DEC of field center for search, format: degrees or hh:mm:ss
        @type dec: str
        @return: list
        """

        try:
            c = coordinates.SkyCoord('{0} {1}'.format(ra, dec),
                                     unit=(u.hourangle, u.deg), frame='fk5')

            return(c)
        except Exception as e:
            pass

    def xy2sky(self, file_name, x, y):

        """
        Converts physical coordinates to WCS coordinates for STDOUT.
        @param file_name: FITS image file name with path.
        @type file_name: str
        @param x: x coordinate of object.
        @type x: float
        @param y: y coordinate of object.
        @type y: float
        @return: str
        """

        try:
            header = fits.getheader(file_name)
            w = WCS(header)
            astcoords_deg = w.wcs_pix2world([[x, y]], 0)
            astcoords = coordinates.SkyCoord(astcoords_deg * u.deg,
                                             frame='fk5')
            alpha = ' '.join(astcoords.to_string(
                style='hmsdms', sep=" ", precision=2)[0].split(" ")[:3])

            delta = ' '.join(astcoords.to_string(
                style='hmsdms', sep=" ", precision=1)[0].split(" ")[3:])

            return("{0} {1}".format(alpha, delta))
        except Exception as e:
            pass

    def xy2sky2(self, file_name, x, y):

        """
        Converts physical coordinates to WCS coordinates for calculations.
        @param file_name: FITS image file name with path.
        @type file_name: str
        @param x: x coordinate of object.
        @type x: float
        @param y: y coordinate of object.
        @type y: float
        @return: list
        """

        try:
            header = fits.getheader(file_name)
            w = WCS(header)
            astcoords_deg = w.wcs_pix2world([[x, y]], 0)

            astcoords = coordinates.SkyCoord(
                astcoords_deg * u.deg, frame='fk5')

            return(astcoords[0])

        except Exception as e:
            pass

    def xy2skywcs(self, file_name, x, y):

        """
        Converts physical coordinates to WCS coordinates
        for STDOUT with wcstools' xy2sky.

        @param file_name: FITS image file name with path.
        @type file_name: str
        @param x: x coordinate of object.
        @type x: float
        @param y: y coordinate of object.
        @type y: float
        @return: str
        """

        try:
            file_path, file_and_ext = path.split(file_name)
            system("xy2sky {0} {1} {2} > {3}/coors".format(
                file_name,
                x,
                y,
                file_path))
            coors = genfromtxt('{0}/coors'.format(file_path),
                               comments='#',
                               invalid_raise=False,
                               delimiter=None,
                               usecols=(0, 1),
                               dtype="U")

            system("rm -rf {0}/coors".format(file_path))

            c = coordinates.SkyCoord('{0} {1}'.format(coors[0], coors[1]),
                                     unit=(u.hourangle, u.deg), frame='fk5')

            alpha = c.to_string(style='hmsdms', sep=" ", precision=2)[:11]
            delta = c.to_string(style='hmsdms', sep=" ", precision=1)[11:]
            
            return('{0} {1}'.format(alpha, delta))
        
        except Exception as e:
            pass

    def xy2sky2wcs(self, file_name, x, y):

        """
        Converts physical coordinates to WCS coordinates for
        calculations with wcstools' xy2sky.
        
        @param file_name: FITS image file name with path.
        @type file_name: str
        @param x: x coordinate of object.
        @type x: float
        @param y: y coordinate of object.
        @type y: float
        @return: str
        """

        try:
            file_path, file_and_ext = path.split(file_name)
            system("xy2sky {0} {1} {2} > {3}/coors".format(
                file_name,
                x,
                y,
                file_path))
            coors = genfromtxt('{0}/coors'.format(file_path),
                               comments='#',
                               invalid_raise=False,
                               delimiter=None,
                               usecols=(0, 1),
                               dtype="U")

            system("rm -rf {0}/coors".format(file_path))

            c = coordinates.SkyCoord('{0} {1}'.format(coors[0], coors[1]),
                                     unit=(u.hourangle, u.deg), frame='fk5')

            return(c)
        except Exception as e:
            pass

    def center_finder(self, file_name):

        """
        It finds image center as WCS coordinates
        @param file_name: FITS image file name with path.
        @type file_name: str
        @return: list
        """

        try:
            self.fitsops = FitsOps()
            naxis1 = self.fitsops.get_header(file_name, "naxis1")
            naxis2 = self.fitsops.get_header(file_name, "naxis2")
            x, y = [float(naxis1) / 2, float(naxis2) / 2]
            coor = self.xy2sky(file_name, x, y)
            ra = ' '.join(coor.split(" ")[:3])
            dec = ' '.join(coor.split(" ")[3:])

            return([ra, dec])
        except Exception as e:
            print(e)

    def solve_field(self,
                    image_path,
                    tweak_order=2,
                    downsample=4,
                    radius=0.5,
                    ra=None,
                    dec=None):

        """
        The astrometry engine will take any image and return
        the astrometry world coordinate system (WCS).
        
        @param image_path: FITS image file name with path
        @type image_path: str
        @param tweak_order: Polynomial order of SIP WCS corrections
        @type tweak_order: integer
        @param downsample: Downsample the image by factor int before
        running source extraction
        @type downsample: integer
        @param radius: Only search in indexes within 'radius' of the
        field center given by --ra and --dec
        @type radius: str
        @param ra: RA of field center for search, format: degrees or hh:mm:ss
        @type ra: str
        @param dec: DEC of field center for search, format: degrees or hh:mm:ss
        @type dec: str
        @return: boolean
        """
    
        try:
            system(("solve-field --no-fits2fits --no-plots "
                    "--no-verify --tweak-order {0} "
                    "--downsample {1} --overwrite --radius {2} --no-tweak "
                    "--ra {3} --dec {4} {5}").format(tweak_order,
                                                     downsample,
                                                     radius,
                                                     ra.replace(" ", ":"),
                                                     dec.replace(" ", ":"),
                                                     image_path))
            # Cleaning
            root, extension = path.splitext(image_path)
            system(("rm -rf {0}-indx.png {0}-indx.xyls "
                    "{0}-ngc.png {0}-objs.png "
                    "{0}.axy {0}.corr "
                    "{0}.match {0}.rdls "
                    "{0}.solved {0}.wcs").format(root))

            if not path.exists(root + '.new'):
                print(image_path + ' cannot be solved!')
                return(False)
            else:
                print('Image has been solved!')
                return(True)
        
        except Exception as e:
            print(e)


class TimeOps:

    def time_stamp(self):

        """
        Returns time stamp as %Y-%m-%IT%H:%M:%S format.
        @return: str
        """

        return str(datetime.utcnow().strftime("%Y-%m-%IT%H:%M:%S"))

    def get_timestamp(self, dt, frmt="%Y-%m-%dT%H:%M:%S.%f"):

        """
        Returns time stamp as %Y-%m-%IT%H:%M:%S format.
        @param dt: Input date
        @type dt: date
        @param frmt: Date format
        @type frmt: str
        @return: date
        """

        try:
            if len(dt) == 19:
                frmt = "%Y-%m-%dT%H:%M:%S"
            
            t = datetime.strptime(dt, frmt)
            return(t)
        except Exception as e:
            print(e)

    def get_timestamp_exp(self, file_name, dt="date-obs", exp="exptime"):

        """
        Returns FITS file's date with exposure time included.
        @param file_name: FITS image file name with path
        @type file_name: str
        @param dt: DATE-OBS keyword
        @type dt: str
        @param exp: Exposure time keyword
        @type exp: str
        @return: date
        """

        fitsops = FitsOps()
        expt = fitsops.get_header(file_name, exp)
        dat = fitsops.get_header(file_name, dt)
        tmstamp = self.get_timestamp(dat)
        ret = tmstamp + timedelta(seconds=float(expt) / 2)

        return(ret)

    def date2jd(self, dt):

        """
        Converts date to Julian Date.
        @param dt: Date
        @type dt: str
        @return: float
        """

        # 2015-03-08 23:10:01.890000
        date_t = str(dt).replace(" ", "T")
        t_jd = Time(date_t, format='isot', scale='utc')

        return(t_jd.jd)

    def convert_time_format(self, timestamp):

        """
        Converts date to MPC date format in MPC report file.
        @param timestamp: Date
        @type timestamp: date
        @return: str
        """

        try:
            y = timestamp.year
            m = timestamp.month
            d = timestamp.day

            h = timestamp.hour
            M = timestamp.minute
            s = timestamp.second

            cday = d + float(h) / 24 + float(M) / 1440 + float(s) / 86400

            if d >= 10:
                ret = "C{} {:02.0f} {:.5f}".format(y, float(m), float(cday))
            else:
                ret = "C{} {:02.0f} 0{:.5f}".format(y, float(m), float(cday))

            return(ret)

        except Exception as e:
            print(e)
