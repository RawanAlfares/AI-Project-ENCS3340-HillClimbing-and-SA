import matplotlib.pyplot as plt
import numpy as np
from data_generate import generate_data
from Hill_Climbing import hill_climbing
from Simulated_Annealing import simulated_annealing

# note : we use ai generetor for this code to plot maps, since we havent learned how to do it yet
# ─────────────────────────────────────────
#  1. Map Visualization
#     shows people + selected hospitals on the grid
# ─────────────────────────────────────────
def plot_map(Population_Points, Population_Weights, candidate_sites, solution, title="Hospital Placement Map"):
    fig, ax = plt.subplots(figsize=(8, 8))

    # plot people — color intensity shows weight
    px = [p[0] for p in Population_Points]
    py = [p[1] for p in Population_Points]
    scatter = ax.scatter(px, py, c=Population_Weights, cmap="Blues", s=40, label="People", zorder=2)
    plt.colorbar(scatter, ax=ax, label="Population Weight")

    # plot candidate sites (not selected)
    for i, site in enumerate(candidate_sites):
        if solution[i] == 0:
            ax.plot(site[0], site[1], "x", color="gray", markersize=5, alpha=0.4)

    # plot selected hospitals
    for i, site in enumerate(candidate_sites):
        if solution[i] == 1:
            ax.plot(site[0], site[1], "r^", markersize=12, label="Hospital" if i == solution.index(1) else "")

    # draw lines from each person to their nearest hospital
    hospitals = [candidate_sites[i] for i in range(len(solution)) if solution[i] == 1]
    for person in Population_Points:
        nearest = min(hospitals, key=lambda h: (person[0]-h[0])**2 + (person[1]-h[1])**2)
        ax.plot([person[0], nearest[0]], [person[1], nearest[1]], "gray", alpha=0.15, linewidth=0.5)

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_title(title, fontsize=14)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"map_{title.replace(' ', '_')}.png", dpi=150)
    plt.close()


# ─────────────────────────────────────────
#  2. Lambda Effect
#     shows how lambda affects cost and number of hospitals
# ─────────────────────────────────────────
def plot_lambda_effect(results):
    lambda_values = sorted(set(r["lambda"] for r in results))

    hc_costs      = [r["avg_cost"]      for r in results if r["algorithm"] == "Hill Climbing"]
    sa_costs      = [r["avg_cost"]      for r in results if r["algorithm"] == "Simulated Annealing"]
    hc_hospitals  = [r["avg_hospitals"] for r in results if r["algorithm"] == "Hill Climbing"]
    sa_hospitals  = [r["avg_hospitals"] for r in results if r["algorithm"] == "Simulated Annealing"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # cost vs lambda
    ax1.plot(lambda_values, hc_costs, "bo-", label="Hill Climbing")
    ax1.plot(lambda_values, sa_costs, "rs-", label="Simulated Annealing")
    ax1.set_xlabel("Lambda (λ)")
    ax1.set_ylabel("Average Cost")
    ax1.set_title("Effect of λ on Total Cost")
    ax1.legend()
    ax1.grid(True)

    # hospitals vs lambda
    ax2.plot(lambda_values, hc_hospitals, "bo-", label="Hill Climbing")
    ax2.plot(lambda_values, sa_hospitals, "rs-", label="Simulated Annealing")
    ax2.set_xlabel("Lambda (λ)")
    ax2.set_ylabel("Average Number of Hospitals")
    ax2.set_title("Effect of λ on Number of Hospitals")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig("lambda_effect.png", dpi=150)
    plt.close()


# ─────────────────────────────────────────
#  3. Algorithm Comparison
#     cost and variance side by side
# ─────────────────────────────────────────
def plot_comparison(results):
    lambda_values = sorted(set(r["lambda"] for r in results))

    hc_costs    = [r["avg_cost"] for r in results if r["algorithm"] == "Hill Climbing"]
    sa_costs    = [r["avg_cost"] for r in results if r["algorithm"] == "Simulated Annealing"]
    hc_variance = [r["variance"] for r in results if r["algorithm"] == "Hill Climbing"]
    sa_variance = [r["variance"] for r in results if r["algorithm"] == "Simulated Annealing"]

    x = np.arange(len(lambda_values))
    width = 0.35

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # cost comparison bar chart
    ax1.bar(x - width/2, hc_costs, width, label="Hill Climbing",       color="steelblue")
    ax1.bar(x + width/2, sa_costs, width, label="Simulated Annealing", color="tomato")
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"λ={l}" for l in lambda_values])
    ax1.set_ylabel("Average Cost")
    ax1.set_title("Cost Comparison")
    ax1.legend()
    ax1.grid(axis="y")

    # variance comparison bar chart
    ax2.bar(x - width/2, hc_variance, width, label="Hill Climbing",       color="steelblue")
    ax2.bar(x + width/2, sa_variance, width, label="Simulated Annealing", color="tomato")
    ax2.set_xticks(x)
    ax2.set_xticklabels([f"λ={l}" for l in lambda_values])
    ax2.set_ylabel("Variance")
    ax2.set_title("Stability Comparison (lower = more stable)")
    ax2.legend()
    ax2.grid(axis="y")

    plt.tight_layout()
    plt.savefig("algorithm_comparison.png", dpi=150)
    plt.close()


# ─────────────────────────────────────────
#  4. Runtime Comparison
# ─────────────────────────────────────────
def plot_runtime(results):
    lambda_values = sorted(set(r["lambda"] for r in results))

    hc_times = [r["avg_time"] for r in results if r["algorithm"] == "Hill Climbing"]
    sa_times = [r["avg_time"] for r in results if r["algorithm"] == "Simulated Annealing"]

    x = np.arange(len(lambda_values))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - width/2, hc_times, width, label="Hill Climbing",       color="steelblue")
    ax.bar(x + width/2, sa_times, width, label="Simulated Annealing", color="tomato")
    ax.set_xticks(x)
    ax.set_xticklabels([f"λ={l}" for l in lambda_values])
    ax.set_ylabel("Average Runtime (seconds)")
    ax.set_title("Runtime Comparison")
    ax.legend()
    ax.grid(axis="y")

    plt.tight_layout()
    plt.savefig("runtime_comparison.png", dpi=150)
    plt.close()