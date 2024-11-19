import itertools
import math

def calculate_entropy(N, M, b_focus, b_C):
    """
    Calculate total entropy for a given set of MCC parameters.
    """
    return N * M * b_focus + b_C

def generate_parameter_sets(target_entropy=256, max_N=10, max_M=10, max_b_focus=256, b_C=256):
    """
    Generate parameter sets that achieve at least the target entropy.
    """
    valid_sets = []
    for N, M, b_focus in itertools.product(range(1, max_N + 1), range(1, max_M + 1), range(64, max_b_focus + 1, 64)):
        entropy = calculate_entropy(N, M, b_focus, b_C)
        if entropy >= target_entropy:
            valid_sets.append((N, M, b_focus, b_C, entropy))
    return valid_sets

def display_parameter_sets(sets):
    """
    Display parameter sets in a human-readable format.
    """
    print(f"{'N':<4} {'M':<4} {'b_focus':<8} {'b_C':<8} {'Entropy':<8}")
    print("-" * 40)
    for N, M, b_focus, b_C, entropy in sets:
        print(f"{N:<4} {M:<4} {b_focus:<8} {b_C:<8} {entropy:<8}")


def calculate_efficiency(N, M, b_focus, b_C, target_entropy):
    """
    Calculate efficiency for a given parameter set.
    Efficiency = Entropy / Computational Cost
    """
    entropy = calculate_entropy(N, M, b_focus, b_C)
    if entropy < target_entropy:
        return 0
    cost = N * M  # Approximation for computational cost
    return entropy / cost

def find_optimal_parameters(target_entropy=256, max_N=10, max_M=10, max_b_focus=256, b_C=256):
    """
    Search for the optimal parameter set with the best efficiency.
    """
    best_efficiency = 0
    best_params = None
    for N, M, b_focus in itertools.product(range(1, max_N + 1), range(1, max_M + 1), range(64, max_b_focus + 1, 64)):
        efficiency = calculate_efficiency(N, M, b_focus, b_C, target_entropy)
        if efficiency > best_efficiency:
            best_efficiency = efficiency
            best_params = (N, M, b_focus, b_C, efficiency)
    return best_params

# Generate and display parameter sets
parameter_sets = generate_parameter_sets(target_entropy=256)
display_parameter_sets(parameter_sets)

# Find and display the optimal parameters
optimal_params = find_optimal_parameters(target_entropy=256)
print("Optimal Parameters:")
print(f"N = {optimal_params[0]}, M = {optimal_params[1]}, b_focus = {optimal_params[2]}, b_C = {optimal_params[3]}")
print(f"Efficiency = {optimal_params[4]:.2f}")


