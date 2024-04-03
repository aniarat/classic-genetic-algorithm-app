import random

class CrossoverMethod:
    def crossover(self, population):
        pass

class SinglePointCrossover(CrossoverMethod):
    def __init__(self, number_of_dimensions):
        self.number_of_dimensions = number_of_dimensions
    def crossover(self, population):
        parent1, parent2 = random.sample(population, 2)
        crossing_point = random.randint(1, min(len(parent1), len(parent2)) - 1)
        child1 = parent1[:crossing_point] + parent2[crossing_point:]
        child2 = parent2[:crossing_point] + parent1[crossing_point:]
        return child1, child2

class TwoPointCrossover(CrossoverMethod):
    def __init__(self, number_of_dimensions):
        self.number_of_dimensions = number_of_dimensions
    def crossover(self, population): 
        
        parent1, parent2 = random.sample(population, 2)
        crossover_points = sorted(random.sample(range(1, min(len(parent1), len(parent2))), 2))
        child1 = parent1[:crossover_points[0]] + parent2[crossover_points[0]:crossover_points[1]] + parent1[crossover_points[1]:]
        child2 = parent2[:crossover_points[0]] + parent1[crossover_points[0]:crossover_points[1]] + parent2[crossover_points[1]:]
        return child1, child2

class ThreePointCrossover(CrossoverMethod):
    def __init__(self, number_of_dimensions):
        self.number_of_dimensions = number_of_dimensions
    def crossover(self, population):
        parent1, parent2 = random.sample(population, 2)
        crossover_points = sorted(random.sample(range(1, min(len(parent1), len(parent2))), 3))
        child1 = parent1[:crossover_points[0]] + parent2[crossover_points[0]:crossover_points[1]] + parent1[crossover_points[1]:crossover_points[2]] + parent2[crossover_points[2]:]
        child2 = parent2[:crossover_points[0]] + parent1[crossover_points[0]:crossover_points[1]] + parent2[crossover_points[1]:crossover_points[2]] + parent1[crossover_points[2]:]
        return child1, child2

class UniformCrossover(CrossoverMethod):
    def __init__(self, probability, number_of_dimensions):
        self.corssingProb = probability
        self.number_of_dimensions = number_of_dimensions

    def crossover(self, population):
        parent1, parent2 = random.sample(population, 2)
        child1 = []
        child2 = []
        for gene1, gene2 in zip(parent1, parent2):
            if random.random() <= self.corssingProb:
                child1.append(gene2)
                child2.append(gene1)
            else:
                child1.append(gene1)
                child2.append(gene2)
        return child1, child2

class GrainCrossover(CrossoverMethod):
    def __init__(self, number_of_dimensions):
        self.number_of_dimensions = number_of_dimensions
    def crossover(self, population):
        parent1, parent2 = random.sample(population, 2)
        child = []
        for gene1, gene2 in zip(parent1, parent2):
            if random.random() <= 0.5:
                child.append(gene1)
            else:
                child.append(gene2)
        return [child]

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
        child1 = parent1[:cp1] + [parent1[i] if parent1[i] == 1 else parent2[i] for i in range(cp1, cp2)] + parent1[cp2:]
        child2 = parent2[:cp1] + [parent2[i] if parent2[i] == 1 else parent1[i] for i in range(cp1, cp2)] + parent2[cp2:]
        return child1, child2
    
class MultivariateCrossover(CrossoverMethod):
    def __init__(self, probability, q, number_of_dimensions):
        self.corssingProb = probability
        self.q = q
        self.number_of_dimensions = number_of_dimensions
    def crossover(self, population):
        #TODO: implementacja
        parent1_total, parent2_total = random.sample(population, 2)
        parent1 = [parent1_total[i : i + len(parent1_total)//self.q] for i in range(0, len(parent1_total), len(parent1_total)//self.q)]
        parent2 = [parent2_total[i : i + len(parent2_total)//self.q] for i in range(0, len(parent2_total), len(parent2_total)//self.q)]

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
    