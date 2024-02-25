from abc import ABC, abstractmethod

from wave_function_collapse.cell import Cell


# A Collapser owns the wave function and knows the relationships between cells
class Collapser(ABC):
    @abstractmethod
    def get_wave_function(self) -> list[Cell]:
        pass

    @abstractmethod
    def get_influenced_cells(self, cell: Cell) -> list[Cell]:
        pass
