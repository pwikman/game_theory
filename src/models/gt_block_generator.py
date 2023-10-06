from itertools import chain, combinations, product

# Functions for generating block games in right order

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))

def potential_support_pairs(game):
    num_strategies = game.num_strategies
    support_sets = [sorted(list(powerset(range(num))), key=lambda x: (len(x), x)) for num in num_strategies]

    combined_supports_list = list(product(*support_sets))
    sorted_combined_supports_list = sorted(combined_supports_list, key=lambda x: (sum(len(y) for y in x), max(len(y) for y in x) - min(len(y) for y in x), x))

    for sorted_combined_supports in sorted_combined_supports_list:
        yield sorted_combined_supports
        
# Recursive function to get payoffs of block game given indices of the players' strategies
def payoff_player(payoff, indices):
    indices = list(indices)
    index = indices.pop(0)
    t_payoff = [payoff[i] for i in index]
    for i, pay in enumerate(t_payoff):
        if len(indices)>0:
            pay_1 = payoff_player(pay, indices)
            t_payoff[i] = pay_1
        else:
            t_payoff[i] = pay
    return t_payoff

def block_game(payoffs, indices):
    block = []
    for p, payoff in enumerate(payoffs):
        index =  [*indices]
        index.pop(p)
        indexes = tuple([indices[p], *index])
        block_n = payoff_player(payoff, indexes)
        block.append(block_n)
    return block