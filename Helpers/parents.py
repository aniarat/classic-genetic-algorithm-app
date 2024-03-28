# import random
# def partial_copy_crossover(parents):
#     p1, p2 = parents[0], parents[1]
#     chromosome_length = len(p1)
#     cp1 = random.randint(0, chromosome_length - 2)
#     cp2 = random.randint(cp1 + 1, chromosome_length - 1)
#
#     c1 = p1[:cp1] + [p1[i] if p1[i] == 1 else p2[i] for i in range(cp1, cp2)] + p1[cp2:]
#     c2 = p2[:cp1] + [p2[i] if p2[i] == 1 else p1[i] for i in range(cp1, cp2)] + p2[cp2:]
#
#     return c1, c2
#
#
# def print_parent(speciments):
#     for spec in speciments:
#         print(spec)
#
#
# def print_parent_as_dec(speciments):
#     for spec in speciments:
#         print(binary_to_decimal(spec))
#
#
# def F(x):
#     return x ** 2 - 2 * x - 5
#
#
# def binatodeci(binary):
#     return sum(val * (2 ** idx) for idx, val in enumerate(reversed(binary)))
#
#
# def binary_to_decimal(binarry_chain, start=-10, end=10):
#     chain_len = len(binarry_chain)
#     return start + binatodeci(binarry_chain) * (end - start) / (2 ** chain_len - 1)
#
#
# def resoults(f, population):
#     res = []
#     for specimen in population:
#         res.append(f(binary_to_decimal(specimen)))
#     return res
#
#
# def find_worst_index(res):
#     index = 0
#     for i in range(len(res)):
#         if res[i] > res[index]:
#             index = i
#     return index
#
#
# def find_two_worst_index(res):
#     index1 = 0
#     index2 = 0
#     for i in range(len(res)):
#         if res[i] > res[index1]:
#             index2 = index1
#             index1 = i
#     return [index1, index2]
#
#
# def find_best_index(res):
#     index = 0
#     for i in range(len(res)):
#         if res[i] < res[index]:
#             index = i
#     return index
#
#
# def mutation(specimen):
#     ran_index = random.randint(0, len(specimen) - 1)
#     specimen[ran_index] *= -1
#     return specimen
#
#
# def get_random_parents(population):
#     rn1 = random.randint(0, len(population) - 1)
#     rn2 = random.randint(0, len(population) - 1)
#     while (rn1 != rn2):
#         rn2 = random.randint(0, len(population) - 1)
#     return [population[rn1], population[rn2]]
#
#
# def lern(start_population, num_of_epochs=10):
#     population = start_population
#     for _ in range(num_of_epochs):
#         res = resoults(F, population)
#         [wi1, wi2] = find_two_worst_index(res)
#         [c1, c2] = partial_copy_crossover(get_random_parents(population))
#         population[wi1] = c1;
#         population[wi2] = c2;
#
#         for spec in population:
#             if random.uniform(0, 1) > 0.8:
#                 spec = mutation(spec)
#     return population
#
#
# def lern_error(start_population, ex_val, max_error=0.01, max_epochs=1_000_000):
#     population = start_population
#     res = resoults(F, population)
#     num_of_epoch = 0
#
#     while abs(ex_val - res[find_best_index(res)]) > max_error and num_of_epoch < max_epochs:
#         wi1, wi2 = find_two_worst_index(res)
#         parents = get_random_parents(population)
#         c1, c2 = partial_copy_crossover(parents)
#
#         population[wi1] = c1
#         population[wi2] = c2
#
#         for i in range(len(population)):
#             if random.uniform(0, 1) > 0.8:
#                 population[i] = mutation(population[i])
#
#         res = resoults(F, population)
#         num_of_epoch += 1
#
#     return population, num_of_epoch
import numpy as np
def initParents(chromosome_length: int, number_of_parents: int) -> list:
    return [list(np.random.randint(0, 2, chromosome_length)) for _ in range(number_of_parents)]
def initPopulation(chromosome_length: int, population_size: int) -> list:
    return [list(np.random.randint(0, 2, chromosome_length)) for _ in range(population_size)]

def printParents(parents: list) -> None:
    for parent in parents:
        print(parent)
