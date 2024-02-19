from src.models.gt_utils import is_strategy_better, stra_em, admissible_block
from src.models.gt_index_calc import calculate_index, rounder
from src.models.gt_block_generator import potential_support_pairs, block_game
from src.models.gt_game_class import create_n_player_game
from src.models.zero_solver import zero_solver

# Functions for finding minimal game blocks
def are_nested_indices(index_set1, index_set2):
    for set1, set2 in zip(index_set1, index_set2):
        if not set(set1).issubset(set2):
            return False
    return True

def mgb_check(index_set, min_gbs):
    for mgb in min_gbs:
        if are_nested_indices(mgb,index_set):
            return True
    return False

def ne_index(pot_sols, indices, game):
    
    ne_and_index = []

    def det_eq_index(sol):
        m_sp = stra_em(sol, indices, game.index)     

        for p in range(game.num_players):

            for s in set(game.index[p]).difference(set(indices[p])):

                if is_strategy_better(game, m_sp, p ,s):
                    return []
                
        return rounder(m_sp,3), calculate_index(game,m_sp)
        
    for sol in pot_sols:
        ne_index = det_eq_index(sol)
        if not ne_index:
            continue
        ne_and_index.append(ne_index)
            
    return ne_and_index

def min_game_blocks(game):
    
    min_gbs = tuple()
    bg_ne_index = []
        
    for indices in potential_support_pairs(game):

        block = block_game(game.payoffs, indices)
        bg = create_n_player_game(block)
        
        if mgb_check(indices, min_gbs):
            continue
            
        if not admissible_block(bg):
            continue
        #tic = time.perf_counter()
        pot_sols = zero_solver(bg, 1e-6)
        #toc = time.perf_counter()
        #print(f"nash solver took {toc - tic:0.4f} seconds")
        #tic = time.perf_counter()
        nei = ne_index(pot_sols, indices, game)
        #toc = time.perf_counter()
        #print(f"ne_index took {toc - tic:0.4f} seconds")
        
        if nei:
            bg_ne_index.append([indices, nei])
        
        ne_index_list = [bg[1] for bg in bg_ne_index if are_nested_indices(bg[0], indices)]
        index_counter = 0
        
        for neis in ne_index_list:
            index_counter += sum([nei[1] for nei in neis])
        if index_counter == 1:
            min_gbs += (indices,)
            yield indices, ne_index_list