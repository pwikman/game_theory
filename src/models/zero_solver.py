import pypolsys
import numpy as np
from src.models.gt_utils import calculate_payoff_diff_and_prob_sum_equations

#Given a generic game, solve for all zeros and output the real ones
def zero_solver(game, tol):
    D = sum(game.num_strategies)
    pol = pypolsys.utils.fromSympy(calculate_payoff_diff_and_prob_sum_equations(game))
    pypolsys.polsys.init_poly(*pol)
    part = pypolsys.utils.make_h_part(D)
    pypolsys.polsys.init_partition(*part)
    bplp = pypolsys.polsys.solve(1e-8, 1e-15, 0.0)
    r = pypolsys.polsys.myroots
    def remove_near_zero_complex(array, tol):
        # Check if the imaginary or real part of any element in a row is close to zero
        is_complex_close_to_zero = lambda row: any(x.real < tol or abs(x.imag) > tol for x in row)
    
        # Create a mask to filter out rows with complex elements close to zero
        mask = np.array([not is_complex_close_to_zero(row) for row in array])
    
        # Return the real parts of the filtered array
        return np.real(array[mask])
    
    def subset_list(input_list, lengths):
        sublists = []
        start = 0

        for length in lengths:
            sublists.append(input_list[start:start + length])
            start += length

        return sublists
    
    ok_sol = remove_near_zero_complex(r[:D,:].transpose(), tol)
    output = []
    for sol in ok_sol:
        output.append(subset_list(sol, game.num_strategies))        
    
    return output
