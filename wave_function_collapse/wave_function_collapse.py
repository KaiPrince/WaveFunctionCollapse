from functools import reduce

from wave_function_collapse.cell import Cell
from wave_function_collapse.collapser import Collapser, T_WaveFunction
from wave_function_collapse.random_provider import RandomProvider


class WaveFunctionCollapse:
    collapser: Collapser

    def __init__(self, collapser: Collapser, random_provider: RandomProvider[Cell] = None):
        if random_provider is None:
            random_provider = RandomProvider()

        self.collapser = collapser
        self.random_provider = random_provider

    def solve(self) -> T_WaveFunction | None:
        # Initialize the wave in the completely unobserved state,
        # i.e. with all the states being possible for each element.
        wave_function = self.collapser.get_wave_function()

        # Repeat the following steps:
        # Observation:
        #   Find a wave element with the minimal nonzero entropy. If there is
        #   no such elements (if all elements have zero or undefined entropy) then break the cycle and go to step (
        #   5).
        #   Collapse this element into a definite state according to its coefficients and the distribution of NxN
        #   patterns in the input.
        # Propagation: propagate information gained on the previous observation step.
        while not all([x.is_collapsed() or x.is_invalid() for x in wave_function]):
            min_entropy = min([cell.entropy() for cell in wave_function if not cell.is_collapsed()])

            cells = [x for x in wave_function if x.entropy() == min_entropy]
            cell = self.random_provider.choice(cells)

            collapsed_cell = cell.collapse()
            new_wave_function = self.collapser.update_wave_function(cell, collapsed_cell, wave_function)
            wave_function = self.propagate(collapsed_cell, new_wave_function)

        # By now all the wave elements are either in a completely observed state (all the coefficients
        # except one being zero) or in the contradictory state (all the coefficients being zero). In
        # the first case return the output. In the second case finish the work without returning
        # anything.

        if any([x.is_invalid() for x in wave_function]):
            return None

        return wave_function

    def propagate(self, cell: Cell, wave_function: T_WaveFunction, visited: list[Cell] = None) -> T_WaveFunction:
        if visited is None:
            visited = []

        new_wave_function = wave_function

        influenced_cells = self.collapser.get_influenced_cells(cell, wave_function)
        influenced_cells_except_already_visited = [x for x in influenced_cells if
                                                   all([not x.is_same(y) for y in visited])]

        pruned_cells = []
        # Breadth-first propagation
        for influenced_cell in influenced_cells_except_already_visited:
            pruned_cell = influenced_cell.eliminate_coefficients(cell)
            if pruned_cell is not influenced_cell:
                if pruned_cell.is_collapsed():  # Optimization
                    pruned_cells.append(pruned_cell)
                new_wave_function = self.collapser.update_wave_function(influenced_cell, pruned_cell, new_wave_function)

        for pruned_cell in pruned_cells:
            new_wave_function = self.propagate(pruned_cell, new_wave_function, [*visited, cell])

        return new_wave_function

    def do_it(self):
        # Get all cells
        cells = self.collapser.get_wave_function()

        # Randomly choose among the cells with the minimum entropy
        cell_entropies = {len(cell.compute_possible_states()) for cell in cells}
        min_entropy = min(cell_entropies.difference({1}))  # Ignore collapsed cells
        min_entropy_cells = [x for x in cells if len(x.compute_possible_states()) == min_entropy]
        cell = self.random_provider.choice(min_entropy_cells)

        states = cell.compute_possible_states()
        for collapse_state in self.random_provider.shuffle(list(states)):
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
