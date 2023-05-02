import numpy as np

from sudoku.board import Board, CellState
from wave_function_collapse.cell import Cell

MIN_ENTROPY = 0


class BoardCollapser:
    board: Board

    def __init__(self, board: Board):
        self.board = board

    def initialize_wave(self) -> list[list[int]]:
        wave: list = np.full([self.board.width, self.board.height], 0).tolist()
        for i, row in enumerate(wave):
            for j, col in enumerate(row):
                wave[i][j] = self.get_entropy(Cell(i, j))
        return wave

    def compute_wave_collapse_queue(self):
        wave = self.initialize_wave()

        collapse_queue = [
            Cell(i, j)
            for i in range(len(wave))
            for j in range(len(wave[0]))
            if wave[i][j] != MIN_ENTROPY
        ]
        collapse_queue.sort(key=lambda cell: wave[cell.row_index][cell.col_index])

        return collapse_queue

    def get_entropy(self, cell: Cell) -> int:
        if self.is_collapsed(cell):
            return MIN_ENTROPY
        else:
            return len(self.compute_possible_states(cell))

    def is_collapsed(self, cell: Cell):
        row_index: int = cell.row_index
        col_index: int = cell.col_index

        cell_value = self.board.get_cell(row_index, col_index)
        return cell_value is not None

    def compute_possible_states(self, cell: Cell):
        row_index = cell.row_index
        col_index = cell.col_index
        possible_states = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for i in range(Board.height):
            cell_value = self.board.get_cell(i, col_index)
            if cell_value in possible_states:
                possible_states.remove(cell_value)

        for j in range(Board.width):
            cell_value = self.board.get_cell(row_index, j)
            if cell_value in possible_states:
                possible_states.remove(cell_value)

        return possible_states

    def set_cell_state(self, cell: Cell, state: CellState):
        row_index = cell.row_index
        col_index = cell.col_index
        self.board.set_cell(row_index, col_index, state)

    def cell_is_invalid(self, cell: Cell) -> bool:
        return self.board.cell_is_invalid(cell.row_index, cell.col_index)

    def revert(self):
        self.board.revert()

    def get_coefficient_cells(self, cell: Cell) -> list[Cell]:
        row_index = cell.row_index
        col_index = cell.col_index
        coefficient_cells: list[Cell] = []

        # ..across row
        for i in range(Board.width):
            if self.is_collapsed(Cell(row_index, i)):
                continue
            coefficient_cells.append(Cell(row_index, i))

        # ..across col
        for i in range(Board.height):
            if self.is_collapsed(Cell(i, col_index)):
                continue
            coefficient_cells.append(Cell(i, col_index))

        return coefficient_cells
