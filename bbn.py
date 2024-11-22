import numpy as np

# Define probabilities from the Bayesian Network
P_A = {"yes": 0.8, "no": 0.2}
P_C = {"yes": 0.5, "no": 0.5}
P_G_given_A_C = {
    ("yes", "yes"): {"Good": 0.9, "OK": 0.1},
    ("yes", "no"): {"Good": 0.7, "OK": 0.3},
    ("no", "yes"): {"Good": 0.6, "OK": 0.4},
    ("no", "no"): {"Good": 0.3, "OK": 0.7},
}
P_J_given_G = {"Good": {"yes": 0.8, "no": 0.2}, "OK": {"yes": 0.2, "no": 0.8}}
P_S_given_G = {"Good": {"yes": 0.7, "no": 0.3}, "OK": {"yes": 0.3, "no": 0.7}}

# Monte Carlo simulation to estimate P(G="Good" | A="yes", C="yes")
def monte_carlo_simulation(num_samples=10000):
    count_good = 0
    count_total = 0

    for _ in range(num_samples):
        # Sample A (Aptitude Skills)
        A = "yes" if np.random.rand() < P_A["yes"] else "no"

        # Sample C (Coding Skills)
        C = "yes" if np.random.rand() < P_C["yes"] else "no"

        # Check if A="yes" and C="yes" (evidence)
        if A == "yes" and C == "yes":
            # Sample G (Grade) given A and C
            G_probabilities = P_G_given_A_C[(A, C)]
            G = "Good" if np.random.rand() < G_probabilities["Good"] else "OK"

            # Count occurrences of G="Good"
            if G == "Good":
                count_good += 1

            # Count total samples matching evidence
            count_total += 1

    # Calculate conditional probability
    if count_total == 0:
        return 0  # Avoid division by zero
    return count_good / count_total

# Run the simulation
estimated_probability = monte_carlo_simulation()
print(f"Estimated P(G='Good' | A='yes', C='yes'): {estimated_probability}")
