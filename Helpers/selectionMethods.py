#from decimalBinaryMath import binary_to_decimal

#def best_selection(f, parents):
#    worst_index = 0
#    for i in range(1,len(parents)):
#        if f(binary_to_decimal(parents[i])) > f(binary_to_decimal(parents[worst_index])):
#            worst_index = i
#    return parents[:worst_index] + parents[worst_index+1:]

#population = [1, 2, 3, 4, 5]
#fitness_values = [10, 8, 6, 9, 7]

#selected_parents = best_selection(fitness_values, population)
#print(selected_parents)

import random

def select_best_individuals(population, fitness_values, num_parents):
    combined_population = list(zip(population, fitness_values))
    
    sorted_population = sorted(combined_population, key=lambda x: x[1], reverse=True)
    
    selected_parents = [individual[0] for individual in sorted_population[:num_parents]]
    
    print("Najlepsza: ", selected_parents)
    return selected_parents

def roulette_wheel_selection(population, fitness_values, num_parents):
    total_fitness = sum(fitness_values)
    relative_fitness = [f / total_fitness for f in fitness_values]
    cumulative_probability = [sum(relative_fitness[:i+1]) for i in range(len(relative_fitness))]

    selected_parents = []
    for _ in range(num_parents):
        rand = random.random()
        for i, cp in enumerate(cumulative_probability):
            if rand <= cp:
                selected_parents.append(population[i])
                break
    print("Ruletka: ", selected_parents)            
    return selected_parents

def tournament_selection(population, fitness_values, tournament_size, num_parents):
    selected_parents = []
    population_size = len(population)
    
    while len(selected_parents) < num_parents:

        tournament_indices = random.sample(range(population_size), tournament_size)

        tournament_fitness_values = [fitness_values[i] for i in tournament_indices]
        winner_index = tournament_indices[tournament_fitness_values.index(max(tournament_fitness_values))]
        winner = population[winner_index]
        
        selected_parents.append(winner)

    print("Turniejowa: ", selected_parents)
    return selected_parents
