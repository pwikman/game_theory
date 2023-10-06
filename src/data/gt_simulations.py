import numpy as np
import time
from src.models.game_class import create_n_player_game
from src.models.gt_min_gb_generic import min_game_blocks

#A function to generate payoffs given touple of number of strategies for each player
def generate_payoffs(num_strategies):
    payoffs = []
    num_players = len(num_strategies)
    # Generate payoffs for each player
    for player in range(num_players):
        num_strategies_without_player = [num_strategies[p] for p in range(num_players) if p != player]
        num_strategies_player = [num_strategies[player]] + num_strategies_without_player

        # Generate payoffs for each strategy combination
        strategy_combinations = np.product(num_strategies_player)
        player_payoffs = np.random.rand(strategy_combinations).reshape(*num_strategies_player).tolist()

        # Assign payoffs to the player
        payoffs.append(player_payoffs)

    return payoffs

#Simulations of two player games ns-times and games with up to Sn strategies for player n
def simulations(ns, S1, S2):

    list_game = {}

    for j in range(2,S1+1):
        for l in range(j,S2+1):
            tic = time.perf_counter()
            list_ne = []
            n_ne = 0

            for i in range(ns):

                current_ne = 0
                random_payoffs = generate_payoffs([j,l])
                random_game = create_n_player_game(random_payoffs)

                for mgb in min_game_blocks(random_game):

                    n_ne +=  len(mgb[1])
                    current_ne += len(mgb[1])
                    
                list_ne.append(current_ne)

                if (i+1)%100==0:
                    toc = time.perf_counter()
                    print("Sekunder: ", np.round(toc -tic,1) ,"Simulations:",i+1, "Mean SO:", n_ne / (i+1))

            list_game['Game'+ str((j,l))] = list_ne

    return list_game

# Simulations of games with m strategies for each of the n players for ns-times
def simulations2(ns, n, m):

    list_ne = []

    tic = time.perf_counter()

    n_ne = 0

    strats = m * np.ones(n)
    strats = strats.astype('int16')

    for i in range(ns):

        current_ne = 0
        random_payoffs = generate_payoffs(strats)
        random_game = create_n_player_game(random_payoffs)

        for mgb in min_game_blocks(random_game):
            n_ne +=  len(mgb[1])
            current_ne += len(mgb[1])
        list_ne.append(current_ne)

        if (i+1)%100==0:
            toc = time.perf_counter()
            print("Sekunder: ", np.round(toc -tic,1) ,"Simulations:",i+1, "Mean SO:", n_ne / (i+1))

    list_ne

    return list_ne