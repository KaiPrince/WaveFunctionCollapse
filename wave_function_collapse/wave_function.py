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
