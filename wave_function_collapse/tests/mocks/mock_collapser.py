from wave_function_collapse.cell import Cell
from wave_function_collapse.collapser import Collapser


class MockCollapser(Collapser):
    def __init__(self, wave_function: list[Cell]):
        self.wave_function = wave_function

    def get_wave_function(self) -> list[Cell]:
        return self.wave_function

    def get_influenced_cells(self, cell: Cell) -> list[Cell]:
        return [x for x in self.wave_function if x is not cell]
