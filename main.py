import time
import random
from data_generate import generate_data
from Hill_Climbing import hill_climbing
from Simulated_Annealing import simulated_annealing
from visulization import plot_map, plot_lambda_effect, plot_comparison, plot_runtime

LAMBDA_VALUES = [1, 10, 50, 100]
NUM_RUNS = 5         # runs per (acllgorithm, lambda) to measure stability
 

#  Run one experiment
def run_experiment(algorithm, name, Population_Points, Population_Weights, candidate_sites, lam, runs=NUM_RUNS):
    costs = []
    times = []
    hospitals_counts = []

    for i in range(runs):
        start = time.time()
        solution, cost = algorithm(Population_Points, Population_Weights, candidate_sites, lam)
        end = time.time()

        num_hospitals = sum(solution)
        costs.append(cost)
        times.append(end - start)
        hospitals_counts.append(num_hospitals)

        print(f"  Run {i+1}: cost={cost:.2f} | hospitals={num_hospitals} | time={end-start:.3f}s")

    avg_cost = sum(costs) / runs
    avg_time = sum(times) / runs
    avg_hospitals = sum(hospitals_counts) / runs
    variance = sum((c - avg_cost) ** 2 for c in costs) / runs

    print(f"\nAverage cost     : {avg_cost:.2f}")
    print(f"Average hospitals: {avg_hospitals:.1f}")
    print(f"Average time     : {avg_time:.4f}s")
    print(f"Variance         : {variance:.2f}\n")

    return {
        "algorithm"   : name,
        "lambda"      : lam,
        "avg_cost"    : avg_cost,
        "avg_time"    : avg_time,
        "avg_hospitals": avg_hospitals,
        "variance"    : variance,
        "all_costs"   : costs
    }



if __name__ == "__main__":

    # generate data once — same data for both algorithms
    Population_Points, Population_Weights, candidate_sites = generate_data()
    print(f"Data generated: {len(Population_Points)} people, {len(candidate_sites)} candidate sites\n")

    all_results = []

    for lam in LAMBDA_VALUES:
        print(f"  Lambda = {lam}")

        # Hill Climbing
        print(f"\n[ Hill Climbing | lambda={lam} ]")
        hc_result = run_experiment(hill_climbing, "Hill Climbing", Population_Points, Population_Weights, candidate_sites, lam)
        all_results.append(hc_result)

        # Simulated Annealing
        print(f"\n[ Simulated Annealing | lambda={lam} ]")
        sa_result = run_experiment(simulated_annealing, "Simulated Annealing", Population_Points, Population_Weights, candidate_sites, lam)
        all_results.append(sa_result)

    #  Summary Table
    print(f"\n{'='*70}")
    print(f"{'FINAL SUMMARY':^70}")
    print(f"{'='*70}")
    print(f"{'Algorithm':<25} {'Lambda':>8} {'Avg Cost':>12} {'Avg Hospitals':>15} {'Avg Time':>10} {'Variance':>10}")
    print(f"{'-'*70}")

    for r in all_results:
        print(f"{r['algorithm']:<25} {r['lambda']:>8} {r['avg_cost']:>12.2f} {r['avg_hospitals']:>15.1f} {r['avg_time']:>10.4f} {r['variance']:>10.2f}")



# generate maps for all lambda values, both algorithms
for lam in LAMBDA_VALUES:
    
    # Hill Climbing map
    solution_hc, cost_hc = hill_climbing(Population_Points, Population_Weights, candidate_sites, lam)
    plot_map(Population_Points, Population_Weights, candidate_sites, solution_hc, 
             title=f"Hill Climbing λ={lam}")

    # Simulated Annealing map
    solution_sa, cost_sa = simulated_annealing(Population_Points, Population_Weights, candidate_sites, lam)
    plot_map(Population_Points, Population_Weights, candidate_sites, solution_sa, 
             title=f"Simulated Annealing λ={lam}")

# comparison plots using all results
plot_lambda_effect(all_results)
plot_comparison(all_results)
plot_runtime(all_results)