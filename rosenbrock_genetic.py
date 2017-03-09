__author__ = 'sebasanper'
import sys
from math import ceil, floor, log
from random import randint, random
import time
from joblib import Parallel, delayed

result = open('rosenbrock_.dat', 'w')
result2 = open('rosenbrock_fit.dat', 'w')
average = open('rosenbrock_aver.dat', 'w')
start_time = time.time()

try:

    def gen_individual(n_turbines, min_x, max_x, min_y, max_y):
        return [gen_turbine(min_x, max_x, min_y, max_y) for k in range(n_turbines)]

    def gen_population(n_ind, n_turbines, min_x, max_x, min_y, max_y):
        return [gen_individual(n_turbines, min_x, max_x, min_y, max_y) for x in range(n_ind)]

    def gen_turbine(min_x, max_x, min_y, max_y):
        a = random()
        b = random()
        return [a * max_x + (1.0 - a) * min_x, b * max_y + (1.0 - b) * min_y]

    def grade_gen(b, n):
        average = 0.0
        for item in b:
            average += item / n
        return average

    n_iter = 100
    n_ind = 200000
    nt = 1
    min_x = -5.
    max_x = 5.
    min_y = -5.
    max_y = 5.
    mutation_rate = 0.01
    selection_percentage = 0.2
    random_selection = 0.05

    pops = gen_population(n_ind, nt, min_x, max_x, min_y, max_y)

    n_ind = len(pops)
    print n_ind
    for iteration in range(n_iter):  # Iteration through generations loop
        start_time2 = time.time()
        pop = pops
        fit = [0.0 for x in range(n_ind)]
        for x in range(n_ind):
            fit[x] = (1.0 - pop[x][0][0]) ** 2.0 + 100.0 * (pop[x][0][1] - pop[x][0][0] ** 2.0) ** 2.0

        aver = grade_gen(fit, float(n_ind))

        average.write('{0:f}\n'.format(aver))

        for i in range(n_ind):
            fit[i] = [- fit[i], i]
        for x in range(nt):
            result.write('{0:f}\t{1:f}\n'.format(pop[max(fit)[1]][x][0], pop[max(fit)[1]][x][1]))
        result.write('\n')

        for y in range(n_ind):
            result2.write('{0:f}\n'.format(fit[y][0]))
        result2.write('\n')

        graded = [x[1] for x in sorted(fit)]

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
        sys.stdout.flush()
    print("--- %s minutes ---" % ((time.time() - start_time) / 60.0))
    result.close()
    result2.close()
    average.close()
except KeyboardInterrupt:
    sys.stdout.flush()
    sys.exit()


# if __name__ == '__main__':
#     files = open('data.dat', 'w')
#     a = gen_population(1, 80, 0, 5457, 0, 3907)
#     for x in range(80):
#         files.write('{0:d}\t{1:d}\n'.format(a[0][x][0], a[0][x][1]))
