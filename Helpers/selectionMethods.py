import random

#TODO: wersje maksymalizacji każdej z selekcji (?)

class SelectionMethod:
    def select(self, population, fitness_values, num_parents):
        pass

class BestSelection(SelectionMethod):
    def select(self, population, fitness_values, num_parents):
        combined_population = list(zip(population, fitness_values))
        sorted_population = sorted(combined_population, key=lambda x: x[1])
        selected_parents = [individual[0] for individual in sorted_population[:num_parents]]
        return selected_parents


class RouletteWheelSelection(SelectionMethod):
    def select(self, population, fitness_values, num_parents):
        total_fitness = sum(fitness_values)
        normalized_fitness = [total_fitness / f for f in fitness_values]
        relative_fitness = [f / sum(normalized_fitness) for f in normalized_fitness]
        cumulative_probability = [sum(relative_fitness[:i+1]) for i in range(len(relative_fitness)) for i in range(len(relative_fitness))]
        selected_parents = []
        for _ in range(num_parents):
            rand = random.random()
            for i, cp in enumerate(cumulative_probability):
                if rand <= cp:
                    selected_parents.append(population[i])
                    break
        return selected_parents

class TournamentSelection(SelectionMethod):
    def __init__(self, tournament_size):
        self.tournament_size = tournament_size

    def select(self, population, fitness_values, num_parents):
        selected_parents = []
        population_size = len(population)
        while len(selected_parents) < num_parents:
            tournament_indices = random.sample(range(population_size), self.tournament_size)
            tournament_fitness_values = [fitness_values[i] for i in tournament_indices]
            winner_index = tournament_indices[tournament_fitness_values.index(min(tournament_fitness_values))]
            winner = population[winner_index]
            selected_parents.append(winner)
        return selected_parents