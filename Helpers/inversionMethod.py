import random

class Inversion:
     def inverse(self, individual, inversion_probability):
        pass

class InversionMethod(Inversion):
    def __init__(self, number_of_dimensions):
        self.number_of_dimensions = number_of_dimensions

    def inverse(self, individual, inversion_probability):
        inverted_individual = individual[:]  # Tworzymy kopię, aby nie modyfikować oryginalnego osobnika
        if random.random() < inversion_probability: # Sprawdzenie, czy inwersja ma zostać zastosowana
            start = random.randint(0, len(inverted_individual) - 1)
            end = random.randint(start, len(inverted_individual) - 1)
            inverted_fragment = inverted_individual[start:end + 1][::-1]
            return inverted_individual[:start] + inverted_fragment + inverted_individual[end + 1 :]
        else:
            return individual
