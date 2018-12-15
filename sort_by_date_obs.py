import os
import sys
import glob
from astrolib import astronomy


fitsdir = sys.argv[1]

types = (fitsdir + '/*.fits', fitsdir + '/*.fit', fitsdir + '/*.fts')  # the tuple of file types
fits_grabbed = []
for fits_files in types:
    fits_grabbed.extend(glob.glob(fits_files))

if len(sorted(fits_grabbed)) < 4:
    print('Please provide at least 3 FITS images to the {0}'.format(fitsdir))
    raise SystemExit

for fits_files in sorted(fits_grabbed):
    fo = astronomy.FitsOps(fits_files)
    date_obs = str(fo.get_header("date-obs")).replace(".", "")

    if "T" not in date_obs:
        time_obs = str(fo.get_header("time-obs")).replace(".", "")
        time_obs = time_obs.replace(":", "")
        fltr = str(fo.get_header("filter")).strip()
        date_obs = "{0}T{1}".format(date_obs.strip(),
                                    time_obs.strip())

    print(">>> mv: {0} > {1}/{2}{3}.fits".format(fits_files, fitsdir, date_obs, fltr))
    os.system("mv {0} {1}/{2}{3}.fits".format(fits_files, fitsdir, date_obs, fltr))