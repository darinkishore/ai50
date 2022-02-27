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
        if col_list.count(col_list[0]) == 3:
            return col_list[0]

    # check two diagonals for possible winners
    # TODO: Double check if there are any diagonal edge cases not covered by these.
    if (board[0][0] == board[1][1]) and (board[1][1] == board[2][2]):
        return board[1][1] # arbitrary, can be any of these 3 vals.
    if (board[0][2] == board [1][1]) and (board[1][1] == board[2][0]):
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
    if win == "X":
        return 1
    elif win == "O":
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == X:
        possibilities = actions(board)
        for action in possibilities:


    raise NotImplementedError

def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, max_value(result(board, action)))
    return v

def max_value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions:
        v = max(v, min_value(result(board, action)))
    return v

