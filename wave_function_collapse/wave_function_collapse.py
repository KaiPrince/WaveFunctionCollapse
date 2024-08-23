from wave_function_collapse.cell import Cell
from wave_function_collapse.wave_function import WaveFunction
from wave_function_collapse.random_provider import RandomProvider


class WaveFunctionCollapse:

    def __init__(self, random_provider: RandomProvider[Cell] = None):
        if random_provider is None:
            random_provider = RandomProvider()
        self.random_provider = random_provider

    def solve(self, wave_function: WaveFunction) -> WaveFunction | None:
        # Initialize the wave in the completely unobserved state,
        # i.e. with all the states being possible for each element.
        current_wave_function = wave_function

        # Repeat the following steps:
        # Observation:
        #   Find a wave element with the minimal nonzero entropy. If there is
        #   no such elements (if all elements have zero or undefined entropy) then break the cycle and go to step (
        #   5).
        #   Collapse this element into a definite state according to its coefficients and the distribution of NxN
        #   patterns in the input.
        # Propagation: propagate information gained on the previous observation step.
        while not current_wave_function.all_collapsed_or_invalid():
            cells = current_wave_function.find_min_entropy_cells()
            cell = self.random_provider.choice(cells)

            collapsed_cell = cell.collapse()
            new_wave_function = current_wave_function.update_wave_function(cell, collapsed_cell)
            current_wave_function = self.propagate(collapsed_cell, new_wave_function)

        # By now all the wave elements are either in a completely observed state (all the coefficients
        # except one being zero) or in the contradictory state (all the coefficients being zero). In
        # the first case return the output. In the second case finish the work without returning
        # anything.

        if current_wave_function.any_invalid():
            return None

        return current_wave_function

    def propagate(self, cell: Cell, wave_function: WaveFunction, visited: list[Cell] = None) -> WaveFunction:
        if visited is None:
            visited = []

        current_wave_function = wave_function

        influenced_cells = current_wave_function.get_influenced_cells(cell)
        influenced_cells_except_already_visited = [x for x in influenced_cells if
                                                   all([not x.is_same(y) for y in visited])]

        pruned_cells = []
        # Breadth-first propagation
        for influenced_cell in influenced_cells_except_already_visited:
            pruned_cell = influenced_cell.eliminate_coefficients(cell)
            if pruned_cell is not influenced_cell:
                if pruned_cell.is_collapsed():  # Optimization
                    pruned_cells.append(pruned_cell)
                current_wave_function = current_wave_function.update_wave_function(influenced_cell, pruned_cell)

        for pruned_cell in pruned_cells:
            current_wave_function = self.propagate(pruned_cell, current_wave_function, [*visited, cell])

        return current_wave_function
