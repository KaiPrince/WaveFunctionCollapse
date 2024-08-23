from wave_function_collapse.cell import Cell
from wave_function_collapse.wave_function import WaveFunction

T_WaveFunction = list[Cell]


class MockWaveFunction(WaveFunction):

    def __init__(self, wave_function: T_WaveFunction):
        self.wave_function = wave_function

    def get_wave_function(self) -> T_WaveFunction:
        return self.wave_function

    def find_min_entropy_cells(self) -> list[Cell]:
        min_entropy = min([cell.entropy() for cell in self.wave_function if not cell.is_collapsed()])

        cells = [x for x in self.wave_function if x.entropy() == min_entropy]

        return cells

    def update_wave_function(self, old_cell: Cell, new_cell: Cell) -> 'MockWaveFunction':
        new_wave_function: T_WaveFunction = [new_cell if old_cell.is_same(x) else x for x in self.wave_function]

        return MockWaveFunction(new_wave_function)

    def get_influenced_cells(self, cell: Cell) -> list[Cell]:
        return [x for x in self.wave_function if x is not cell]

    def all_collapsed_or_invalid(self) -> bool:
        return all([x.is_collapsed() or x.is_invalid() for x in self.wave_function])

    def any_invalid(self) -> bool:
        return any([x.is_invalid() for x in self.wave_function])
