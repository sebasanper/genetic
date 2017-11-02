__author__ = 'sebasanper'
# Eddy Viscosity wake model applied to horns rev.
def Ainslie(a, Nt, rad):

    import wake
    from eddy_viscosity import ainslie
    from math import sqrt, log, cos, sin
    from numpy import deg2rad
    from power_curve5MW import power5MW_kW as power  # Power curve 5 MW NREL

    windrose = open('horns_rev_windrose.dat', 'r')

    def determine_front(wind_angle, x_t1, y_t1, x_t2, y_t2):
        wind_angle = deg2rad(wind_angle)
        b = (x_t2 - x_t1) * cos(wind_angle) + (y_t2 - y_t1) * sin(wind_angle)
        if b > 0.0:
            return True, b
        else:
            return False, 0.0

    nt = Nt  # Number of turbines
    D = 2.0 * rad  # Diameter
    layout_x = [0.0 for x in range(nt)]
    layout_y = [0.0 for x in range(nt)]
    for x in range(nt):
        layout_x[x] = float(a[x][0] / D)
        layout_y[x] = float(a[x][1] / D)

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

    ##  Power curve 2 MW Siemens
    # def power(U0):
    #     if U0 < 4.0:
    #         return 0.0
    #     elif U0 >= 4.0:
    #         return 19.7907842158 * U0 ** 2.0 - 74.9080669331 * U0 + 37.257967033  # From 4 to 11 m/s

    # for wind in range(0, len(windrose_speed)):
    for wind in range(0, 1):
        U1 = windrose_speed[wind]  # Free stream wind speed
        U0 = U1 * (90.0 / 10.0) ** 0.11  # Power or log law for wind shear profile
        # U0 = U1 * log(70.0 / 0.005) / log(10.0 / 0.005)
        angle = windrose_angle[wind]
        angle3 = angle + 180.0
        wake_deficit_matrix = [[0.0 for x in range(nt)] for x in range(nt)]
        for turbine in range(0, nt):
            parallel_distance = [0.0 for x in range(0, nt)]
            perpendicular_distance = [0.0 for x in range(0, nt)]
            flag = [False for x in range(nt)]
            for i in range(nt):
                flag[i], parallel_distance[i] = determine_front(angle3, layout_x[turbine], layout_y[turbine], layout_x[i], layout_y[i])
                perpendicular_distance[i] = wake.crosswind_distance(deg2rad(angle3), layout_x[turbine], layout_y[turbine], layout_x[i], layout_y[i])

            # Matrix with effect of each turbine <i = turbine> on every other turbine <j> of the farm
            for j in range(nt):
                if flag[j] is True:
                    if perpendicular_distance[j] <= 2.5:
                        wake_deficit_matrix[turbine][j] = ainslie(0.46, U0, parallel_distance[j], perpendicular_distance[j])
                    else:
                        wake_deficit_matrix[turbine][j] = 0.0
                elif flag[j] is False:
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
        efficiency = 0.0
        for l in range(nt):
            profit += power(total_speed[l])
            efficiency = profit * 100.0 / (nt * power(U0))
        efficiency_proportion[wind] = efficiency * windrose_frequency[wind] / 100.0
        summation += efficiency_proportion[wind]
    return summation

# if __name__ == '__main__':
#     start_time = time.time()
#     analysis()
#     print("--- %s seconds ---" % (time.time() - start_time))
