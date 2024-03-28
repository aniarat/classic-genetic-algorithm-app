import random
import time

from Helpers.decimalBinaryMath import binary_to_decimal
from Helpers.parents import initPopulation
from matplotlib import pyplot as plt
import numpy as np
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
          F):
    return_string = ''
    best_values = []
    avg_values = []
    population = initPopulation(chromosome_length, size_of_population)
    result = F(binary_to_decimal(find_best_spec(F,population)))
    return_string += '\n---------------------------START---------------------------\n'
    return_string += 'x=' + f'{binary_to_decimal(find_best_spec(F,population))}' + '\n'
    return_string += 'y=' + f'{result}' + '\n'
    start_time = time.perf_counter()
    for _ in range(number_of_epoch):
        population = selection_function(population,
                                        [F(binary_to_decimal(individual)) for individual in population],
                                        number_of_parents)

        best_values.append(F(binary_to_decimal(find_best_spec(F,population))))
        avg_values.append(np.mean([F(binary_to_decimal(individual)) for individual in population]))

        if random.random() >= crossing_probability:
            children = crossing_function(population)
            population += children

    end_time = time.perf_counter()
    result = F(binary_to_decimal(population[0]))
    return_string += '---------------------------END---------------------------\n'
    return_string += 'x=' + f'{binary_to_decimal(find_best_spec(F,population))}' + '\n'
    return_string += 'y=' + f'{result}' + '\n'
    return_string += 'Czas: ' + f'{end_time - start_time:0.4f}' + ' sekund\n'

    make_plot(best_values, 'best')
    make_plot(avg_values, 'avg')

    return return_string

def make_plot(values, file_name):
    plt.plot(values)
    plt.yscale("log")
    plt.title('Skanujące - najleszych')
    plt.xlabel('Population')
    plt.ylabel(file_name)
    plt.savefig(f'{file_name}.png')
    plt.figure()
