from random import randint
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from time import time
from PNPOLY import pnpoly
from math import sqrt

from ray_crossing_polygon_test import Point, Polygon

q = Polygon([Point(424386.,	6147543.),
             Point(423974., 6151447.),
             Point(429014.,	6151447.),
             Point(429431.,	6147543.)])

r = Polygon([Point(0., 0.),
             Point(0., 100.),
             Point(100., 100.),
             Point(100., 0.)])

# Test 1: Point inside of polygon
# p1 = Point(90, 118)
# print q.contains(p1)

nvert = 4
vertx = [424386., 423974, 429014., 429431.]
verty = [6147543., 6151447., 6151447., 6147543.]

inside = []
plot_data = open("data.dat", "w")
start = time()
for i in range(423974, 429431, 80):
    for j in range(6147543, 6151447, 80):
        # a = q.contains(Point(i, j))
        a = pnpoly(nvert, vertx, verty, i, j)
        if a:
            inside.append((i, j))

print "make inside mesh time is " + str(time() - start) + "s"

# for i in range(19, 151):
#     for j in range(9, 126):
#         a = q.contains(Point(i, j))
#         if a:
#             inside.append((i, j))

k = len(inside)
h = randint(0, k - 1)
points = [inside[h]]
plot_data.write("{0:d}\t{1:d}\t{2:d}\n".format(points[-1][0], points[-1][1], 0))

print "First point is: " + str(points)

for nt in range(1, 160):
    dist = []
    i = 0
    for item in inside:
        total_distance = []
        for point in points:
            total_distance.append(sqrt((item[0] - point[0]) ** 2.0 + (item[1] - point[1]) ** 2.0))
        min_distance = min(total_distance)
        dist.append((min_distance, i))
        i += 1

    next = inside[max(dist)[1]]

    plot_data.write("{0:d}\t{1:d}\t{2:d}\n".format(next[0], next[1], nt))
    points.append(next)
    inside.remove(next)

plot_data.close()
print "Final time is " + str(time() - start) + "s"

verts = [(424386.,	6147543.),
         (423974., 6151447.),
         (429014.,	6151447.),
         (429431.,	6147543.),
         (424386.,	6147543.)
         ]

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
ax.set_xlim(423974, 429431)
ax.set_ylim(6147543, 6151447)
toplot_x, toplot_y = zip(*points)
plt.plot(toplot_x, toplot_y, 'ro')
plt.show()
