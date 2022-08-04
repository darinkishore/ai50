"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    # Any board is a 3x3 list.
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    If 9 empty spots, X is next. If 8, O. If 7, X. Repeat.
    """
    open_spaces = 0
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                open_spaces += 1
    return X if open_spaces % 2 == 1 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) [(row, col)] available on the board.
    """
    actions = set()
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                actions.add((row, col))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError
    else:
        new_board = copy.deepcopy(board)
        current_player = player(new_board)
        new_board[action[0]][action[1]] = current_player
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check all rows for possible winners.
    for row in range(3):
        row_list = board[row]
        if row_list.count(row_list[0]) == 3:
            return row_list[0]

    # check all columns for possible winners.
    for col in range(3):
        col_list = []
        for row in range(3):
            col_list += [board[row][col]]
        if col_list.count(col_list[0]) == 3:  # there are 3 X's or O's in one of the cols
            return col_list[0]

    # check two diagonals for possible winners
    # TODO: Double check if there are any diagonal edge cases not covered by these.
    if (board[0][0] == board[1][1]) and (board[1][1] == board[2][2]):
        return board[1][1]  # arbitrary, can be any of these 3 vals.
    if (board[0][2] == board[1][1]) and (board[1][1] == board[2][0]):
        return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    open_spaces = 0
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                open_spaces += 1
    return True if open_spaces == 0 else False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Given a state s:

    The maximizing player picks action a in Actions(s) that produces the highest value of Min-Value(Result(s, a)).
    The minimizing player picks action a in Actions(s) that produces the lowest value of Max-Value(Result(s, a)).
    """
    if terminal(board):
        return None

    if player(board) == X:
        possibilities = [(result(board, action), action) for action in actions(board)]
        best_action = possibilities[0][1]  # first value of first tuple
        max_act = min_value(possibilities[0][0], -math.inf)  # unsure if this is right way to indicate
        possibilities.remove(possibilities[0])

        for possible_board in possibilities:
            current_min = min_value(possible_board[0], max_act)
            if max_act > current_min:
                continue
            else:
                max_act = current_min
                best_action = possible_board[1]
        return best_action

    if player(board) == O:
        possibilities = [(result(board, action), action) for action in actions(board)]
        best_action = possibilities[0][1]
        min_act = max_value(possibilities[0][0], math.inf)
        possibilities.remove(possibilities[0])

        for possible_board in possibilities:
            current_max = max_value(possible_board[0], min_act)
            if min_act < current_max:
                continue
            else:
                min_act = current_max  # number to compare to
                best_action = possible_board[1]
        return best_action  # == min_act


def min_value(board, curr_min):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        if v > curr_min:
            v = min(v, max_value(result(board, action)))
    return v


def max_value(board, curr_max):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        if v < curr_max:  # may not work!
            v = max(v, min_value(result(board, action)))
    return v
