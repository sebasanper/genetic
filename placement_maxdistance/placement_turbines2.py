from random import randint
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from time import time
from PNPOLY import pnpoly
from math import sqrt, floor, ceil

from ray_crossing_polygon_test import Point, Polygon
def place_turbines():
    q = Polygon([Point(424386.,	6147543.),
                 Point(423974., 6151447.),
                 Point(429014.,	6151447.),
                 Point(429431.,	6147543.)])
# 484178.55, 5732482.8], [500129.9, 5737534.4], [497318.1, 5731880.24], [491858.00, 5725044.75]], [[491858.00, 5725044.75], [497318.1, 5731880.24], [503163.37, 5729155.3], [501266.5, 5715990.05
    r = Polygon([Point(484178.55, 5732482.8),
                 Point(500129.9, 5737534.4),
                 Point(497318.1, 5731880.24),
                 Point(503163.37, 5729155.3), 
                 Point(501266.5, 5715990.05)])

    # Test 1: Point inside of polygon
    # p1 = Point(90, 118)
    # print q.contains(p1)

    nvert = 5
    vertx = [484178.55, 500129.9, 497318.1, 503163.37, 501266.5]
    verty = [5732482.8, 5737534.4, 5731880.24, 5729155.3, 5715990.05]

    inside = []
    plot_data = open("data.dat", "w")
    for i in range(int(floor(min(vertx))), int(ceil(max(vertx))), 10):
        for j in range(int(floor(min(verty))), int(ceil(max(verty))), 10):
            # a = q.contains(Point(i, j))
            if pnpoly(nvert, vertx, verty, i, j):
                inside.append((i, j))


    # for i in range(19, 151):
    #     for j in range(9, 126):
    #         a = q.contains(Point(i, j))
    #         if a:
    #             inside.append((i, j))

    k = len(inside)
    h = randint(0, k - 1)
    points = [inside[h]]
    # plot_data.write("{0:d}\t{1:d}\t{2:d}\n".format(points[-1][0], points[-1][1], 0))

    for nt in range(1, 74):
        dist = []
        i = 0
        for item in inside:
            min_distance = 999999999999999999
            for point in points:
                distance = abs(item[0] - point[0]) + abs(item[1] - point[1])
                if distance < min_distance:
                    min_distance = distance
            dist.append((min_distance, i))
            i += 1

        next = inside[max(dist)[1]]
        plot_data.write("{0}\t{1}\t{2}\n".format(next[0], next[1], nt))
        points.append(next)
        inside.remove(next)

    return points
# plot_data.close()
# print "Final time is " + str(time() - start) + "s"

if __name__ == '__main__':
    points = place_turbines()

    verts = [(484178.55, 5732482.8),
                 (500129.9, 5737534.4),
                 (497318.1, 5731880.24),
                 (503163.37, 5729155.3), 
                 (501266.5, 5715990.05)]

    codes = [Path.MOVETO,
             Path.LINETO,
             Path.LINETO,
             Path.LINETO,
             Path.CLOSEPOLY,
             ]

    path = Path(verts, codes)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    patch = patches.PathPatch(path, facecolor='orange', lw=2)
    ax.add_patch(patch)
    ax.set_xlim(484178.55, 503163.37)
    ax.set_ylim(5715990.05, 5737534.4)
    toplot_x, toplot_y = zip(*points)
    plt.plot(toplot_x, toplot_y, 'ro')
    plt.show()
