# -*- coding: utf-8 -*-
# Authors: Yücel Kılıç
# This is an open-source software licensed under GPLv3.


try:
    import numpy as np
except ImportError:
    print('Python cannot import numpy. Make sure numpy is installed.')
    raise SystemExit

try:
    import pandas as pd
except ImportError:
    print('Python cannot import pandas. Make sure pandas is installed.')
    raise SystemExit

try:
    import sources
except ImportError:
    print('Python cannot import sources.py. Make sure sources.py is in',
          'the same folder as mod.py.')
    raise SystemExit

try:
    import asteroids
except ImportError:
    print('Python cannot import asteroids.py. Make sure asteroids.py is in',
          'the same folder as mod.py.')
    raise SystemExit

try:
    import visuals
except ImportError:
    print('Python cannot import visuals.py. Make sure visuals.py is in',
          'the same folder as mod.py.')
    raise SystemExit

import sys
import time
import os
import glob


if __name__ == '__main__':

    start = time.time()

    try:
        fitsdir, reference = sys.argv[1], sys.argv[2]
    except:
        print('Usage error!')
        print('Usage: python3 mod.py <fits_dir> <ref_image> [ds9]')

    outdir = fitsdir + '/modpy'

    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    print('\nAligning images...', end=' ')
    sources.align(fitsdir, reference, outdir)
    elapsed = int(time.time() - start)
    print('Complete!')
    print('Aligned images are saved as *affineremap.fits.')
    print('Elapsed time: {0} min {1} sec.'.format(elapsed // 60, elapsed % 60))

    print('\nCreating catalog files...', end=' ')
    sources.make_catalog(outdir, outdir)
    elapsed = int(time.time() - start)
    print('Complete!')
    print('Catalog files are saved as *affineremap.pysexcat.')
    print('Elapsed time: {0} min {1} sec.'.format(elapsed // 60, elapsed % 60))

    print('\nBuilding master catalog file...', end=' ')
    sources.make_master(outdir)
    elapsed = int(time.time() - start)
    print('Complete!')
    print('Master catalog file is saved as master.pysexcat.')
    print('Elapsed time: {0} min {1} sec.'.format(elapsed // 60, elapsed % 60))

    print('\nDetecting candidates...', end=' ')
    asteroids.all_candidates(outdir, outdir)
    elapsed = int(time.time() - start)
    print('Complete!')
    print('Candidates for each image are saved as *affineremap.cnd.')
    print('Elapsed time: {0} min {1} sec.'.format(elapsed // 60, elapsed % 60))

    print('\nDetecting moving objects...\n')
    lines = asteroids.detect_lines(outdir, fitsdir)

    if len(lines) == 0:
        print('modpy could not find any moving objects in the images.')
        raise SystemExit

    fast_objects, slow_objects = asteroids.results(fitsdir, lines)
    pd.set_option('expand_frame_repr', False)
    COLUMNS = ['FileID', 'Flags', 'x', 'y', 'Flux', 'Background', 'ObjectID',
               'Speed(px/min)']

    elapsed = int(time.time() - start)
    print('\nMoving object detection completed.')
    print('Elapsed time: {0} min {1} sec.'.format(elapsed // 60, elapsed % 60))

    if fast_objects.size:

        fast_objects = pd.DataFrame.from_records(fast_objects, columns=COLUMNS)
        print('\nFAST MOVING OBJECTS:\n')
        print(fast_objects)

    if slow_objects.size:

        slow_objects = pd.DataFrame.from_records(slow_objects, columns=COLUMNS)
        print('\nSLOW MOVING OBJECTS:\n')
        print(slow_objects)

    print()

#    print('Creating png files...')
#
#    if fast_objects.size and slow_objects.size:
#        objects = np.concatenate((fast_objects, slow_objects), axis=0)
#    elif not fast_objects.size and slow_objects.size:
#        objects = slow_objects
#    elif not slow_objects.size and fast_objects.size:
#        objects = fast_objects
#
#    images = sorted(glob.glob(fitsdir + '/*.fits'))
#
#    for i, image in enumerate(images):
#        visuals.fits2png(image, outdir,
#                         objects[objects[:, 0].astype(int) == i])
#        print('{0} converted.'.format(image))
#
#    elapsed = int(time.time() - start)
#    print('png conversion completed.')
#    print('Elapsed time: {0} min {1} sec.'.format(elapsed // 60, elapsed % 60))
#
#
#    elif sys.argv[1] == '-fits2png' and len(sys.argv) == 4:
#        '''
#        Converts FITS images into PNG files.
#        Usage: python asterotrek.py -fits2png <image(s)> <outdir>
#        '''
#        try:
#            print 'Please wait until processing is complete.'
#            f2n = visuals.Plot()
#
#            if os.path.isdir(sys.argv[2]):
#                for image in sorted(glob.glob('%s/*.fits' %(sys.argv[2]))):
#                    f2n.fits2png(image, sys.argv[3])
#                    print '%s converted into %s.' %(image, sys.argv[3])
#            elif os.path.isfile(sys.argv[2]):
#                f2n.fits2png(sys.argv[2], sys.argv[3])
#                print '%s converted into %.' %(sys.argv[2], sys.argv[3])
#            print 'Converted all FITS files to PNG files.'
#            print 'Elapsed time: %s min. %s sec.' %(int((time.time() - start) / 60), '%.2f' % ((time.time() - start) % 60))
#        except:
#            print 'Usage error!'
#            print 'Usage: python asterotrek.py -fits2png <image(s)> <outdir>' 
#            raise SystemExit
#
#    elif sys.argv[1] == '-plot2ds9' and len(sys.argv) == 4:
#        '''
#        Plots catalogue files into ds9.
#        Usage: python asterotrek.py -plot2ds9 <image> <catfile>    		
#        '''
#        try:
#            print 'Please wait until processing is complete.'
#            p2ds9 = visuals.Plot()
#            p2ds9.plot2ds9(sys.argv[2], sys.argv[3])
#            print 'Elapsed time: %s min. %s sec.' %(int((time.time() - start) / 60), '%.2f' % ((time.time() - start) % 60))
#        except:
#            print 'Usage error!'
#            print 'Usage: python asterotrek.py -fits2png <image(s)> <outdir>' 
#            raise SystemExit
#    elif sys.argv[1] == '-makegif':
#        '''
#        Converts PNG images to animated GIF file.
#        Usage: python asterotrek.py -makegif <PNG(s)> <outdir>    		
#        '''
#        try:
#            print 'Please wait until processing is complete.'
#            os.popen('convert -delay 20 -loop 0 %s/*.png %s/%s.gif' %(sys.argv[2], sys.argv[2], sys.argv[3]))
#            '%.2f' % 3.14159
#            print 'Elapsed time: %s min. %s sec.' %(int((time.time() - start) / 60), '%.2f' % ((time.time() - start) % 60))
#        except:
#            print 'Usage error!'
#            print 'python asterotrek.py -makegif <PNG(s)> <outdir>' 
#            raise SystemExit
