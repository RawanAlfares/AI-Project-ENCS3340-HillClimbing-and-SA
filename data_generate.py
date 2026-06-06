# Method that generates random population, their demands wieght, and possible hospital locations.
import random

def generate_data(num_people=100, num_candidates=100):

    Population_Points=[]
    for i in range(num_people):
       x = random.uniform(0, 100)
       y = random.uniform(0, 100)
       coordinates=(x,y)
       Population_Points.append(coordinates)


    Population_Weights = []
    for i in range(num_people):
        weight=random.randint(1, 10)
        Population_Weights.append(weight)
    

    candidate_sites = []
    for i in range(num_candidates):
        x=random.uniform(0, 100)
        y=random.uniform(0, 100)
        coordinates=(x,y)
        candidate_sites.append(coordinates)
    
    return Population_Points, Population_Weights, candidate_sites