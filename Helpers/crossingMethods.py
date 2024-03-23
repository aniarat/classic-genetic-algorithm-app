import random
def single_point_crossing(F, population):
    p1 = population[0]
    p2 = population[1]
    crossingPoint = random.randint(0,len(p1))
    return [p1[:crossingPoint] + p2[crossingPoint:]]