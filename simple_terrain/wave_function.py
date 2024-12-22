from typing import Tuple

from wave_function_collapse.cell import Cell
from wave_function_collapse.wave_function import WaveFunction


class SimpleTerrainWaveFunction(WaveFunction):
    map: list[list[Cell]]
    map_height: int
    map_width: int

    def __init__(self, data: list[list[Cell]], map_height: int, map_width: int):
        self.map = data
        self.map_height = map_height
        self.map_width = map_width

    def find_min_entropy_cells(self) -> list[Cell]:
        cells = [
            cell for cell in
            self._get_all_cells()
            if not cell.is_collapsed() and not cell.is_invalid()
        ]
        cells.sort(key=lambda cell: cell.entropy())

        return cells

    def all_collapsed_or_invalid(self) -> bool:
        return all([x.is_collapsed() or x.is_invalid() for x in self._get_all_cells()])

    def any_invalid(self) -> bool:
        return any([x.is_invalid() for x in self._get_all_cells()])

    def _update_wave_function(self, old_cell: Cell, new_cell: Cell) -> 'WaveFunction':
        x, y = self._find_cell_coords(old_cell)

        new_map = [[x for x in y] for y in self.map]
        new_map[y][x] = new_cell

        return SimpleTerrainWaveFunction(new_map, self.map_height, self.map_width)

    def _get_influenced_cells(self, cell: Cell) -> list[Cell]:
        x, y = self._find_cell_coords(cell)

        cells = []

        if y > 0:
            cells.append(self.map[y - 1][x])  # Above
            if x > 0:
                cells.append(self.map[y - 1][x - 1])  # Above Left
            if x < self.map_width - 1:
                cells.append(self.map[y - 1][x + 1])  # Above Right

        if x > 0:
            cells.append(self.map[y][x - 1])  # Left
        if x < self.map_width - 1:
            cells.append(self.map[y][x + 1])  # Right

        if y < self.map_height - 1:
            cells.append(self.map[y + 1][x])  # Below
            if x > 0:
                cells.append(self.map[y + 1][x - 1])  # Below Left
            if x < self.map_width - 1:
                cells.append(self.map[y + 1][x + 1])  # Below Right

        return cells

    def _find_cell_coords(self, target: Cell) -> Tuple[int, int] | None:
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell.is_same(target):
                    return x, y

    def _get_all_cells(self) -> list[Cell]:
        cells = [
            self.map[i][j]
            for i in range(self.map_height)
            for j in range(self.map_width)
        ]

        return cells
