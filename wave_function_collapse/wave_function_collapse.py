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
            current_wave_function = current_wave_function.update_wave_function_and_propagate(cell, collapsed_cell)

        # By now all the wave elements are either in a completely observed state (all the coefficients
        # except one being zero) or in the contradictory state (all the coefficients being zero). In
        # the first case return the output. In the second case finish the work without returning
        # anything.

        if current_wave_function.any_invalid():
            return None

        return current_wave_function
