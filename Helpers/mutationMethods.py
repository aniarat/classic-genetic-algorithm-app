import random


class MutationMethod:
    def mutate(self, individual, mutation_rate):
        pass


class EdgeMutation(MutationMethod):
    def __init__(self, number_of_dimensions):
        self.number_of_dimensions = number_of_dimensions

    def mutate(self, individual, mutation_rate):
        mutated_individual = individual[:]
        for i in range(len(mutated_individual)):
            if random.random() < mutation_rate:
                # Jeśli gen jest na krawędzi, zamień go na losową wartość
                if i == 0 or i == len(mutated_individual) - 1:
                    mutated_individual[i] = random.randint(0, 1)  # Przyjmujemy binarne geny
                # Jeśli gen nie jest na krawędzi, wykonaj mutację z prawdopodobieństwem 50%
                else:
                    if random.random() < 0.5:
                        mutated_individual[i] = 1 if mutated_individual[i] == 0 else 0

        return mutated_individual


class SinglePointMutation(MutationMethod):
    def __init__(self, number_of_dimensions):
        self.number_of_dimensions = number_of_dimensions

    def mutate(self, individual, mutation_rate):
        mutated_individual = individual[:]  # Tworzymy kopię, aby nie modyfikować oryginalnego osobnika

        # Iterujemy przez wszystkie geny w osobniku
        for i in range(len(mutated_individual)):
            # Sprawdzamy, czy wykonujemy mutację na tym genie zgodnie z prawdopodobieństwem mutacji
            if random.random() < mutation_rate:
                # Wybieramy losowy nowy gen (może to być np. losowa liczba z odpowiedniego zakresu)
                new_gene = random.randint(0, 1)  # Zakładam, że geny są binarne (0 lub 1)
                # Zamieniamy wartość genu w osobniku na nową wartość
                mutated_individual[i] = new_gene

        return mutated_individual


class TwoPointMutation(MutationMethod):
    def __init__(self, number_of_dimensions):
        self.number_of_dimensions = number_of_dimensions

    def mutate(self, individual, mutation_rate):
        mutated_individual = individual[:]  # Tworzymy kopię, aby nie modyfikować oryginalnego osobnika

        # Wybieramy dwa różne punkty mutacji
        mutation_points = random.sample(range(len(mutated_individual)), 2)
        mutation_points.sort()  # Sortujemy punkty, aby uzyskać zakres mutacji

        # Iterujemy przez wszystkie geny w zakresie mutacji
        for i in range(mutation_points[0], mutation_points[1] + 1):
            # Sprawdzamy, czy wykonujemy mutację na tym genie zgodnie z prawdopodobieństwem mutacji
            if random.random() < mutation_rate:
                # Wybieramy losowy nowy gen (może to być np. losowa liczba z odpowiedniego zakresu)
                new_gene = random.randint(0, 1)  # Zakładam, że geny są binarne (0 lub 1)
                # Zamieniamy wartość genu w osobniku na nową wartość
                mutated_individual[i] = new_gene
        return mutated_individual
