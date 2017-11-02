import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from ray_crossing_polygon_test import Point, Polygon
from time import time

def pnpoly(nvert, vertx, verty, testx, testy):
    c = False
    j = nvert - 1
    for i in range(nvert):
        if ((verty[i] > testy) != (verty[j] > testy)) and (testx < (vertx[j] - vertx[i]) * (testy - verty[i]) / (verty[j] - verty[i]) + vertx[i]):
            c = not c
        j = i
    return c

# print pnpoly(4, [0., 0., 100., 100.], [0., 100., 100., 0.], 0., 10.)

if __name__ == "__main__":

    nvert = 4
    vertx = [20., 50., 125., 150.]
    verty = [10., 125., 90., 10.]

    q = Polygon([Point(20., 10.),
                 Point(50., 125.),
                 Point(125., 90.),
                 Point(150., 10.)])

    output = open("inside_short.dat", "w")
    start = time()
    for i in range(160):
        for j in range(135):
            output.write("{0:d}\t{1:d}\t{2:d}\t{3:d}\n".format(i, j, pnpoly(nvert, vertx, verty, i, j), q.contains(Point(i, j))))
    output.close()
    print "short"
    print time() - start

    # plot_data = open("inside_long.dat", "w")
    # start2 = time()
    # for i in range(160):
    #     for j in range(135):
    #         plot_data.write("{0:d}\t{1:d}\t{2:d}\n".format(i, j, q.contains(Point(i, j))))
    # plot_data.close()
    # print "long"
    # print time() - start2

    # Plot ------------------------------------------------------------------
    # verts = [(20, 10),
    #          (50, 125),
    #          (125, 90),
    #          (150, 10),
    #          (150, 10)
    #          ]
    # codes = [Path.MOVETO,
    #          Path.LINETO,
    #          Path.LINETO,
    #          Path.LINETO,
    #          Path.CLOSEPOLY,
    #          ]
    #
    # path = Path(verts, codes)
    #
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # patch = patches.PathPatch(path, facecolor='orange', lw=2)
    # ax.add_patch(patch)
    # ax.set_xlim(10, 160)
    # ax.set_ylim(0, 135)
    # plt.plot([20, 130, 35, 50], [50, 80, 90, 10], 'ro')
    # plt.show()