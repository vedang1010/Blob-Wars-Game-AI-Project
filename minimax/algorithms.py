from blobwars.board import Board
from blobwars.constants import COLS, DEPTH, ROWS

def min_func(state: Board, depth, alpha):
    if depth >= DEPTH:
        return state.evaluate(), state

    best_state = None
    min_val = COLS * ROWS
    beta = COLS * ROWS

    for child in state.get_all_children(2):
        value = max_func(child, depth+1, beta)[0]
        # min_val = min(min_val, value)
        if min_val > value:
            best_state = child
            min_val = value
        beta = min(beta, min_val)
        if min_val <= alpha:
            break
    # print(f'best state for minimizer \n{best_state}')
    return min_val, best_state


def max_func(state: Board, depth, beta):
    if depth >= DEPTH:
        return state.evaluate(), state

    best_state = None
    max_val = - COLS * ROWS
    alpha = - COLS * ROWS

    for child in state.get_all_children(1):
        value = min_func(child, depth+1, alpha)[0]
        # max_val = max(max_val, value)
        if max_val < value:
            max_val = value
            best_state = child
        alpha = max(alpha, max_val)
        if max_val >= beta:
            break
    # print(f'best state for maximizer \n{best_state}')
    return max_val, best_state

