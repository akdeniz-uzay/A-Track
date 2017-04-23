# -*- coding: utf-8 -*-
from mpcreporter import ast
from mpcreporter import env

import sys
import os

efile_op = env.file_op(verb=True)

afile_tp = ast.dt_op(verb=True)
afits_op = ast.fits_op(verb=True)
amag_op = ast.mag_op(verb=True)
aonline_op = ast.online_op(verb=True)
alin_op = ast.linear_op(verb=True)

images_dir = sys.argv[1]
the_res_file = sys.argv[2]

magnitude = 20.5
radius = 14.84
output = "./mpc_out.txt"
database = "/Users/ykilic/Documents/playground/mpc_reporter/data/MPCORB.DAT"
observatory = "A84"

print("Analysing A-Track result file...")

my_files = efile_op.get_file_list(images_dir)
res_file = efile_op.read_res(the_res_file)

ra = afits_op.get_header(my_files[0], "objctra")
dec = afits_op.get_header(my_files[0], "objctdec")

solve_wcs = afits_op.solve_field(my_files[0], ra=ra, dec=dec)
root, extension = os.path.splitext(my_files[0])
wcs_file = "./" + root + ".new"

observer = afits_op.get_header(my_files[0], "observer")
telescope = afits_op.get_header(my_files[0], "telescop")
contact = "yucelkilic@myrafproject.org"
catalog = "GAIA"

print("--------------------MPC Report File----------------------------------")

h = afits_op.return_out_file_header(obs=observer, tel=telescope,
                                    cod=observatory,
                                    contact=contact,
                                    catalog=catalog)

out_file = open(output, "w")
out_file.write("%s\n" % (h))
print(h)
for i in res_file:
    theid, frame, x, y, flux = i

    coors = afits_op.xy2sky(wcs_file, x, y)
    coors2 = afits_op.xy2sky2(wcs_file, x, y)
    coors2ra = coors2.ra.degree[0]
    coors2dec = coors2.dec.degree[0]

    fltr = afits_op.get_header(my_files[int(frame)],
                               "filter").replace(" ", "_")

    tm = afile_tp.get_timestamp_exp(my_files[int(frame)])
    tmm = afile_tp.convert_time_format(tm)

    mag = amag_op.flux2mag(flux)

    ccoor = afits_op.center_finder(wcs_file)

    namesky = aonline_op.find_skybot_objects(tm, coors2ra, coors2dec)

    for u in range(len(namesky)):
        justID = namesky[u][0]

        if alin_op.is_object(afits_op.radec2wcs(namesky[u][2],
                                                namesky[u][3]),
                             coors2):
            print("%s         %s %s          %s %s      %s" % (
                efile_op.find_if_in_database_id(database, justID),
                tmm, coors, mag, fltr, observatory))
            out_file.write("%s         %s %s          %s %s      %s\n" % (
                efile_op.find_if_in_database_id(database, justID),
                tmm, coors, mag, fltr, observatory))
            break
        else:
            p = "*NO%02.f         %s %s          %s %s      %s" % (
                theid, tmm, coors, mag, fltr, observatory)
            print(p)
            out_file.write("%s\n" % (p))
            break
print("----- end -----")
out_file.write("----- end -----")
out_file.close()
