from wave_function_collapse.board_collapser import BoardCollapser
from wave_function_collapse.cell import Cell


class WaveFunctionCollapse:
    collapser: BoardCollapser

    def __init__(self, collapser: BoardCollapser):
        self.collapser = collapser

    def try_solve(self) -> bool:
        # Initialize the wave in the completely unobserved state, i.e. with all the boolean coefficients being true.
        collapse_queue = self.collapser.compute_wave_collapse_queue()

        # Repeat the following steps:
        # Observation:
        #   Find a wave element with the minimal nonzero entropy. If there is
        #   no such elements (if all elements have zero or undefined entropy) then break the cycle (4) and go to step (
        #   5).
        #   Collapse this element into a definite state according to its coefficients and the distribution of NxN
        #   patterns in the input.
        # Propagation: propagate information gained on the previous observation step.

        for cell in collapse_queue:
            cell_collapsed = self.try_observe_cell(cell)

            # By now all the wave elements are either in a completely observed state (all the coefficients except
            # one being zero) or in the contradictory state (all the coefficients being zero). In the first case
            # return the output. In the second case finish the work without returning anything.
            # compute_board_entropy = np.vectorize(self.get_entropy) board_entropy = compute_board_entropy(
            # self.board)
            if not cell_collapsed:
                return False

        return True

    def try_observe_cell(self, cell: Cell) -> bool:
        possible_states = self.collapser.compute_possible_states(cell)
        for state in possible_states:
            # Try a state
            self.collapser.set_cell_state(cell, state)

            # Backtrack
            if self.collapser.cell_is_invalid(cell) or not self.try_propagate(cell):
                self.collapser.revert()

        return self.collapser.is_collapsed(cell)

    def try_propagate(self, cell: Cell) -> bool:
        coefficient_cells: list[Cell] = self.collapser.get_coefficient_cells(cell)
        for cell in coefficient_cells:
            was_collapsed = self.try_observe_cell(cell)
            if not was_collapsed:
                return False

        return True
