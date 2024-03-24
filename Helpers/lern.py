import random

from Helpers.decimalBinaryMath import binary_to_decimal
from Helpers.parents import initParents


def lern(number_of_epoch: int,
         size_of_population: int,
         chromsome_length: int,
         number_of_parents: int,
         crossing_function,
         mutation_function,
         selection_function,
         F):
    population = initParents(chromsome_length, number_of_parents)
    wynik = F(binary_to_decimal(population[0]))
    print('x=', binary_to_decimal(population[0]))
    print('y=',wynik)
    for _ in range(number_of_epoch):
        population = selection_function(F, parents=population)
        children = crossing_function(F, population)
        population += children
        for i in range(len(population)):
            if random.uniform(0, 1) > 0.8:
                population[i] = mutation_function(population[i])
    wynik = F(binary_to_decimal(population[0]))
    print('x=', binary_to_decimal(population[0]))
    print('y=',wynik)
    return population
