"""
Author: Corbin Mayes 1/24/19
Discussed with Hunter Gallant
"""


import chess
import math
import random
from time import sleep

class MinimaxAI():
    def __init__(self, depth=2):
        self.depth = depth
        self.calls = 0

    """
    Chooses the next best possible move for whichever player the AI is
    """
    def choose_move(self, board):
        moves = list(board.legal_moves)
        self.calls = 0

        move = random.choice(moves)
        value = 0
        for j in range(1, self.depth+1):
            for i in moves:
                if board.turn:
                    board.push(i)
                    new_value = self.max_value(board, j-1)
                    board.pop()
                    if value < new_value:
                        move = i
                        value = new_value
                else:
                    board.push(i)
                    new_value =  self.min_value(board, j-1)
                    board.pop()
                    if value > new_value:
                        move = i
                        value = new_value
        print("Minimax calls: " + str(self.calls))
        print("Minimax depth: " + str(self.depth))
        return move

    """
    Returns the greatest value of the next board state
    """
    def max_value(self, board, depth):
        self.calls += 1
        if board.is_game_over():
            return self.utility(board)
        if depth > 0 :
            v = -math.inf
            for a in list(board.legal_moves):
                board.push(a)
                v = max(v,self.min_value(board, depth-1))
                board.pop()
            return v
        else:
            return self.utility(board)

    """
    Returns the smallest value of the next board state
    """
    def min_value(self, board, depth):
        self.calls += 1
        if board.is_game_over():
            return self.utility(board)
        if depth > 0:
            v = math.inf
            for a in list(board.legal_moves):
                board.push(a)
                v = min(v,self.max_value(board, depth-1))
                board.pop()
            return v
        else:
            return self.utility(board)

    """
    Get the value of the board
    """
    def utility(self, board):
        value = 0

        #checks all the pieces on the board
        for i in range(0,64):
            piece_class = board.piece_at(i)
            if piece_class != None:
                piece = piece_class.symbol()

                #the value of each individual piece on the board
                if piece == "Q": value += 9
                elif piece == "R": value += 5
                elif piece == "B" or piece == "N": value += 3
                elif piece == "P": value += 1
                elif piece == "q": value += -9
                elif piece == "r": value += -5
                elif piece == "b" or piece == "n": value += -3
                elif piece == "p": value += -1
        if board.turn:
            if board.is_check(): value -= 1000
        else:
            if board.is_check(): value += 1000
        return value