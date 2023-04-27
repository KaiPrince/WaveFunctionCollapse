import numpy as np

from sudoku.board import Board, Cell

MIN_ENTROPY = 0
MAX_ENTROPY = 9


class WaveFunctionCollapse:
    board: Board

    def __init__(self, board: Board):
        self.board = board

    def solve(self):
        # Initialize the wave in the completely unobserved state, i.e. with all the boolean coefficients being true.
        wave = self.initialize_wave(self.board)

        # Repeat the following steps:
        # Observation:
        #   Find a wave element with the minimal nonzero entropy. If there is
        #   no such elements (if all elements have zero or undefined entropy) then break the cycle (4) and go to step (
        #   5).
        #   Collapse this element into a definite state according to its coefficients and the distribution of NxN
        #   patterns in the input.
        # Propagation: propagate information gained on the previous observation step.
        pass

        # By now all the wave elements are either in a completely observed state (all the coefficients except one being
        # zero) or in the contradictory state (all the coefficients being zero). In the first case return the output.
        # In the second case finish the work without returning anything.
        pass

    def initialize_wave(self, board: Board):
        map_to_entropy = np.vectorize(self.get_entropy)
        wave = map_to_entropy(board).tolist()
        return wave

    def get_entropy(self, cell: Cell):
        if self.is_collapsed(cell):
            return MIN_ENTROPY
        else:
            return MAX_ENTROPY

    def is_collapsed(self, cell: Cell):
        return cell is not None
