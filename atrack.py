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
            print('\nMOVING OBJECTS:\n')
            print(s)
            f.write('MOVING OBJECTS:\n\n')
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
            f.write('UNCERTAIN OBJECTS:\n\n')
            f.write(s)

    n_moving = len(moving_objects.ObjectID.unique())
    n_uncertain = len(uncertain_objects.ObjectID.unique())
    print('\nA-Track has detected', n_moving, 'moving objects and', n_uncertain,
          'uncertain objects.')

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
