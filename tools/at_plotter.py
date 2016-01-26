
# -*- coding: utf-8 -*-
# Authors: Yücel Kılıç, Murat Kaplan, Nurdan Karapınar, Tolga Atay.
# This is an open-source software licensed under GPLv3.
# Last Edit: 27 Jan 2016 00:20

'''Plot A-Track Result.
Usage:
    at_plotter.py <result_file> <interval>
    at_plotter.py (-h | --help)
    at_plotter.py --version

Options:
    -h --help             Show this screen.
    --version             Show version.
    <result_file>         A-Track result file
    <interval>            Interval for points
'''

try:
    from docopt import docopt, DocoptExit
except:
    print('Python cannot import docopt. Make sure docopt is installed.')
    raise SystemExit

import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    arguments = docopt(__doc__, version='at-plotter.py 0.1-dev')

    try:
        result_file, interval = (arguments['<result_file>'],
                                 int(arguments['<interval>']))
    except DocoptExit as e:
        print('Usage error!')
        print(e)

    plt.figure(figsize=(10, 10), facecolor='white', edgecolor='red')

    data = np.genfromtxt(result_file, comments=' ObjectID')
    cdata = []

    for i in range(1, len(np.unique(data[:, 0])) + 1):
        line = data[(data[:, 0] == i)]
        for j, row in enumerate(line):
            operatorx = line[0, 3] - line[len(line) - 1, 3]
            operatory = line[0, 4] - line[len(line) - 1, 4]
            if operatorx > 0:
                operatorx = -1
            else:
                operatorx = +1

            if operatory > 0:
                operatory = -1
            else:
                operatory = +1

            line[j, 3] = row[3] + j * interval * operatorx
            line[j, 4] = row[4] + j * interval * operatory
        cdata = cdata + line.tolist()

    adata = np.array(cdata)
    filled_markers = ['o', 'v', 's', 'p', '*', 'h', 'H', 'D', 'd']

    for fileid in np.unique(data[:, 1]):
        fdata = adata[adata[:, 1] == fileid]
        plt.scatter(fdata[:, 3], fdata[:, 4], s=50, c=np.random.rand(3, 1),
                    marker=filled_markers[int(fileid) % len(filled_markers)],
                    label='Frame ' + str(int(fileid)))

    plt.legend(loc=2)

    for k in range(1, len(np.unique(adata[:, 0])) + 1):
        line = adata[(adata[:, 0] == k)]
        operatorx = line[0, 3] - line[len(line) - 1, 3]
        operatory = line[0, 4] - line[len(line) - 1, 4]
        if operatorx > 0:
            operatorx = -1
        else:
            operatorx = +1

        if operatory > 0:
            operatory = -1
        else:
            operatory = +1

        plt.arrow(line[0, 3] - interval * operatorx,
                  line[0, 4] - interval * operatory,
                  line[len(line) - 1, 3] - line[0, 3] +
                  interval * operatorx * 2,
                  line[len(line) - 1, 4] - line[0, 4] +
                  interval * operatory * 2,
                  head_width=20,
                  head_length=20,
                  fc='k', ec='k')

        if line[0, 7] < 0.1:
            tc = 'red'
        else:
            tc = 'lime'

        plt.annotate('ObjectID {0}'.format(str(k)),
                     xy=(line[0, 3], line[0, 4]),
                     xytext=(10, 0),
                     textcoords='offset points', color=tc)

    plt.xlim([0, 2048])
    plt.ylim([0, 2048])
    plt.title('A-Track v1.0 - Detected Asteroids')
    plt.xlabel("X_IMAGE (px)")
    plt.ylabel("Y_IMAGE (px)")
    ax = plt.gca()
    ax.set_aspect('equal', 'datalim')

    plt.show()

    '''
    plt.savefig()
    '''
