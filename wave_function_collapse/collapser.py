from abc import ABC, abstractmethod, abstractproperty

from wave_function_collapse.cell import Cell
from wave_function_collapse.random_provider import RandomProvider

T_WaveFunction = list[Cell]


# A Collapser owns the wave function and knows the relationships between cells
class Collapser(ABC):
    @abstractmethod
    def get_wave_function(self) -> T_WaveFunction:
        pass

    def find_min_entropy_cells(self, wave_function: T_WaveFunction):
        min_entropy = min([cell.entropy() for cell in wave_function if not cell.is_collapsed()])

        cells = [x for x in wave_function if x.entropy() == min_entropy]

        return cells

    def update_wave_function(self, old_cell: Cell, new_cell: Cell, wave_function: T_WaveFunction) -> T_WaveFunction:
        return [new_cell if old_cell.is_same(x) else x for x in wave_function]

    @abstractmethod
    def get_influenced_cells(self, cell: Cell, wave_function: T_WaveFunction) -> list[Cell]:
        pass
