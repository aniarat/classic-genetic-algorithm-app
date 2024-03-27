import random

class CrossoverMethod:
    def crossover(self, population):
        pass

class SinglePointCrossover(CrossoverMethod):
    def crossover(self, population):
        parent1, parent2 = random.sample(population, 2)
        crossing_point = random.randint(1, min(len(parent1), len(parent2)) - 1)
        child1 = parent1[:crossing_point].tolist() + parent2[crossing_point:].tolist()
        child2 = parent2[:crossing_point].tolist() + parent1[crossing_point:].tolist()
        print(child1)
        print(child2)
        return child1, child2

class TwoPointCrossover(CrossoverMethod):
    def crossover(self, population): 
        
        parent1, parent2 = random.sample(population, 2)
        crossover_points = sorted(random.sample(range(1, min(len(parent1), len(parent2))), 2))
        child1 = parent1[:crossover_points[0]].tolist() + parent2[crossover_points[0]:crossover_points[1]].tolist() + parent1[crossover_points[1]:].tolist()
        child2 = parent2[:crossover_points[0]].tolist() + parent1[crossover_points[0]:crossover_points[1]].tolist() + parent2[crossover_points[1]:].tolist()
        print(child1)
        print(child2)
        return child1, child2

class ThreePointCrossover(CrossoverMethod):
    def crossover(self, population):
        parent1, parent2 = random.sample(population, 2)
        crossover_points = sorted(random.sample(range(1, min(len(parent1), len(parent2))), 3))
        child1 = parent1[:crossover_points[0]].tolist() + parent2[crossover_points[0]:crossover_points[1]].tolist() + parent1[crossover_points[1]:crossover_points[2]].tolist() + parent2[crossover_points[2]:].tolist()
        child2 = parent2[:crossover_points[0]].tolist() + parent1[crossover_points[0]:crossover_points[1]].tolist() + parent2[crossover_points[1]:crossover_points[2]].tolist() + parent1[crossover_points[2]:].tolist()
        print(child1)
        print(child2)
        return child1, child2

class UniformCrossover(CrossoverMethod):
    def __init__(self, probability):
        self.corssingProb = probability

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
        print(child1)
        print(child2)
        return child1, child2

class GrainCrossover(CrossoverMethod):
    def crossover(self, population):
        parent1, parent2 = random.sample(population, 2)
        child = []
        for gene1, gene2 in zip(parent1, parent2):
            if random.random() <= 0.5:
                child.append(gene1)
            else:
                child.append(gene2)
        print(child)
        return child

class ScanningCrossover(CrossoverMethod):
    def __init__(self, num_parents):
        self.numberOfParents = num_parents

    def crossover(self, population):
        parents = random.sample(population, self.numberOfParents)
        chromosome_length = len(parents[0])
        child = [None] * chromosome_length
        
        for j in range(chromosome_length):
            chosen_parent_index = random.randint(0, self.numberOfParents - 1)
            child[j] = parents[chosen_parent_index][j]
        
        print(child)
        return child

class PartialCopyCrossover(CrossoverMethod):
    def crossover(self, population):
        parent1, parent2 = random.sample(population, 2)
        chromosome_length = len(parent1)
        cp1 = random.randint(0, chromosome_length - 2)
        cp2 = random.randint(cp1 + 1, chromosome_length - 1)
        child1 = parent1[:cp1].tolist() + [parent1[i] if parent1[i] == 1 else parent2[i] for i in range(cp1, cp2)] + parent1[cp2:].tolist()
        child2 = parent2[:cp1].tolist() + [parent2[i] if parent2[i] == 1 else parent1[i] for i in range(cp1, cp2)] + parent2[cp2:].tolist()
        print(child1)
        print(child2)
        return child1, child2
    
class MultivariateCrossover(CrossoverMethod):
    def crossover(self, population, pc, q):
        #TODO: implementacja
        return 