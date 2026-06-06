import random
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

#function that generates k-small difference neighbors by flipping one site each
def generate_neighbors(solution, k=10):
    neighbors = []
    for _ in range(k):
        new_sol = solution.copy()
        i = random.randint(0, len(solution) - 1)
        new_sol[i] = 1 - new_sol[i] #flip 0=>1 (add hospital) , 1=>0 (remove hospital)
        neighbors.append(new_sol)
    return neighbors


def hill_climbing(Population_Points, Population_Weights, candidate_sites, lam, iterations=500):

    current_Sol = random_solution(len(candidate_sites))
    current_cost = calculate_cost(current_Sol,Population_Points, Population_Weights, candidate_sites, lam)
    no_improve=0

    for _ in range(iterations):
        neighbors = generate_neighbors(current_Sol, k=10)

        best_neighbor = None
        best_cost = float("inf")

        for i in neighbors:
            cost = calculate_cost(i, Population_Points, Population_Weights, candidate_sites, lam)
           
            if cost < best_cost:
                best_cost = cost
                best_neighbor = i

        if best_cost < current_cost:
            current_Sol = best_neighbor
            current_cost = best_cost
            no_improve=0
        else:
            no_improve+=1
            if no_improve>=20:
                break

    return current_Sol, current_cost
