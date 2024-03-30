import random
import time

from Helpers.decimalBinaryMath import binary_to_decimal
from Helpers.parents import initPopulation
import numpy as np

from Helpers.plotsNFiles import make_plot, save_to_file


def find_best_spec(f,parents):
    best_index = 0
    for i in range(1, len(parents)):
        if f(binary_to_decimal(parents[i])) < f(binary_to_decimal(parents[best_index])):
            best_index = i
    return parents[best_index]

def learn(number_of_epoch: int,
          size_of_population: int,
          chromosome_length: int,
          number_of_parents: int,
          crossing_probability: int,
          crossing_function,
          mutation_function,
          selection_function,
          func,
          title):
    return_string = ''
    best_values = []
    avg_values = []
    stdev_values = []
    population = initPopulation(chromosome_length, size_of_population)
    result = func(binary_to_decimal(find_best_spec(func, population)))
    return_string += '\n---------------------------START---------------------------\n'
    return_string += f'f({binary_to_decimal(find_best_spec(func, population))}) = {result}' + '\n'
    start_time = time.perf_counter()
    for _ in range(number_of_epoch):
        population = selection_function(population,
                                        [func(binary_to_decimal(individual)) for individual in population],
                                        number_of_parents)

        best_values.append(func(binary_to_decimal(find_best_spec(func, population))))
        all_res = [func(binary_to_decimal(individual)) for individual in population]
        avg_values.append(np.mean(all_res))
        stdev_values.append(np.std(all_res))

        if random.random() >= crossing_probability:
            children = crossing_function(population)
            population += children

    end_time = time.perf_counter()
    result = func(binary_to_decimal(population[0]))
    return_string += '---------------------------END---------------------------\n'
    return_string += f'f({binary_to_decimal(find_best_spec(func, population))}) = {result}' + '\n'
    return_string += 'Czas: ' + f'{end_time - start_time:0.4f}' + ' sekund\n'

    make_plot(best_values, 'best', title, 'log')
    save_to_file(best_values, 'best')
    make_plot(avg_values, 'avg', title)
    make_plot(stdev_values, 'std', title)

    return return_string

