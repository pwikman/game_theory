
import sympy as sp
import itertools
import numpy as np

def rounder(sol, digit):
    return [np.round(np.array(sublist).astype(np.float64), digit) for sublist in sol]

def calculate_expected_payoff_diff_equations_fj(game):
    n = game.num_players
    # Create symbolic probability variables
    probabilities = [[sp.Symbol(f'p{i+1}{j+1}') for j in range(game.num_strategies[i])] for i in range(n)]

    def expected_payoff(player, strategy):
        s = game.num_strategies[player]
        payoff = 0

        # Create a modified list of strategy ranges, replacing the player's strategy range with [strategy]
        strategy_ranges = [range(game.num_strategies[p]) if p != player else [strategy] for p in range(n)]
        for indices in itertools.product(*strategy_ranges):
            probability_combination = [probabilities[p][indices[p]] if p != player else 1 for p in range(n)]
            payoff_value = game.payoffs[player][strategy]
            for i, index in enumerate(indices):
                if i != player:
                    payoff_value = payoff_value[index]
            payoff_term = payoff_value * sp.prod(probability_combination)

            payoff += payoff_term
        return payoff

    def expected_payoff_from_mixed_strategy(player):
        s = game.num_strategies[player]
        total_payoff = 0
        for strategy in range(s):
            total_payoff += probabilities[player][strategy] * expected_payoff(player, strategy)
        return total_payoff

    payoff_differences_equations = []
    for player in range(n):
        player_payoff_diff = []
        for strategy in range(game.num_strategies[player]):
            diff = probabilities[player][strategy] * (expected_payoff(player, strategy) - expected_payoff_from_mixed_strategy(player))
            player_payoff_diff.append(diff)
        payoff_differences_equations.append(player_payoff_diff)

    # Flatten the list of lists
    flat_payoff_differences_equations = [diff for sublist in payoff_differences_equations for diff in sublist]

    return flat_payoff_differences_equations

def calculate_index(game, mix_sp):
    # Get the flattened payoff difference equations
    payoff_differences_equations = calculate_expected_payoff_diff_equations_fj(game)
    
    n = game.num_players
    probabilities = [[sp.Symbol(f'p{i+1}{j+1}') for j in range(game.num_strategies[i])] for i in range(n)]

    # Flatten the list of probability variables
    flat_probabilities = [p for sublist in probabilities for p in sublist]

    # Calculate the Jacobian
    jacobian_matrix = sp.Matrix(payoff_differences_equations).jacobian(flat_probabilities)
    for p in range(n):
        jacobian_matrix = jacobian_matrix.subs([(probabilities[p][i], mix_sp[p][i]) for i in range(game.num_strategies[p])])
    output = np.array(jacobian_matrix).astype(np.float64)
    return np.sign((-1)**(sum(game.num_strategies))) * np.sign(np.linalg.det(output))