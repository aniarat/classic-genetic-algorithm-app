import copy
import random
import time

from Helpers.decimalBinaryMath import binary_to_decimal
from Helpers.parents import initPopulation
import numpy as np

from Helpers.plotsNFiles import make_plot, save_to_file


class Model:
    end_population = []
    start_time = 0
    end_time = 0
    stddev_values = []
    avg_values = []
    best_spec = []
    best_values = []

    def __init__(self,
                 number_of_epoch: int,
                 size_of_population: int,
                 chromosome_length: int,
                 number_of_parents: int,
                 crossing_probability: int,
                 crossing_function,
                 mutation_function,
                 selection_function,
                 mutation_prob,
                 number_of_dimensions,
                 func,
                 title):
        self.number_of_epoch = number_of_epoch
        self.size_of_population = size_of_population
        self.chromosome_length = chromosome_length
        self.number_of_parents = number_of_parents
        self.crossing_probability = crossing_probability
        self.crossing_function = crossing_function
        self.mutation_function = mutation_function
        self.selection_function = selection_function
        self.mutation_prob = mutation_prob
        self.number_of_dimensions = number_of_dimensions
        self.func = func
        self.title = title
        self.init_population = initPopulation(chromosome_length, number_of_dimensions, size_of_population)

    def find_best_spec(self, fnu, population):
        best_index = 0
        for i in range(1, len(population)):
            value1 = self.binaryToDecimalSpec(population[best_index])
            value2 = self.binaryToDecimalSpec(population[i])
            if fnu(*value1) > fnu(*value2):
                best_index = i
        return population[best_index]

    def getStartString(self):
        return_string = ''
        map1 = map(binary_to_decimal, self.find_best_spec(self.func, self.init_population))
        map2 = copy.deepcopy(map1)
        result = self.func(*map1)
        return_string += '\n---------------------------START---------------------------\n'
        return_string += f'f{list(map2)} = {result}' + '\n'
        return return_string

    def getEndString(self):
        return_string = ''
        map1 = map(binary_to_decimal, self.find_best_spec(self.func, self.end_population))
        map2 = copy.deepcopy(map1)
        result = self.func(*map1)
        return_string += '\n----------------------------END----------------------------\n'
        return_string += f'f{list(map2)} = {result}' + '\n'
        return_string += 'Czas: ' + f'{self.end_time - self.start_time:0.4f}' + ' sekund\n'
        return return_string

    def appendToAllArrays(self, all_res, population):
        self.avg_values.append(np.mean(all_res))
        self.stddev_values.append(np.std(all_res))
        self.best_spec.append(self.binaryToDecimalSpec(self.find_best_spec(self.func, population)))
        self.best_values.append(self.func(*self.best_spec[-1]))

    @staticmethod
    def binaryToDecimalSpec(spec):
        return list(map(binary_to_decimal, spec))

    def fitness(self):
        self.start_time = time.perf_counter()
        population = self.init_population
        for i in range(self.number_of_epoch):
            all_res = list(self.func(*self.binaryToDecimalSpec(individual)) for individual in population)
            self.appendToAllArrays(all_res, population)
            temp_population = self.selection_function(population,
                                                      all_res,
                                                      self.number_of_parents)
            
            while len(temp_population) < self.size_of_population:
                if random.random() >= self.crossing_probability:
                    temp_population += self.crossing_function(temp_population)

            # TODO: Uncomment after mutation function implementation
            for i in range(len(temp_population)):
                 for j in range(len(temp_population[i])):
                     if random.random() >= self.mutation_prob:
                         temp_population[i][j] = self.mutation_function(temp_population[i][j], self.mutation_prob)
            # TODO: Add combo that choose min or max of function
            temp_population.append(self.find_best_spec(self.func, population))
            population = temp_population
        self.end_population = population
        self.end_time = time.perf_counter()

    def getChats(self):
        make_plot(self.best_values, 'best', self.title)
        save_to_file(self.best_values, self.best_spec, 'best')
        make_plot(self.avg_values, 'avg', self.title)
        make_plot(self.stddev_values, 'std', self.title)
