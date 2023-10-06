import sympy as sp

class Game:
    """
    A class used to represent a game in strategic form.

    ...

    Attributes
    ----------
    num_players : int
        number of players in the game
    num_strategies : list
        a list of the number of strategies for each player
    payoffs : list
        payoff matrix of the game of the form [player][strategy_player][strategy_player1, strategy_player2, ...] 
        (if player is, e.g. player 1, then strategy_player is the strategy of player 1 and strategy_player1 is the strategy of player 2)
    indices : list
        indices of the strategies for each player in the payoff matrix
    probas : list
        list of the probabilities of each strategy for each player

    Methods
    -------
    create_n_player_game(payoffs)
        creates a game with n players and variable strategies for each player
    get_strategy_indices(payoffs)
        returns the indices of the strategies for each player
    """
    def __init__(self, num_players, num_strategies, payoffs, indices, probas):
        self.num_players = num_players
        self.num_strategies = num_strategies
        self.payoffs = payoffs
        self.index = indices
        self.proba = probas

""" A function that creates a game with n players and variable strategies for each player. Uses the get_strategy_indices function to get the indices of the strategies for each player."""


def create_n_player_game(payoffs):
    num_players = len(payoffs)
    num_strategies = [len(payoffs[i]) for i in range(num_players)]
    indices = get_strategy_indices(payoffs)
    probas = [[sp.Symbol(f'p{i+1}{j+1}') for j in range(num_strategies[i])] for i in range(num_players)]

    return Game(num_players, num_strategies, payoffs, indices, probas)

""" A function that returns the indices of the strategies for each player"""

def get_strategy_indices(payoffs):
    strategy_indices = []

    for player_payoffs in payoffs:
        player_strategy_indices = []
        for i, _ in enumerate(player_payoffs):
            player_strategy_indices.append(i)
        strategy_indices.append(tuple(player_strategy_indices))

    return tuple(strategy_indices)