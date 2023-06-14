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
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0

    for i in [0, 1, 2]:
        for j in [0, 1, 2]:
            if board[i][j] == None:
                count += 1

    # If the number of available cells are even, return X; otherwise, return O
    if (count % 2) == 0:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    available = set()

    # if a cell in the board is available, then append to available set
    for i in [0, 1, 2]:
        for j in [0, 1, 2]:
            if board[i][j] == None:
                available.add((i, j))
    return available

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Check if the action is valid
    if action not in actions(board):
        raise Exception("That cell is not available")

    # make the movement
    new_board = copy.deepcopy(board)

    if player(board) == X:
        new_board[action[0]][action[1]] = X
    else:
        new_board[action[0]][action[1]] = O


    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # check all possibilities
    for i in [0, 1, 2]:
        if board[i][0] == board[i][1] == board[i][2] != None:
            return board[i][0]
        elif board[0][i] == board[1][i] == board[2][i] != None:
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != None:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] != None:
        return board[0][2]
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) == X or winner(board) == O:
        return True

    # if no one wins and there are available cells, keep going
    for i in [0, 1, 2]:
        for j in [0, 1, 2]:
            if board[i][j] == None:
                return False
    # if no one wins and there is no available cell, the game is over.
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    #Store the value in the dictionary
    dic = {}

    # If the turn is X, pick the max one
    if player(board) == X:
        for action in actions(board):
            dic[action] = minvalue(result(board, action))
        return max(dic, key=dic.get)

    # If the turn is O, pick the min one
    if player(board) == O:
        for action in actions(board):
            dic[action] = maxvalue(result(board, action))
        return min(dic, key=dic.get)

def maxvalue(board):
    if terminal(board):
        return utility(board)

    #Calculate the maximum possibility
    v = -math.inf
    for action in actions(board):
        v = max(v, minvalue(result(board, action)))
    return v

def minvalue(board):
    if terminal(board):
        return utility(board)

    # Calculate the minimum possibility
    v = math.inf
    for action in actions(board):
        v = min(v, maxvalue(result(board, action)))
    return v
