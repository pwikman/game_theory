import numpy as np
import time
from src.models.gt_game_class import create_n_player_game
from src.models.gt_min_gb_generic import min_game_blocks
from multiprocessing import Pool, cpu_count 
import argparse
import os  # Import the os module
import csv

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
        player_payoffs = np.random.normal(0, 1, strategy_combinations).reshape(*num_strategies_player).tolist()

        # Assign payoffs to the player
        payoffs.append(player_payoffs)

    return payoffs

#Simulations of two player games ns-times and games with up to Sn strategies for player n
def simulation_worker1(params):
    S1, S2 = params  # Unpack only S1 and S2

    current_ne = 0
    random_payoffs = generate_payoffs([S1, S2])
    random_game = create_n_player_game(random_payoffs)

    for mgb in min_game_blocks(random_game):
        current_ne += len(mgb[1])

    return current_ne

def simulations(ns, S1, S2, num_processes=4):
    list_game = {}
    n_ne = 0  # Track total NE across all simulations

    tic = time.perf_counter()

    # Generate parameters for worker processes (no more i)
    sim_params = [(S1, S2) for _ in range(ns)] 

    with Pool(num_processes) as pool:
        results = pool.map(simulation_worker1, sim_params)

        # Store results in the dictionary
        for i, result in enumerate(results):
            game_key = 'Game' + str((S1, S2, ns))
            if game_key not in list_game:
                list_game[game_key] = []
            list_game[game_key].append(result)

            n_ne += result  # Update total NE

            toc = time.perf_counter()
            print("Seconds: ", np.round(toc - tic, 1), 
                  "Simulations:", i + 1,
                  "Mean SO (Total):", n_ne / (i + 1)) 

    return list_game

# Simulations of games with m strategies for each of the n players for ns-times

def simulation_worker2(n, m):  # Function to be run in each process
    strats = m * np.ones(n).astype('int16')

    current_ne = 0
    random_payoffs = generate_payoffs(strats)
    random_game = create_n_player_game(random_payoffs)

    for mgb in min_game_blocks(random_game):
        current_ne += len(mgb[1])

    return current_ne

def simulations2(ns, n, m, num_processes=4):  # Add optional num_processes
    list_game =  {}
    n_ne = 0

    tic = time.perf_counter()

    with Pool(num_processes) as pool:
        # More granular control over work distribution 
        work_per_process = ns // num_processes
        leftover_work = ns % num_processes
        work_assignments = [work_per_process] * num_processes
        for i in range(leftover_work):
            work_assignments[i] += 1

        results = pool.starmap(simulation_worker2, [(n, m) for _ in range(ns)])

        for i, result in enumerate(results):
            game_key = 'Game' + str((n, m, ns))
            if game_key not in list_game:
                list_game[game_key] = []
            list_game[game_key].append(result)

            n_ne += result  # Update total NE

            toc = time.perf_counter()
            print("Seconds: ", np.round(toc - tic, 1), 
                  "Simulations:", i + 1,
                  "Mean SO (Total):", n_ne / (i + 1)) 

    return list_game


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run simulations with configurable parameters.')
    parser.add_argument('-n', '--num_simulations', type=int, default=1000,
                        help='Number of simulations to run.')
    parser.add_argument('-s1', '--S1', type=int, default=2, 
                        help='Value of S1 for simulations.')
    parser.add_argument('-s2', '--S2', type=int, default=3, 
                        help='Value of S2 for simulations.')
    parser.add_argument('-t', '--sim_type', choices=['sim1', 'sim2'], default='sim1',
                        help='Choose between simulations or simulations2 function.')

    args = parser.parse_args()
    parser.add_argument('-o', '--output_dir', default='.',
                        help='Directory to save the results CSV file (default: current directory)')

    args = parser.parse_args()

    # ... (Simulation execution) ...
    if args.sim_type == 'sim1':
        simulation_func = simulations
    else:
        simulation_func = simulations2

    # Run simulations with chosen parameters
    results = simulation_func(args.num_simulations, args.S1, args.S2)
    
    # --- Results Saving ---
    output_filename = f"results_{args.S1}_{args.S2}.csv"
    output_filepath = os.path.join(args.output_dir, output_filename)

    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Assuming results is a dictionary with 'Game...' keys and lists of values
    with open(output_filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for game_key, ne_list in results.items():
            writer.writerow([game_key])  # Write the game key as a header
            for i in ne_list:
                writer.writerow([i])  # Write the list of equilibrium values 

    print(f"Results saved to: {output_filepath}")
