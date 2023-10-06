import sympy as sp
import itertools

def calculate_expected_payoff_diff_equations(game, probabilities):
    """Given that all other players play according to some mixed-strategy profile, 
    the function calculates for each player the expected payoff from using each pure strategy 
    compared to the players' last strategy."""

    n = game.num_players

    def expected_payoff(player, strategy):
        """Gives the expected payoff to a player from using a pure strategy given 
        that all other players play according to some mixed-strategy profile."""

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

    payoff_differences_equations = []


    for player in range(n):

        player_payoff_diff = []

        for strategy in range(game.num_strategies[player]-1):

            diff = expected_payoff(player, strategy) - expected_payoff(player, game.num_strategies[player]-1)
            player_payoff_diff.append(diff)

        payoff_differences_equations.append(player_payoff_diff)

    # Flatten the list of lists
    flat_payoff_differences_equations = [diff for sublist in payoff_differences_equations for diff in sublist]

    return flat_payoff_differences_equations

def calculate_payoff_diff_and_prob_sum_equations(game):

    probabilities = game.proba

    # Collect the equations in a list
    equations = []
    
    for player_payoff_diff in calculate_expected_payoff_diff_equations(game, probabilities):
        equations.append(sp.poly(player_payoff_diff , *[p for player_probs in probabilities for p in player_probs]))

    for player_probs in probabilities:
        prob_sum_eq = sum(player_probs) - 1
        equations.append(sp.poly(prob_sum_eq, *[p for player_probs in probabilities for p in player_probs]))


    return equations


# Function for determining whether a strategic is strictly dominated

def is_strategy_strictly_dominated(game, player, strategy):
    """Given a player and a pure strategy, check if the strategy is strictly dominated by another (pure) strategy"""
    
    # Get payoffs from player playing a certain strategy

    def get_payoff(indices, player, strategy):
        payoff = game.payoffs[player][strategy]
        for i, index in enumerate(indices):
            if i != player:
                payoff = payoff[index]
        return payoff
    
    other_strategies = [i for i in range(game.num_strategies[player]) if i != strategy]
    
    for other_strategy in other_strategies:
        temp = 0
        temp2 = 0
        for indices in itertools.product(*[range(game.num_strategies[p]) if p != player 
                                            else other_strategies for p in range(game.num_players)]):
            temp2 += 1
            payoff_current_strategy = get_payoff(indices, player, strategy)

            payoff_other_strategy = get_payoff(indices, player, other_strategy)
            
            if payoff_current_strategy > payoff_other_strategy:
                break
            else:
                temp += 1
        if temp == temp2: return True
            
    return False



# Functions for determining whether a block is admissible

def admissible_block(game):
    """ A block is admissible if in the block game there is no player that has a pure strategy 
    that is strictly dominated by another pure strategy. """

    for p in range(game.num_players):
        for s in range(game.num_strategies[p]):
            if is_strategy_strictly_dominated(game, p, s):
                return False
    return True

# Functions to check whether a completely mixed Nash equilibrium of block game is Nash in larger game

def is_strategy_better(game, mixed_strategy_profile, player, new_strategy):

    num_players = game.num_players
    num_strategies = game.num_strategies
    probabilities = game.proba
    
    def expected_payoff(player, strategy):

        payoff = 0

        # Create a modified list of strategy ranges, replacing the player's strategy range with [strategy]
        strategy_ranges = [range(num_strategies[p]) if p != player else [strategy] for p in range(num_players)]
        for indices in itertools.product(*strategy_ranges):
            probability_combination = [probabilities[p][indices[p]] if p != player else 1 for p in range(num_players)]
            payoff_value = game.payoffs[player][strategy]
            for i, index in enumerate(indices):
                if i != player:
                    payoff_value = payoff_value[index]
            payoff_term = payoff_value * sp.prod(probability_combination)

            payoff += payoff_term
        return payoff

    def expected_payoff_from_mixed_strategy(player):
        total_payoff = 0
        for strategy in range(num_strategies[player]):
            total_payoff += probabilities[player][strategy] * expected_payoff(player, strategy)
        return total_payoff

    # Calculate the current expected payoff
    current_expected_payoff = expected_payoff_from_mixed_strategy(player)
    potential_expected_payoff = expected_payoff(player, new_strategy)

    for p,s in enumerate(num_strategies):
        current_expected_payoff = current_expected_payoff.subs([(probabilities[p][i], mixed_strategy_profile[p][i]) for i in range(s)])
    # Calculate the expected payoff if the player switches to the new strategy
        potential_expected_payoff = potential_expected_payoff.subs([(probabilities[p][i], mixed_strategy_profile[p][i]) for i in range(s)])
    # Check if the new strategy is better
    return potential_expected_payoff > current_expected_payoff

#Project the zero in the smaller game onto the larger game

def stra_em(ne_cand, block_index, index):
    full_sp = [
        [ne_cand[p][block_index[p].index(s)] if s in block_index[p] else 0 for s in index[p]]
        for p in range(len(index))
    ]
    return full_sp