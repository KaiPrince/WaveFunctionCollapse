from abc import ABC, abstractmethod

from wave_function_collapse.cell import Cell


# A WaveFunction owns the wave function and knows the relationships between cells
class WaveFunction(ABC):
    @abstractmethod
    def find_min_entropy_cells(self) -> list[Cell]:
        pass

    @abstractmethod
    def update_wave_function(self, old_cell: Cell, new_cell: Cell) -> 'WaveFunction':
        pass

    @abstractmethod
    def get_influenced_cells(self, cell: Cell) -> list[Cell]:
        pass

    @abstractmethod
    def all_collapsed_or_invalid(self) -> bool:
        pass

    @abstractmethod
    def any_invalid(self) -> bool:
        pass

    def update_wave_function_and_propagate(self, cell: Cell, collapsed_cell: Cell) -> 'WaveFunction':
        new_wave_function = self.update_wave_function(cell, collapsed_cell)
        new_wave_function = new_wave_function.propagate(collapsed_cell)
        return new_wave_function

    def propagate(self, cell: Cell, visited: list[Cell] = None) -> 'WaveFunction':
        if visited is None:
            visited = []

        current_wave_function = self

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
            current_wave_function = current_wave_function.propagate(pruned_cell, [*visited, cell])

        return current_wave_function
