import numpy as np

from sudoku.board import Board

MIN_ENTROPY = 0
MAX_ENTROPY = 9


class WaveFunctionCollapse:
    board: Board

    def __init__(self, board: Board):
        self.board = board

    def solve(self) -> Board:
        # Initialize the wave in the completely unobserved state, i.e. with all the boolean coefficients being true.
        wave = self.initialize_wave()

        # Repeat the following steps:
        # Observation:
        #   Find a wave element with the minimal nonzero entropy. If there is
        #   no such elements (if all elements have zero or undefined entropy) then break the cycle (4) and go to step (
        #   5).
        #   Collapse this element into a definite state according to its coefficients and the distribution of NxN
        #   patterns in the input.
        # Propagation: propagate information gained on the previous observation step.

        # ..Find a cell to collapse
        for i in range(Board.width):
            for j in range(Board.height):
                if self.board.is_collapsed(i, j):
                    continue

                # .. collapse the cell
                cell_collapsed = self.observe_cell(i, j)
                if not cell_collapsed:
                    # Failure
                    raise NotImplementedError

                # TODO propagate
                # TODO backtrack

        # By now all the wave elements are either in a completely observed state (all the coefficients except one being
        # zero) or in the contradictory state (all the coefficients being zero). In the first case return the output.
        # In the second case finish the work without returning anything.
        # compute_board_entropy = np.vectorize(self.get_entropy)
        # board_entropy = compute_board_entropy(self.board)

        return self.board

    def initialize_wave(self) -> list[list[int]]:
        wave: list = np.full([self.board.width, self.board.height], 0).tolist()
        for i, row in enumerate(wave):
            for j, col in enumerate(row):
                wave[i][j] = self.get_entropy(i, j)
        return wave

    def get_entropy(self, row_index: int, col_index: int) -> int:
        if self.board.is_collapsed(row_index, col_index):
            return MIN_ENTROPY
        else:
            return len(self.board.compute_possible_states(row_index, col_index))

    def observe_cell(self, row_index: int, col_index: int) -> bool:
        possible_states = self.board.compute_possible_states(row_index, col_index)
        for state in possible_states:
            # Try a state
            self.board.set_cell(row_index, col_index, state)

            # Backtrack
            is_invalid = self.board.cell_is_invalid(row_index, col_index)
            if is_invalid:
                self.board.revert()
                continue

            # Propagate
            # ..Find a cell to collapse
            failed = False
            for i in range(Board.width):
                for j in range(Board.height):
                    if self.board.is_collapsed(i, j):
                        continue

                    was_collapsed = self.observe_cell(i, j)
                    if not was_collapsed:
                        failed = True
                        self.board.revert()
                        break

                if failed:
                    break

        return self.board.is_collapsed(row_index, col_index)
