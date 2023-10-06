
from src.models.zero_solver  import zero_solver
from src.models.gt_block_generator import potential_support_pairs, block_game
from src.models.game_class import create_n_player_game
from src.models.gt_utils import stra_em, is_strategy_better, is_strategy_strictly_dominated

# Nash equilibrium solver

def ne_solver(game): #, index = False
    result = []

    for indices in potential_support_pairs(game):
        block = block_game(game.payoffs, indices)
        bg = create_n_player_game(block)

        skip_indices = False
        for p in range(game.num_players):
            if skip_indices:
                break
            for s in range(bg.num_strategies[p]):
                if is_strategy_strictly_dominated(bg, p, s):
                    skip_indices = True
                    break
                    
        skip_eq = False
        pot_sol = zero_solver(bg, 1e-6)
        
        for sol in pot_sol:
            m_sp = stra_em(sol, indices, game.index)           
            for p in range(game.num_players):
                if skip_eq:
                    break
                for s in set(game.index[p]).difference(set(indices[p])):
                    if is_strategy_better(game, m_sp, p ,s):
                        skip_eq = True
                        break
            if skip_eq:
                break
            result.append(m_sp)

    return result