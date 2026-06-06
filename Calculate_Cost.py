import math
from math import pow
# calculates how good a hospital placement is based on distance and building cost
def calculate_cost(solution, population, weight, candidates, lam):

    # function that calculate the distance 
    def dist(a, b):
        return math.sqrt(pow((a[0]-b[0]),2) + pow((a[1]-b[1]),2))

    #selected hospitals
    selected = []
    for i in range(len(solution)):
        if solution[i] == 1:
            selected.append(candidates[i])

    #if there is no selected hospitals
    if len(selected) == 0:
        return float("inf")

    total_distance = 0

    for i in range(len(population)):
        person = population[i]
        nearest_hospital = 999999

        for hospital in selected:
            distance = dist(person, hospital)
            if distance < nearest_hospital:
                nearest_hospital = distance

        total_distance += nearest_hospital * weight[i]

    hospitals_cost = lam * len(selected)

    return total_distance + hospitals_cost