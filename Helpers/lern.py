import random
import time

from Helpers.decimalBinaryMath import binary_to_decimal
from Helpers.parents import initPopulation
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

        if random.random() >= crossing_probability:
            children = crossing_function(population)
            population += children

    end_time = time.perf_counter()
    result = F(binary_to_decimal(population[0]))
    return_string += '---------------------------END---------------------------\n'
    return_string += 'x=' + f'{binary_to_decimal(find_best_spec(F,population))}' + '\n'
    return_string += 'y=' + f'{result}' + '\n'
    return_string += 'Czas: ' + f'{end_time - start_time:0.4f}' + ' sekund\n'
    return return_string
