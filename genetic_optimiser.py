__author__ = 'Sebastian Sanchez Perez-Moreno. Email: s.sanchezperezmoreno@tudelft.nl'

import sys
from math import ceil, floor, log
from random import randint, random
# from ainslieOKoptimise import ainslie as fitness
# from larsenOKoptimise import larsen as fitness
from jensenOKoptimise import jensen as fitness
from wake import distance
import time
from joblib import Parallel, delayed

result = open('gen7_best_layout_ainslie.dat', 'w', 1)
result2 = open('gen7_fitness_ainslie.dat', 'w', 1)
average = open('gen7_average_fitness_ainslie.dat', 'w', 1)
start_time = time.time()

#  gen1 with     n_iter = 8000    n_ind = 100    mutation_rate = 0.01    selection_percentage = 0.3  random_selection = 0.05 100-13.24%=86.76% eff.
#  gen 2 same as gen1. Corrected min distance to 2D, instead of 1D. Changed to maximise efficiency instead. Using n_ind = 50 individuals for speed. 87.53% efficiency.
#  gen3     n_iter = 20    n_ind = 100. 2000 functions calls = 8 hrs.
#  gen 5 same as gen 3 more iter to 50
#  gen 6 windrose 360 degrees for speed. selection rate 0.2. each iteration took 10.69 minutes. 1069 minutes in total. too long.
#  gen7 as gen6 with     n_iter = 50    n_ind = 80

windrose = open('horns_rev_windrose2.dat', 'r')
windrose_angle = []
windrose_speed = []
windrose_frequency = []
for line in windrose:
    columns = line.split()
    windrose_angle.append(float(columns[0]))
    windrose_speed.append(float(columns[1]))
    windrose_frequency.append(float(columns[2]))

windrose.close()

try:
    def gen_individual(n_turbines, min_x, max_x, min_y, max_y):
        return [gen_turbine(min_x, max_x, min_y, max_y) for k in range(n_turbines)]

    def gen_population(n_ind, n_turbines, min_x, max_x, min_y, max_y):
        return [gen_individual(n_turbines, min_x, max_x, min_y, max_y) for x in range(n_ind)]

    def gen_turbine(min_x, max_x, min_y, max_y):
        a = [float(randint(min_x, max_x)), float(randint(min_y, max_y))]
        while a[1] < - 3907.0 / 412.0 * float(a[0]) + 3907.0:
            a[0] = float(randint(min_x, max_x))
            a[1] = float(randint(min_y, max_y))
        while a[1] > 3907.0 / 417.0 * (5457.0 - float(a[0])):
            a[0] = float(randint(min_x, max_x))
            a[1] = float(randint(min_y, max_y))
        return a

    def grade_gen(b, n):
        average = 0.0
        for item in b:
            average += item / n
        return average

    def find_distance(nt, a, diam, min_x, max_x, min_y, max_y):
        n = 0
        while n == 0:
            n = 1
            for i in range(nt):
                for j in range(nt):
                    if i != j and distance(a[i][0], a[i][1], a[j][0], a[j][1]) < 2.0 * diam:
                        # print 'counting'
                        a[j] = gen_turbine(min_x, max_x, min_y, max_y)
                        n = 0
        return a

    n_iter = 50
    n_ind = 80
    nt = 80
    diam = 80.0
    min_x = 0
    max_x = 5457
    min_y = 0
    max_y = 3907
    mutation_rate = 0.01
    selection_percentage = 0.2
    random_selection = 0.05

    pops = gen_population(n_ind, nt, min_x, max_x, min_y, max_y)
    # pops.append([])
    # layout = open('horns_rev.dat', 'r')
    # for line in layout:
    #    columns = line.split()
    #    pops[-1].append([float(columns[0]) - 423974.0, float(columns[1]) - 6147540.0])
    # layout.close()
    n_ind = len(pops)
    for iteration in range(n_iter):  # Iteration through generations loop
        start_time2 = time.time()
        pop = pops
        # for x in range(nt):
        #     result.write('{0:d}\t{1:d}\n'.format(int(pop[0][x][0]), int(pop[0][x][1])))
        # result.write('\n')
        pop = Parallel(n_jobs=-1)(delayed(find_distance)(nt, pop[x], diam, min_x, max_x, min_y, max_y) for x in range(n_ind))  # Parallel verification of minimum distance between turbines to 2D
        # for x in range(nt):
        #     result.write('{0:d}\t{1:d}\n'.format(int(pop[0][x][0]), int(pop[0][x][1])))
        # result.write('\n')
        # Calls the Wake Model
        fit = Parallel(n_jobs=-1)(delayed(fitness)(pop[i]) for i in range(n_ind))  # Parallel evaluation of fitness of all individuals

        aver = grade_gen(fit, float(n_ind))

        average.write('{0:f}\n'.format(aver))

        for i in range(n_ind):
            fit[i] = [fit[i], i]
        for x in range(nt):
            result.write('{0:d}\t{1:d}\n'.format(int(pop[max(fit)[1]][x][0]), int(pop[max(fit)[1]][x][1])))  # This max implies maximisation.
        result.write('\n')

        for y in range(n_ind):
            result2.write('{0:f}\n'.format(fit[y][0]))
        result2.write('\n')

        graded = [x[1] for x in sorted(fit, reverse=True)]

        retain_length = int(len(graded) * selection_percentage)
        parents_index = graded[:retain_length]

        # Add randomly other individuals for variety
        for item in graded[retain_length:]:
            if random_selection > random():
                parents_index.append(item)

        # Mutation of individuals
        for item in parents_index:
            if mutation_rate > random():
                place = randint(0, len(pop[item]) - 1)
                pop[item][place] = gen_turbine(min_x, max_x, min_y, max_y)

        pops = []
        for item in parents_index:
            pops.append(pop[item])

        # Crossover function. Create children from parents
        parents_length = len(parents_index)
        desired_length = n_ind - parents_length
        children = []
        while len(children) < desired_length:
            parent1 = randint(0, parents_length - 1)
            parent2 = randint(0, parents_length - 1)
            if parent1 != parent2:
                parent1 = pop[parents_index[parent1]]
                parent2 = pop[parents_index[parent2]]
                cross_place = randint(0, nt - 1)
                child = parent1[:cross_place] + parent2[cross_place:]
                children.append(child)
        pops.extend(children)

        print("%d iteration--- %s minutes ---" % (iteration, (time.time() - start_time2) / 60.0))
        print len(pops)
    print("--- %s minutes ---" % ((time.time() - start_time) / 60.0))
    result.close()
    result2.close()
    average.close()
except KeyboardInterrupt:
    sys.stdout.flush()
    sys.exit()
