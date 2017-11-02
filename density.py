__author__ = 'sebasanper'

data = open('last_best.dat', 'r')
hist = open('density.dat', 'w')
x = []
y = []
x_res = 9
y_res = 9
for line in data:
    columns = line.split()
    x.append(float(columns[0]))
    y.append(float(columns[1]))

x_min = 0.0
x_max = 5457.0
y_min = 0.0
y_max = 3907.0

delta_x = (x_max - x_min) / float(x_res)
delta_y = (y_max - y_min) / float(y_res)

histogram = [[0 for h in range(x_res)] for g in range(y_res)]

for i in range(x_res):
    for j in range(y_res):
        for turb in range(len(x)):
            if x[turb] >= x_min + (float(i)) * delta_x and x[turb] < x_min + (float(i + 1)) * delta_x:
                if y[turb] >= y_min + (float(j)) * delta_y and y[turb] < y_min + (float(j + 1)) * delta_y:
                    histogram[i][j] += 1

for j in range(x_res):
    for i in range(y_res):
        hist.write('{0:d} '.format(histogram[i][j]))
    hist.write('\n')

hist.close()
data.close()