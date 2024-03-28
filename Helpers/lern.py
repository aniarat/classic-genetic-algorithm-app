import random

from Helpers.decimalBinaryMath import binary_to_decimal
from Helpers.parents import initPopulation


def lern(number_of_epoch: int,
         size_of_population: int,
         chromosome_length: int,
         number_of_parents: int,
         crossing_function,
         mutation_function,
         selection_function,
         F):
    population = initPopulation(chromosome_length, size_of_population)
    result = F(binary_to_decimal(population[0]))
    print('x=', binary_to_decimal(population[0]))
    print('y=', result)
    for _ in range(number_of_epoch):
        population = selection_function(population, [F(binary_to_decimal(individual)) for individual in population],
                                        number_of_parents)
        children = crossing_function(population)
        population += children
        for i in range(len(population)):
            if random.uniform(0, 1) > 0.8:
                population[i] = mutation_function(population[i])
    result = F(binary_to_decimal(population[0]))
    print('x=', binary_to_decimal(population[0]))
    print('y=', result)
    return population
