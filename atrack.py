# -*- coding: utf-8 -*-
# Authors: Yücel Kılıç, Murat Kaplan, Nurdan Karapınar, Tolga Atay.
# This is an open-source software licensed under GPLv3.

try:
    import pandas as pd
except ImportError:
    print('Python cannot import pandas. Make sure pandas is installed.')
    raise SystemExit

try:
    import sources
except ImportError:
    print('Python cannot import sources.py. Make sure sources.py is in',
          'the same folder as atrack.py.')
    raise SystemExit

try:
    import asteroids
except ImportError:
    print('Python cannot import asteroids.py. Make sure asteroids.py is in',
          'the same folder as atrack.py.')
    raise SystemExit

try:
    import visuals
except ImportError:
    print('Python cannot import visuals.py. Make sure visuals.py is in',
          'the same folder as atrack.py.')
    raise SystemExit

import time
import os
import glob
import argparse
from mpcreporter import ast
from mpcreporter import env

from configparser import ConfigParser

config = ConfigParser()

if os.path.exists('./atrack.config'):
    config.read('./atrack.config')
else:
    print('Python cannot open the configuration file. Make sure atrack.config',
          'is in the same folder as atrack.py.')
    raise SystemExit

if __name__ == '__main__':

    start = time.time()
    parser = argparse.ArgumentParser(prog='python3 atrack.py',
                                     description='A-Track.')
    parser.add_argument('fits_dir',
                        help='FITS image directory')
    parser.add_argument('--ref',
                        type=str,
                        metavar='ref_image',
                        help='reference FITS image for alignment (with path)')
    parser.add_argument('--skip-align',
                        action='store_true',
                        help='skip alignment if alignment is already done')
    parser.add_argument('--skip-cats',
                        action='store_true',
                        help='skip creating catalog files ' +
                        'if they are already created')
    parser.add_argument('--skip-mpcreport',
                        action='store_true',
                        help='skip creating MPC file')
    parser.add_argument('--skip-pngs',
                        action='store_true',
                        help='skip creating PNGs')
    parser.add_argument('--skip-gif',
                        action='store_true',
                        help='skip creating animation file')
    parser.add_argument('--version',
                        action='version',
                        help='show version',
                        version='A-Track version 1.0')

    arguments = parser.parse_args()
    fitsdir, reference = arguments.fits_dir, arguments.ref

    outdir = fitsdir + '/atrack'

    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    if not arguments.skip_align:
        print('\nAligning images...', end=' ')
        sources.align(fitsdir, reference, outdir)
        elapsed = int(time.time() - start)
        print('Complete!')
        print('Aligned images are saved as *affineremap.fits.')
        print('Elapsed time: {0} min {1} sec.'
              .format(elapsed // 60, elapsed % 60))

    if not arguments.skip_cats:
        print('\nCreating catalog files...', end=' ')
        sources.make_catalog(outdir, outdir)
        elapsed = int(time.time() - start)
        print('Complete!')
        print('Catalog files are saved as *affineremap.pysexcat.')
        print('Elapsed time: {0} min {1} sec.'
              .format(elapsed // 60, elapsed % 60))

    print('\nBuilding master catalog file...', end=' ')
    sources.make_master(outdir)
    elapsed = int(time.time() - start)
    print('Complete!')
    print('Master catalog file is saved as master.pysexcat.')
    print('Elapsed time: {0} min {1} sec.'
          .format(elapsed // 60, elapsed % 60))

    print('\nDetecting candidates...', end=' ')
    asteroids.all_candidates(outdir, outdir)
    elapsed = int(time.time() - start)
    print('Complete!')
    print('Candidates for each image are saved as *affineremap.cnd.')
    print('Elapsed time: {0} min {1} sec.'.format(elapsed // 60, elapsed % 60))

    print('\nDetecting moving objects...\n')
    lines = asteroids.detect_lines(outdir, fitsdir)

    if len(lines) == 0:
        print('A-Track could not find any moving objects in the images.')
        raise SystemExit

    moving_objects, uncertain_objects = asteroids.results(fitsdir, lines)
    pd.set_option('expand_frame_repr', False)
    COLUMNS = ['FileID', 'Flags', 'x', 'y', 'Flux', 'Background', 'ObjectID',
               'Speed(px/min)']
    NEWCOLS = ['ObjectID', 'FileID', 'Flags', 'x', 'y', 'Flux', 'Background',
               'Speed(px/min)']

    elapsed = int(time.time() - start)
    print('\nMoving object detection completed.')
    print('Elapsed time: {0} min {1} sec.'.format(elapsed // 60, elapsed % 60))

    if moving_objects.size:

        moving_objects = pd.DataFrame.from_records(moving_objects,
                                                   columns=COLUMNS)
        moving_objects = moving_objects.reindex_axis(NEWCOLS, axis=1)
        moving_objects[['FileID',
                        'Flags',
                        'ObjectID']] = moving_objects[['FileID',
                                                       'Flags',
                                                       'ObjectID']].astype(int)
        with open('{0}/results.txt'.format(outdir), 'w') as f:
            s = moving_objects.to_string(justify='center', index=False)
            print('========================================================\n')
            print('MOVING OBJECTS:\n')
            print(s)
            f.write('# MOVING OBJECTS:\n')
            f.write(s)

    if uncertain_objects.size:

        uncertain_objects = pd.DataFrame.from_records(uncertain_objects,
                                                      columns=COLUMNS)
        uncertain_objects = uncertain_objects.reindex_axis(NEWCOLS, axis=1)
        uncertain_objects[['FileID',
                           'Flags',
                           'ObjectID']] = uncertain_objects[[
                               'FileID',
                               'Flags',
                               'ObjectID']].astype(int)
        with open('{0}/results.txt'.format(outdir), 'a') as f:
            f.write('\n\n')
            s = uncertain_objects.to_string(justify='center', index=False)
            print('\nUNCERTAIN OBJECTS:\n')
            print(s)
            f.write('# UNCERTAIN OBJECTS:\n')
            f.write(s)

    try:
        n_moving = len(moving_objects.ObjectID.unique())

    except AttributeError:
        n_moving = 0

    try:
        n_uncertain = len(uncertain_objects.ObjectID.unique())

    except AttributeError:
        n_uncertain = 0

    print('\nA-Track has detected',
          n_moving, 'moving objects and',
          n_uncertain,
          'uncertain objects.')

    if not arguments.skip_mpcreport:
        efile_op = env.file_op(verb=True)

        afile_tp = ast.dt_op(verb=True)
        afits_op = ast.fits_op(verb=True)
        amag_op = ast.mag_op(verb=True)
        aonline_op = ast.online_op(verb=True)
        alin_op = ast.linear_op(verb=True)

        images_dir = outdir
        the_res_file = "{0}/results.txt".format(outdir)

        magnitude = float(config.get('mpcreport', 'LIM_MAG'))
        radius = float(config.get('mpcreport', 'RADIUS'))
        output = "{0}/mpc_out.txt".format(outdir)
        database = config.get('mpcreport', 'MPC_DATABASE_PATH')
        observatory = config.get('mpcreport', 'OBSERVATORY')

        print("Analysing A-Track result file...")

        my_files = efile_op.get_file_list(images_dir)
        res_file = efile_op.read_res(the_res_file)

        ra = afits_op.get_header(my_files[0],
                                 config.get('mpcreport',
                                            'RA'))
        dec = afits_op.get_header(my_files[0],
                                  config.get('mpcreport',
                                             'DEC'))

        solve_wcs = afits_op.solve_field(my_files[0],
                                         ra=ra,
                                         dec=dec)

        if not solve_wcs:
            raise SystemExit

        root, extension = os.path.splitext(my_files[0])
        wcs_file = root + ".new"

        observer = afits_op.get_header(my_files[0],
                                       config.get('mpcreport', 'OBSERVER'))
        telescope = afits_op.get_header(my_files[0],
                                        config.get('mpcreport', 'TELESCOPE'))
        contact = config.get('mpcreport', 'CONTACT')
        catalog = config.get('mpcreport', 'CATALOG')

        print("----------------MPC Report File-----------------------")

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

            # ccoor = afits_op.center_finder(wcs_file)

            namesky = aonline_op.find_skybot_objects(tm,
                                                     coors2ra,
                                                     coors2dec)
            # print(namesky)

            for u in range(len(namesky)):
                # justID = namesky[u][0]
                justname = namesky[u][1]

                if alin_op.is_object(afits_op.radec2wcs(namesky[u][2],
                                                        namesky[u][3]),
                                     coors2):
                    mpcname = efile_op.find_if_in_database_name(database,
                                                                justname)
                    if len(mpcname) == 5:
                        spc = "         "
                    elif len(mpcname) > 5:
                        spc = "  "

                    print("%s%s%s %s          %s %s      %s" % (mpcname,
                                                                spc,
                                                                tmm,
                                                                coors,
                                                                mag,
                                                                fltr,
                                                                observatory))
                    out_file.write("%s%s%s %s          %s %s      %s\n" % (
                        mpcname,
                        spc,
                        tmm,
                        coors,
                        mag,
                        fltr,
                        observatory))
                    break
                else:
                    p = "       NO%03.f* %s %s          %s %s      %s" % (
                        theid, tmm, coors, mag, fltr, observatory)
                    print(p)
                    out_file.write("%s\n" % (p))
                    break
        print("----- end -----")
        out_file.write("----- end -----")
        out_file.close()

    if not arguments.skip_pngs:
        print('\nCreating PNG files...\n')

        if moving_objects.size and uncertain_objects.size:
            objects = pd.concat((moving_objects, uncertain_objects), axis=0,
                                ignore_index=True)
        elif not moving_objects.size and uncertain_objects.size:
            objects = uncertain_objects
        elif not uncertain_objects.size and moving_objects.size:
            objects = moving_objects

        images = sorted(glob.glob(outdir + '/*affineremap.fits'))

        for i, image in enumerate(images):
            asteroid = objects[objects['FileID'] == i]
            visuals.fits2png(image, outdir, asteroid)
            print('{0} converted to png.'.format(image))

        elapsed = int(time.time() - start)
        print('\nPNG conversion completed.')
        print('Elapsed Time: {0} min {1} sec.'
              .format(elapsed // 60, elapsed % 60))

        if not arguments.skip_gif:
            print('\nCreating GIF (animation) file...')
            os.popen('convert -delay 20 -loop 0 ' +
                     '{0}/*.png {0}/animation.gif'.format(outdir))
            print('{0}/animation.gif created.'.format(outdir))
    print('Elapsed Time: {0} min {1} sec.'.format(elapsed // 60, elapsed % 60))
    print()
