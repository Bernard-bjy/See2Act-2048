"""
greedy algorithm
"""

import numpy as np
from copy import deepcopy

class GreedyAlgorithm:
    def __init__(self):
        self.directions = ['up', 'right', 'down', 'left']
        self.key_map = {
            'up': 'w',
            'right': 'd',
            'down': 's',
            'left': 'a'
        }

    def move(self, board, direction):
        # similuate the move
        new_board = deepcopy(board)
        # direction options
        if direction == 'up':
            moved, score = self._move_up(new_board)
        elif direction == 'right':
            moved, score = self._move_right(new_board)
        elif direction == 'down':
            moved, score = self._move_down(new_board)
        elif direction == 'left':
            moved, score = self._move_left(new_board)
        else:
            return new_board, 0, False

        return new_board, score, moved
    
    def _move_left(self,board):
        score = 0
        moved = False

        for row in range(4):
            # get the non_zero num
            line = [x for x in board[row] if x != 0]

            merged = []
            i = 0
            while i < len(line):
                if i + 1 < len(line) and line[i] ==line[i + 1]:
                    merged.append(line[i] * 2)
                    score += line[i] * 2
                    i += 2
                    moved = True
                else:
                    merged.append(line[i])
                    i += 1
            # fill zeros
            merged += [0] * (4 - len(merged))
            if list(board[row]) != merged:
                moved = True
            board[row] = merged
        return moved, score
    
    def _move_right(self, board):
        """
        _move_right: reverse, turn left, reverse
        """
        board = np.fliplr(board)
        moved, score = self._move_left(board)
        board = np.fliplr(board)
        return moved, score
    
    def _move_up(self,board):
        """
        _move_up: transposition, turn left, transpositioon
        """
        board = board.T
        moved, score = self._move_left(board)
        board = board.T
        return moved, score
    
    def _move_down(self, board):
        """
        _move_down: transposition, turn right, transposition
        """
        board = board.T
        moved, score = self._move_right(board)
        board = board.T
        return moved, score
    
    def count_empty_cells(self, board):
        return np.sum(board == 0)
    
    def evaluate_func(self, board):
        empty = self.count_empty_cells(board)
        
        # monotonicity function
        monotonicity = self._calc_monotonicity(board)
        # max num position
        max_tile_pos = self._max_tile_position(board)
        # weighted score(changed as needed)
        return empty * 30 + monotonicity * 20 + max_tile_pos * 10
    
    def _calc_monotonicity(self, board):
        score = 0
        for i in range(4):
            for j in range(3):
                if board[i][j] >= board[i][j + 1]:
                    score += 1

        for j in range(4):
            for i in range(3):
                if board[i][j] >= board[i + 1][j]:
                    score += 1
        
        return score
    
    def _max_tile_position(self, board):
        max_val = np.max(board)
        max_pos = np.where(board == max_val)
        i, j = max_pos[0][0], max_pos[1][0]

        if (i, j) in [(0,0), (0,3), (3,0), (3,3)]:
            return 10
        elif i in [0,3] or j in [0,3]:
            return 5
        return 0
    
    def get_best_move(self, board):
        """
        choice the best move
        """
        best_score = -float('inf')
        best_direction = None

        for direction in self.directions:
            new_board, score, moved = self.move(board, direction)
            if not moved:
                continue
            
            eval_score = self.evaluate_func(new_board)
            if eval_score > best_score:
                best_score = eval_score
                best_direction = direction

        if best_direction is None:
             # no valid move, return up as default
            return 'up'
        return best_direction
        
if __name__ == "__main__":
    # test the greedy algorithm
    board = np.array([[2, 0, 0, 2],
                      [4, 4, 0, 0],
                      [8, 4, 2, 0],
                      [16, 0, 0, 0]])
    
    greedy = GreedyAlgorithm()
    best_move = greedy.get_best_move(board)
    print(f"Best move: {best_move}")