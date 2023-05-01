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
        # wave = self.initialize_wave()

        # Repeat the following steps:
        # Observation:
        #   Find a wave element with the minimal nonzero entropy. If there is
        #   no such elements (if all elements have zero or undefined entropy) then break the cycle (4) and go to step (
        #   5).
        #   Collapse this element into a definite state according to its coefficients and the distribution of NxN
        #   patterns in the input.
        # Propagation: propagate information gained on the previous observation step.
        for i in range(Board.width):
            for j in range(Board.height):
                cell = self.board.get_cell(i, j)
                if self.is_collapsed(cell):
                    continue

                self.observe_cell(i, j)

                is_invalid = self.board.cell_is_invalid(i, j)
                if is_invalid:
                    self.board.revert()
                    continue

                # TODO propagate
                # TODO backtrack

        # By now all the wave elements are either in a completely observed state (all the coefficients except one being
        # zero) or in the contradictory state (all the coefficients being zero). In the first case return the output.
        # In the second case finish the work without returning anything.
        # compute_board_entropy = np.vectorize(self.get_entropy)
        # board_entropy = compute_board_entropy(self.board)

        return self.board

    def initialize_wave(self):
        wave: list = np.full([self.board.width, self.board.height], 0).tolist()
        for i, row in enumerate(wave):
            for j, col in enumerate(row):
                wave[i][j] = self.get_entropy(i, j)
        return wave

    def get_entropy(self, row_index, col_index):
        cell: Cell = self.board.get_cell(row_index, col_index)

        if self.is_collapsed(cell):
            return MIN_ENTROPY
        else:
            return len(self.board.compute_possible_states(row_index, col_index))

    def is_collapsed(self, cell: Cell):
        return cell is not None

    def observe_cell(self, row_index: int, col_index: int):
        possible_states = self.board.compute_possible_states(row_index, col_index)
        new_value = possible_states.pop()
        self.board.set_cell(row_index, col_index, new_value)
        return self.board
