import copy
import random
import time

from Consts.enums import MinMax, CrossingMechods, SelectionMechods, MutationMechods, FunctionsOptions
from Helpers.crossingMethods import SinglePointCrossover, MultivariateCrossover, PartialCopyCrossover, \
    ScanningCrossover, GrainCrossover, UniformCrossover, ThreePointCrossover, TwoPointCrossover
from Helpers.decimalBinaryMath import binary_to_decimal
from Helpers.functions import rastrigin, schwefel
from Helpers.mutationMethods import EdgeMutation, SinglePointMutation, TwoPointMutation
from Helpers.parents import initPopulation
import numpy as np

from Helpers.plotsNFiles import make_plot, save_to_file
from Helpers.selectionMethods import BestSelection, RouletteWheelSelection, TournamentSelection


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
                 crossing_function: CrossingMechods,
                 mutation_function: MutationMechods,
                 selection_function: SelectionMechods,
                 mutation_prob: float,
                 number_of_dimensions: int,
                 func: FunctionsOptions,
                 title,
                 direction: MinMax,
                 tournament_size: int,
                 q: int):
        self.number_of_epoch = number_of_epoch
        self.size_of_population = size_of_population
        self.chromosome_length = chromosome_length
        self.number_of_parents = number_of_parents
        self.crossing_probability = crossing_probability
        self.mutation_prob = mutation_prob
        self.number_of_dimensions = number_of_dimensions
        self.func = func
        self.title = title
        self.init_population = initPopulation(chromosome_length, number_of_dimensions, size_of_population)
        self.direction = direction

        self.func = rastrigin(number_of_dimensions) if func == FunctionsOptions.RASTRIGIN else schwefel(number_of_dimensions)

        match selection_function:
            case SelectionMechods.BEST:
                selection = BestSelection(number_of_dimensions)
                self.selection_function = selection.select if self.direction == MinMax.MIN else selection.maxSelect
            case SelectionMechods.ROULETTE:
                selection = RouletteWheelSelection(number_of_dimensions)
                self.selection_function = selection.select
            case SelectionMechods.TOURNAMENT:
                selection = TournamentSelection(tournament_size, number_of_dimensions)
                self.selection_function = selection.select if self.direction == MinMax.MIN else selection.maxSelect
                self.selectionName = SelectionMechods.TOURNAMENT_STRING.value
        match crossing_function:
            case CrossingMechods.SINGLE_POINT:
                self.crossing_function = SinglePointCrossover(number_of_dimensions).crossover
            case CrossingMechods.DOUBLE_POINT:
                self.crossing_function = TwoPointCrossover(number_of_dimensions).crossover
            case CrossingMechods.TRIPLE_POINT:
                self.crossing_function = ThreePointCrossover(number_of_dimensions).crossover
            case CrossingMechods.UNIFORM:
                self.crossing_function = UniformCrossover(crossing_probability, number_of_dimensions).crossover
            case CrossingMechods.GRAIN:
                self.crossing_function = GrainCrossover(number_of_dimensions).crossover
            case CrossingMechods.SCANNING:
                self.crossing_function = ScanningCrossover(number_of_parents, number_of_dimensions).crossover
            case CrossingMechods.PARTIAL:
                self.crossing_function = PartialCopyCrossover(number_of_dimensions).crossover
            case CrossingMechods.MULTIVARIATE:
                self.crossing_function = MultivariateCrossover(crossing_probability, q, number_of_dimensions).crossover
        match mutation_function:
            case MutationMechods.EDGE:
                self.mutation_function = EdgeMutation(number_of_dimensions).mutate
            case MutationMechods.SINGLE_POINT:
                self.mutation_function = SinglePointMutation(number_of_dimensions).mutate
            case MutationMechods.DOUBLE_POINT:
                self.mutation_function = TwoPointMutation(number_of_dimensions).mutate

    def find_best_spec(self, fn, population, direction: MinMax):
        best_index = 0
        for i in range(1, len(population)):
            value1 = self.binaryToDecimalSpec(population[best_index])
            value2 = self.binaryToDecimalSpec(population[i])
            if ((fn(value1) > fn(value2) and direction == MinMax.MIN)
                    or
                    (fn(value1) < fn(value2) and direction == MinMax.MAX)):
                best_index = i
        return population[best_index]

    def getStartString(self):
        return_string = ''
        map1 = map(binary_to_decimal, self.find_best_spec(self.func, self.init_population, self.direction))
        map2 = copy.deepcopy(map1)
        result = self.func(list(map1))
        return_string += '\n---------------------------START---------------------------\n'
        return_string += 'f('
        for val in list(map2):
            return_string += f'{val:.4f}, '
        return_string = return_string[:-2]
        return_string += f') = {result:.4f}' + '\n'
        return return_string

    def getEndString(self):
        return_string = ''
        map1 = map(binary_to_decimal, self.find_best_spec(self.func, self.end_population, self.direction))
        map2 = copy.deepcopy(map1)
        result = self.func(list(map1))
        return_string += '\n----------------------------END----------------------------\n'
        return_string += 'f('
        for val in list(map2):
            return_string += f'{val:.4f}, '
        return_string = return_string[:-2]
        return_string += f') = {result:.4f}' + '\n'
        return_string += 'Czas: ' + f'{self.end_time - self.start_time:0.4f}' + ' sekund\n'
        return return_string

    def appendToAllArrays(self, all_res, population):
        self.avg_values.append(np.mean(all_res))
        self.stddev_values.append(np.std(all_res))
        self.best_spec.append(self.binaryToDecimalSpec(self.find_best_spec(self.func, population, self.direction)))
        self.best_values.append(self.func(self.best_spec[-1]))

    @staticmethod
    def binaryToDecimalSpec(spec):
        return list(map(binary_to_decimal, spec))

    def fitness(self):
        self.best_values = []
        self.avg_values = []
        self.stddev_values = []
        self.best_spec = []
        self.start_time = time.perf_counter()
        population = self.init_population
        for i in range(self.number_of_epoch):
            is_best_alive = False
            all_res = list(self.func(self.binaryToDecimalSpec(individual)) for individual in population)
            self.appendToAllArrays(all_res, population)
            temp_population = self.selection_function(population, all_res, self.number_of_parents)

            while len(temp_population) < self.size_of_population:
                if random.random() >= self.crossing_probability:
                    temp_population += self.crossing_function(temp_population)

            best_new_spec = self.find_best_spec(self.func, temp_population, self.direction)

            for spec_index in range(self.size_of_population):
                spec = temp_population[spec_index]
                if not is_best_alive and spec == best_new_spec:
                    is_best_alive = True
                    continue
                for chrom_index in range(self.number_of_dimensions):
                    if random.random() >= self.mutation_prob:
                        temp_population[spec_index][chrom_index] = self.mutation_function(spec[chrom_index],
                                                                                          self.mutation_prob)

            population = temp_population

        self.end_population = population
        self.end_time = time.perf_counter()

    def getChats(self):
        make_plot(self.best_values, 'best', self.title)
        save_to_file(self.best_values, self.best_spec, 'best')
        make_plot(self.avg_values, 'avg', self.title)
        make_plot(self.stddev_values, 'std', self.title)
