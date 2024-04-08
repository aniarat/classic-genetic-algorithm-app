import random
from typing import Tuple, List, Any

import numpy as np


class CrossoverMethod:
    def crossover(self, population):
        pass


class SinglePointCrossover(CrossoverMethod):
    def __init__(self, number_of_dimensions):
        self.number_of_dimensions = number_of_dimensions

    def crossover(self, population: list[list[int]]) -> tuple[list[list[Any]]]:
        parent1, parent2 = random.sample(population, 2)
        child1 = []
        child2 = []
        for i in range(self.number_of_dimensions):
            child1.append([])
            child2.append([])
            crossing_point = random.randint(1, len(parent1[0]) - 1)
            child1[i] = parent1[i][:crossing_point] + parent2[i][crossing_point:]
            child2[i] = parent2[i][:crossing_point] + parent1[i][crossing_point:]
        return child1, child2


class TwoPointCrossover(CrossoverMethod):
    def __init__(self, number_of_dimensions):
        self.number_of_dimensions = number_of_dimensions

    def crossover(self, population: list[list[int]]) -> tuple[list[list[int]], list[list[int]]]:
        parent1, parent2 = random.sample(population, 2)
        n, m = np.array(parent1).shape
        child1, child2 = [], []

        for i in range(n):
            child1.append([])
            child2.append([])
            crossing_point1, crossing_point2 = sorted(random.sample(range(1, m), 2))
            child1[i] = parent1[i][:crossing_point1] + parent2[i][crossing_point1:crossing_point2] + parent1[i][
                                                                                                  crossing_point2:]
            child2[i] = parent2[i][:crossing_point1] + parent1[i][crossing_point1:crossing_point2] + parent2[i][crossing_point2:]

        return child1, child2


class ThreePointCrossover(CrossoverMethod):
    def __init__(self, number_of_dimensions):
        self.number_of_dimensions = number_of_dimensions

    def crossover(self, population: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        parent1, parent2 = random.sample(population, 2)
        n, m = np.array(parent1).shape
        crossover_points = sorted(random.sample(range(1, m), 3))
        child1 = []
        child2 = []
        for i in range(n):
            child1.append([])
            child2.append([])
            child1[i] = parent1[i][:crossover_points[0]] + parent2[i][crossover_points[0]:crossover_points[1]] + parent1[i][
                                                                                                        crossover_points[
                                                                                                            1]:
                                                                                                        crossover_points[
                                                                                                            2]] + parent2[i][
                                                                                                                  crossover_points[
                                                                                                                      2]:]
            child2[i] = parent2[i][:crossover_points[0]] + parent1[i][crossover_points[0]:crossover_points[1]] + parent2[i][
                                                                                                        crossover_points[
                                                                                                            1]:
                                                                                                        crossover_points[
                                                                                                            2]] + parent1[i][
                                                                                                                  crossover_points[
                                                                                                                      2]:]

        return child1, child2


class UniformCrossover(CrossoverMethod):
    def __init__(self, probability, number_of_dimensions):
        self.corssingProb = probability
        self.number_of_dimensions = number_of_dimensions

    def crossover(self, population: List[List[int]]) -> list[list[list[list[Any]]]]:
        parent1, parent2 = random.sample(population, 2)
        n = len(parent1)
        children1, children2 = [], []
        for i in range(n):
            child1, child2 = [], []
            for j in range(self.number_of_dimensions):
                child1.append([])
                child2.append([])
                for gene1, gene2 in zip(parent1[i], parent2[i]):
                    if random.random() <= self.corssingProb:
                        child1[j].append(gene2)
                        child2[j].append(gene1)
                    else:
                        child1[j].append(gene1)
                        child2[j].append(gene2)

            children1.append(child1)
            children2.append(child2)

        return children1 + children2


class GrainCrossover(CrossoverMethod):
    def __init__(self, number_of_dimensions):
        self.number_of_dimensions = number_of_dimensions

    def crossover(self, population: List[List[int]]) -> list[list[list[Any]]]:
        parent1, parent2 = random.sample(population, 2)
        n = len(parent1[0])

        children = []
        for i in range(n):
            child = []
            for j in range(self.number_of_dimensions):
                child.append([])
                for gene1, gene2 in zip(parent1[j], parent2[j]):
                    if random.random() <= 0.5:
                        child[j].append(gene1)
                    else:
                        child[j].append(gene2)
                children.append(child)
        return children


class ScanningCrossover(CrossoverMethod):
    def __init__(self, num_parents, number_of_dimensions):
        self.numberOfParents = num_parents
        self.number_of_dimensions = number_of_dimensions

    def crossover(self, population):
        parents = random.sample(population, self.numberOfParents)
        chromosome_length = len(parents[0][0])
        child = []
        for i in range(self.number_of_dimensions):
            child.append([None] * chromosome_length)
            for j in range(chromosome_length):
                chosen_parent_index = random.randint(0, self.numberOfParents - 1)
                child[i][j] = parents[chosen_parent_index][i][j]

        return [child]


class PartialCopyCrossover(CrossoverMethod):
    def __init__(self, number_of_dimensions):
        self.number_of_dimensions = number_of_dimensions

    def crossover(self, population):
        parent1, parent2 = random.sample(population, 2)
        child1 = []
        child2 = []
        for i in range(self.number_of_dimensions):
            chromosome_length = len(parent1[i])
            cp1: int = random.randint(0, chromosome_length - 2)
            cp2: int = random.randint(cp1 + 1, chromosome_length - 1)
            child1.append(parent1[i][:cp1] + [parent1[i][j] if parent1[i][j] == 1 else
                                              parent2[i][j] for j in range(cp1, cp2)] + parent1[i][cp2:])
            child2.append(parent2[i][:cp1] + [parent2[i][j] if parent2[i][j] == 1 else
                                              parent1[i][j] for j in range(cp1, cp2)] + parent2[i][cp2:])
        return [child1, child2]


class MultivariateCrossover(CrossoverMethod):
    def __init__(self, probability, q, number_of_dimensions):
        self.corssingProb = probability
        self.q = q
        self.number_of_dimensions = number_of_dimensions

    def crossover(self, population):
        parent1_total, parent2_total = random.sample(population, 2)
        parent1 = []
        parent2 = []
        number_of_genes = len(parent1_total[0])
        for chrom_index in range(self.number_of_dimensions):
            parent1.append([parent1_total[chrom_index][i: i + number_of_genes // self.q] for i in
                            range(0, len(parent1_total[chrom_index]), number_of_genes // self.q)])
            parent2.append([parent2_total[chrom_index][i: i + number_of_genes // self.q] for i in
                            range(0, len(parent2_total[chrom_index]), number_of_genes // self.q)])

        child1 = []
        child2 = []
        for chrom_index in range(self.number_of_dimensions):
            child1.append([])
            child2.append([])
            for i in range(len(parent1[0])):
                rnd = random.random()
                if rnd <= self.corssingProb:
                    crossover_point = random.randint(0, len(parent1[0][i]) - 1)
                    child1[chrom_index] += parent1[chrom_index][i][:crossover_point] + parent2[chrom_index][i][
                                                                                       crossover_point:]
                    child2[chrom_index] += parent2[chrom_index][i][:crossover_point] + parent1[chrom_index][i][
                                                                                       crossover_point:]
                else:
                    child1[chrom_index] += parent1[chrom_index][i]
                    child2[chrom_index] += parent2[chrom_index][i]

        return child1, child2
