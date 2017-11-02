# __author__ = 'sebasanper'
from __future__ import print_function
from openmdao.core.component import Component
from openmdao.core.problem import Problem, Group
from openmdao.components.paramcomp import ParamComp
import time
from random import randint
import numpy as np


class JensenModel(Component):

    def __init__(self):
        super(JensenModel, self).__init__()

        self.add_param('a', shape=(80, 2))

        self.add_output('eff', shape=1)

    def solve_nonlinear(self, params, unknowns, resids):

        a = params['a']

        from math import sqrt, log
        import wake
        windrose = open('horns_rev_windrose2.dat', 'r')
        nt = 80
        layout_x = [0.0 for x in range(nt)]
        layout_y = [0.0 for x in range(nt)]
        for x in range(nt):
            layout_x[x] = float(a[x][0])
            layout_y[x] = float(a[x][1])

        windrose_angle = []
        windrose_speed = []
        windrose_frequency = []
        for line in windrose:
            columns = line.split()
            windrose_angle.append(float(columns[0]))
            windrose_speed.append(float(columns[1]))
            windrose_frequency.append(float(columns[2]))

        windrose.close()
        summation = 0.0

        def Ct(U0):
            return 0.0001923077 * U0 ** 4.0 + -0.0075407925 * U0 ** 3.0 + 0.096462704 * U0 ** 2.0 - 0.5012354312 * U0 + 1.7184749184

        def power(U0):
            if U0 < 4.0:
                return 0.0
            elif U0 >= 4.0:
                return 19.7907842158 * U0 ** 2.0 - 74.9080669331 * U0 + 37.257967033  # From 4 to 11 m/s

        for wind in range(0, len(windrose_speed)):
        # for wind in range(0, 1):
            U1 = windrose_speed[wind]  # Free stream wind speed
            U0 = U1 * (70.0 / 10.0) ** 0.11  # Power or log law for wind shear profile
            # U0 = U1 * log(70.0 / 0.005) / log(10.0 / 0.005)
            k = 0.04  # Decay constant
            r0 = 40.0  # Turbine rotor radius
            angle = windrose_angle[wind]
            angle3 = angle + 180.0
            wake_deficit_matrix = [[0.0 for x in range(nt)] for x in range(nt)]
            for turbine in range(nt):
                flag = [False for x in range(nt)]
                proportion = [0.0 for x in range(nt)]
                for i in range(nt):
                    try:
                        proportion[i], flag[i] = wake.determine_if_in_wake(layout_x[turbine], layout_y[turbine], layout_x[i], layout_y[i], k, r0, angle3)
                    except TypeError:
                        print(layout_x[turbine], layout_y[turbine], layout_x[i], layout_y[i], k, r0, angle3)

                # Matrix with effect of each turbine <i = turbine> on every other turbine <j> of the farm
                for j in range(nt):
                    if turbine != j and flag[j] is True:
                        wake_deficit_matrix[turbine][j] = proportion[j] * wake.wake_deficit(0.81, k, wake.distance(layout_x[turbine], layout_y[turbine], layout_x[j], layout_y[j]), r0)
                    elif turbine == j:
                        wake_deficit_matrix[turbine][j] = 0.0

            total_deficit = [0.0 for x in range(nt)]
            total_speed = [0.0 for x in range(nt)]
            for j in range(nt):
                for i in range(nt):
                    total_deficit[j] += wake_deficit_matrix[i][j] ** 2.0
                total_deficit[j] = sqrt(total_deficit[j])
                total_speed[j] = U0 * (1.0 - total_deficit[j])

            # Farm efficiency
            profit = 0.0
            efficiency_proportion = [0.0 for x in range(0, len(windrose_frequency))]
            for l in range(nt):
                profit += power(total_speed[l])
            efficiency = profit * 100.0 / (float(nt) * power(U0))
            efficiency_proportion[wind] = efficiency * windrose_frequency[wind] / 100.0
            summation += efficiency_proportion[wind]
        unknowns['eff'] = summation  # Farm efficiency

if __name__ == '__main__':
    start_time = time.time()

    top = Problem()

    top.root = Group()

    def gen_individual(n_turbines, min_x, max_x, min_y, max_y):
        return [gen_turbine(min_x, max_x, min_y, max_y) for k in range(n_turbines)]

    def gen_population(n_ind, n_turbines, min_x, max_x, min_y, max_y):
        return np.array([gen_individual(n_turbines, min_x, max_x, min_y, max_y) for x in range(n_ind)])

    def gen_turbine(min_x, max_x, min_y, max_y):
        a = [float(randint(min_x, max_x)), float(randint(min_y, max_y))]
        while a[1] < - 3907.0 / 412.0 * float(a[0]) + 3907.0:
            a[0] = float(randint(min_x, max_x))
            a[1] = float(randint(min_y, max_y))
        while a[1] > 3907.0 / 417.0 * (5457.0 - float(a[0])):
            a[0] = float(randint(min_x, max_x))
            a[1] = float(randint(min_y, max_y))
        return a

    top.root.add('positions', ParamComp('a', gen_population(1, 80, 0.0, 5457.0, 0.0, 3907.0)[0]))

    top.root.add('model', JensenModel())

    top.root.connect('positions.a', 'model.a')

    top.setup()
    top.run()

    print(top.root.unknowns['model.eff'])
    print(top.root.unknowns['positions.a'])

    print("--- %s seconds ---" % (time.time() - start_time))
