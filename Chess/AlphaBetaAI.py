"""
Corbin Mayes - 1/24/19
Discussed with Hunter Gallant
"""


import chess
from math import inf
import math
import random


class AlphaBetaAI():
    def __init__(self, depth = 2):
        self.depth = depth
        self.transposition_table = set()

    """
    Picks the best possible move for the robot to take
    """
    def choose_move(self, board):
        moves = list(board.legal_moves)
        best_moves = []
        value = 0

        #checks all the current moves
        for i in moves:

            #if the AI is white
            if board.turn:
                board.push(i)
                new_value = self.ab_max_value(board, self.depth -1)
                if value<new_value:
                    best_moves = [i]
                    value = new_value
                elif value == new_value:
                    best_moves.append(i)

            #if the AI is black
            else:
                board.push(i)
                new_value = self.ab_min_value(board, self.depth-1)
                if value>new_value:
                    best_moves = [i]
                    value = new_value
                elif value == new_value:
                    best_moves.append(i)
            board.pop()

        #Test to take the best move or just another random move
        if len(best_moves) >0:
            best_move = random.choice(best_moves)
        else:
            if len(moves)>0:
                best_move = random.choice(moves)
            else:
                best_move = None
        if best_move != None:
            print("AlphaBetaAI recommending move: " + str(best_move))
        return best_move

    """
    Returns the greatest value of the next board state
    """

    def ab_max_value(self, board, depth, alpha=-math.inf, beta=math.inf):
        if board.is_game_over() or depth == 0:
            return self.utility(board)
        if depth > 0:
            v = -math.inf
            for a in list(board.legal_moves):
                board.push(a)
                tmp_board = hash(str(board))
                if tmp_board not in self.transposition_table:
                    v = max(v, self.ab_min_value(board, depth - 1, alpha, beta))
                    alpha = max(alpha, v)
                    self.transposition_table.add(tmp_board)
                board.pop()
                if alpha >= beta: break
        return v

    """
    Returns the smallest value of the next board state
    """

    def ab_min_value(self, board, depth, alpha=-math.inf, beta=math.inf):
        if board.is_game_over() or depth == 0:
            return self.utility(board)
        if depth > 0:
            v = math.inf
            for a in list(board.legal_moves):
                board.push(a)
                tmp_board = hash(str(board))
                if tmp_board not in self.transposition_table:
                    v = min(v, self.ab_max_value(board, depth - 1, alpha, beta))
                    beta = min(beta, v)
                    self.transposition_table.add(tmp_board)
                board.pop()
                if alpha >= beta: break
        return v


    """
    Get the value of the board
    """

    def utility(self, board):
        value = 0

        # checks all the pieces on the board
        for i in range(0, 64):
            piece_class = board.piece_at(i)
            if piece_class != None:
                piece = piece_class.symbol()

                # the value of each individual piece on the board
                if piece == "Q": value += 9
                elif piece == "R": value += 5
                elif piece == "B" or piece == "N": value += 3
                elif piece == "P": value += 1
                elif piece == "q": value += -9
                elif piece == "r": value += -5
                elif piece == "b" or piece == "n": value += -3
                elif piece == "p": value += -1
        #checks for piece and check or checkmate and evaluates the value accordingly
        if board.turn:
            if board.is_check():
                value -= 100
                if board.is_checkmate():
                    value-= 1000
        else:
            if board.is_check():
                value += 100
                if board.is_checkmate():
                    value+=1000
        return value