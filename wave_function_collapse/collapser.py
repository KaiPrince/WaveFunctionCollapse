from abc import ABC, abstractmethod

from wave_function_collapse.cell import Cell

T_WaveFunction = list[Cell]


# A Collapser owns the wave function and knows the relationships between cells
class Collapser(ABC):
    @abstractmethod
    def get_wave_function(self) -> T_WaveFunction:
        pass

    def update_wave_function(self, old_cell: Cell, new_cell: Cell, wave_function: T_WaveFunction):
        return [x if x is not old_cell else new_cell for x in wave_function]

    @abstractmethod
    def get_influenced_cells(self, cell: Cell, wave_function: T_WaveFunction) -> list[Cell]:
        pass
