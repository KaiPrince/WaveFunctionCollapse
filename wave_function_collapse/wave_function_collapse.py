import random

from wave_function_collapse.cell import Cell
from wave_function_collapse.collapser import Collapser


class WaveFunctionCollapse:
    collapser: Collapser

    def __init__(self, collapser: Collapser):
        self.collapser = collapser

    def try_solve(self) -> bool:
        # Initialize the wave in the completely unobserved state,
        # i.e. with all the states being possible for each element.
        collapse_queue = self.collapser.get_wave_function()

        # Repeat the following steps:
        # Observation:
        #   Find a wave element with the minimal nonzero entropy. If there is
        #   no such elements (if all elements have zero or undefined entropy) then break the cycle and go to step (
        #   5).
        #   Collapse this element into a definite state according to its coefficients and the distribution of NxN
        #   patterns in the input.
        # Propagation: propagate information gained on the previous observation step.
        while any([not cell.is_collapsed() and not cell.is_invalid() for cell in collapse_queue]):
            # Randomly choose among the cells with the minimum entropy
            cell_entropies = {len(cell.compute_possible_states()) for cell in collapse_queue if not cell.is_collapsed()}
            min_entropy = min(cell_entropies)
            min_entropy_cells = [x for x in collapse_queue if len(x.compute_possible_states()) == min_entropy]

            for cell in random.sample(list(min_entropy_cells), k=len(min_entropy_cells)):
                if self.try_observe_cell(cell):
                    break

        # By now all the wave elements are either in a completely observed state (all the coefficients except
        # one being zero) or in the contradictory state (all the coefficients being zero). In the first case
        # return the output. In the second case finish the work without returning anything.
        # compute_board_entropy = np.vectorize(self.get_entropy) board_entropy = compute_board_entropy(
        # self.board)

        return True

    def try_observe_cell(self, cell: Cell) -> bool:
        if cell.is_collapsed():
            # Already collapsed
            return True

        # Collapse randomly
        possible_states = cell.compute_possible_states()
        for state in random.sample(list(possible_states), k=len(possible_states)):
            cell.collapse(state)

            if self.try_propagate(cell):
                # Succeeded, move on
                return True

            cell.revert()

        return False

    def try_propagate(self, cell: Cell, visited: set[Cell] = None) -> bool:
        if visited is None:
            visited = set()

        influenced_cells = self.collapser.get_influenced_cells(cell)
        influenced_cells_except_already_visited = set(influenced_cells).difference(visited)
        for influenced_cell in influenced_cells_except_already_visited:
            influenced_cell.eliminate_coefficients(cell)

            if (
                    influenced_cell.is_invalid()
                    or not self.try_propagate(influenced_cell, visited.union({influenced_cell}))
            ):
                influenced_cell.revert()
                return False

        return True

    def do_it(self):
        # Get all cells
        cells = self.collapser.get_wave_function()

        # Randomly choose among the cells with the minimum entropy
        cell_entropies = {len(cell.compute_possible_states()) for cell in cells}
        min_entropy = min(cell_entropies.difference({1}))  # Ignore collapsed cells
        min_entropy_cells = [x for x in cells if len(x.compute_possible_states()) == min_entropy]
        cell = random.choice(min_entropy_cells)

        states = cell.compute_possible_states()
        for collapse_state in random.sample(list(states), k=len(states)):
            cell.collapse(collapse_state)

            rollback_cells = []
            for prune_cell in self.collapser.get_influenced_cells(cell):
                prune_cell.eliminate_coefficients(cell)
                rollback_cells.append(prune_cell)
                if prune_cell.is_invalid():
                    for revert_cell in rollback_cells:
                        revert_cell.revert()
                    cell.revert()
                    break
