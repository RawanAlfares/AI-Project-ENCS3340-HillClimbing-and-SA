import random
import math
from Calculate_Cost import calculate_cost

#function that convert the random candidate sites (solution) into 0's and 1's 
#selects 15% of the candidate sites to be 1's and the rest to be 0's
def random_solution(size_candidate_sites):
    solution=[]
    for _ in range(size_candidate_sites):
        if random.random()< 0.15:
            solution.append(1)
        else:
            solution.append(0)

    #ensure at least one hspital is selected  
    if sum(solution) == 0:
        solution[random.randint(0, size_candidate_sites - 1)] = 1
        
    return solution

#function that generates one neighbor by flipping one site rendmoly
def generate_neighbors(solution, k=10):
    new_sol = solution.copy()
    i = random.randint(0, len(solution) - 1)
    new_sol[i] = 1 - new_sol[i] #flip 0=>1  , 1=>0 (remove hospital)
    return new_sol

def generate_neighbor(solution):
    new_solution = solution.copy()

    index = random.randint(0, len(solution) - 1)

    if new_solution[index] == 0:
        new_solution[index] = 1
    else:
        new_solution[index] = 0

    return new_solution


def simulated_annealing(people_points,people_count,candidate_sites,lam,T0=1000,
 alpha=0.95,max_steps=500):

    current_Sol = random_solution(len(candidate_sites))
    current_cost = calculate_cost(current_Sol,people_points,people_count,candidate_sites,lam)

    best_Sol = current_Sol.copy()
    best_cost = current_cost

    T=T0 #starting temperature

    while T > 0.001:
        neighbor = generate_neighbor(current_Sol)

        if sum(neighbor) == 0:
            T*=alpha
            continue
        new_cost = calculate_cost( neighbor,people_points,people_count, candidate_sites,lam)
        cost_difference = new_cost - current_cost

        if cost_difference < 0:
            current_Sol = neighbor
            current_cost = new_cost
#if the neighbor is worse then accept the propability
        else:
            probability = math.exp(-cost_difference / T)
            if random.random() < probability:
                current_Sol = neighbor
                current_cost = new_cost

        if current_cost < best_cost:
            best_Sol = current_Sol
            best_cost = current_cost
        # cool down the temperature
        T*=alpha
        
    return best_Sol, best_cost