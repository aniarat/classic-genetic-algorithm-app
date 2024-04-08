import random
from typing import Tuple, List, Any

import numpy as np


class CrossoverMethod:
    def crossover(self, population):
        pass


class SinglePointCrossover(CrossoverMethod):
    def __init__(self, number_of_dimensions):
        self.number_of_dimensions = number_of_dimensions

    def crossover(self, population: list[list[int]]) -> tuple[list[list[int]], list[list[int]]]:
        parent1, parent2 = random.sample(population, 2)
        # n -> liczba chromosoów
        # m -> liczba genów w chromosomie
        n, m = np.array(parent1).shape
        child1 = []
        child2 = []
        for i in range(n):
            crossing_point = random.randint(1, m - 1)
            child1.append(parent1[i][:crossing_point] + parent2[i][crossing_point:])
            child2.append(parent2[i][:crossing_point] + parent1[i][crossing_point:])
        return child1, child2


class TwoPointCrossover(CrossoverMethod):
    def __init__(self, number_of_dimensions):
        self.number_of_dimensions = number_of_dimensions

    def crossover(self, population: list[list[int]]) -> tuple[list[list[int]], list[list[int]]]:
        parent1, parent2 = random.sample(population, 2)
        n, m = np.array(parent1).shape
        children1, children2 = [], []
        
        for i in range(n):
            crossing_point1, crossing_point2 = sorted(random.sample(range(1, m), 2))
            child1 = parent1[i][:crossing_point1] + parent2[i][crossing_point1:crossing_point2] + parent1[i][crossing_point2:]
            child2 = parent2[i][:crossing_point1] + parent1[i][crossing_point1:crossing_point2] + parent2[i][crossing_point2:]
            children1.append(child1)
            children2.append(child2)
    
        return children1, children2


class ThreePointCrossover(CrossoverMethod):
    def __init__(self, number_of_dimensions):
        self.number_of_dimensions = number_of_dimensions

    def crossover(self, population: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        parent1, parent2 = random.sample(population, 2)
        n, m = np.array(parent1).shape
        crossover_points = sorted(random.sample(range(1, m), 3))
        children1, children2 = [], []
        
        for i in range(n):
            child1 = parent1[i][:crossover_points[0]] + parent2[i][crossover_points[0]:crossover_points[1]] + parent1[i][
                                                                                                        crossover_points[
                                                                                                            1]:
                                                                                                        crossover_points[
                                                                                                            2]] + parent2[i][
                                                                                                                  crossover_points[
                                                                                                                      2]:]
            child2 = parent2[i][:crossover_points[0]] + parent1[i][crossover_points[0]:crossover_points[1]] + parent2[i][
                                                                                                        crossover_points[
                                                                                                            1]:
                                                                                                        crossover_points[
                                                                                                            2]] + parent1[i][
                                                                                                                  crossover_points[
                                                                                                                      2]:]
            children1.append(child1)
            children2.append(child2)

        return children1, children2


class UniformCrossover(CrossoverMethod):
    def __init__(self, probability, number_of_dimensions):
        self.corssingProb = probability
        self.number_of_dimensions = number_of_dimensions

    def crossover(self, population: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        parent1, parent2 = random.sample(population, 2)
        n = len(parent1)
        children1, children2 = [], []
        
        for i in range(n):
            child1, child2 = [], []
            for gene1, gene2 in zip(parent1[i], parent2[i]):
                if random.random() <= self.corssingProb:
                    child1.append(gene2)
                    child2.append(gene1)
                else:
                    child1.append(gene1)
                    child2.append(gene2)
                    
            children1.append(child1)
            children2.append(child2)
        

        return children1, children2


class GrainCrossover(CrossoverMethod):
    def __init__(self, number_of_dimensions):
        self.number_of_dimensions = number_of_dimensions

    def crossover(self, population: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        parent1, parent2 = random.sample(population, 2)
        n = len(parent1)

        children = []
        for i in range(n):
            child = []
            for gene1, gene2 in zip(parent1[i], parent2[i]):
                if random.random() <= 0.5:
                    child.append(gene1)
                else:
                    child.append(gene2)
            children.append(child)
        return [children]


#TODO:ogarnąć skanujące???????
class ScanningCrossover(CrossoverMethod):
    def __init__(self, num_parents, number_of_dimensions):
        self.numberOfParents = num_parents
        self.number_of_dimensions = number_of_dimensions

    def crossover(self, population):
        parents = random.sample(population, self.numberOfParents)
        chromosome_length = len(parents[0])
        child = [None] * chromosome_length
        
        for j in range(chromosome_length):
            chosen_parent_index = random.randint(0, self.numberOfParents - 1)
            child[j] = parents[chosen_parent_index][j]

        return [child]


class PartialCopyCrossover(CrossoverMethod):
    def __init__(self, number_of_dimensions):
        self.number_of_dimensions = number_of_dimensions

    def crossover(self, population):
        parent1, parent2 = random.sample(population, 2)
        chromosome_length = len(parent1)
        cp1 = random.randint(0, chromosome_length - 2)
        cp2 = random.randint(cp1 + 1, chromosome_length - 1)
        child1 = parent1[:cp1] + [parent1[i] if parent1[i] == 1 else parent2[i] for i in range(cp1, cp2)] + parent1[
                                                                                                            cp2:]
        child2 = parent2[:cp1] + [parent2[i] if parent2[i] == 1 else parent1[i] for i in range(cp1, cp2)] + parent2[
                                                                                                            cp2:]
        
        
        return child1, child2


class MultivariateCrossover(CrossoverMethod):
    def __init__(self, probability, q, number_of_dimensions):
        self.corssingProb = probability
        self.q = q
        self.number_of_dimensions = number_of_dimensions

    def crossover(self, population):
        parent1_total, parent2_total = random.sample(population, 2)
        parent1 = [parent1_total[i: i + len(parent1_total) // self.q] for i in
                   range(0, len(parent1_total), len(parent1_total) // self.q)]
        parent2 = [parent2_total[i: i + len(parent2_total) // self.q] for i in
                   range(0, len(parent2_total), len(parent2_total) // self.q)]

        child1 = []
        child2 = []

        for i in range(self.q):
            rnd = random.random()
            if rnd <= self.corssingProb:
                crossover_point = random.randint(0, len(parent1[i]) - 1)
                child1 += (parent1[i][:crossover_point] + parent2[i][crossover_point:])
                child2 += (parent2[i][:crossover_point] + parent1[i][crossover_point:])
            else:
                # Jeśli krzyżowanie nie jest wykonane, potomstwo to kopie rodziców
                child1 += parent1[i]
                child2 += parent2[i]


        return child1, child2
